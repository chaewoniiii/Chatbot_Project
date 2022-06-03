from .models import TrainData, UserChatData
import pandas as pd

# 기본 데이터 db등록
# 1회만 실행

# db등록함수
def insert_train_db(data):
    temp = TrainData()

    temp.intent = data['intent']
    temp.ner = data['ner']
    temp.query = data['query']
    temp.answer = data['answer']
    temp.answer_add = data['answer_add']
    temp.stage = data['stage']
    temp.stage_change = data['stage_change']

    temp.save()

def insert_user_db(data):
    temp = UserChatData

    temp.query = data['query']
    temp.ai_intent = data['ai_intent']
    temp.ai_ner = data['ai_ner']
    
    temp.save()

basic_data = []

# 기본정보 입력
def insert_basic_db():
    basic_data = pd.read_excel('basic_datas.xlsx', header=0)

    for num, data in basic_data.iterrows():
        insert_train_db(data)
