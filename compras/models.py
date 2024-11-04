from database.db import Table

compras_columns = {
    "nota_fiscal": "INTEGER NOT NULL",
    "modelo_nota": "INTEGER NOT NULL DEFAULT 55",
    "serie": "INTEGER NOT NULL DEFAULT 1",
    "fornecedor_id": "INTEGER NOT NULL",
    "valor_total": "INTEGER NOT NULL",
    "data_chegada": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
    "data_emissao": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
    "data_cadastro": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
    "data_ultima_alteracao": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
}

Compras = Table(
    "compras", compras_columns, primary_keys=["nota_fiscal", "modelo_nota", "serie"]
)

compras_item_columns = {
    "quantidade": "INTEGER NOT NULL",
    "custo": "INTEGER NOT NULL",
    "desconto": "INTEGER NOT NULL",
    "produto_id": "INTEGER NOT NULL",
    "compra_id": "INTEGER NOT NULL",
    "data_cadastro": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
    "data_ultima_alteracao": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
}

ComprasItem = Table("compras_item", compras_item_columns)
