from django import forms
from funcionario.models import Funcionario, CargoFuncionario


class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = "__all__"


class CargoFuncionarioForm(forms.ModelForm):
    class Meta:
        model = CargoFuncionario
        fields = "__all__"
