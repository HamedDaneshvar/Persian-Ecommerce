from django.urls import path
from . import api

app_name = "shop"

# API urls
urlpatterns = [
    path('', api.ProductListCreateAPI.as_view(), name="product-list-create"),
    path('<int:pk>/', api.ProductDetailAPI.as_view(), name="product-detail"),
    path('category/', api.CategoryListCreateAPI.as_view(),
         name="category-list-create"),
    path('category/<int:pk>/', api.CategoryDetailAPI.as_view(),
         name="category-detail"),
]
