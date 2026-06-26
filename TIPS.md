# Dicas, sugestões e boas práticas

## Fluxo do Alembic

Passo 1 - Sempre que alterar um model
1. Gerar migration

```alembic revision --autogenerate -m "add nickname to customers"```

2. Revisar migration

Sempre abrir o arquivo, nunca confiar no Alembic
```alembic/versions/xxxxx.py```

e revisar
* colunas corretas?
* índices corretos?
* foreign keys corretas?
* não tentou deletar algo indevido?

3. Aplicar migration 

```alembic upgrade head```

Passo 2 - Criar teste real de migration 

Sugestão: Customer
Adicione uma coluna temporária:
```nickname = Column(String, nullable=True)```

Depois rodar:
```alembic revision --autogenerate -m "add nickname to customers"```


Se o alembic detectar, então o pipeline esta 100%:

Detected added column 'customers.nickname'

Por fim, aplicamos:

```alembic upgrade head```