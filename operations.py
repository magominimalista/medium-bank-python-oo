from database import cursor, conn
from datetime import datetime

class Cliente:
    def __init__(self, id, nome, cpf, senha):
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.senha = senha

    def registrar(self):
        cursor.execute("INSERT INTO clientes (nome, cpf, senha) VALUES (?, ?, ?)", (self.nome, self.cpf, self.senha))
        conn.commit()
        return cursor.lastrowid

    @staticmethod
    def login(cpf, senha):
        cursor.execute("SELECT * FROM clientes WHERE cpf = ? AND senha = ?", (cpf, senha))
        result = cursor.fetchone()
        if result:
            return Cliente(result[0], result[1], result[2], result[3])
        else:
            return None

class Conta:
    def __init__(self, cliente_id, agencia='001'):
        self.cliente_id = cliente_id
        self.agencia = agencia
        cursor.execute("INSERT INTO contas (agencia, cliente_id) VALUES (?, ?)", (self.agencia, self.cliente_id))
        conn.commit()

    def realizar_transacao(self, conta_numero, valor, tipo):
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO transacoes (conta_numero, valor, tipo, data_hora) VALUES (?, ?, ?, ?)", (conta_numero, valor, tipo, data_hora))
        conn.commit()

    def sacar(self, conta_numero, valor, tipo): 
        saldo = self.verificar_saldo(conta_numero)
        if saldo >= valor:
            cursor.execute("BEGIN TRANSACTION")
            self.realizar_transacao(conta_numero, valor, tipo)
            conn.commit()
            print("Saque realizado com sucesso!")
            return True
        else:
            print("Erro ao realizar o saque! Fundos insuficientes.")
            return False

    def verificar_saldo(self, conta_numero):
        cursor.execute("SELECT tipo, valor FROM transacoes WHERE conta_numero = ?", (conta_numero,))
        transacoes = cursor.fetchall()
        saldo = 0
        for transacao in transacoes:
            if transacao[0] == 'deposito':
                saldo += transacao[1]
            elif transacao[0] == 'saque':
                saldo -= transacao[1]
        return saldo
        
    def historico_transacoes(self, conta_numero):
        cursor.execute("SELECT * FROM transacoes WHERE conta_numero = ?", (conta_numero,))
        transacoes = cursor.fetchall()
        saldo = self.verificar_saldo(conta_numero)
        
        print(f"Histórico de transações para a conta {conta_numero}:\n")
        print(f"{'ID':<10}{'Valor':<10}{'Tipo':<10}{'Data e Hora':<20}{'Número da Conta':<15}")
        for transacao in transacoes:
            print(f"{transacao[0]:<10}{transacao[1]:<10}{transacao[2]:<10}{transacao[4]:<20}{transacao[3]:<15}")
        print(f"\nSaldo final: {saldo}")
