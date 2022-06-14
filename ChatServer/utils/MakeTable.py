class MakeTable:
    
    # Database 인스턴스 객체로 생성
    def __init__(self, db):
        self.db = db

    # 테이블 확인
    def check_table(self, table):
        sql = f'SELECT count(*) as result FROM Information_schema.tables \
            WHERE table_schema = "mydb118" \
            AND table_name = "{table}"'
        
        result = self.db.select_one(sql)
        # print('테이블결과:',result['result'])
        return result['result']   # 있으면1, 없으면 0

    # 테이블 생성
    def make_table_chat(self):
        if self.check_table('user_chat_data') == 0: return 0
        
        sql = f'CREATE TABLE user_chat_data (\
            id INT NOT NULL AUTO_INCREMENT, \
            query TEXT, \
            ai_intent VARCHAR(32), \
            ai_ner VARCHAR(32), \
            check_answer VARCHAR(32), \
            reg_date DATETIME DEFAULT CURRENT_TIMESTAMP, \
            PRIMARY KEY(id)\
            ) ENGINE=MYISAM CHARSET=utf8;'

        result = self.db.select_one(sql)
        return result

    def make_table_answer(self):
        pass

    # 테이블 삭제
    def drop_table(self, table):
        pass

    # 테이블 데이터 초기화(엑셀파일기준)
    def init_table_chat(self, file):
        pass
   
    def init_table_answer(self, file):
        pass
    

    
    







# 엑셀파일 넣기
# LOAD DATA INFILE '/test/abcd.csv' INTO TABLE ABC FIELDS TERMINATED BY ',';