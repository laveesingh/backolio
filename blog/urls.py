from django.conf.urls import url

from blog import views

urlpatterns = [
    url(r'^post/create/', views.post_create),
]