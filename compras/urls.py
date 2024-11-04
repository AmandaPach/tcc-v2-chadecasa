from django.urls import path
from .views import compra_list, verify_nota

app_name = "compras"

urlpatterns = [
    path("", compra_list, name="list"),
    path("nota/", verify_nota, name="verify_nota"),
]
