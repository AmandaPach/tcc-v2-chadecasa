from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Produto, Categoria, TipoProduto

from compras.models import ComprasItem
from utils import process_form_data


def produto_list(request):
    if request.method == "POST":
        data = process_form_data(request.POST)
        produto_id = data.pop("id")
        if not all(data.values()):
            return HttpResponse("Campo obrigatório não preenchido", status=400)

        produto_nome = data["nome_produto"]
        produtos = Produto.list(nome_produto=produto_nome)
        if produtos and "id" not in data:
            return HttpResponse(
                status=400, content=f'Produto "{produto_nome}" já cadastrado'
            )

        if produto_id:
            Produto.update(produto_id, **data)
            return HttpResponse(status=200)

        Produto.create(data)
        new_produto = Produto.list()[-1]
        return HttpResponse(new_produto, status=200)

    categorias = Categoria.list()
    tipos = TipoProduto.list()
    produtos = Produto.list()

    for index, produto in enumerate(produtos):
        compras = ComprasItem.list(produto_id=produto["id"])
        if not compras:
            produtos[index]["preco_medio"] = "-"
            continue
        total = 0
        for compra in compras:
            total_item = (compra["custo"] - compra["desconto"]) * compra["quantidade"]
            total += total_item
        produtos[index]["preco_medio"] = f"R$ {total:.2f}"

    for index, produto in enumerate(produtos):
        categoria = Categoria.list(id=produto["categoria_id"])
        if categoria:
            categoria = categoria[0]
            produtos[index]["categoria_nome"] = categoria["nome_categoria"]

        tipo = TipoProduto.list(id=produto["tipo_id"])
        if tipo:
            tipo = tipo[0]
            produtos[index]["tipo_nome"] = tipo["nome_tipo"]

    return render(
        request,
        "produtos/produto_list.html",
        {"produtos": produtos, "categorias": categorias, "tipos": tipos},
    )


@csrf_exempt
def produto_manage(request, produto_id):
    if request.method == "DELETE":
        Produto.delete_from_id(produto_id)
        return HttpResponse(status=200)
    if request.method == "GET":
        produto = Produto.get(produto_id)
        if not produto:
            return HttpResponse(status=400, content="Produto não encontrado")
        if produto["categoria_id"]:
            categoria = Categoria.get(produto["categoria_id"])
            produto["categoria"] = categoria["nome_categoria"]
        if produto["tipo_id"]:
            tipo = TipoProduto.get(produto["tipo_id"])
            produto["tipo"] = tipo["nome_tipo"]
        return JsonResponse(produto, status=200)
    return HttpResponse(status=400, content="Método não permitido")


def categoria_list(request):
    if request.method == "POST":
        data = process_form_data(request.POST)
        data['status'] = data.get('status', '') == 'on'
        categoria_id = data.pop("id", False)

        categoria_nome = data["nome_categoria"]
        if not categoria_nome:
            return HttpResponse("Campo obrigatório não preenchido", status=400)


        categorias = Categoria.list(nome_categoria=categoria_nome)
        if categorias and not categoria_id:
            return HttpResponse(
                status=400, content=f'Categoria "{categoria_nome}" já cadastrada'
            )

        if categoria_id:
            Categoria.update(categoria_id, **data)
            return HttpResponse(status=200)

        Categoria.create(data)
        new_categoria = Categoria.list()[-1]
        return JsonResponse(new_categoria, status=200)

    categorias = Categoria.list()
    return render(request, "produtos/categoria_list.html", {"categorias": categorias})


@csrf_exempt
def categoria_manage(request, categoria_id):
    if request.method == "DELETE":
        produtos = Produto.list(categoria_id=categoria_id)
        if produtos:
            return HttpResponse(
                status=400, content="Existem produtos vinculados a esta categoria"
            )

        Categoria.delete_from_id(categoria_id)
        return HttpResponse(status=200)
    if request.method == "GET":
        categoria = Categoria.get(categoria_id)
        if not categoria:
            return HttpResponse(status=400, content="Categoria não encontrada")
        return JsonResponse(categoria, status=200)
    return HttpResponse(status=400, content="Método não permitido")


def tipo_produto_list(request):
    if request.method == "POST":
        data = process_form_data(request.POST)
        tipo_id = data.pop("id", False)
        data['status'] = data.get('status', '') == 'on'

        tipo_nome = data["nome_tipo"]
        tipos = TipoProduto.list(nome_tipo=tipo_nome)
        if tipos and not tipo_id:
            return HttpResponse(
                status=400, content=f'Tipo de produto "{tipo_nome}" já cadastrado'
            )

        if tipo_id:
            TipoProduto.update(tipo_id, **data)
            return HttpResponse(status=200)

        TipoProduto.create(data)
        new_produto = TipoProduto.list()[-1]
        return HttpResponse(new_produto, status=200)

    tipos_produtos = TipoProduto.list()
    return render(
        request, "produtos/tipo_produto_list.html", {"tipos_produtos": tipos_produtos}
    )


@csrf_exempt
def tipo_produto_manage(request, tipo_produto_id):
    if request.method == "DELETE":
        produtos = Produto.list(tipo_id=tipo_produto_id)
        if produtos:
            return HttpResponse(
                status=400, content="Existem produtos vinculados a este tipo de produto"
            )

        TipoProduto.delete_from_id(tipo_produto_id)
        return HttpResponse(status=200)

    if request.method == "GET":
        tipo_produto = TipoProduto.get(tipo_produto_id)
        if not tipo_produto:
            return HttpResponse(status=400, content="Tipo de produto não encontrado")
        return JsonResponse(tipo_produto, status=200)

    return HttpResponse(status=400, content="Método não permitido")