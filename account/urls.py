from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    #path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('', views.message_board, name='message_board'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    #path('login/message_board.html', views.message_board, name='message_board'),
    path('staff/post_numbers/', views.num_post, name='post-numbers'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('staff/staff_index', views.staff_index, name='staff-index'),
    path('post_numbers/', views.num_post, name="post-numbers"),
    path('user_profile/', views.user_profile, name="profilo-utente"),
    path('json/', views.last_hour, name="json-response"),
    path('account/staff/search/', views.search, name='search'),
    path('admin/account/userip/', views.getIp, name='getIp'),
    path('utente/<int:pk>/', views.user_profile, name="profilo-utente"),
]