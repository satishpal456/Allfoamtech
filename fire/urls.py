"""firebase URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name="login_page"),
    path('log_in/', views.log_in, name='log_in'),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('logout/', views.logout, name='logout'),
    path('user_list/', views.user_list, name='user_list'),
    path('view_list/<str:id>/', views.view_list, name='view_list'),
    path('qr_code/', views.qr_code, name='qr_code'),
    path('post_generate_qr/', views.post_generate_qr, name='post_generate_qr'),
    path('qr_code_list/', views.qr_code_list, name='qr_code_list'),
    path('ublock/<str:d_id>/', views.ublock, name='ublock'),
    path('u_unblock/<str:d_id>/', views.u_unblock, name='u_unblock'),
    path('video_details_home/', views.video_details_home, name='video_details_home'),
    path('quiz_list/<str:id>/', views.quiz_list, name='quiz_list'),
    path('add_ques/', views.add_ques, name='add_ques'),
    path('merchant_list/', views.merchant_list, name='merchant_list'),
    path('add_merchant/', views.add_merchant, name='add_merchant'),
    







    # path('block/', views.block, name='block'),
    # path('Unblock/', views.Unblock, name='Unblock'),

    # path('dashboard/', views.dashboard , name='dashboard'),
]
