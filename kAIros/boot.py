# boot.py -- run on boot-up

# Connecting to the network
# import network

# sta_if = network.WLAN(network.STA_IF)

# if not sta_if.isconnected():
#     print('connecting to network...')
#     sta_if.active(True)
#     sta_if.connect('lianderthalin', 'lianderthalin')
#     while not sta_if.isconnected():
#         pass
# print('network config:', sta_if.ifconfig())