from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Pagamento, CondicaoPagamento, Parcela
from utils import process_form_data


def pagamento_list(request):
    if request.method == "POST":
        data = process_form_data(request.POST)
        data['status'] = data.get('status', '') == 'on'
        pagamento_id = data.pop("id")

        if not data.get("nome_forma_pgto"):
            return HttpResponse("Campo obrigatório não preenchido", status=400)

        if pagamento_id:
            Pagamento.update(pagamento_id, **data)
            return HttpResponse(status=200)

        Pagamento.create(data)
        new_pagamento = Pagamento.list()[-1]
        return JsonResponse(new_pagamento, status=200)
    pagamentos = Pagamento.list()
    return render(
        request, "pagamento/formaPagamento_list.html", {"pagamentos": pagamentos}
    )


@csrf_exempt
def pagamento_manage(request, pagamento_id):
    if request.method != "DELETE":
        return JsonResponse(status=400)
    Pagamento.delete_from_id(pagamento_id)
    return HttpResponse(status=200)


def condicao_pagamento_list(request):
    if request.method == "POST":
        data_lists = dict(request.POST.lists())
        data_lists.pop("csrfmiddlewaretoken")
        data_lists['status'] = data_lists.get('status', '') == 'on'
        nome = data_lists.pop("nome_condicao_pgto", False)[0]
        condicao_id = data_lists.pop("id")[0]
        if not nome:
            return HttpResponse(status=400, content="Campo obrigatório não preenchido.")

        parcelas_count = len(data_lists["parcela"])

        existente_condicao = CondicaoPagamento.list(nome_condicao_pgto=nome)
        if existente_condicao and "id" not in data_lists:
            return HttpResponse(
                status=400, content="Já existe uma condição de pagamento com esse nome."
            )

        required_colunas = [
            ("Parcela", "parcela"),
            ("Dias", "dias"),
            ("Percentual", "percentual"),
            ("Desconto", "desconto"),
            ("Taxa", "taxa"),
            ("Multa", "multa"),
            ("Forma de Pagamento", "forma_pagamento"),
        ]

        for coluna, key in required_colunas:
            if key not in data_lists:
                return HttpResponse(
                    status=400, content=f"Campo {coluna} é obrigatório."
                )

        if condicao_id:
            CondicaoPagamento.update(
                condicao_id, nome_condicao_pgto=nome, parcela=parcelas_count
            )
            Parcela.delete(condicao_pgto_id=condicao_id)

        CondicaoPagamento.create(
            {
                "nome_condicao_pgto": nome,
                "parcela": parcelas_count,
            }
        )
        new_condicao_pagamento = CondicaoPagamento.list()[-1]

        for i in range(len(data_lists["parcela"])):
            parcela = {
                "numero_parcela": data_lists["parcela"][i],
                "dia_pgto_parcela": data_lists["dias"][i],
                "porcentagem_pgto_parcela": data_lists["percentual"][i],
                "desconto_pgto_parcela": data_lists["desconto"][i],
                "juros_pgto_parcela": data_lists["taxa"][i],
                "multa_pgto_parcela": data_lists["multa"][i],
                "forma_pgto_id": data_lists["forma_pagamento"][i],
                "condicao_pgto_id": new_condicao_pagamento["id"],
            }
            Parcela.create(parcela)

        if "id" in data_lists:
            return HttpResponse(status=200)

        return JsonResponse(new_condicao_pagamento, status=200)

    condicoes = CondicaoPagamento.list()
    for condicao in condicoes:
        parcelas = Parcela.list(condicao_pgto_id=condicao["id"])
        condicao["parcelas"] = parcelas
    pagamentos = Pagamento.list()
    return render(
        request,
        "pagamento/condicaoPagamento_list.html",
        {"condicoes": condicoes, "pagamentos": pagamentos},
    )


@csrf_exempt
def condicao_pagamento_manage(request, condicao_pagamento_id):
    if request.method == "GET":
        condicao_pagamento = CondicaoPagamento.get(condicao_pagamento_id)
        if not condicao_pagamento:
            return HttpResponse(
                status=400, content="Condição de pagamento não encontrada"
            )
        parcelas = Parcela.list(condicao_pgto_id=condicao_pagamento_id)
        condicao_pagamento["parcelas"] = parcelas
        return JsonResponse(condicao_pagamento, status=200)
    if request.method == "DELETE":
        CondicaoPagamento.delete_from_id(condicao_pagamento_id)
        return HttpResponse(status=200)
    return HttpResponse(status=400, content="Método não permitido")