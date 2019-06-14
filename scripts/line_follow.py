#!/usr/bin/env python3
import tensorflow as tf
from tensorflow import keras
import os
import sys
from geometry_msgs.msg import Twist
import rospy
import numpy as np
import matplotlib.pyplot as plt
from std_msgs.msg import Int8MultiArray

class NeuralNetwork:
	def __init__(self):
		self.session = tf.Session()
		self.graph = tf.get_default_graph()
		self.model_path = '/home/nvidia/catkin_ws/src/udv/scripts/model.keras'
		self.model = None
		with self.graph.as_default():
			with self.session.as_default():
				self.model = keras.models.load_model(self.model_path)
				print("Initialized")
	def predict(self,x):
		with self.graph.as_default():
			with self.session.as_default():
				y = self.model.predict(x)
		return y


pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

NN = NeuralNetwork()

def image_callback(data):
	img = np.asarray(data.data, dtype=np.float32)
	img = np.reshape(img, (1,32*32))
	print(f"Debug {img.shape}, {img.dtype}")

	vel = NN.predict(img)

	linear = vel[0][0]/3
	angular = vel[0][1]
	topub = Twist()
	topub.linear.x = linear
	topub.angular.z = angular
	print("Predicted Linear: "+str(linear)+" Predicted Angular: "+str(angular))
	pub.publish(topub)


print("Init node")
rospy.init_node('line_follow',anonymous=True)
rospy.Subscriber('/line_vector',Int8MultiArray,image_callback)
print("Spinning!")
rospy.spin()
