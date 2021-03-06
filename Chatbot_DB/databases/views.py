from django.shortcuts import render
from .db_func import *
from .insert_data import *
from .check_post import *
# from django.http import JsonResponse
from django.http import HttpResponse
import json

from django.views.decorators.csrf import csrf_exempt

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
@csrf_exempt
def db_main(request):
    if request.method == 'POST':
        data = db_search(request)
        return HttpResponse(data, content_type="text/json-comment-filtered")
        # return JsonResponse({'reload_all': False, 'queryset_json': data})
    return render(request, 'temp_page.html')

# 관리자페이지-메인 학습요청
@csrf_exempt
def db_train(request):
    return render(request, 'temp_page.html')

# 관리자페이지-메인 테스트요청
@csrf_exempt
def db_test(request):
    return render(request, 'temp_page.html')

# 관리자페이지-데이터 db요청
@csrf_exempt
def db_data(request):
    if request.method == 'POST':
        data = json.dumps(db_search(request))
        return HttpResponse(data, content_type="text/json-comment-filtered")
    return render(request, 'temp_page.html')

# 관리자페이지-데이터 db수정
@csrf_exempt
def db_mod_data(request):
    if request.method == 'POST':
        data = json.dumps(db_search(request))
        context = {'mod_state': 'clear'}
        return HttpResponse(context, content_type="text/json-comment-filtered")
    return render(request, 'temp_page.html')

# 관리자페이지-응답 db요청
@csrf_exempt
def db_chat(request):
    if request.method == 'POST':
        data = json.dumps(db_search(request))
        return HttpResponse(data, content_type="text/json-comment-filtered")
    return render(request, 'temp_page.html')

# 관리자페이지-응답 db수정
@csrf_exempt
def db_mod_chat(request):
    if request.method == 'POST':
        data = json.dumps(db_search(request))
        context = {'mod_state': 'clear'}
        return HttpResponse(context, content_type="text/json-comment-filtered")
    return render(request, 'temp_page.html')

# train_db초기화
def train_db_init(request):
    insert_basic_db()
    return render(request, 'temp_page.html')

# 챗봇엔진서버 요청
# TODO