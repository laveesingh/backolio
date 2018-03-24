from django.shortcuts import render
from django.http import JsonResponse

from main.models import Post
# Create your views here.

def create_post(request):
    body = request.POST
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
    return JsonResponse({'message': 'successful'})
