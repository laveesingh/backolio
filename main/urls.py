from django.conf.urls import url

from main import views

urlpatterns = [
    url(r'^post/create/', views.post_create),
]
