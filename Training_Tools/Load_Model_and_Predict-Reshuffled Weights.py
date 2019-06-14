#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
import cv2


# In[2]:


mat = np.genfromtxt("data.csv",delimiter=",")


# In[3]:


model = keras.models.load_model('model.model')


# In[4]:


np.random.shuffle(mat)
# Split 80/20 train/test
train = mat[:int(0.8*np.shape(mat)[0]),:]
valid = train[int(0.8*np.shape(mat)[0]):]
train = train[:int(0.8*np.shape(mat)[0])]
test = mat[int(0.8*np.shape(mat)[0]):,:]


# In[47]:



'''
Get weights using layer.get_weights() and push to empty_array list
(1024,300)
(300,200)
(200,200)
(200,2)

Set weights using model.set_weights()
'''

empty_array = list()

for layer in model.layers:
    weights = layer.get_weights()
    empty_array.append(weights)
    print(str(len(weights[0])) +", " + str(len(weights[1])))
    for w in weights:
        w = np.random.permutation(w.flat).reshape(w.shape)
    layer.set_weights(weights)



# In[48]:


np.random.shuffle(test)
row = test[0]
img = row[:32*32]
print(np.shape(img))
vel = row[32*32:]
img2 = np.reshape(img,(32,32))
plt.imshow(img2)

img = np.reshape(img,(1,1024,))

print(np.shape(img))
pre = model.predict(img)
print(pre)

print(f"Actual : {vel[0]}, {vel[1]}")
print(f"Predict: {pre[0][0]}, {pre[0][1]}")


# In[ ]:





# In[ ]:




