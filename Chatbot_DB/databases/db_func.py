import json

from django.core import serializers
from .models import TrainData, UserChatData

# 웹페이지
# 관리자페이지-메인 db요청
def db_search(cond):
    json_data = []
    # 검색조건 받는곳
    # TODO

    # 검색조건에 맞는 데이터검색
    temp = TrainData.objects.all()

    # json 변환
    # json_data = json.dumps(temp)
    json_data = json.loads(serializers.serialize('json', temp, ensure_ascii=False))

    return json_data




# 관리자페이지-메인 학습요청
# TODO

# 관리자페이지-메인 테스트요청
# TODO

# 관리자페이지-데이터 db요청
# TODO

# 관리자페이지-데이터 db수정
# TODO

# 관리자페이지-응답 db요청
# TODO

# 관리자페이지-응답 db수정
# TODO