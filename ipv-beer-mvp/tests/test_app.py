import pytest
import app as sistema


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(
        sistema, "DB_PATH", tmp_path / "teste.db"
    )
    sistema.init_db()
    sistema.app.config["TESTING"] = True

    with sistema.app.test_client() as client:
        yield client


def test_pagina_inicial(client):
    resposta = client.get("/")
    assert resposta.status_code == 200


def test_cadastro_cliente(client):
    resposta = client.post("/clientes", data={
        "name": "Cliente Teste",
        "phone": "83999999999",
        "address": "Rua Central"
    })
    assert resposta.status_code == 302


def test_cliente_sem_nome(client):
    resposta = client.post("/clientes", data={
        "name": "",
        "phone": "",
        "address": ""
    })
    assert resposta.status_code == 302


def test_pedidos_sem_cliente(client):
    resposta = client.get("/pedidos")
    assert resposta.status_code == 200