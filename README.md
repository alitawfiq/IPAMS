# OBSTask

1-Run the OBSTask.sql file on postgres
2-Define your database credentials on config.properties file

Model

  Class models.Subnet
  Has 6 attributes
  
    subnet_id : The primary key of the subnet
    subnet_value : the value
    vlan : The VLAN ID
    subnet_name : The given name of the subnet
    min : The minimum of the range
    max : The maximum of the range
    ip_addresses : The IP addresses under this subnet

  Class models.IP
  Has 5 attributes
  
    ip_id : The primary key of the IP
    ip_address : The address
    ip_name : The given name of the IP
    is_available : Whether its available or not
    subnet_id : The id of the subnet to which it belongs to

Controller(app.py):

1- @app.route("/subnets/<int:subnetValue>", methods=["GET", "POST", "DELETE"])
   def subnetOperations(subnetValue)
  
  This method takes the subnet value and the method type("GET", "POST", "DELETE") 
  
  
  "GET" : Returns details regarding a subnet. (VLAN ID, utilization percentage, subnet name, subnet range)
  
  "POST" : Add a subnet with a specific range and a VLAN ID.
  
  "DELETE" : Delete a subnet with a specific range and a VLAN ID, and all the assigned IPs to it.

2- @app.route("/subnets/<int:subnetValue>/vlans/<int:vlanValue>", methods=["PATCH", "DELETE"])
   def vlanOperations(subnetValue, vlanValue)
  
  This method takes the subnet value, vlanid and the method type("PATCH" , "DELETE") 
  
  
  "PATCH" : Modify a VLAN ID assigned to an already existing subnet.
  
  "DELETE" : Delete a VLAN ID assigned to an already existing subnet.
  
3- @app.route("/ips/<string:ipAddress>", methods=["GET", "PATCH"])
   def ipOperations(ipAddress)
  
  This method takes the Ip Address and the method type("PATCH" , "GET") 
  
  
  "PATCH" : Reserve a free IP of a specific subnet with a given name.
  
  "GET" : Get details regarding an IP. (parent Subnet, is it free or used)

  

  
  
  
  
  
  
  


