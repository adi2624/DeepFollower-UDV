# DeepFollower-UDV
Authors: Aditya Rajguru and Chris Collander

Link to the dataset csv file: https://drive.google.com/open?id=1Mq_hCnv71FbnvIK51-y-P6cqUspKFuLQ

Description of Folders:
  ---Training Tools:
                   |
                    ---- model.model - The Trained Keras Model 
                    ---- Train_Model.ipynb - The Notebook used for training
                    ---- Load Model and Predict.ipynb - Validation Notebook. (CSV file required for use)
  ---config:
           |
            ---- udv.urdf - The Robot Model for RViz
            ---- taranis.config.yaml - ROS Settings file for the controller
            ---- laser.config.yaml - ROS Setting for the Laser Scanner (not utilized in this project)
  ---launch:
           |
            ---- line_follow.launch - ROS Launch file for starting the Deep Learning Line Follow Instance
            ---- udv.launch - Secondary launch file (motor control disabled)
  ---scripts:
            |
             ---- data.py - Used to collect data and store it in the home directory with the format: --- data -
                                                                                                               |
                                                                                                                --- images
                                                                                                                --- cmd_vel
             ---- find_slope.py - Utility Node to predict the angle of the curve ahead
             ---- image_listener.py - ROS Subscriber to the /camera/color/image_raw topic. (Name may differ based upon camera)
             ---- image_masking_test.py - Test file for checking image segmentation
             ---- line_follow.py - ROS Node to pass data to TensorFlow and subsequently send commands to motor.
             ---- track_line.py - Utility Node to track the line.
             

The distinguishing factor between this robot and other line following robots is that a regression based approach is able to predict velocities and provide that as a continuous control input whereas other approaches use classification of which direction to move in namely left, right and straight. The different approach enables the robot to follow the trajectory much more efficiently.

The Project Report is as follows:

Project Start Date: 01/14/2019
Project End Date: 05/27/2019


Principle of Operation:

The major difference between the approach we take and other line following robots is the use of regression to predict velocities of a robot. For the purpose of this document we will refer to linear x velocity as Lx and Angular Z velocity as Az from now on.

Lx Œ [0,1.0]  and Az Œ [-1.0,1.0].

Notice that the Lx has been kept in the positive range to prevent the robot from starting backwards in the loop.

The Neural Network used has the following architecture:

Layer 1: 300 perceptrons, Input [1,1024] ; Activation = ReLu
Layer 2: 200 perceptrons, Input [200,300] ; Activation = ReLu
Layer 3: 200 perceptrons, Input [200,200] ; Activation = ReLu
Layer 4: 2 perceptrons, Input [200,2] ; Activation = Linear

Optimizer: Adam
Metric for Accuracy: Mean Squared Error

Accuracy achieved: 99.1%

Method for Binarization:

Apply Gaussian Blur using a (5,5) kernel.
Convert Image to HSV
Apply mask in the range of [0,0,226] to [255,255,255] . (Note: The tapes used have the inherent property of a high V value in HSV)

After the 3rd step, a segmented image is obtained.

Resize the image to 32x32
Binarize the image


This being a Neural Network, Supervised Learning was used and data was collected on a track laid out with various curves and bend with one color tape. 37500 images were collected with their corresponding cmd_vel. Data was doubled by mirroring the image and changing Az. 

At the end the dataset had approximately 75000 images. This is what the network was trained on. Input is a vector for an image, output is the predicted Lx and Az. 

Tests were conducted on the same track and excellent results were obtained. The only problem that came up was on a 75 degree continuous loop where the camera went out of view, hence shutting down the neural network.

Overall motion of the robot was inherently smooth.

Conclusion: Lightweight neural network with less than 8 hours of training data able to follow a line if the image is succesfully masked using Deep Learning. 

Potential Applications: Rapid Deployment of Robots in disaster struck areas possible with a high hue tape.



Flow of Control:

1) Get 640x480 monocular image
2) Figure out threshold for tape color and carpet color (Hard coded with results from a decision tree)
3) Mask the image
4) Binarize the image
5) Resize to small size
6) Feed processed image to Neural Network
7) Publish out the predicted velocities to the motors
