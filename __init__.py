import numpy
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import LSTM
from tensorflow.keras.callbacks import ModelCheckpoint
import tensorflow as tf
from keras.utils import np_utils
from download import *
from random import choice, randint
import sys
sys.stdout = open('output.txt','w')
raw_text = download_thoughts().lower()
# create mapping of unique chars to integers
chars = sorted(list(set(raw_text)))
char_to_int = dict((c, i) for i, c in enumerate(chars))
int_to_char = dict((i, c) for i, c in enumerate(chars))
# summarize the loaded data
n_chars = len(raw_text)
n_vocab = len(chars)
print(("Total Characters: ", n_chars))
print(("Total Vocab: ", n_vocab))
# prepare the dataset of input to output pairs encoded as integers
seq_length = 100
dataX = []
dataY = []
for i in range(0, n_chars - seq_length, 1):
	seq_in = raw_text[i:i + seq_length]
	seq_out = raw_text[i + seq_length]
	dataX.append([char_to_int[char] for char in seq_in])
	dataY.append(char_to_int[seq_out])
n_patterns = len(dataX)
print(("Total Patterns: ", n_patterns))
# reshape X to be [samples, time steps, features]
X = numpy.reshape(dataX, (n_patterns, seq_length, 1))
# normalize
X = X / float(n_vocab)
# one hot encode the output variable
y = np_utils.to_categorical(dataY)

print(list(y)[0])
y = y.tolist()
for i in range(len(y)):
	y[i].extend([0.0,0.0,0.0])
y = numpy.array(y)

print(X.shape,y.shape)
# define the LSTM model

with tf.device('/device:GPU:1'):
	model = Sequential()
	model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
	model.add(Dropout(0.2))
	model.add(LSTM(256))
	model.add(Dropout(0.2))
	model.add(Dense(y.shape[1], activation='softmax'))

	#model.load_weights('best.hdf5')

	model.compile(loss='categorical_crossentropy', optimizer='adam')
	# define the checkpoint
	filepath="best2.hdf5"
	checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
	callbacks_list = [checkpoint]
	# fit the model
	model.fit(X, y, epochs=1, batch_size=64, callbacks=callbacks_list, use_multiprocessing = True)

# pick a random seed
	print(raw_text.split('|'))
	pattern = choice(raw_text.split('|'))
	pattern = pattern[:int(len(pattern))].rjust(seq_length)
	if len(pattern) > seq_length:
		pattern = pattern[:seq_length]
	pattern = [char_to_int[value] for value in pattern]
	print("Seed:")
	print("\"", ''.join([int_to_char[value] for value in pattern]), "\"")
	# generate characters
	reslist = []
	for i in range(1000):
		x = numpy.reshape(pattern, (1, len(pattern), 1))
		x = x / float(n_vocab)
		prediction = model.predict(x, verbose=0)
		index = numpy.argmax(prediction)
		result = int_to_char[index]
		seq_in = [int_to_char[value] for value in pattern]
		reslist.append(result)
		pattern.append(index)
		pattern = pattern[1:len(pattern)]
	print(''.join(reslist))
