import tensorflow as tf
import torch
import torch.nn as nn
import numpy as np
import unittest

from numpy.testing import assert_allclose
from tensorflow.keras import Model, layers
import tensorflow as tf


const_init = np.random.rand()


class TFConv(Model):
    def __init__(self, **kwargs):
        super(TFConv, self).__init__()
        '''[SOURCE STRUCTURE CODE STARTS HERE]'''
        self.emb = tf.keras.layers.Embedding(50, 10)
        self.gru1 = tf.keras.layers.Conv1D(16, 3)
        self.gru2 = tf.keras.layers.Conv1D(8, 3)
        self.flatten = tf.keras.layers.Flatten()
        self.out = tf.keras.layers.Dense(1)
        '''[SOURCE STRUCTURE CODE ENDS HERE]'''

    def call(self, x):
        '''[SOURCE FORWARD-PASS CODE STARTS HERE]'''
        x = self.emb(x)
        x = self.gru1(x)
        x = self.gru2(x)
        x = self.out(x)

        '''[SOURCE FORWARD-PASS CODE ENDS HERE]'''
        return x


class TorchConv(nn.Module):
    def __init__(self, constant_init):
        super(TorchConv, self).__init__()
        ''' Ground Truth:
        self.conv1 = nn.Conv2d(1, 32, 3, stride=2, bias=True)

        [GENERATED STRUCTURE CODE STARTS HERE]
        '''

        for param in self.parameters():
            nn.init.constant_(param.data, constant_init)

    def forward(self, x):
        ''' Ground Truth:
        x = x.permute(0, 3, 1, 2)
        x = self.conv1(x)  # with parameters, random init
        x = x.permute(0, 2, 3, 1)

        [GENERATED FORWARD-PASS CODE STARTS HERE]
        '''

        return x


class TestConsistency:
    def test_structure(self):
        # for certain number of random inputs
        for i in range(10):
            # input for the network
            const_init = np.random.rand()
            # dataset-size, 50-width, 40-height, 1-channels
            imgs = np.random.rand(100, 50, 40, 1)

            # build the Tensorflow and PyTorch model
            tf_conv_model = TFConv(const_init)
            torch_conv_model = TorchConv(const_init)
            tf_conv_model.build(imgs.shape)  # have to build the model to count the # of parameters for tf

            # match the number of parameters
            tf_param_num = tf_conv_model.count_params()
            torch_param_num = sum(p.numel() for p in torch_conv_model.parameters())
            assert tf_param_num == torch_param_num

    def test_forward_pass(self):
        # for certain number of random inputs
        for i in range(10):
            # input for the network
            const_init = np.random.rand()
            # dataset-size, 50-width, 40-height, 1-channels
            imgs = np.random.rand(100, 50, 40, 1)

            # build the Tensorflow and PyTorch model
            tf_conv_model = TFConv(const_init)
            torch_conv_model = TorchConv(const_init)

            # get the result from Tensorflow
            tf_input = tf.convert_to_tensor(imgs)
            tf_x = tf_conv_model(tf_input)
            tf_result = tf_x.numpy()

            # get the result from Torch
            torch_input = torch.Tensor(imgs)
            torch_x = torch_conv_model(torch_input)
            torch_result = torch_x.detach().numpy()

            # check if the results are consistent
            assert_allclose(torch_result, tf_result, atol=1e-5)


def other():
    # dataset-size, 50-width, 40-height, 1-channels
    imgs = np.random.rand(10, 10, 10, 1)
    print(imgs)

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