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
def post_create(request):
    body = json.loads(request.body.decode('utf-8'))
    title = body.get('title')
    description = body.get('description')
    content = body.get('content')
    print(title, description, content)
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

def get_posts(request):
    posts = serializers.serialize('json', Post.objects.all())
    posts = json.loads(posts)
    print('type:', type(posts))
    return JsonResponse({'posts': posts})

