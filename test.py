import re
# import os.path
import os
import csv

ip_base = "10.1.237."

### GENERATE ALL
ips = []
for ip in range(256):
    ips.append(ip_base + str(ip))

### TEST A FEW
# ips = [
#     "10.1.237.18", #c
#     "10.1.237.19", #c
#     "10.1.237.20", #c
#     "10.1.237.21", #c
#     "10.1.237.22", #c
#     "10.1.237.23", #c
#     "10.1.237.24", #c
# ]

device = {"Origin":"", "Device ID": "", "IP address":"", "Interface":"", "Port ID":""}

for ip in ips:
    if os.path.isfile("cdp{}.txt".format(ip)):
        files = "cdp{}.txt".format(ip)
        # print(files)
    
        with open(files, "r") as file:
            for line in file:
                device["Origin"] = ip

                device_id = re.search(r'(Device ID: )(.*)', line)
                if device_id:
                    device["Device ID"] = device_id.group(2)

                ip_address = re.search(r'(IP address: )(.*)', line)
                if ip_address:
                    device["IP address"] = ip_address.group(2)

                port = re.search(r'(Port ID \(outgoing port\): )([a-zA-Z0-9]*/[0-9]*)', line)
                if port:
                    device["Port ID"] = port.group(2)
                
                interface_id = re.search(r'(Interface: )(.*)(,)', line)
                if interface_id:
                    device["Interface"] = interface_id.group(2)

                separador1 = re.search(r'(Management address)', line)
                if separador1:
                    with open("recopilado.csv", "a") as f:
                        f.write(device["Origin"] + ", " + device["Interface"] + ", " + device["Port ID"] + ", " + device["IP address"] + ", " + device["Device ID"] + '\n')
                    
                    print("{}, {}, {}, {}, {}".format(device["Origin"], device["Interface"], device["Port ID"], device["IP address"], device["Device ID"]))
                    device["Origin"] = ""
                    device["Device ID"] = ""
                    device["IP address"] = ""
                    device["Interface"] = ""
                    device["Port ID"] = ""
        
    else:
        print("Arhcivo no encontrado: {}".format(ip))


