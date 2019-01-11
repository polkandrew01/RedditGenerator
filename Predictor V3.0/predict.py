import numpy as np
from numpy.random import choice
from keras.models import Sequential
from keras.layers import Dense, LSTM, TimeDistributed, Activation
import random
from SpellCheck import correction

DATA_DIR = 'data/reddit.txt'
WEIGHT = 'weights/reddit_700_epoch_40.hdf5'
SEQ_LENGTH = 200
HIDDEN_DIM = 700
LAYER_NUM = 3
BATCH_SIZE = 128
GENERATE_LENGTH = 5000

ALPHABET = "abcdefghijklmnopqrstuvwxyz'ABCDEFGHIJKLMNOPQRSTUVWXYZ"

data = open(DATA_DIR, 'r', encoding='utf-8').read()
chars = sorted(list(set(data)))
VOCAB_SIZE = len(chars)

ix_to_char = {ix:char for ix, char in enumerate(chars)}
char_to_ix = {char:ix for ix, char in enumerate(chars)}

def generate_text(model, length=1000):
    text = ''
    ix = np.random.randint(VOCAB_SIZE)
    y_char = [ix_to_char[ix]]

    X = np.zeros((1, length, VOCAB_SIZE))

    word = ''
    
    for i in range(length):
        X[0, i, :][ix] = 1

        letter = ix_to_char[ix]
        if letter in ALPHABET:
            word+=letter
        else:
            if word != '' and word.lower() != 'i':
                word = correction(word)
            print(word, end='')
            print(letter, end='')
            text += word
            text += letter
            word = ''
        
        #print(ix_to_char[ix], end="")
        prediction = model.predict(X[:, :i+1, :], verbose=0)
        if random.random() * 100 < 10:
            ix = choice(len(prediction[0][0]), p=prediction[0][0])
        y_char.append(ix_to_char[ix])
        ix = np.argmax(prediction[0],1)[-1]

    file = open('RedditGen.txt', 'a', encoding='utf-8')
    file.write(text+'\n')
    file.close()
    return ('').join(y_char)

model = Sequential()
model.add(LSTM(HIDDEN_DIM, input_shape=(None, VOCAB_SIZE), return_sequences=True))
for i in range(LAYER_NUM - 1):
    model.add(LSTM(HIDDEN_DIM, return_sequences=True))
model.add(TimeDistributed(Dense(VOCAB_SIZE)))
model.add(Activation('softmax'))

model.load_weights(WEIGHT)

model.compile(loss="categorical_crossentropy", optimizer="rmsprop")

for i in range(10):
    generate_text(model, GENERATE_LENGTH)
