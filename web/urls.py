from django.conf.urls import url
from . import views
from .views import register , active
from django.urls import path, include

# create_user = views.UserViewSet.as_view({'POST': 'create'})

urlpatterns = [
    path('register/', views.register),
    path('register/<int:id>/<str:token>/', views.active, name='active'),

]

