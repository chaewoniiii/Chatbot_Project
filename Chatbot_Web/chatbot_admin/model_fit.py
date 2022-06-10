import tensorflow as tf
from sklearn.model_selection import train_test_split
import numpy as np
# from ChatServer.utils.Preprocess import Preprocess

from tensorflow.keras import preprocessing
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Embedding, Dense, TimeDistributed, Dropout, Bidirectional
from tensorflow.keras.optimizers import Adam
from .read_file import read_file

import os, sys
sys.path.append('../ChatServer')
from utils.Preprocess import Preprocess

def model_fit():

    corpus = read_file(os.path.join('../ChatServer/models/ner', 'new_new_dict.txt'))
    p = Preprocess(word2index_dic=os.path.join('../ChatServer/train_tools/dict', 'chatbot_dict.bin'),
                userdic=os.path.join('../ChatServer/utils', 'user_dic_test.txt'))
 

    sentences, tags = [], []
    for t in corpus:
        tagged_sentence = []
        sentence, bio_tag = [], []
        for w in t:
            tagged_sentence.append((w[1], w[3]))
            sentence.append(w[1])
            bio_tag.append(w[3])
        
        sentences.append(sentence)
        tags.append(bio_tag)

    tag_tokenizer = preprocessing.text.Tokenizer(lower=False) 
    tag_tokenizer.fit_on_texts(tags) 

    vocab_size = len(p.word_index) + 1
    tag_size = len(tag_tokenizer.word_index) + 1

    x_train = [p.get_wordidx_sequence(sent) for sent in sentences]
    y_train = tag_tokenizer.texts_to_sequences(tags)

    index_to_ner = tag_tokenizer.index_word
    index_to_ner[0] = 'PAD'
    flag = 0
    max_len = 40 
    
    x_train = preprocessing.sequence.pad_sequences(x_train, padding='post', maxlen=max_len)
    y_train = preprocessing.sequence.pad_sequences(y_train, padding='post', maxlen=max_len)
    

    x_train, x_test, y_train, y_test = train_test_split(x_train, y_train,
                                                        test_size=.2)
    flag = 0
    if flag == 0:
        y_train = tf.keras.utils.to_categorical(y_train, num_classes=tag_size)  
        y_test = tf.keras.utils.to_categorical(y_test, num_classes=tag_size)
        flag +=1
    
    model = Sequential()
    model.add(Embedding(input_dim=vocab_size, output_dim=30, input_length=max_len, mask_zero=True))
    model.add(Bidirectional(LSTM(200, return_sequences=True, dropout=0.50, recurrent_dropout=0.25)))
    model.add(TimeDistributed(Dense(tag_size, activation='softmax')))
    model.compile(loss='categorical_crossentropy', optimizer=Adam(0.01), metrics=['accuracy'])

    return model, x_train, x_test, y_train, y_test