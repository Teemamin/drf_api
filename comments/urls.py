from django.urls import path
from comments import views

urlpatterns = [
    path('comments/', views.CommentList.as_view()),
    # path('posts/<int:pk>/', views.PostDetail.as_view()),
]