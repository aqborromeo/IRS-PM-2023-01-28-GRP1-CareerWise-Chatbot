#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 10:26:12 2023

@author: n0248727
"""
import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import json
import pickle
import numpy as np

from tensorflow.python.keras.models import Input
#from tensorflow import keras
#from tensorflow.keras import Input

from tensorflow.keras.models import Sequential

from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD
import random

print("Hello World")



-----

import nltk
nltk.download('punkt')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import json
import pickle

import numpy as np
#from tensorflow import keras
#from tensorflow.keras import Input
from tensorflow.python.keras.models import Input
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
#from tensorflow.keras.optimizers import SGD
#from keras.models import Sequential
#from keras.layers import Dense, Activation, Dropout
#from keras.optimizers import SGD
import random