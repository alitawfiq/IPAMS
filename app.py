import configparser

from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from models import Subnet, IP

# Get enviroment properties
config = configparser.RawConfigParser()
config.read('ConfigFile.properties')

app = Flask(__name__)
# Database configurations
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://{username}:{password}@{host}/{dbName}'\
                                    .format(username=config.get('DatabaseSection', 'database.userName'),
                                            password=config.get('DatabaseSection', 'database.password'),
                                            host=config.get('DatabaseSection', 'database.host'),
                                            dbName=config.get('DatabaseSection', 'database.dbName'))
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_POOL_SIZE"] = 20
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)


# Add and delete a subnet with a specific range and a VLAN ID.
@app.route("/subnets/<int:subnetValue>", methods=["GET", "POST", "DELETE"])
def subnetOperations(subnetValue):
    # Get details regarding a subnet. (VLAN ID, network IP, subnet mask, utilization percentage, subnet name)
    if request.method == "GET":
        subnet = Subnet.query.filter_by(subnet_value=subnetValue).first()
        if subnet is not None:
            utilizationPercentage = \
                db.engine.execute("SELECT ( CAST(count(ip.ip_address) as float) / CAST((sn.max - sn.min) AS float "
                                  ") ) * 100  FROM ip as ip, subnet as sn where ip.subnet_id=  (select subnet_id "
                                  "from subnet where subnet_value={subnetValue}) group by sn.subnet_id LIMIT 1".
                                  format(subnetValue=subnetValue)).first()[0]
            map = {'utilizationPercentage': utilizationPercentage}
            return jsonify(subnet.serialize, map)
    # Add a subnet with a specific range and a VLAN ID.
    elif request.method == "POST":
        json_data = request.json
        isExistingSubnet = Subnet.query.filter_by(subnet_value=subnetValue).first()
        ipsList = []
        if isExistingSubnet is None:
            # Add a subnet
            subnet = Subnet(subnetValue, json_data["vlan"], json_data["subnetName"], json_data["min"], json_data["max"])
            db.session.add(subnet)
            db.session.commit()
            # Add all ips in that subnet, free to be reserved
            ipsRange = subnet.max - subnet.min
            subnetId = Subnet.query.filter_by(subnet_value=subnetValue).first().subnet_id
            for i in range(1, ipsRange):
                ip = IP(ip_address="255.255.255.{i}".format(i=i), ip_name=None,
                        is_available=0, subnet_id=subnetId)
                ipsList.append(ip)
            db.session.bulk_save_objects(ipsList)
            db.session.commit()
            return {"success": "Subnet Added!"}
        else:
            return {"error": "Subnet already exists!"}
    # Delete a subnet.
    elif request.method == "DELETE":
        subnet = Subnet.query.filter_by(subnet_value=subnetValue).first()
        if subnet is not None:
            ips = IP.query.filter_by(subnet_id=subnet.subnet_id).all()
            db.session.delete(subnet)
            for ip in ips:
                db.session.delete(ip)
            db.session.commit()
            return {"success": "Subnet deleted!"}
        else:
            return {"error": "No Subnet to delete!"}
    else:
        return {"error": "Request method not implemented"}


# Modify and Delete a VLAN ID assigned to an already existing subnet.
@app.route("/subnets/<int:subnetValue>/vlans/<int:vlanValue>", methods=["PATCH", "DELETE"])
def vlanOperations(subnetValue, vlanValue):
    # Modify a VLAN ID assigned to an already existing subnet.
    if request.method == "PATCH":
        subnet = Subnet.query.filter_by(subnet_value=subnetValue).first()
        if subnet is not None:
            subnet.vlan = vlanValue
            db.session.merge(subnet)
            db.session.commit()
            return {"success": "Subnet's Vlan modified!"}
        else:
            return {"error": "No vlan to modify!"}
    # Delete a VLAN ID assigned to an already existing subnet.
    elif request.method == "DELETE":
        subnet = Subnet.query.filter_by(subnet_value=subnetValue).first()
        if subnet is not None:
            subnet.vlan = 0
            db.session.merge(subnet)
            db.session.commit()
            return {"success": "Subnet's Vlan deleted!"}
        else:
            return {"error": "No Vlan to delete!"}
    else:
        return {"error": "Request method not implemented"}


@app.route("/ips/<string:ipAddress>", methods=["GET", "PATCH"])
def ipOperations(ipAddress):
    # Get details regarding an IP. (parent Subnet, is it free or used)
    if request.method == "GET":
        ipObj = IP.query.filter_by(ip_address=ipAddress).first()
        subnet = Subnet.query.filter_by(subnet_id=ipObj.subnet_id).first()
        if ipObj is not None and subnet is not None:
            return {"ipName": ipObj.ip_name,
                    "subnetParent": subnet.subnet_value,
                    "subnetParentName": subnet.subnet_name,
                    "isAvailable": "Used" if ipObj.is_available else "Free"}
        else:
            return {"error": "IP or Subnet doesn't exist"}

    # Reserve a free IP of a specific subnet with a given name.
    elif request.method == "PATCH":
        existingIp = IP.query.filter_by(ip_address=ipAddress).first()
        if existingIp is not None and existingIp.is_available == 0:
            existingIp.is_available = 1
            existingIp.ip_name = request.args.get('ipName')
            db.session.merge(existingIp)
            db.session.commit()
            return {"success": "IP reserved !"}
        elif existingIp.is_available == 1:
            return {"error": "Sorry ip is used, please try another one!"}
        else:
            return {"error": "IP doesn't exists!"}
    else:
        return {"error": "Request method not implemented"}
