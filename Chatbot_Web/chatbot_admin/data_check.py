from email.policy import default
from itsdangerous import json
import pandas as pd
import pymysql
import pymysql.cursors
import logging

import os, sys
sys.path.append('../ChatServer')
from utils.Database import Database
from config.DatabaseConfig import *

class COUNTBAD:
    def __init__(self, db):
        self.db = db

    def bad_count(self):
        sql = "SELECT count(CASE WHEN ai_ner != 'None' AND (ai_intent = '인사' OR ai_intent = '욕설') OR check_answer = 'Bad' THEN 1 end) AS result FROM user_chat_data"

        result = self.db.select_one(sql)

        return result['result']

    def select_data(self, data):
        if data == 'all':
            sql = "SELECT * FROM user_chat_data"
        elif data == 'Bad':
            sql = f"SELECT * FROM user_chat_data WHERE check_answer  = '{data}'"
        else:
            sql = f"SELECT * FROM user_chat_data WHERE ai_intent  = '{data}'"
        # print('sql', sql)
        result = self.db.select_all(sql)
        return result

def database():
    db = Database(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db_name=DB_NAME
    )
    return db

def bad_data_len():
    db = database()
    db.connect()

    co = COUNTBAD(db)
    result = co.bad_count()

    return result




def select_data(data):
    db = database()
    db.connect()
    
    da = COUNTBAD(db)
    result = da.select_data(data)

    result = pd.DataFrame(result)
    result = result.to_json(orient = 'records')
    arr = []
    arr = json.loads(result)
    return arr

    
    

    