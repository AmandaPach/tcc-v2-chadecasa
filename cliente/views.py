from http.client import HTTP_PORT
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

from .models import Cliente
from local.models import Cidade
from utils import process_form_data, validar_cpf


def index(request):
    if request.method == "POST":
        data = process_form_data(request.POST)
        cliente_id = data.pop("id")
        data['status'] = data.get('status', '') == 'on'
        data['estrangeiro_cliente'] = data.get('estrangeiro_cliente', '') == 'on'
        required_fields = [
            "nome_cliente",
            "sobrenome_cliente",
            "sexo_cliente",
            "data_nascimento_cliente",
            "rua_cliente",
            "numero_rua_cliente",
            "telefone_cliente",
            "bairro_cliente",
            "cep_cliente",
            "cidade_id",
        ]
        for field in required_fields:
            if not data.get(field):
                print(field)
                return HttpResponse(f"Campo obrigatório não preenchido", status=400)
        estrangeiro = data.get("estrangeiro_cliente")
        cpf_cliente = data.get("cpf_cliente")
        if not validar_cpf(cpf_cliente):
            return HttpResponse("CPF inválido. Verifique e tente novamente", status=400)
        
        unique_fields = {
            "cpf_cliente": ("CPF", cpf_cliente),
            "rg_cliente": ("RG", data.get("rg_cliente")),
        }

        for field, (field_name, field_value) in unique_fields.items():
            if not field_value:
                if estrangeiro == "on":
                    continue
                return HttpResponse(
                    f"{field_name} é obrigatório para nativos", status=400
                )

            unique_lista = Cliente.list(
                **{
                    field: (
                        field_value
                        if not isinstance(field_value, list)
                        else field_value[0]
                    )
                }
            )
            if unique_lista and "id" not in data:
                return HttpResponse(
                    f'{field_name} "{field_value}" já cadastrado', status=400
                )

        if cliente_id:
            Cliente.update(cliente_id, **data)
            return HttpResponse(status=200)

        Cliente.create(data)
        new_cliente = Cliente.list()[-1]
        return HttpResponse(new_cliente, status=200)

    clientes = Cliente.list()
    cidades = Cidade.list()
    return render(
        request, "cliente/cliente_list.html", {"clientes": clientes, "cidades": cidades}
    )


@csrf_exempt
def manage(request, cliente_id):
    if request.method == "DELETE":
        Cliente.delete_from_id(cliente_id)
        return HttpResponse(status=200)

    if request.method == "GET":
        cliente = Cliente.get(cliente_id)
        if not cliente:
            return HttpResponse(status=400, content="Cliente não encontrado")
        cliente_cidade = cliente.get("cidade_id")
        cliente_estado = cliente.get("estado_id")
        cliente["cidade"] = cliente_cidade["nome_cidade"] if cliente_cidade else None
        cliente["estado"] = cliente_estado["nome_estado"] if cliente_estado else None
        return JsonResponse(cliente, status=200)

    return HttpResponse(status=400, content="Método não permitido")