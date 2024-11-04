from django.urls import path
from .views import (
    pagamento_list,
    condicao_pagamento_list,
    pagamento_manage,
    condicao_pagamento_manage,
)

app_name = "pagamento"

urlpatterns = [
    path("", pagamento_list, name="list"),
    path("<int:pagamento_id>/", pagamento_manage, name="manage"),
    path("condicao/", condicao_pagamento_list, name="condicao-list"),
    path(
        "condicao/<int:condicao_pagamento_id>/",
        condicao_pagamento_manage,
        name="condicao-manage",
    ),
]
