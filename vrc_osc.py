from pythonosc.udp_client import SimpleUDPClient

def create_client():
    ip = '127.0.0.1'
    port = 5005
    udp_client = SimpleUDPClient(ip, port)

#/tracking/trackers/1/position
#/tracking/trackers/1/rotation
#/tracking/trackers/2/position
#/tracking/trackers/2/rotation
#/tracking/trackers/3/position
#/tracking/trackers/3/rotation
#/tracking/trackers/4/position
#/tracking/trackers/4/rotation
#/tracking/trackers/5/position
#/tracking/trackers/5/rotation
#/tracking/trackers/6/position
#/tracking/trackers/6/rotation
#/tracking/trackers/7/position
#/tracking/trackers/7/rotation
#/tracking/trackers/8/position
#/tracking/trackers/8/rotation

#CONFIGURE THESE SO PEOPLE CAN USE FULLBODY ON DESKTOP AND MOBILE IN THE FUTURE
#/tracking/trackers/head/position
#/tracking/trackers/head/rotation