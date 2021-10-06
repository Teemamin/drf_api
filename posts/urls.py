from django.urls import path
from posts import views

urlpatterns = [
    path('posts/', views.PostList.as_view()),
    # path('profiles/<int:pk>/', views.ProfileDetail.as_view()),
]