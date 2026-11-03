# IPV Beer — MVP de gerenciamento

Sistema web simples para apoiar a rotina da IPV Beer, distribuidora de água mineral.

## Funcionalidades do MVP
- Painel inicial com resumo de clientes, pedidos, pedidos pendentes e vendas de pedidos entregues.
- Cadastro de clientes com nome, telefone e endereço.
- Registro de pedidos com produto, quantidade e preço unitário.
- Acompanhamento do status: Pendente, Em entrega, Entregue ou Cancelado.

## Tecnologias
- Python
- Flask
- SQLite
- HTML e CSS

## Como executar
1. Instale o Python 3.10 ou superior.
2. Abra o terminal na pasta do projeto.
3. (Opcional, recomendado) Crie um ambiente virtual:
   - Windows: `python -m venv .venv` e `.venv\\Scripts\\activate`
   - Linux/macOS: `python3 -m venv .venv` e `source .venv/bin/activate`
4. Instale as dependências: `pip install -r requirements.txt`
5. Inicie o sistema: `python app.py`
6. Acesse no navegador: `http://127.0.0.1:5000`

O banco `ipvbeer.db` é criado automaticamente na primeira execução.

## Observações
Este projeto é um MVP acadêmico para demonstração. Utilize dados fictícios durante testes. Antes de uso comercial, implemente autenticação, cópias de segurança, validações adicionais e proteção adequada dos dados.
## Funcionalidades do sistema

O sistema IPV Beer foi desenvolvido para auxiliar no gerenciamento de uma distribuidora de água mineral.

Principais funcionalidades:
- Cadastro e gerenciamento de clientes.
- Registro e acompanhamento de pedidos.
- Controle do status dos pedidos.
- Visualização de informações no painel principal.

## Objetivo

Facilitar a organização das vendas, melhorar o atendimento aos clientes e tornar o controle dos pedidos mais eficiente.

## Revisão técnica

O projeto IPV Beer utiliza Python com Flask para organizar as funcionalidades do sistema, SQLite para armazenar os dados e HTML e CSS para a interface. A estrutura busca manter o código organizado, facilitar a manutenção e permitir futuras melhorias.

A revisão técnica considera a validação dos dados dos clientes e pedidos, a organização das rotas e a segurança no armazenamento das informações.
