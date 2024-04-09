from database import conn
from operations import Cliente, Conta

def menu():
    while True:
        print("\n1. Cadastrar")
        print("2. Logar")
        print("3. Sair")
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            nome = input("Digite seu nome: ")
            cpf = input("Digite seu CPF: ")
            senha = input("Digite sua senha: ")
            cliente = Cliente(None, nome, cpf, senha)
            cliente_id = cliente.registrar()
            print("Registro realizado com sucesso!\n")
            print("Criando conta...")
            conta = Conta(cliente_id)
            print("Cadastro realizado com sucesso!")
            
        elif opcao == '2':
            menu_logado()
            
        elif opcao == '3':
            print("Saindo...")
            break

def menu_logado():
    
    cpf = input("Digite seu CPF: ")
    senha = input("Digite sua senha: ")
    usuario_logado = Cliente.login(cpf, senha)

    if usuario_logado:
        conta_numero = usuario_logado.id
        conta = Conta(conta_numero)
        print("\nLogin bem-sucedido!\n")
    else:
        print("CPF ou senha incorretos.")
        menu()
            
    while True:
        print("\n1. Depositar")
        print("2. Sacar")
        print("3. Saldo")
        print("4. Extrato")
        print("5. Sair")
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            valor = float(input("Digite o valor a depositar: "))
            conta.realizar_transacao(conta_numero, valor, 'deposito')
            print("Depósito realizado com sucesso!")
            
        elif opcao == '2':
            valor = float(input("Digite o valor a sacar: "))
            conta.sacar(conta_numero, valor, 'saque')
            
        elif opcao == '3':
            saldo = conta.verificar_saldo(conta_numero)
            print(f"Seu saldo é: {saldo}")
            
        elif opcao == '4':
            conta.historico_transacoes(conta_numero)
            
        elif opcao == '5':
            print("Saindo...")
            break

menu()

# Feche a conexão
conn.close()
