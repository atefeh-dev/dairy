from django.conf.urls import url
from . import views
from django.urls import path, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

# create_user = views.UserViewSet.as_view({'POST': 'create'})

urlpatterns = [
    path('users/', views.UserViewSet.as_view({
        'get': 'list',
        'post': 'create', })),

    path('ResetPassword/<str:pk>/', views.UserViewSet.as_view({
        'post': 'update', })),
]

urlpatterns = format_suffix_patterns(urlpatterns)
