"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from dj_rest_auth.views import PasswordResetConfirmView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    # API urls
    # authentication
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/auth/', include('accounts.api_urls', namespace='api-auth')),
    path('api/v1/auth/password/reset/confirm/<uibd64>/<token>/',
         PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # other app
    path('api/v1/shop/', include('shop.api_urls', namespace='api-shop')),

    # Traditional Django urls
    path('admin/', admin.site.urls),
    path('accounts/', include("accounts.urls", namespace="accounts")),
    path('cart/', include("cart.urls", namespace="cart")),
    path('orders/', include("orders.urls", namespace="orders")),
    path('coupons/', include("coupons.urls", namespace="coupons")),
    path('payments/', include("payments.urls", namespace="payments")),
    path('reviews/', include("reviews.urls", namespace="reviews")),
    path('', include("shop.urls", namespace="shop")),
]
urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,
                      document_root=settings.STATIC_ROOT)


# API Schema
urlpatterns += [
    # YOUR PATTERNS
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/v1/swagger/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1/schema/redoc/',
         SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
