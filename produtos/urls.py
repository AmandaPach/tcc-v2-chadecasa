from django.urls import path
from produtos.views import (
    produto_list,
    categoria_list,
    tipo_produto_list,
    produto_manage,
    categoria_manage,
    tipo_produto_manage,
)

app_name = "produtos"

urlpatterns = [
    path("", produto_list, name="list"),
    path("<int:produto_id>/", produto_manage, name="manage"),
    path("tipos/", tipo_produto_list, name="tipo-produto-list"),
    path(
        "tipos/<int:tipo_produto_id>/", tipo_produto_manage, name="tipo-produto-manage"
    ),
    path("categorias/", categoria_list, name="categoria-list"),
    path("categorias/<int:categoria_id>/", categoria_manage, name="categoria-manage"),
]
