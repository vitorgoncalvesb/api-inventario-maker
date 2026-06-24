from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI(title="API Inova Lab - Inventario Maker")


class ComponenteSchema(BaseModel):
    nome: str = Field(..., min_length=2, description="Nome do componente maker")
    quantidade: int = Field(
        ...,
        ge=0,
        description="Quantidade em estoque (deve ser maior ou igual a zero)",
    )
    categoria: str = Field(
        ...,
        description="Categoria do item (ex: Atuadores, Microcontroladores)",
    )
    estado_conservacao: str = Field(
        ...,
        description="Estado de conservacao do componente (ex: Bom, Usado, Danificado)",
    )


estoque_laboratorio = [
    {
        "id": 1,
        "nome": "Arduino Sensor Shield",
        "quantidade": 15,
        "categoria": "Placas de Expansao",
        "estado_conservacao": "Bom",
    },
    {
        "id": 2,
        "nome": "Micro Servo Motor SG90",
        "quantidade": 42,
        "categoria": "Atuadores",
        "estado_conservacao": "Bom",
    },
    {
        "id": 3,
        "nome": "Esteira em Acrilico",
        "quantidade": 2,
        "categoria": "Mecanica",
        "estado_conservacao": "Usado",
    },
]


@app.get("/")
def raiz():
    return {
        "mensagem": "API do Laboratorio Maker operante. Acesse /docs para ver a documentacao."
    }


@app.get("/componentes")
def listar_componentes():
    return estoque_laboratorio


@app.post("/componentes", status_code=201)
def adicionar_componente(novo_componente: ComponenteSchema):
    if estoque_laboratorio:
        maior_id = max(item["id"] for item in estoque_laboratorio)
        novo_id = maior_id + 1
    else:
        novo_id = 1

    componente_dict = novo_componente.model_dump()
    componente_dict["id"] = novo_id

    estoque_laboratorio.append(componente_dict)
    return {
        "mensagem": "Componente adicionado com sucesso!",
        "componente": componente_dict,
    }


@app.put("/componentes/{componente_id}")
def atualizar_componente(componente_id: int, dados_atualizados: ComponenteSchema):
    for item in estoque_laboratorio:
        if item["id"] == componente_id:
            item.update(dados_atualizados.model_dump())
            return {
                "mensagem": "Componente atualizado com sucesso!",
                "componente": item,
            }

    raise HTTPException(
        status_code=404,
        detail="Componente nao encontrado no laboratorio.",
    )


@app.delete("/componentes/{componente_id}")
def remover_componente(componente_id: int):
    for index, item in enumerate(estoque_laboratorio):
        if item["id"] == componente_id:
            estoque_laboratorio.pop(index)
            return {
                "mensagem": f"Componente com ID {componente_id} foi removido do estoque."
            }

    raise HTTPException(
        status_code=404,
        detail="Componente nao encontrado no laboratorio.",
    )
