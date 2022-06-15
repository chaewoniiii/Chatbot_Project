import tensorflow as tf
from sklearn.model_selection import train_test_split
import numpy as np
# from ChatServer.utils.Preprocess import Preprocess
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras import preprocessing
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Embedding, Dense, Dropout, Conv1D, GlobalMaxPool1D, concatenate, LSTM, TimeDistributed, Dropout, Bidirectional
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model
from .read_file import read_file
import os, sys
sys.path.append('../ChatServer')
from utils.Preprocess import Preprocess

def intent_fit():
    MAX_SEQ_LEN = 15
    
    train_file = os.path.join('./static/data/total_train_data_1.csv')
    data = pd.read_csv(train_file, encoding='cp949')
    intent_count = int(data.nunique()['intent'])

    p = Preprocess(word2index_dic=os.path.join('../ChatServer/train_tools/dict', 'chatbot_dict.bin'),
                userdic=os.path.join('../ChatServer/utils', 'user_dic_test.tsv'))

    queries = data['query'].tolist()
    intents = data['intent'].tolist()
    sequences = []

    for sentence in queries:
        pos = p.pos(sentence)
        keywords = p.get_keywords(pos, without_tag=True)
        seq = p.get_wordidx_sequence(keywords)
        sequences.append(seq)

    padded_seqs = preprocessing.sequence.pad_sequences(sequences, maxlen=MAX_SEQ_LEN, padding='post')

    # 학습용, 검증용, 테스트용 데이터셋 생성
    ds = tf.data.Dataset.from_tensor_slices((padded_seqs, intents))
    ds = ds.shuffle(len(queries)) 

    # 학습셋:검증셋:테스트셋 = 7:2:1
    train_size = int(len(padded_seqs) * 0.7)
    val_size = int(len(padded_seqs) * 0.2)
    test_size = int(len(padded_seqs) * 0.1)

    train_ds = ds.take(train_size).batch(20)
    val_ds = ds.skip(train_size).take(val_size).batch(20)
    test_ds = ds.skip(train_size + val_size).take(test_size).batch(20)

    # 하이퍼 파라미터 설정
    dropout_prob = 0.5
    EMB_SIZE = 128
    EPOCH = 5
    VOCAB_SIZE = len(p.word_index) + 1 

    # ④ CNN 모델 정의
    # keras 함수형 모델 방식으로 구현
    input_layer = Input(shape=(MAX_SEQ_LEN,))  # 입려크기
    embedding_layer = Embedding(VOCAB_SIZE, EMB_SIZE, input_length=MAX_SEQ_LEN)(input_layer)
    dropout_emb = Dropout(rate=dropout_prob)(embedding_layer)

    conv1 = Conv1D(
        filters=128,
        kernel_size=3,
        padding='valid',
        activation=tf.nn.relu)(dropout_emb)
    pool1 = GlobalMaxPool1D()(conv1)

    conv2 = Conv1D(
        filters=128,
        kernel_size=4,
        padding='valid',
        activation=tf.nn.relu)(dropout_emb)
    pool2 = GlobalMaxPool1D()(conv2)

    conv3 = Conv1D(
        filters=128,
        kernel_size=5,
        padding='valid',
        activation=tf.nn.relu)(dropout_emb)
    pool3 = GlobalMaxPool1D()(conv3)

    # 3,4,5gram 이후 합치기
    concat = concatenate([pool1, pool2, pool3])

    hidden = Dense(128, activation=tf.nn.relu)(concat)
    dropout_hidden = Dropout(rate=dropout_prob)(hidden)
    logits = Dense(intent_count, name='logits')(dropout_hidden)  # 5개의 의도 클래스를 분류 의도 클래스 더 추가시 수정
    predictions = Dense(5, activation=tf.nn.softmax)(logits)

    model = Model(inputs=input_layer, outputs=predictions)
    model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

    model.fit(train_ds, validation_data=val_ds, epochs=EPOCH, verbose=1)

    model.save('./static/data/intent_model_test.h5')

    

def model_fit(ep):
    global x
    global y
    
    corpus = read_file(os.path.join('../ChatServer/models/ner', 'new_new_dict.txt'))
    p = Preprocess(word2index_dic=os.path.join('../ChatServer/train_tools/dict', 'chatbot_dict.bin'),
                userdic=os.path.join('../ChatServer/utils', 'user_dic_test.tsv'))

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
                                                        test_size=.2,
                                                        random_state=1234)
    flag = 0
    if flag == 0 or not model:
        y_train = tf.keras.utils.to_categorical(y_train, num_classes=tag_size)  
        y_test = tf.keras.utils.to_categorical(y_test, num_classes=tag_size)
        flag +=1
    
    model = Sequential()
    model.add(Embedding(input_dim=vocab_size, output_dim=30, input_length=max_len, mask_zero=True))
    model.add(Bidirectional(LSTM(200, return_sequences=True, dropout=0.50, recurrent_dropout=0.25)))
    model.add(TimeDistributed(Dense(tag_size, activation='softmax')))
    model.compile(loss='categorical_crossentropy', optimizer=Adam(0.01), metrics=['accuracy'])
    print(ep)
    model.fit(x_train, y_train, batch_size=128, epochs=ep)

    model.save('./static/data/ner_model_test.h5')
    x = x_test
    y = y_test

def model_eve():

    model = load_model('./static/data/ner_model_test.h5')

    return model.evaluate(x, y)