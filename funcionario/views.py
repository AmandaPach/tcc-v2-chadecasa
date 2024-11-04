from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import Funcionario, Cargo
from local.models import Cidade
from utils import process_form_data, validar_cpf

funcionario_required_fields = [
    "nome_funcionario",
    "sobrenome_funcionario",
    "sexo_funcionario",
    "telefone_funcionario",
    "data_nascimento_funcionario",
    "rua_funcionario",
    "numero_rua_funcionario",
    "cep_funcionario",
    "cidade_id",
    "cargo_id",
]

cargo_required_fields = ["nome_cargo"]


def funcionario_list(request):
    if request.method == "POST":
        data = process_form_data(request.POST)
        funcionario_id = data.pop("id")
        funcionario_cpf = data.pget("cpf_funcionario")

        if funcionario_cpf and not validar_cpf(funcionario_cpf):
            return HttpResponse("CPF inválido. Verifique e tente novamente", status=400)

        for field in funcionario_required_fields:
            if not data.get(field):
                print(field)
                return HttpResponse(f"Campo obrigatório não preenchido", status=400)

        unique_fields = {
            "cpf_funcionario": ("CPF", data.get("cpf_funcionario")),
            "rg_funcionario": ("RG", data.get("rg_funcionario")),
        }
        for field, (field_name, field_value) in unique_fields.items():
            if not field_value:
                estrangeiro = data.get("estrangeiro_funcionario")
                if estrangeiro == "on" and field == "rg_funcionario":
                    continue
                return HttpResponse(f"{field_name} não informado", status=400)

            unique_lista = Funcionario.list(**{field: field_value})
            if unique_lista and funcionario_id:
                return HttpResponse(
                    f'{field_name} "{field_value}" já cadastrado', status=400
                )

        if funcionario_id:
            Funcionario.update(funcionario_id, **data)
            return HttpResponse(status=200)

        Funcionario.create(data)
        novo_funcionario = Funcionario.list()[-1]
        return HttpResponse(novo_funcionario, status=200)

    funcionarios = Funcionario.list()
    for funcionario in funcionarios:
        funcionario["cargo"] = Cargo.get(funcionario["cargo_id"])["nome_cargo"]
    cargos = Cargo.list()
    cidades = Cidade.list()
    return render(
        request,
        "funcionario/funcionario_list.html",
        {"funcionarios": funcionarios, "cargos": cargos, "cidades": cidades},
    )


@csrf_exempt
def funcionario_manage(request, funcionario_id):
    if request.method == "DELETE":
        Funcionario.delete_from_id(funcionario_id)
        return HttpResponse(status=200)
    if request.method == "GET":
        funcionario = Funcionario.get(funcionario_id)
        if not funcionario:
            return HttpResponse(status=400, content="Funcionário não encontrado")
        return JsonResponse(funcionario, status=200)
    return HttpResponse(status=400, content="Método não permitido")


def cargo_list(request):
    if request.method == "POST":
        data = process_form_data(request.POST)
        cargo_id = data.pop("id")

        for field in cargo_required_fields:
            if not data.get(field):
                return HttpResponse(f"Campo obrigatório não preenchido", status=400)

        cargos_existentes = Cargo.list(nome_cargo=data["nome_cargo"])
        if cargos_existentes and not cargo_id:
            return HttpResponse(
                status=400, content="Já existe um Cargo com esse nome cadastrado."
            )

        if cargo_id:
            Cargo.update(cargo_id, **data)
            return HttpResponse(status=200)

        Cargo.create(data)
        novo_cargo = Cargo.list()[-1]
        return JsonResponse(novo_cargo, status=200)
    cargos = Cargo.list()
    return render(request, "funcionario/cargo_list.html", {"cargos": cargos})


@csrf_exempt
def cargo_manage(request, cargo_id):
    if request.method == "DELETE":
        funcionarios = Funcionario.list(cargo_id=cargo_id)
        if funcionarios:
            return HttpResponse(
                status=400,
                content=f"Não é possível remover um Cargo que possui funcionários. Remova os funcionários primeiro: {', '.join([funcionario['nome_funcionario'] for funcionario in funcionarios])}",
            )
        Cargo.delete_from_id(cargo_id)
        return HttpResponse(status=200)
    if request.method == "GET":
        cargo = Cargo.get(cargo_id)
        if not cargo:
            return HttpResponse(status=400, content="Cargo não encontrado")
        return JsonResponse(cargo, status=200)
    return HttpResponse(status=400, content="Método não permitido")