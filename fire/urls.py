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
# from rest_framework import as_view

urlpatterns = [
    path('', views.login_page, name="login_page"),
    path('log_in/', views.log_in, name='log_in'),
    path('merchant_login_page/', views.merchant_login_page, name='merchant_login_page'),
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
    path('merchant_details/<str:id>/', views.merchant_details, name='merchant_details'),
    path('mblock/<str:m_id>/', views.mblock, name='mblock'),
    path('m_unblock/<str:m_id>/', views.m_unblock, name='m_unblock'),
    path('product_list/', views.product_list, name='product_list'),
    path('add_product/', views.add_product, name='add_product'),
    path('post_product/', views.post_product, name='post_product'),
    path('batch/', views.batch, name='batch'),
    path('batch_view/<str:b_id>/', views.batch_view, name='batch_view'),

    # path('get_user', views.get),


    







    # path('block/', views.block, name='block'),
    # path('Unblock/', views.Unblock, name='Unblock'),

    # path('dashboard/', views.dashboard , name='dashboard'),
]
