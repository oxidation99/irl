#!/usr/bin/env python
import rospy
import rospkg
import math
import st
import numpy as np
from std_msgs.msg import String, Int16
import time
import pickle
import os, sys
import rospkg

class ArmBehaviors:
    def __init__(self):
        rospy.init_node('behavior_arm', anonymous=True)
        rospy.Subscriber('/behaviors_cmd', String, self.behavior_callback, queue_size=10)
        rospy.Subscriber('arm_status', Int16, self.status_callback, queue_size=10)
        self.pub = rospy.Publisher('/arm_cmd', String, queue_size=10)
        self.sound_pub = rospy.Publisher('/edwin_sound', String, queue_size=10)
        self.behaviors = {}
        self.moving = False

        self.create_behaviors()
        print "Starting behavior node"


    def status_callback(self, armstatus):
    	if armstatus == 1:
    		self.moving = True
    	else:
    		self.moving = False

    def behavior_callback(self, cmdin):
        print "RECEIVED CMD: ", cmdin
        cmd = str(cmdin).replace("data: ", "")
        self.pub.publish("set_speed:: 1000")
        time.sleep(1)
        if cmd == "random":
            cmd = "impatient"
        elif "R_" in cmd:
            self.pub.publish("run_route:: "+cmd)
        elif cmd in self.behaviors.keys():
            cmd_list = self.behaviors[cmd].split(", ")
            for elem in cmd_list:
            	while self.moving == True:
            		continue
                if "R_" in elem:
                    msg = "data: run_route:: " + str(elem)
                elif "SPD" in elem:
                    msg = "data: set_speed:: " + str(elem.split("SPD: ")[1])
                else:
                    joint = elem.split(":")[0]
                    pos = elem.split(":")[1]
                    if joint == "H":
                        msg = "data: rotate_hand:: " + pos
                    elif joint == "WR":
                        msg = "data: rotate_wrist:: " + pos
                    elif joint == "E":
                        msg = "data: rotate_elbow:: " + pos
                    elif joint == "S":
                        msg = "data: rotate_shoulder:: " + pos
                    elif joint == "WA":
                        msg = "data: rotate_waist:: " + pos
                    elif joint == "SL":
                        msg = "no message"
                        # msg = "data: sleeping:: " + pos
                        time.sleep(float(pos))

                print "Publishing: ", msg
                time.sleep(1.5)
                self.pub.publish(msg)


    def create_behaviors(self):
        self.behaviors["impatient"] = "R_impat, SL: 1.5, R_ttt"
        self.behaviors["happy_butt_wiggle"] = "R_curl_up, WA: 4500, WA: 5400, WA: 4500, SL: .5, R_look"
        self.behaviors["curiosity"] =  "R_curious, WR: 800, H: 0"
        self.behaviors["greet"] = "R_greet1, WR:1500, H: 100, H: 0"
        # self.behaviors["sad"] = "H: 1000, WR: 1900, SPD: 300, R_sad_turn, SPD: 350, R_inhale, R_1_weep, R_2_weep, R_3_weep, R_4_weep, R_5_weep, SL: .5, R_sigh_up, SL: .5, SPD: 500, R_sigh_down, SL: .5, SPD: 1000, R_look"
        self.behaviors["sad"] = "SPD: 300, R_sad_turn, SL: 2, SPD: 1000, WA: 14000, WA: 15000, WA: 14000, SL: 1, R_look" #"SPD: 350, R_sigh_up, SL: .5, SPD: 500, R_sigh_down, SL: .5, SPD: 1000, R_look"

        self.behaviors["nudge"] = "R_look, R_nudge, R_look"
        self.behaviors["nod"] = "R_stare, E:13000, E:12000"
        # self.behaviors["gloat"] = "H: 1000	, WR: 1700, SPD: 350, R_laugh, SPD: 500, R_pretentious_look, WR: 500, SL: 1, WR: 700, SL: 1, WR: 900, SL: 1, WR: 1100"
        self.behaviors["angry"] = "SPD: 200, R_stare, SPD: 1000"
        self.behaviors["sleep"] = "R_sleep"
        self.behaviors["laugh"] = "SPD: 700, R_laugh, SPD: 1000"
        self.behaviors["idle_look_distance"] = "R_look_distance, SL: 1, WR: 1500, SL: .5, WR: 2300, R_look"
        self.behaviors["idle_sniff"] = "R_1_sniff, SPD: 1000, R_2_sniff, R_look"
        self.behaviors["idle_yawn"] = "SPD: 200, R_yawn, SL: .5, SPD: 500, R_slouch, SL: 1, R_look"
        self.behaviors["idle_butt_wiggle"] = "R_scrunch_up, WA: 1250, WA: 750, WA: 1250, WA: 750, WA: 1250, WA: 750"
        self.behaviors["idle_1_lookaround"] = "R_1_lookaround"
        self.behaviors["idle_2_lookaround"] = "H: 0, R_2_lookaround"
        self.behaviors["idle_3_lookaround"] = "R_3_lookaround, WR: 0, SL: .5, WR: 800"
        self.behaviors["idle_head_bobble"] = "R_head_bobble, R_look"
        self.behaviors["idle_wander"] = "R_squirrel, SL: 1, SPD: 300, R_follow_squirrel, SL: 1, SPD: 500, R_look"
        self.behaviors["idle_spin"] = "R_spin_position, WA: -7000, WA: 7000, WA: 5000, R_look"

        rospack = rospkg.RosPack()
        PACKAGE_PATH = rospack.get_path("edwin")

        pickle.dump(self.behaviors, open(PACKAGE_PATH + '/params/behaviors.txt', 'wb'))

    def loop_all(self):
        for key in self.behaviors.keys():
            print " "
            print "--------"
            print "RUNNING: ", key
            print "--------"
            print " "
            self.behavior_callback(key)
            time.sleep(5)

    def run_once(self, key):
        time.sleep(2)
        print " "
        print "--------"
        print "RUNNING: ", key
        print "--------"
        print " "
        self.behavior_callback(key)
        time.sleep(2)

    def run(self):
        r = rospy.Rate(10)
        while not rospy.is_shutdown():
            r.sleep()

if __name__ == '__main__':
    behavior_eng = ArmBehaviors()
    # behavior_eng.run_once("greet")
    behavior_eng.run_once("sad")
    # behavior_eng.run()
    # behavior_eng.loop_all()
