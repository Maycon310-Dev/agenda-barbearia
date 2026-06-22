import os
from banco import criar_tabela
from clientes import (cadastrar_cliente, listar_clientes, buscar_cliente, excluir_cliente, atualizar_cliente)
from servicos import (cadastrar_servico,  listar_servicos, excluir_servico, atualizar_servico)
from profissionais import (cadastrar_barbeiro, listar_barbeiros, buscar_barbeiro)
from agendamentos import (agendar_horario, listar_agendamentoJoin, cancelar_agendamento, buscar_agendamento, atualizar_agendamento, atualizar_meu_agendamento)
from usuarios import (cadastrar_cliente_com_usuario,cadastrar_barbeiro_com_usuario)
from login import (login)


def limpar_tela():
    os.system("cls")

def voltar_menu():
    input("\nPressione ENTER para continuar...")
    limpar_tela()

criar_tabela()

while True:

    limpar_tela()

    print("=" * 70)
    print("          SISTEMA DE GESTÃO BARBEARIA")
    print("=" * 70)
    print("1 - Login")
    print("2 - Criar Conta Cliente")
    print("0 - Sair")
    print("=" * 70)

    acesso = input("Escolha uma opção: ")

    if acesso == "1":
        limpar_tela()
        usuario_logado = login()

        if not usuario_logado:
            voltar_menu()
            continue

    elif acesso == "2":
        limpar_tela()
        cadastrar_cliente_com_usuario()
        voltar_menu()
        continue

    elif acesso == "0":

        break

    else:
        limpar_tela()
        print("Opção inválida")
        voltar_menu()
        continue

    perfil = usuario_logado[3].upper()

    limpar_tela()  
    # ==========================
    # MENU CLIENTE
    # ==========================
    if perfil == "CLIENTE":

        while True:

            limpar_tela()

            print("=" * 50)
            print("           ÁREA DO CLIENTE")
            print("=" * 50)
            print("1 - Listar serviços")
            print("2 - Agendar horário")
            print("3 - Listar agendamentos")
            print("4 - Cancelar agendamento")
            print("5 - Atualizar agendamento")
            print("0 - Voltar")

            opcao = input("\nEscolha: ")

            if opcao == "1":
                limpar_tela()
                listar_servicos()
                voltar_menu()

            elif opcao == "2":
                limpar_tela()
                agendar_horario(usuario_logado[0])
                voltar_menu()

            elif opcao == "3":
                limpar_tela()
                listar_agendamentoJoin(usuario_logado[0],perfil)
                voltar_menu()

            elif opcao == "4":
                limpar_tela()
                cancelar_agendamento(usuario_logado[0])
                voltar_menu()

            elif opcao == "5":
                limpar_tela()
                atualizar_meu_agendamento(usuario_logado[0])
                voltar_menu()

            elif opcao == "0":
                break

            else:
                print("Opção inválida!")
                voltar_menu()

    # ==========================
    # MENU BARBEIRO
    # ==========================
    elif perfil == "BARBEIRO":

        while True:

            limpar_tela()

            print("=" * 50)
            print("         ÁREA DO BARBEIRO")
            print("=" * 50)

            print("1 - Minha Agenda")
            print("2 - Buscar Cliente")
            print("3 - Listar Agendamentos")
            print("0 - Logout")

            opcao = input("\nEscolha: ")

            if opcao == "1":
                listar_agendamentoJoin()
                voltar_menu()

            elif opcao == "2":
                buscar_cliente()
                voltar_menu()

            elif opcao == "3":
                listar_agendamentoJoin(usuario_logado[0],perfil)
                voltar_menu()

            elif opcao == "0":
                break

    # ==========================
    # MENU ADMINISTRATIVO
    # ==========================
    elif perfil == "ADMIN":

        while True:

            limpar_tela()

            print("=" * 50)
            print("         ÁREA ADMINISTRATIVA")
            print("=" * 50)

            print("\nCLIENTES")
            print("1 - Cadastrar Cliente")
            print("2 - Listar Clientes")
            print("3 - Buscar Cliente")
            print("4 - Excluir Cliente")
            print("5 - Atualizar Cliente")

            print("\nSERVIÇOS")
            print("6 - Cadastrar Serviço")
            print("7 - Listar Serviços")
            print("8 - Excluir Serviço")
            print("9 - Atualizar Serviço")

            print("\nBARBEIROS")
            print("10 - Cadastrar Barbeiro")
            print("11 - Listar Barbeiros")
            print("12 - Buscar Barbeiro")

            print("\nAGENDAMENTOS")
            print("13 - Buscar Agendamento")

            print("\n0 - Voltar")

            opcao = input("\nEscolha: ")

            if opcao == "1":
                limpar_tela()
                cadastrar_cliente()
                voltar_menu()

            elif opcao == "2":
                limpar_tela()
                listar_clientes()
                voltar_menu()

            elif opcao == "3":
                limpar_tela()
                buscar_cliente()
                voltar_menu()

            elif opcao == "4":
                limpar_tela()
                excluir_cliente()
                voltar_menu()

            elif opcao == "5":
                limpar_tela()
                atualizar_cliente()
                voltar_menu()

            elif opcao == "6":
                limpar_tela()
                cadastrar_servico()
                voltar_menu()

            elif opcao == "7":
                limpar_tela()
                listar_servicos()
                voltar_menu()

            elif opcao == "8":
                limpar_tela()
                excluir_servico()
                voltar_menu()

            elif opcao == "9":
                limpar_tela()
                atualizar_servico()
                voltar_menu()

            elif opcao == "10":
                limpar_tela()
                cadastrar_barbeiro_com_usuario()
                voltar_menu()

            elif opcao == "11":
                limpar_tela()
                listar_barbeiros()
                voltar_menu()

            elif opcao == "12":
                limpar_tela()
                buscar_barbeiro()
                voltar_menu()

            elif opcao == "13":
                limpar_tela()
                buscar_agendamento()
                voltar_menu()

            elif opcao == "0":
                break

            else:
                print("Opção inválida!")
                voltar_menu()

    else:
        print("Opção inválida!")
        voltar_menu()