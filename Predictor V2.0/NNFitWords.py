#Recurrent Network
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils

import re

filename = "data/reddit.txt"
raw_text = open(filename).read()
raw_text = raw_text.lower()

raw_words = open("data/google-10000-english-usa.txt").read()
raw_words = raw_words.lower()
raw_words = re.findall(r"[\w']+", raw_words)

raw_text1 = re.findall(r"[\w']+", raw_text)

raw_text = raw_words + raw_text1

chars = sorted(list(set(raw_text)))
char_to_int = dict((c, i) for i, c in enumerate(chars))

n_chars = len(raw_text1)
#n_chars = 50000
n_vocab = len(chars)
print("Total Characters: ", n_chars)
print("Total Vocab: ", n_vocab)

seq_length = 200
dataX = []
dataY = []
for i in range(0, n_chars - seq_length, 1):
    seq_in = raw_text1[i:i+seq_length]
    seq_out = raw_text1[i + seq_length]
    dataX.append([char_to_int[char] for char in seq_in])
    dataY.append(char_to_int[seq_out])
n_patterns = len(dataX)
print("Total Patterns: ", n_patterns)

X = np.reshape(dataX, (n_patterns, seq_length, 1))

X = X / float(n_vocab)

y = np_utils.to_categorical(dataY)

model = Sequential()
model.add(LSTM(256, input_shape=(X.shape[1],  X.shape[2]), return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(256))
model.add(Dropout(0.4))
model.add(Dense(y.shape[1], activation='softmax'))

#filename = 'weights-02-7.4287.hdf5'
#model.load_weights(filename)
model.compile(loss='categorical_crossentropy', optimizer='adam')

filepath="weights/reddit-weights-{epoch:02d}-{loss:.4f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]

model.fit(X, y, epochs=10, batch_size=64, callbacks=callbacks_list)
