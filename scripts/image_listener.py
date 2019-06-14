#!/usr/bin/env python
import rospy
import numpy as np
import sys

import cv2
from sensor_msgs.msg import Image
from std_msgs.msg import Int8MultiArray
from cv_bridge import CvBridge,CvBridgeError
from time import time

bridge = CvBridge()
last_hsv_values = np.array([0,0,0])

pub = None

def callback(data):
    print("Debug A {}".format(time()))
    cv_image = bridge.imgmsg_to_cv2(data,desired_encoding="bgr8")   #use bgr8 instead of passthrough otherwise the orange color tape will appear to be blue.
    blur = cv2.GaussianBlur(cv_image,(5,5),0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv,np.array([0,0,226]),np.array([255,255,255]))
    small_image = cv2.resize(mask,(32,32))
    binarized_image = cv2.bitwise_and(small_image,1)
    print("Debug C {}".format(time()))
    talker(binarized_image)

def listener():
    rospy.init_node('image_listener',anonymous=True)
    rospy.Subscriber("/camera/color/image_raw",Image,callback)
    rospy.spin()

def talker(img):
    img = img.flatten()
    topub = Int8MultiArray(data = img.tolist())
    pub.publish(topub)

pub = rospy.Publisher('line_vector',Int8MultiArray, queue_size = 10)
listener()
