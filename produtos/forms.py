from django import forms
from produtos.models import Produto, TipoProduto, Categoria


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = [
            "nome_produto",
            "descricao_produto",
            "preco_custo_produto",
            "unid_medida_produto",
            "categoria",
            "tipo",
        ]

        help_texts = {
            "nome_produto": 'Digite o nome do produto. Ex: "Bolo de cenoura"',
            "descricao_produto": "Descreva brevemente o produto",
            "preco_custo_produto": "Preço que você pagou pelo produto",
            "unid_medida_produto": "Unidade de medida do produto. Ex: Kg, Uni",
        }

        widgets = {
            "descricao_produto": forms.Textarea(
                attrs={
                    "rows": 4,  # Altura do campo
                    "cols": 40,  # Largura do campo
                }
            ),
        }

    def clean_preco_custo_produto(self):
        preco_custo = self.cleaned_data.get("preco_custo_produto")
        if preco_custo <= 0:
            raise forms.ValidationError(
                "O preço de custo não pode ser zero ou negativo."
            )
        return preco_custo

    def clean_preco_venda_produto(self):
        preco_venda = self.cleaned_data.get("preco_venda_produto")
        if preco_venda <= 0:
            raise forms.ValidationError(
                "O preço de venda não pode ser zero ou negativo."
            )
        return preco_venda

    def clean_preco_medio_produto(self):
        preco_medio = self.cleaned_data.get("preco_medio_produto")
        if preco_medio <= 0:
            raise forms.ValidationError("O preço médio não pode ser zero ou negativo.")
        return preco_medio


class TipoForm(forms.ModelForm):
    class Meta:
        model = TipoProduto
        fields = ["id_tipo", "nome_tipo", "descricao_tipo", "data_cadastro"]
        help_texts = {
            "nome_tipo": 'Digite o nome do tipo. Ex: "Insumo", "Produto final", etc.',
            "descricao_tipo": "Descreva brevemente o tipo de produto.",
        }
        widgets = {
            "descricao_tipo": forms.Textarea(
                attrs={
                    "rows": 4,  # Altura do campo
                    "cols": 40,  # Largura do campo
                    "class": "form-control",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Se existir uma instância, habilitar os campos como somente leitura 'id_tipo', data_ultima_alteracao' e data_cadastro'
        if self.instance and self.instance.pk:
            self.fields["id_tipo"] = forms.DateTimeField(
                widget=forms.TextInput(
                    attrs={
                        "readonly": "readonly",
                        "disabled": "disabled",
                        "class": "form-control",
                    }
                ),
                initial=self.instance.id_tipo,
            )

            self.fields["data_ultima_alteracao"] = forms.DateTimeField(
                widget=forms.TextInput(
                    attrs={
                        "readonly": "readonly",
                        "disabled": "disabled",
                        "class": "form-control",
                    }
                ),
                initial=self.instance.data_ultima_alteracao,
            )

            # Adicionar o campo 'data_cadastro' como somente leitura
            self.fields["data_cadastro"] = forms.DateTimeField(
                widget=forms.TextInput(
                    attrs={
                        "readonly": "readonly",
                        "disabled": "disabled",
                        "class": "form-control",
                    }
                ),
                initial=self.instance.data_cadastro,
            )
        else:
            # Remover 'id_tipo', 'data_ultima_alteracao' e 'data_cadastro' se for um novo registro
            del self.fields["data_cadastro"]

        # Adicionando o estilo de uppercase enquanto o usuário digita
        self.fields["nome_tipo"].widget.attrs.update(
            {"style": "text-transform: uppercase;", "class": "form-control"}
        )
        self.fields["descricao_tipo"].widget.attrs.update(
            {"style": "text-transform: uppercase;", "class": "form-control"}
        )


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = [
            "nome_categoria",
            "descricao_categoria",
        ]

        help_texts = {
            "nome_categoria": 'Digite o nome da categoria. Ex: "Bebida", "Sobremesa", etc.',
            "descricao_categoria": "Descreva brevemente a categoria de produto.",
        }

        widgets = {
            "descricao_categoria": forms.Textarea(
                attrs={
                    "rows": 4,  # Altura do campo
                    "cols": 40,  # Largura do campo
                }
            ),
        }
