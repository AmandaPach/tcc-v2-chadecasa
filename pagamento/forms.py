from django import forms
from django.forms import inlineformset_factory
from pagamento.models import CondicaoPagamento, Parcela
from crispy_forms.helper import FormHelper


class CondicaoPagamentoForm(forms.ModelForm):
    class Meta:
        model = CondicaoPagamento
        fields = ["nome_condicao_pgto"]
        help_texts = {
            "nome_condicao_pgto": 'Exemplo: 30 / 60 / 90 BB"',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"

        self.fields["nome_condicao_pgto"].widget.attrs.update(
            {"style": "text-transform: uppercase;", "class": "form-control"}
        )


class ParcelaForm(forms.ModelForm):
    class Meta:
        model = Parcela
        fields = ["numero_parcela", "dia_pgto_parcela"]


# Criação do formset para as parcelas
ParcelaFormSet = inlineformset_factory(
    CondicaoPagamento, Parcela, form=ParcelaForm, extra=1, can_delete=True
)
