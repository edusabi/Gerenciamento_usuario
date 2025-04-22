import sqlite3
import csv
from rich.console import Console
from rich.table import Table
import unicodedata

# Conectar ao banco
conn = sqlite3.connect("usuarios.db")
cursor = conn.cursor()

# Criar tabela se não existir
cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS usuarios(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               nome TEXT NOT NULL,
               email TEXT NOT NULL,
               data_nascimento TEXT NOT NULL 
    )
''')
conn.commit()

def cadastrar_user(nome, email, data_nascimento):
    cursor.execute("INSERT INTO usuarios (nome, email, data_nascimento) VALUES (?, ?, ?)", (nome, email, data_nascimento))
    conn.commit()
    console = Console()
    console.print(f"[bold green]Usuário '{nome}' cadastrado com sucesso![/bold green]")

def listar_usuarios():
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()

    console = Console()

    if len(usuarios) == 0:
        console.print("[bold red]Nenhum usuário cadastrado.[/bold red]")
        return

    # Criar tabela com rich
    table = Table(title="[bold cyan]Lista de Usuários[/bold cyan]", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=5)
    table.add_column("Nome", style="green", width=20)
    table.add_column("Email", style="blue", width=30)
    table.add_column("Nascimento", style="yellow", width=15)

    # Adicionar usuários à tabela
    for usuario in usuarios:
        table.add_row(str(usuario[0]), usuario[1], usuario[2], usuario[3])

    console.print(table)

def deletar_user():
    console = Console()
    console.print("\nDigite o E-mail do usuário que deseja deletar: ", end="")
    email = input()
    cursor.execute("DELETE FROM usuarios WHERE email = ?", (email,))
    conn.commit()

    if cursor.rowcount > 0:
        console.print(f"[bold green]Usuário com e-mail '{email}' deletado com sucesso.[/bold green]")
    else:
        console.print("[bold red]Usuário não encontrado.[/bold red]")

def atualizar_user():
    console = Console()
    console.print("\nDigite o E-mail do usuário que deseja atualizar: ", end="")
    email = input()

    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    usuario = cursor.fetchone()

    if usuario:
        # Exibir usuário em uma tabela
        table = Table(title="[bold cyan]Usuário Encontrado[/bold cyan]", show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim", width=5)
        table.add_column("Nome", style="green", width=20)
        table.add_column("Email", style="blue", width=30)
        table.add_column("Nascimento", style="yellow", width=15)
        table.add_row(str(usuario[0]), usuario[1], usuario[2], usuario[3])
        console.print(table)

        console.print("\nNovo nome (pressione Enter para manter o mesmo): ", end="")
        novo_nome = input()
        console.print("Novo email (pressione Enter para manter o mesmo): ", end="")
        novo_email = input()
        console.print("Nova data de nascimento (pressione Enter para manter a mesma): ", end="")
        nova_data = input()

        novo_nome = novo_nome if novo_nome.strip() else usuario[1]
        novo_email = novo_email if novo_email.strip() else usuario[2]
        nova_data = nova_data if nova_data.strip() else usuario[3]

        cursor.execute("""
            UPDATE usuarios
            SET nome = ?, email = ?, data_nascimento = ?
            WHERE email = ?
        """, (novo_nome, novo_email, nova_data, email))

        conn.commit()
        console.print("[bold green]Usuário atualizado com sucesso![/bold green]\n")
    else:
        console.print("[bold red]Usuário não encontrado.[/bold red]")

def buscar_user():
    console = Console()
    console.print("\nDigite o nome do usuário que deseja buscar: ", end="")
    nome = input()

    # Normalizar o nome pesquisado, removendo acentos e convertendo para minúsculas
    nome_normalizado = ''.join(
        c for c in unicodedata.normalize('NFD', nome.lower())
        if unicodedata.category(c) != 'Mn'
    )

    # Buscar todos os usuários para normalizar os nomes no lado do Python
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()

    usuario_encontrado = None
    for usuario in usuarios:
        # Normalizar o nome do banco, removendo acentos e convertendo para minúsculas
        nome_banco_normalizado = ''.join(
            c for c in unicodedata.normalize('NFD', usuario[1].lower())
            if unicodedata.category(c) != 'Mn'
        )
        if nome_normalizado == nome_banco_normalizado:
            usuario_encontrado = usuario
            break

    if usuario_encontrado:
        # Exibir usuário em uma tabela
        table = Table(title="[bold cyan]Usuário Encontrado[/bold cyan]", show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim", width=5)
        table.add_column("Nome", style="green", width=20)
        table.add_column("Email", style="blue", width=30)
        table.add_column("Nascimento", style="yellow", width=15)
        table.add_row(str(usuario_encontrado[0]), usuario_encontrado[1], usuario_encontrado[2], usuario_encontrado[3])
        console.print(table)
    else:
        console.print("[bold red]Usuário não encontrado.[/bold red]")

def exportar_usuarios():
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()

    console = Console()

    if not usuarios:
        console.print("[bold red]Nenhum usuário para exportar.[/bold red]")
        return

    with open("usuarios_exportados.txt", "w", encoding="utf-8") as arquivo:
        for usuario in usuarios:
            linha = ", ".join(str(campo) for campo in usuario)
            arquivo.write(linha + "\n")

    console.print("[bold green]Usuários exportados com sucesso para 'usuarios_exportados.txt'.[/bold green]")

def filtrar_por_ano():
    console = Console()
    console.print("Digite o ano de nascimento para filtrar (ex.: 1990): ", end="")
    ano = input()
    cursor.execute("SELECT * FROM usuarios WHERE data_nascimento LIKE ?", (f"%{ano}",))
    usuarios = cursor.fetchall()

    if not usuarios:
        console.print(f"[bold red]Nenhum usuário encontrado para o ano {ano}.[/bold red]")
        return

    # Criar tabela com rich
    table = Table(title=f"[bold cyan]Usuários Nascidos em {ano}[/bold cyan]", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=5)
    table.add_column("Nome", style="green", width=20)
    table.add_column("Email", style="blue", width=30)
    table.add_column("Nascimento", style="yellow", width=15)

    for usuario in usuarios:
        table.add_row(str(usuario[0]), usuario[1], usuario[2], usuario[3])

    console.print(table)

def fechar_conexao():
    conn.close()

def fechar_conexao():
    conn.close()


