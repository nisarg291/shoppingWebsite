"""healthcare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin

from django.conf import settings
from django.urls import path,include
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .views import (
    ProductListView,
)
from django.conf.urls.static import static
#from app.views import notifications,clear_notifications
from app.views import islogin
from . import views
from app import views as vw
from shop import views as sp
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('logout',vw.dj_logout,name="logout"),
    path('register/',vw.register,name="register"),
    path('Page=<int:id>',views.next,name='next'),
    path('login',vw.dj_login,name="login"),
    #path('accounts/',include('allauth.urls')),
    path('verification/', include('verify_email.urls'),name="verification"),
    path("password-reset/", PasswordResetView.as_view(template_name='password_reset.html'),name="password_reset"),
    #path("password-reset/", PasswordResetView.as_view(template_name='password_reset.html'),name="password_reset"),
   # path('login/', views.login_view, name = 'login'),
	#path("password-reset/done/", PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name="password_reset_done"),
    path('islogin', islogin),
	path("password-reset-confirm/<uidb64>/<token>/", PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name="password_reset_confirm"),

	path("password-reset-complete/", PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name="password_reset_complete"),
    
	path("password-reset/done/", PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name="password_reset_done"),

	path("password-reset-confirm/<uidb64>/<token>/", PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name="password_reset_confirm"),
    path("otpverify",vw.otpverify,name="otpverify"),
    path('product/<int:id>',views.productview,name="productview"),
    path('addtocart/<int:id>',views.addToCart,name="addToCart"),
    path('addcart/',views.addCart,name="addCart"),
    path('updateCart/',views.updateCart,name="updateCart"),
    path('Search', views.search, name='search'),
    path('cart/',views.cart,name="cart"),
    path('address/',views.address,name="address"),
    path('SearchPage=<int:id>',views.search1,name='searchNext'),
    path('payment/', views.payment, name='payment'),
    path('response/',views.response, name='response'),
    path(r'^activate/('r'?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',vw.activate, name='activate'),

   # path('notifications', notifications),
	#path('notifications/clear', clear_notifications)
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
