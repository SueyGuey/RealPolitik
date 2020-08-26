"""realpolitik URL Configuration

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
from django.urls import path, include
from django.contrib.auth import views as auth_view
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

from pages.views import home, contact, about, HomeDetailView
from accounts import views as acc_view

urlpatterns = [
	path('', include("pages.urls")),
    path('register/', acc_view.register, name = "register"),
    path('login/', auth_view.LoginView.as_view(template_name = 'login.html'), name = "login"),
    path('logout/', auth_view.LogoutView.as_view(template_name = 'logout.html'), name = "logout"),
    path('password-reset/', auth_view.PasswordResetView.as_view(template_name = 'password_reset.html'), name = "password_reset"),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name = 'password_reset_done.html'), name = "password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name = 'password_reset_confirm.html'), name = "password_reset_confirm"),
    path('admin/', admin.site.urls),
    path('profile/', acc_view.profile, name = "profile" ),
    path('contact/', contact, name = "contact" ),
    path('about/', about, name = "about" ),
    path('<int:pk>', HomeDetailView.as_view(), name = "ArticleDetail")
]

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)