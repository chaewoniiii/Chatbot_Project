from django.shortcuts import render
from .web_func import *
from django.core import serializers
from django.http import HttpResponse
import json

web_url = ''

def test(request):
    # posts = Post.objects.filter(published_at__isnull=False).order_by('-published_at')
    data = [
        {
            'test1': '123',
            'test2': '234',
        },
        {
            'test3': 'asd',
            'test4': 'qwe',
        }
    ]
    # post_list = serializers.serialize('json', data)
    post_list = json.dumps(data)
    return HttpResponse(post_list, content_type="text/json-comment-filtered")

# 웹페이지
# 관리자페이지-메인 db요청
def db_main(request):
    if request.method == 'POST':
        data = json.dumps(db_search(request))
        return HttpResponse(data, content_type="text/json-comment-filtered")
    return render(request, 'temp_page.html')

# 관리자페이지-메인 학습요청
def db_train(request):
    return render(request, 'temp_page.html')

# 관리자페이지-메인 테스트요청
def db_test(request):
    return render(request, 'temp_page.html')

# 관리자페이지-데이터 db요청
def db_data(request):
    if request.method == 'POST':
        data = json.dumps(db_search(request))
        return HttpResponse(data, content_type="text/json-comment-filtered")
    return render(request, 'temp_page.html')

# 관리자페이지-데이터 db수정
def db_mod_data(request):
    if request.method == 'POST':
        data = json.dumps(db_search(request))
        context = {'mod_state': 'clear'}
        return HttpResponse(context, content_type="text/json-comment-filtered")
    return render(request, 'temp_page.html')

# 관리자페이지-응답 db요청
def db_chat(request):
    if request.method == 'POST':
        data = json.dumps(db_search(request))
        return HttpResponse(data, content_type="text/json-comment-filtered")
    return render(request, 'temp_page.html')

# 관리자페이지-응답 db수정
def db_mod_chat(request):
    if request.method == 'POST':
        data = json.dumps(db_search(request))
        context = {'mod_state': 'clear'}
        return HttpResponse(context, content_type="text/json-comment-filtered")
    return render(request, 'temp_page.html')


# 챗봇엔진서버 요청
# TODO