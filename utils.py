def process_form_data(data):
    data = dict(data)
    data.pop("csrfmiddlewaretoken")
    first_object = data.get(list(data.keys())[0])
    if isinstance(first_object, list):
        data = {key: value[0] for key, value in data.items()}
    return data

def validar_cpf(cpf: str) -> bool:
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    if int(cpf[9]) != (soma * 10 % 11) % 10:
        return False
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    return int(cpf[10]) == (soma * 10 % 11) % 10

def validar_cnpj(cnpj: str) -> bool:
    cnpj = ''.join(filter(str.isdigit, cnpj))
    if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
        return False
    pesos = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(cnpj[i]) * pesos[i] for i in range(12))
    if int(cnpj[12]) != (soma % 11) % 10:
        return False
    pesos = [6] + pesos
    soma = sum(int(cnpj[i]) * pesos[i] for i in range(13))
    return int(cnpj[13]) == (soma % 11) % 10