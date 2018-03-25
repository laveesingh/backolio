from django.conf.urls import url

from blog import views

urlpatterns = [
    url(r'^post/create/', views.post_create),
    url(r'^post/list/', views.get_posts),
    url(r'^tools/cfreport/', views.generate_cf_report)
]
