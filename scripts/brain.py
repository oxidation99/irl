#!/usr/bin/env python

"""
To run all the necessary components for the brain_eng

rosrun edwin arm_node.py
rosrun edwin arm_behaviors.py
rosrun edwin draw.py
rosrun edwin edwin_audio.py
rosrun edwin soundboard.py
rosrun rosserial_python serial_node.py _port:=/dev/ttyUSB1 _baud:=9600
"""

import rospy
import rospkg
import random
import math
import time
import numpy as np
import pickle, os, sys
from std_msgs.msg import String, Int16


import WritingDemo
import PresenceDemo
import TicTacToe
import PlayPushCup

class EdwinBrain:
    def __init__(self):
        rospy.init_node('edwin_brain', anonymous=True)
        rospy.Subscriber('/arm_debug', String, self.arm_debug_callback, queue_size = 1)
        rospy.Subscriber('/vm_choice', String, self.visualmenu_callback, queue_size = 1)

        self.arm_pub = rospy.Publisher('/arm_cmd', String, queue_size=2)
        self.behav_pub = rospy.Publisher('/behaviors_cmd', String, queue_size=2)
        self.control_pub = rospy.Publisher('/all_control', String, queue_size=2)


        self.idling = False
        self.exit = False #should be catch all to exit all long running commands
        self.command = None

        time.sleep(0.2)
        print "edwin brain is running"

    def arm_debug_callback(self, data):
        if "ROUTE CREATE DONE" in data.data:
            rospack = rospkg.RosPack()
            self.PACKAGE_PATH = rospack.get_path("edwin")

            #We only load the behavoirs and routes once we know inits worked
            self.behaviors = pickle.load(open(self.PACKAGE_PATH + '/params/behaviors.txt', 'rb'))
            self.routes = pickle.load(open(self.PACKAGE_PATH + '/params/routes.txt', 'rb'))
            self.control_pub.publish("idle:init")
            self.idling = True

    def visualmenu_callback(self, data):
        try:
            self.command = data.data
        except data.data == None:
            print("nothing to be had")


    def demo(self):
        while True:
            #cmd = str(raw_input("Demo ID: "))
            cmd = self.command
            self.control_pub.publish("idle:stop")
            if cmd == "w":
                g = WritingDemo.Game()
                g.run()
            elif cmd == "pd":
                g = PresenceDemo.Game()
                g.run()
            elif cmd == "ttt":
                g = TicTacToe.Game(init=True)
                g.run()
            elif cmd == "pc":
                g = PlayPushCup.PushCupGame(init=True)
                g.run()
            elif cmd == "help":
                print "w -> WritingDemo \n pd -> PresenceDemo \n ttt -> TicTacToe"
            self.control_pub.publish("idle:go")

    def run(self):
        r = rospy.Rate(10)
        while not rospy.is_shutdown():
            r.sleep()

if __name__ == '__main__':
    brain_eng = EdwinBrain()
    brain_eng.demo()
