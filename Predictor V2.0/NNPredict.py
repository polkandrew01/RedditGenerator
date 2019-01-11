import os
os.environ['CUDA_VISIBLE_DEVICES']='-1'
import sys
import numpy as np
import random
from numpy.random import choice
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
from SpellCheck import correction

letters = 'abcdefghijklmnopqrstuvwxyz'

filename = "data/douglas adams.txt"
raw_text = open(filename).read()
raw_text = raw_text.lower()

chars = sorted(list(set(raw_text)))
char_to_int = dict((c, i) for i, c in enumerate(chars))
int_to_char = dict((i, c) for i, c in enumerate(chars))

n_chars = len(raw_text)
n_vocab = len(chars)
print("Total Characters: ", n_chars)
print("Total Vocab: ", n_vocab)

seq_length = 200
dataX = []
dataY = []
for i in range(0, n_chars - seq_length, 1):
    seq_in = raw_text[i:i+seq_length]
    seq_out = raw_text[i + seq_length]
    dataX.append([char_to_int[char] for char in seq_in])
    dataY.append(char_to_int[seq_out])
n_patterns = len(dataX)
print("Total Patterns: ", n_patterns)

X = np.reshape(dataX, (n_patterns, seq_length, 1))

X = X / float(n_vocab)

y = np_utils.to_categorical(dataY)

model = Sequential()
model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(256))
model.add(Dropout(0.4))
model.add(Dense(y.shape[1], activation='softmax'))

filename = "weights/douglas-letter-improvement-03-2.4250-bigger.hdf5"
model.load_weights(filename)
model.compile(loss='categorical_crossentropy', optimizer='adam')

start = np.random.randint(0, len(dataX)-1)
pattern = dataX[start]
print('')
#print("Seed:")
#print("\"", ''.join([int_to_char[value] for value in pattern]), "\"")
lastWord = ''
for i in range(random.randint(100,1001)):
    x = np.reshape(pattern, (1, len(pattern), 1))
    x = x / float(n_vocab)
    prediction = model.predict(x, verbose=0)
    if random.randint(0,101) > 75:
        index = choice(len(prediction[0]), p=prediction[0])
    else:
        index = np.argmax(prediction)
    result = int_to_char[index]
    seq_in = [int_to_char[value] for value in pattern]

    if result not in letters:

        if lastWord != '':
            lastWord = correction(lastWord)
        
        sys.stdout.write(lastWord)
        lastWord = ''
        sys.stdout.write(result)
    lastWord+=result        

    pattern.append(index)
    pattern = pattern[1:len(pattern)]
#print("\nDone")
