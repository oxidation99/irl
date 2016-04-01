#!/usr/bin/env python
import rospy
import random
import math
import time
import numpy as np
from std_msgs.msg import String, Int16

class RouteCreator:
    def __init__(self):
        rospy.init_node('route_creator', anonymous=True)
        self.arm_pub = rospy.Publisher('/arm_cmd', String, queue_size=2)

        time.sleep(2)
        print "Initializing"

    def create(self):
        r1 = "R_mv2; 3296, 2308, 999, 0, 0, 0, 200, 2400, 1800, 720, 240, 2, 3296, 2308, 999, 0, 0, 0"
        # self.arm.create_route("R_stare", [[3296, 2308, 999, 0, 0, 0]])
        # self.arm.create_route("R_ttt", [[200, 2400, 1800, 720, 240, 2.1]])
        # self.arm.create_route("R_look", [[3664, 1774, 3013, 11, 0, 21]])
        # self.arm.create_route("R_playful", [[2027, 981, 98, -11, 0, 72]])
        # self.arm.create_route("R_sleep", [[0, 1891, 1732, 48, 0, 0]])
        # self.arm.create_route("R_wakeup", [[0, 3523, 5032, 1, 0, 0]])
        # self.arm.create_route("R_leaving", [[-2689, 2612, 375, 27, 0, 18]])
        # self.arm.create_route("R_greet1", [[3665, 1774, 3013, 0, 0, 0]])
        # self.arm.create_route("R_curious", [[3664, 1774, 3013, 0, 0, 0]])

        msg = "create_route:: " + r1
        print "Sending message: ", msg
        self.arm_pub.publish(msg)

    def run(self):
        self.create()
        # time.sleep(3)
        # r = rospy.Rate(10)
        # while not rospy.is_shutdown():
        #     self.create()
        #     r.sleep()

if __name__ == '__main__':
    rc = RouteCreator()
    rc.run()
