from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("", views.orders_list, name="orders_list"),
    path("create/", views.order_create, name="order_create"),
]
