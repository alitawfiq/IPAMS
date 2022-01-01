from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Subnet(db.Model):
    """
    Subnet Model
    """

    __tablename__ = "subnet"

    subnet_id = db.Column(db.Integer, primary_key=True)
    subnet_value = db.Column(db.Integer, nullable=False)
    vlan = db.Column(db.Integer, nullable=True)
    subnet_name = db.Column(db.String, nullable=True)
    min = db.Column(db.Integer, nullable=True)
    max = db.Column(db.Integer, nullable=True)
    ip_addresses = db.relationship('IP', lazy=True)
    # vlan_ids = db.relationship('VLAN', lazy=True)
    # person_id = db.Column(db.Integer, db.ForeignKey('person.id'),nullable=False)


    def __init__(self, subnet_value, vlan, subnet_name, min, max):
        self.subnet_value = subnet_value
        self.vlan = vlan
        self.subnet_name = subnet_name
        self.min = min
        self.max = max

    def __repr__(self):
        return f"<Item {self.subnet_id}>"

    @property
    def serialize(self):
        """
        Return item in serializeable format
        """
        return {
                "subnetValue": self.subnet_value,
                "subnetName": self.subnet_name,
                "vlan": self.vlan,
                "min": self.min,
                "max": self.max
                }


class IP(db.Model):
    """
    IP Model
    """

    __tablename__ = "ip"

    ip_id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.Integer, nullable=False)
    ip_name = db.Column(db.String, nullable=False)
    is_available = db.Column(db.Integer, nullable=True)
    subnet_id = db.Column(db.Integer,  db.ForeignKey('subnet.subnet_id'), nullable=False)

    def __init__(self, ip_address, ip_name, is_available, subnet_id):
        self.ip_address = ip_address
        self.ip_name = ip_name
        self.is_available = is_available
        self.subnet_id = subnet_id

    def __repr__(self):
        return f"<Item {self.ip_id}>"

    @property
    def serialize(self):
        """
        Return item in serializeable format
        """
        return {
            "ip_address": self.ip_address,
            "ip_name": self.ip_name,
            "is_available": self.is_available,
            "subnet_id": self.subnet_id
        }

#
# class VLAN(db.Model):
#     """
#     VLAN Model
#     """
#     __tablename__ = "vlan"
#
#     vlan_id = db.Column(db.Integer, primary_key=True)
#     vlan_value = db.Column(db.String, nullable=False)
#     subnet_id = db.Column(db.Integer, db.ForeignKey('subnet.subnet_id'), nullable=False)
#
#     def __init__(self, vlan_value, subnet_id):
#         self.vlan_value = vlan_value
#         self.subnet_id = subnet_id
#
#     def __repr__(self):
#         return f"<Item {self.vlan_id}>"
