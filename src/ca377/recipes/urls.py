from django.urls import path

from . import views

urlpatterns = [
    # Every path here has a recipes/ in front of it
    # The name is the name of the URL and we can use it in templates
    path('', views.index, name='index'),
    path('index.html', views.index, name='index'),
]
