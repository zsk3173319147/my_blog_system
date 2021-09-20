from os import name
from django.urls import path

from . import views

app_name='blog'

urlpatterns=[
    path('',views.IndexView.as_view(),name='index'),
    path('full.width',views.full_width,name='full_width'),
    path('about/',views.about,name='about'),
    path('contact',views.contact,name='contact'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    path('archives/<int:year>/<int:month>/',views.archive,name='archive'),
    path('categories/<int:pk>/',views.CategoryView.as_view(),name='category'),
    path('tags/<int:pk>/',views.tag,name='tag')
    ]
