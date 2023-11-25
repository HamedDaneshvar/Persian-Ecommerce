from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("", views.orders_list, name="orders_list"),
    path("create/", views.order_create, name="order_create"),
    path("<int:id>/", views.order_detail, name="order_detail"),
    path("<int:order_id>/payment/", views.send_to_payment,
         name="order_payment")
]
