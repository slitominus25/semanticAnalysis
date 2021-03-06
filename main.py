#Обучающая модель

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from nltk.stem.lancaster import LancasterStemmer
from nltk.tokenize import RegexpTokenizer

# директория датасета

import os

dataframe = pd.read_csv("C:/Users/user/Desktop/training.1600000.processed.noemoticon.csv", encoding = "ISO-8859-1", header=None).iloc[:, [0, 4, 5]].sample(frac=1).reset_index(drop=True)

from keras.preprocessing import sequence
import re

def preprocess_tweet(tweet):
    #предобработка твита
    #Удаление лишних символов,замена ссылко на URL,имён пользователей на AT_USER, удаление хэштегов
    #arguments: tweet = a single tweet in form of string
    #отправляем твит в lower case, весь твит становится 1 предложением
    tweet.lower()
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
    tweet = re.sub('@[^\s]+','AT_USER', tweet)
    tweet = re.sub('[\s]+', ' ', tweet)
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    tweet = re.sub(r'\W*\b\w{1,3}\b', '', tweet)
    return tweet

users = np.array(dataframe.iloc[:, 1].values)
tweets = np.array(dataframe.iloc[:, 2].apply(preprocess_tweet).values)
sentiment = np.array(dataframe.iloc[:, 0].values)

from keras.preprocessing.text import Tokenizer

vocab_size = 400000
tk = Tokenizer(num_words=vocab_size)
#tw = tweets
tk.fit_on_texts(tweets)
t = tk.texts_to_sequences(tweets)
X = np.array(sequence.pad_sequences(t, maxlen=20, padding='post'))
y = sentiment

print(X.shape, y.shape)

from keras.models import Sequential
from keras.layers import Dense, Flatten, LSTM, Conv1D, MaxPooling1D, Dropout, Activation
from keras.layers.embeddings import Embedding
from sklearn.preprocessing import MinMaxScaler
from matplotlib import pyplot as plt

y[y == 4] = 1

model = Sequential()
model.add(Embedding(vocab_size, 32, input_length=20))
#1ый свёрточный слой
model.add(Conv1D(filters=128, kernel_size=5, padding='same', activation='relu'))
model.add(MaxPooling1D(pool_size=2))
model.add(Dropout(0.2))
#2ый свёрточный слой
model.add(Conv1D(filters=64, kernel_size=6, padding='same', activation='relu'))
model.add(MaxPooling1D(pool_size=2))
model.add(Dropout(0.2))
#3ый свёрточный слой
model.add(Conv1D(filters=32, kernel_size=7, padding='same', activation='relu'))
model.add(MaxPooling1D(pool_size=2))
model.add(Dropout(0.2))
#4ый свёрточный слой
model.add(Conv1D(filters=32, kernel_size=8, padding='same', activation='relu'))
model.add(MaxPooling1D(pool_size=2))
model.add(Dropout(0.2))

model.add(Flatten())
model.add(Dense(1,activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()

history = model.fit(X, y, batch_size=128, verbose=1, validation_split=0.2, epochs=10)

model.save('model.h5')

with open('file_to_write', 'w') as f:
s = "Accuracy " + history.history['acc'] + " train " + history.history['val_acc'] + " validation"
f.write(s)

plt.plot(history.history['loss'])
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.show()
plt.savefig('Figure 1')

plt.plot(history.history['acc'])
plt.xlabel('Accuracy')
plt.ylabel('Loss')
plt.show()
plt.savefig('Figure 1')


#Вызов обученной модели
user_seq=preprocess_tweet('disgusting week ')
t_1 = tk.texts_to_sequences([user_seq])
user_vector = np.array(sequence.pad_sequences(t_1, maxlen=20, padding='post'))
print("USER_Sequence:",user_seq)
print('USER_Vector:',user_vector)
x_predict_user=user_vector.reshape((1, 20))
print('USER_Sentiment:',model.predict(x_predict_user)[0][0])