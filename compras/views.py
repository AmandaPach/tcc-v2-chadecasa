from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from .models import Compras, ComprasItem
from fornecedor.models import Fornecedor
from produtos.models import Produto, Categoria, TipoProduto
from pagamento.models import Pagamento, CondicaoPagamento


@csrf_exempt
def verify_nota(request):
    if request.method != "POST":
        return HttpResponse(status=405, content="Método não permitido.")

    nota_fiscal = request.POST.get("nota_fiscal")
    modelo_nota = request.POST.get("modelo_nota")
    serie = request.POST.get("serie")
    fornecedor_id = request.POST.get("fornecedor")

    compras_list = Compras.list(
        **{
            "nota_fiscal": nota_fiscal,
            "modelo_nota": modelo_nota,
            "serie": serie,
            "fornecedor_id": fornecedor_id,
        }
    )

    if compras_list:
        return HttpResponse(
            status=400, content="Já existe nota fiscal com esses dados."
        )

    return HttpResponse(status=200, content="Nota fiscal válida.")


def compra_list(request):
    if request.method == "POST":
        data_lists = dict(request.POST.lists())
        data_lists.pop("csrfmiddlewaretoken")

        nota_fiscal = data_lists.pop("nota_fiscal", True)[0]
        modelo_nota = data_lists.pop("modelo_nota", True)[0]
        serie = data_lists.pop("serie", True)[0]
        fornecedor_id = data_lists.pop("fornecedor_id", True)[0]

        data_emissao = data_lists.pop("data_emissao", True)[0]
        data_chegada = data_lists.pop("data_chegada", True)[0]

        if not data_emissao or not data_chegada:
            return HttpResponse(status=400, content="Data inválida.")

        to_date = lambda x: timezone.make_aware(
            timezone.datetime.strptime(x, "%Y-%m-%d")
        )
        data_emissao = to_date(data_emissao)
        data_chegada = to_date(data_chegada)

        valor_total = float(data_lists.pop("valor_total", True)[0])

        compras_list = Compras.list(
            **{
                "nota_fiscal": nota_fiscal,
                "modelo_nota": modelo_nota,
                "serie": serie,
                "fornecedor_id": fornecedor_id,
            }
        )
        if compras_list:
            return HttpResponse(status=400, content="Compra já cadastrada.")

        if data_emissao > timezone.localtime():
            return HttpResponse(status=400, content="Data de emissão inválida.")

        if data_chegada < data_emissao:
            return HttpResponse(status=400, content="Data de chegada inválida.")

        Compras.create(
            {
                "nota_fiscal": nota_fiscal,
                "modelo_nota": modelo_nota,
                "serie": serie,
                "fornecedor_id": fornecedor_id,
                "valor_total": valor_total,
                "data_emissao": data_emissao,
                "data_chegada": data_chegada,
            }
        )

        ultima_compra = Compras.list()[-1]

        for i in range(len(data_lists["produto_id"])):
            produto_id = data_lists["produto_id"][i]
            quantidade = data_lists["quantidade"][i]
            custo = data_lists["custo"][i]
            desconto = data_lists["desconto"][i]

            ComprasItem.create(
                {
                    "produto_id": produto_id,
                    "quantidade": quantidade,
                    "custo": custo,
                    "desconto": desconto,
                    "compra_id": ultima_compra["id"],
                }
            )

            Produto.update(produto_id, {"quantidade": quantidade})
        return JsonResponse(ultima_compra, status=200)

    compras_list = Compras.list()
    for i, compra in enumerate(compras_list):
        fornecedor_id = compra["fornecedor_id"]
        fornecedor = Fornecedor.get(fornecedor_id)
        compras_list[i]["fornecedor_nome"] = fornecedor["nome_fantasia_fornecedor"]
    fornecedores = Fornecedor.list()
    produtos = Produto.list()
    categorias = Categoria.list()
    tipos = TipoProduto.list()
    forma_pagamento = Pagamento.list()
    condicao_pagamento = CondicaoPagamento.list()

    return render(
        request,
        "compras/compra_list.html",
        {
            "compras": compras_list,
            "fornecedores": fornecedores,
            "produtos": produtos,
            "categorias": categorias,
            "tipos": tipos,
            "forma_pagamentos": forma_pagamento,
            "condicoes": condicao_pagamento,
        },
    )


def categoria_list(request):
    if request.method == "POST":
        data = request.POST
        data.pop("csrfmiddlewaretoken")
        Categoria.create(data)
        return redirect("compras:categoria_list")

    categorias = Categoria.list()
    return render(
        request,
        "compras/categoria_list.html",
        {
            "categorias": categorias,
        },
    )