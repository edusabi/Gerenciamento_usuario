from rich.console import Console
from rich.text import Text

import database

console = Console()

def menu():
    while True:
        print(" ")
        console.print("=== MENU ===", style="bold blue")
        print("""1 - LISTAR USUÁRIOS 
2 - CADASTRAR USUÁRIO 
3 - DELETAR USUÁRIO 
4 - BUSCAR USUÁRIO POR NOME
5 - BUSCAR USUÁRIO POR DATA_NASC
6 - ATUALIZAR USUÁRIO 
7 - EXPORTAR USUÁRIO EM .txt
8 - SAIR
        """)
        
        console.print("Escolha uma opção:", style="bold magenta")
        entrada = input("> ")

        if not entrada.isdigit():
            print("")
            print("Digite apenas números!")
            continue

        opcao = int(entrada)

        if opcao == 1:
            database.listar_usuarios()

        elif opcao == 2:
            nome = input("Digite seu nome: ")
            email = input("Digite seu email: ")
            data_nascimento = input("Digite sua data de nascimento (dd/mm/yyyy): ")
            print(" ")
            database.cadastrar_user(nome,email,data_nascimento)

        elif opcao == 3:
            database.deletar_user()
        elif opcao == 4:
            database.buscar_user()
        elif opcao == 5:
            database.filtrar_por_ano()
        elif opcao == 6:
            database.atualizar_user()
        elif opcao == 7:
            database.exportar_usuarios()
        elif opcao == 8:
            print("Você saiu!")
            database.fechar_conexao()
            break

        else:
            print("Você digitou um caractere errado!")


menu()