"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from main.views import get_main, get_about, get_catalog, get_delivery, get_contacts, get_basket, get_account_login, get_account_register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', get_main, name = 'main'),
    path('about/', get_about, name = 'about'),
    path('catalog/', get_catalog, name = 'catalog'),
    path('delivery/', get_delivery, name = 'delivery'),
    path('contacts/', get_contacts, name = 'contacts'),
    path('basket/', get_basket, name = 'basket'),
    path('login/', get_account_login, name = 'login'),
    path('register/', get_account_register, name = 'register'),
]
