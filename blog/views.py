import json
from collections import defaultdict
import requests

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from blog.models import Post
# Create your views here.


class Response:

    def __init__(self, **kwargs):
        self.message = kwargs.get('message')
        self.status = kwargs.get('status')
        self.data = kwargs.get('data')

    def serialize(self):
        return self.__repr__()

    def deserialize(self):
        return self.__dict__

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return json.dumps(self.__dict__)


@csrf_exempt
def create_post(request):
    res = Response()
    body = json.loads(request.body.decode('utf-8'))
    title = body.get('title')
    description = body.get('description')
    content = body.get('content')
    if not (title and description and content):
        res.message = 'request is missing data'
        res.status = 1
        return JsonResponse(res.deserialize())
    post = Post.objects.create(
        title=title,
        description=description,
        content=content
    )
    post = json.loads(serializers.serialize('json', Post.objects.filter(pk=post.pk)))
    res.message = 'successful'
    res.status = 0
    res.data = post
    return JsonResponse(res.deserialize())


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
    res = Response()
    queryset = Post.objects.all()
    if not queryset:
        res.message = 'could not find any posts, maybe the list is empty'
        res.status = 1
        return JsonResponse(res.deserialize())
    try:
        serialized_queryset = serializers.serialize('json', queryset)
    except Exception as e:
        print(e)
        res.message = 'could not json serialize the queryset'
        res.status = 1
        return JsonResponse(res.deserialize())
    res.message = 'successful'
    res.status = 0
    res.data = json.loads(serialized_queryset)
    return JsonResponse(res.deserialize())


def get_post(request, pk):
    res = Response()
    queryset = Post.objects.filter(pk=pk)
    if not queryset:
        res.message = 'post with id {0} does not exist'.format(pk)
        res.status = 1
        return JsonResponse(res.deserialize())
    try:
        post = serializers.serialize('json', queryset)
    except Exception as e:
        print(e)
        res.message = 'could not json serialize the queryset'
        res.status = 1
        return JsonResponse(res.deserialize())
    res.message = 'successful'
    res.status = 0
    res.data = json.loads(post)[0]
    return JsonResponse(res.deserialize())


def delete_post(request, pk):
    queryset = Post.objects.filter(pk=pk)
    res = Response()
    if queryset:
        post = queryset.first()
        post.delete()
        res.message = 'successful'
        res.status = 0
        res.data = json.loads(serializers.serialize('json', queryset))[0]
    else:
        res.message = 'post with id {0} does not exist'.format(pk)
        res.status = 1
    return JsonResponse(res.deserialize())


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
