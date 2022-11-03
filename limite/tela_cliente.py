from limite.telaAbstrata import TelaAbstrata


class TelaCliente(TelaAbstrata):
      def __init__(self):
            super().__init__()

      def tela_opcoes(self):
            print("Gerenciar clientes")
            print("Selecione a opção desejada:")
            print("1 - Cadastrar um cliente")
            print("2 - Alterar um cliente")
            print("3 - Excluir um cliente")
            print("4 - Listar clientes")
            print("5 - Listar clientes por gasto")
            print("0 - Retornar")

            opcao = self.verifica_opção([0, 1, 2, 3, 4, 5])
            print("\n"*3)
            return opcao

      def pega_cpf(self):
            cpf = input("Insira o CPF do cliente ou insira '0' para voltar: ")
            while self.verificarInt(cpf) == False:
                  cpf = input("A opção escolhida deve ser um número inteiro, por favor, tente novamente: ")
            return int(cpf)


      def entrar_dados_cliente(self):
            print("-------- Insira os dados do cliente ----------")
            # Setar nome
            nome = input("Nome: ")
            while self.verificarString(nome) == False:
                  nome = input("Nome: ")
            # Setar cpf
            cpf = input("CPF: ")
            while self.verificarInt(cpf) == False:
                  cpf = input("CPF: ")
            cpf = int(cpf)
            return {"nome": nome, "cpf": cpf}

      def mostra_cliente(self, dados_cliente: dict):
            print(f"Cliente: {dados_cliente['num']}")
            print(f"  Nome: {dados_cliente['nome']}")
            print(f"  CPF: {dados_cliente['cpf']}")
            print(f"  Gasto: {dados_cliente['gasto']}")
            print("\n"*1)

      def mostra_melhores(self, dados_melhores: list):
            for i in range(len(dados_melhores)):
                  print(f"{dados_melhores[i][0]:30}{dados_melhores[i][1]:^10,.2f}")
            
