from .models import TrainData, UserChatData
import pandas as pd
import os

# 기본 데이터 db등록

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
    # db 초기화
    TrainData.objects.all().delete()
    
    # # xlsx파일 불러오기
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    XLSX_DIR = os.path.join(BASE_DIR, 'basic_datas.xlsx')
    basic_data = pd.read_excel(XLSX_DIR, header=0)

    # 저장
    for num, data in basic_data.iterrows():
        insert_train_db(data)

    # 확인
    temp = TrainData.objects.all()
    print(temp)
