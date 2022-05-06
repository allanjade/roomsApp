from xml.etree.ElementInclude import include
from django.urls import URLPattern, path
from . import views


urlpatterns =[
    path('', views.getRoutes),
    path('roomlist/', views.getRooms),
    path('roomlist/<str:pk>', views.getRoom)
    ]

