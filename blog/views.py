import json
from collections import defaultdict
import requests

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from blog.models import Post
# Create your views here.


@csrf_exempt
def create_post(request):
    body = json.loads(request.body.decode('utf-8'))
    title = body.get('title')
    description = body.get('description')
    content = body.get('content')
    flag = 0
    if not title or not description or not content:
        print("Request is missing data")
        flag = 1
    else:
        Post.objects.create(
            title=title,
            description=description,
            content=content
        )
    if not flag:
        return JsonResponse({'message': 'failure'})
    return JsonResponse({'message': 'successful'})


@csrf_exempt
def update_post(request):
    body = json.loads(request.body.decode('utf-8'))
    pk = body.get('pk')
    title = body.get('title')
    description = body.get('description')
    content = body.get('content')
    flag = 0
    if not title or not description or not content:
        print("Request is missing data")
        flag = 1
    else:
        Post.objects.create(
            pk=pk,
            title=title,
            description=description,
            content=content
        )
    if not flag:
        return JsonResponse({'message': 'failure'})
    return JsonResponse({'message': 'successful'})


def get_posts(request):
    posts = serializers.serialize('json', Post.objects.all())
    posts = json.loads(posts)
    print('type:', type(posts))
    return JsonResponse({'posts': posts})


def get_post(request, pk):
    post = serializers.serialize('json', Post.objects.filter(pk=pk))
    post = json.loads(post)
    return JsonResponse({'post': post})


def delete_post(request, pk):
    post = Post.objects.filter(pk=pk)
    if post:
        post = post.first()
    else:
        return JsonResponse({
            'message': 'no such post exists',
            'status': 1
        })
    post.delete()
    return JsonResponse({
        'message': 'successful',
        'status': 0
    })


# this can be written directly on the frontend
def generate_cf_report(request):
    username = request.GET.get('username')
    url = 'http://codeforces.com/api/user.status?handle=%s' % str(username)
    data = requests.get(url)
    json_data = json.loads(data.text)
    return_dict = defaultdict(int)
    for submission in json_data['result']:
        return_dict[submission['verdict']] += 1
    return JsonResponse({'report': return_dict})
