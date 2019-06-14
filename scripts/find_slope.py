#!/usr/bin/env python
import rospy
import numpy as np
import cv2
from std_msgs.msg import Int8MultiArray
from sklearn.linear_model import LinearRegression
from std_msgs.msg import Float32

pub = rospy.Publisher('predicted_angle',Float32, queue_size = 10)

def callback(data):
	coords = np.zeros((1,2))
	img = np.asarray(data.data)
	img = np.reshape(img,(32,32))
	for row in range(img.shape[0]):
		for col in range(img.shape[1]):
			val = img[row,col]
			if val:
				new_row = [[row,col]]
				coords = np.concatenate((coords,new_row),axis=0)
	coords = coords[1:,:]
	regr = LinearRegression()
	X = coords[:,0].T
	y = coords[:,1].T
	n = X.shape[0]
	Xb = np.c_[np.ones((n,1)),X]
	theta_best = np.linalg.inv(Xb.T.dot(Xb)).dot(Xb.T).dot(y)
	# print(theta_best)
	print(np.degrees(np.arctan(theta_best[1])))
	talker(np.degrees(np.arctan(theta_best[1])))

def listener():
	rospy.init_node('slope_predictor',anonymous=True)
	rospy.Subscriber('line_vector',Int8MultiArray, callback)
	rospy.spin()

def talker(angle):
	pub.publish(angle)

listener()
