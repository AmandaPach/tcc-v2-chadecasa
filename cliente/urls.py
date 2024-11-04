from django.urls import path
from cliente.views import index, manage

app_name = "cliente"

urlpatterns = [
    path("", index, name="list"),
    path("<int:cliente_id>/", manage, name="manage"),
]
