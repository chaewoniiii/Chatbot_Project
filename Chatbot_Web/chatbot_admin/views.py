from itertools import accumulate
from django.http import JsonResponse
from django.shortcuts import render
from matplotlib.font_manager import json_load
from django.views.decorators.csrf import csrf_exempt
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.model_selection import train_test_split
import numpy as np
from utils.Preprocess import Preprocess
import os
from tensorflow.keras import preprocessing
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Embedding, Dense, TimeDistributed, Dropout, Bidirectional
from tensorflow.keras.optimizers import Adam


def model_fit():
    def read_file(file_name):
        sents = []
        with open(file_name, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for idx, l in enumerate(lines):
                if l[0] == ';' and lines[idx + 1][0] == '$':
                    this_sent = []
                elif l[0] == '$' and lines[idx - 1][0] == ';':
                    continue
                elif l[0] == '\n':
                    sents.append(this_sent)
                else:
                    this_sent.append(tuple(l.split()))
        return sents

    corpus = read_file(os.path.join('./models/ner', 'ner_train.txt'))
    p = Preprocess(word2index_dic=os.path.join('./train_tools/dict', 'chatbot_dict.bin'),
                userdic=os.path.join('./utils', 'user_dic.tsv'))

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
    # model.add(Bidirectional(LSTM(200, return_sequences=True, dropout=0.50, recurrent_dropout=0.25)))
    model.add(Bidirectional(LSTM(200, return_sequences=True, dropout=0.50, recurrent_dropout=0, activation='relu')))
    model.add(TimeDistributed(Dense(tag_size, activation='softmax')))
    model.compile(loss='categorical_crossentropy', optimizer=Adam(0.01), metrics=['accuracy'])

    return model, x_train, x_test, y_train, y_test

# Create your views here.
def cb_main(request):
    
    return render(request, 'cb_main.html')

def cb_data(request):
    return render(request, 'cb_data.html')

def cb_req(request):
    return render(request, 'cb_req.html')


@csrf_exempt
def cb_learn(request):
    ep = int(request.POST['ep'])
    
    model, x_train, x_test, y_train, y_test = model_fit()
    
    model.fit(x_train, y_train, batch_size=128, shuffle=True, epochs=ep)
    
    context = {
        'loading' : 'fin',
        'learn_data' : ep,
    }
    return JsonResponse(context)

def cb_test(request):
    model, x_train, x_test, y_train, y_test = model_fit()
    acc = model.evaluate(x_test, y_test)
    acc = round(acc[1] * 100, 2)
    context = {
        'loading' : 'fin',
        'accu' : acc,
    }
    return JsonResponse(context)