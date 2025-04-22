Sistema de Gerenciamento de Usuários
Um sistema simples em Python para gerenciar usuários, usando SQLite e rich para uma interface de terminal estilizada. Permite cadastrar, listar, buscar, atualizar, deletar, exportar usuários e filtrar por ano de nascimento, com busca insensível a acentos e maiúsculas/minúsculas.
Funcionalidades

Cadastrar, listar, buscar, atualizar e deletar usuários.
Exportar usuários para um arquivo de texto.
Filtrar usuários por ano de nascimento.
Busca por nome ignora acentos (ex.: João = Joao).
Tabelas e mensagens coloridas com rich.

Pré-requisitos

Python 3.6+
Biblioteca rich

Instalação

Instale a dependência:
pip install rich


Baixe o script gerenciador_usuarios.py.


Uso

Execute o script:
python gerenciador_usuarios.py


Use o menu interativo:
=== Sistema de Gerenciamento de Usuários ===
1. Cadastrar usuário
2. Listar usuários
3. Buscar usuário
4. Atualizar usuário
5. Deletar usuário
6. Exportar usuários para TXT
7. Filtrar por ano de nascimento
0. Sair


Exemplo:

Cadastrar:
Nome: João Silva
Email: joao.silva@email.com
Data de nascimento (DD/MM/AAAA): 15/03/1990
Usuário 'João Silva' cadastrado com sucesso!


Buscar:
Digite o nome do usuário que deseja buscar: Joao
Usuário Encontrado
┌─────┬────────────────────┬──────────────────────────────┬───────────────┐
│ ID  │ Nome               │ Email                        │ Nascimento    │
├─────┼────────────────────┼──────────────────────────────┼───────────────┤
│ 1   │ João Silva         │ joao.silva@email.com         │ 15/03/1990    │
└─────┴────────────────────┴──────────────────────────────┴───────────────┘




Notas

Busca sem acentos: Usa unicodedata para normalizar nomes, permitindo buscas sem acentos.
Banco: Dados salvos em usuarios.db.
Exportação: Resultados em usuarios_exportados.txt.


