from django import forms
from local.models import Pais, Estado


class PaisForm(forms.ModelForm):
    class Meta:
        model = Pais
        fields = ["nome_pais", "sigla_pais"]
        error_messages = {
            "nome_pais": {
                "unique": "Este país já está cadastrado.",
            }
        }

    nome_pais = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Digite o nome do país"}),
    )

    def clean_nome_pais(self):
        nome_pais = self.cleaned_data.get("nome_pais").upper()
        if Pais.objects.filter(nome_pais=nome_pais).exists():
            raise forms.ValidationError("Este país já está cadastrado.")
        return nome_pais

    def clean_sigla(self):
        sigla = self.cleaned_data.get("sigla").upper()
        return sigla


class EstadoForm(forms.ModelForm):
    class Meta:
        model = Estado
        fields = "__all__"
        error_messages = {
            "nome_estado": {
                "unique": "Este estado já está cadastrado.",
            }
        }

    nome_estado = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Digite o nome do estado"}),
    )
