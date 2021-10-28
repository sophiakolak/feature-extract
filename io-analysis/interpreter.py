import os 
import tensorflow as tf
import numpy as np
import torch
import re
import logging
tf.get_logger().setLevel(logging.ERROR)

from typing import Dict
#from commons.library_api import LibraryAPI
from itertools import permutations
import concurrent.futures
from concurrent.futures.process import BrokenProcessPool
from concurrent.futures import TimeoutError
#from commons.synthesis_program import TorchProgram, Program
from typing import List
from multiprocessing.pool import Pool

class Interpreter:

    def __init__(self, constant_init: float = 0.0001):
        self.executor = Pool(maxtasksperchild=1)
        self.constant_init = constant_init
        self.jobs = []

    @staticmethod
    def create_layer_tf(layer: str):
        # Alias
        return eval(layer)
    
    def tf_forward_pass(self, tf_layer, input_tensor: np.ndarray):
        try:
            self.tf_init_layer(tf_layer)
            tf_input = self.np_tensor_to_tf(input_tensor)
            tf_output = tf_layer(tf_input)
            tf_result = self.tf_tensor_to_np(tf_output)
            return True, tf_result
        except Exception as e:
            return False, [str(e)]

    def tf_init_layer(self, tf_layer):
        # Normal Layers
        try:
            tf_layer.kernel_initializer = tf.initializers.Constant(self.constant_init)
            tf_layer.bias_initializer = tf.initializers.Constant(self.constant_init)
        except:
            pass

        # Embeddings
        try:
            tf_layer.embeddings_initializer = tf.initializers.Constant(self.constant_init)
        except:
            pass

    @staticmethod
    def np_tensor_to_tf(tensor: np.ndarray) -> tf.Tensor:
        return tf.convert_to_tensor(tensor)
    
    @staticmethod
    def tf_tensor_to_np(tensor: tf.Tensor) -> np.ndarray:
        return tensor.numpy()