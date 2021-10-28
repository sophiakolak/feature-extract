import tensorflow as tf
import torch
import torch.nn as nn
import numpy as np
import unittest

from numpy.testing import assert_allclose
from tensorflow.keras import Model
import tensorflow as tf

const_init = np.random.rand()

class TFConv(Model):
    def __init__(self, **kwargs):
        super(TFConv, self).__init__()
        # input should be 227x227x3 images
        '''[SOURCE STRUCTURE CODE STARTS HERE]'''
        self.conv_1 = tf.keras.layers.Conv2D(96, (11, 11), strides=(4, 4))
        self.relu = tf.keras.layers.ReLU()
        self.pool_1 = tf.keras.layers.MaxPool2D((2, 2), strides=(2, 2))
        self.conv_2 = tf.keras.layers.Conv2D(256, (11, 11), strides=(1, 1))
        self.relu = tf.keras.layers.ReLU()
        self.pool_2 = tf.keras.layers.MaxPool2D((2, 2), strides=(2, 2))
        self.conv_3 = tf.keras.layers.Conv2D(384, (3, 3), strides=(1, 1))
        self.relu = tf.keras.layers.ReLU()
        self.conv_4 = tf.keras.layers.Conv2D(384, (3, 3), strides=(1, 1))
        self.relu = tf.keras.layers.ReLU()
        self.conv_5 = tf.keras.layers.Conv2D(256, (3, 3), strides=(1, 1))
        self.relu = tf.keras.layers.ReLU()
        self.pool_3 = tf.keras.layers.MaxPool2D((2, 2), strides=(2, 2))
        self.flat = tf.keras.layers.Flatten()
        self.fc1 = tf.keras.layers.Dense(4096)
        self.relu = tf.keras.layers.ReLU()
        self.fc2 = tf.keras.layers.Dense(1000)
        self.relu = tf.keras.layers.ReLU()
        self.fc3 = tf.keras.layers.Dense(17)
        self.soft = tf.keras.layers.Softmax()

        '''[SOURCE STRUCTURE CODE ENDS HERE]'''

    def call(self, x):
        '''[SOURCE FORWARD-PASS CODE STARTS HERE]'''
        x = self.conv_1(x)
        x = self.pool_1(x)
        x = self.conv_2(x)
        x = self.pool_2(x)
        x = self.conv_3(x)
        x = self.conv_4(x)
        x = self.conv_5(x)
        x = self.pool_3(x)
        x = self.flat(x)
        x = self.fc1(x)
        #x = self.dropout1(x)
        x = self.fc2(x)
        #x = self.dropout2(x)
        x = self.fc3(x)
        '''[SOURCE FORWARD-PASS CODE ENDS HERE]'''

        return x

def other():
    # dataset-size, 50-width, 40-height, 1-channels
    imgs = np.random.rand(10, 227, 227, 3)
#   imgs = np.random.rand(10, 10, 10, 1)
    #print(imgs)

    # build the Tensorflow and PyTorch model
    tf_conv_model = TFConv()

    # get the result from Tensorflow
    tf_input = tf.convert_to_tensor(imgs)
    tf_x = tf_conv_model(tf_input)
    tf_result = tf_x.numpy()

    print(tf_result)


if __name__ == '__main__':
    # unittest.main()
    other()