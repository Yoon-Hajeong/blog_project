from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('<int:id>/', views.blog_detail, name='blog_detail'),
    path('write/', views.post_write, name='post_write'),
    path('edit/<int:id>/', views.post_edit, name='post_edit'),
    path('delete/<int:id>/', views.post_delete, name='post_delete'),
    path('search/<str:tag>/', views.post_search, name='post_search_tag'),
    path('search/', views.post_search, name='post_search'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('blog/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),

]