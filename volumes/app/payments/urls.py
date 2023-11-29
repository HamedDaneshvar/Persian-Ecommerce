from django.urls import path
from . import views

app_name = "payments"
urlpatterns = [
    path("request/", views.send_request, name="request"),
    path("verify/", views.verify, name="verify"),
    path("inactive/", views.inactive_gateway, name="inactive_gateway"),
]
