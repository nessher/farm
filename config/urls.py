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
from main.views import get_main, get_about, get_catalog, get_category_catalog, get_delivery, get_contacts, cart_add, \
    cart_detail, account_auth, profile, checkout, orders
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', get_main, name = 'main'),
    path('about/', get_about, name = 'about'),
    path('catalog/', get_category_catalog, name = 'catalog'),
    path('catalog/<int:id>/', get_catalog, name = 'catalog_current'),
    path('delivery/', get_delivery, name = 'delivery'),
    path('contacts/', get_contacts, name = 'contacts'),
    path('cart/', cart_detail, name = 'cart_detail'),
    path('cart/add/<int:product_id>/', cart_add, name='cart_add'),
    path('checkout/', checkout, name='checkout'),
    path('orders/', orders, name='orders'),
    path('auth/', account_auth, name = 'auth'),
    path('profile/', profile, name = 'profile'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
