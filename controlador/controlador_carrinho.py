from limite.tela_carrinho import TelaCarrinho
from entidade.carrinho import Carrinho
from entidade.cliente import *
from excecao.naohacarrinho import NaoHaCarrinhoException
from DAOs.carrinhoDAO import CarrinhoDAO

class ControladorCarrinho():

  def __init__(self, controlador_sistema):
    self.__controlador_sistema = controlador_sistema
    self.__tela_carrinho = TelaCarrinho()
    self.__carrinho_DAO = CarrinhoDAO()

  def menu(self):
        """
        print("1 - Criar novo carrinho")
        print("2 - Comprar um produto")
        print("3 - Devolver um produto")
        print("4 - Listar carrinhos")
        print("5 - Finalizar um carrinho")
        print("0 - Retornar")
        """
        switcher = {0: self.finalizar,
                    1: self.incluir_carrinho,
                    2: self.comprar,
                    3: self.devolver,
                    4: self.lista_carrinhos,
                    5: self.finalizar_carrinho}
        while True:  
            opção = self.__tela_carrinho.tela_opcoes()
            if opção == 0:
              break
            funcao_escolhida = switcher[opção]
            funcao_escolhida()

  def pega_carrinho_por_cpf(self, cpf: int):
    try:
        for carrinho in self.__carrinho_DAO.get_all():
            if carrinho.cliente.cpf == cpf:
                return carrinho
        else:
            raise NaoHaCarrinhoException  #Se não encontrar um carrinho com cpf 'cpf'
    except NaoHaCarrinhoException:
          return None

  def incluir_carrinho(self):
    while True:
      self.__controlador_sistema.controlador_cliente.listar_clientes()
      cpf = self.__tela_carrinho.pega_cpf()
      if cpf == 0:
          break
      carrinho = self.pega_carrinho_por_cpf(cpf)
      while carrinho is not None and cpf != 0: # Caso exista um carrinho e não houver ordem de retornar
        if carrinho is not None: # Caso já exista um carrinho para esse CPF
          self.__tela_carrinho.mostra_mensagem(f"{carrinho.cliente.nome} já possui um carrinho. Insira outro CPF ou '0' para retornar.")
        cpf = self.__tela_carrinho.pega_cpf()
        if cpf == 0:
            break
        carrinho = self.pega_carrinho_por_cpf(cpf)
      if cpf == 0:  # Sai do while True se receber código de saída 
        break
      cliente = self.__controlador_sistema.controlador_cliente.pega_cliente_por_cpf(cpf)  # Tenta pegar o cliente
      if cliente is not None: # Encontrou o cliente
        self.__carrinho_DAO.add(Carrinho(cliente))
        self.__tela_carrinho.mostra_mensagem("Carrinho registrado com sucesso!")
        break
      else:
        self.__tela_carrinho.mostra_mensagem(f"Não há cliente com CPF {cpf}, você inseriu o valor correto?")
      if carrinho != None:  # Talvez eu tenha removido a forma de chagar aqui, mas é melhor prevenir que remediar
        self.__tela_carrinho.mostra_mensagem(f"Já há um carrinho registrado no CPF {cpf}")

  def comprar(self): # 
    self.lista_carrinhos()
    cpf = self.__tela_carrinho.pega_cpf()
    carrinho = self.pega_carrinho_por_cpf(cpf)
    while carrinho is None and cpf != 0:  # Não encontrou um carrinho para esse cpf e não recebeu código de saída
      self.__tela_carrinho.mostra_mensagem(f"Não há carrinho para o CPF {cpf}, você inseriu o valor correto?")
      cpf = self.__tela_carrinho.pega_cpf()
      if cpf == 0:
          break
      carrinho = self.pega_carrinho_por_cpf(cpf)
    if cpf != 0:  # Se não houver código de saída
      pacote = self.__controlador_sistema.controlador_produto.comprar()
      if pacote is None: # Não há estoque do produto.
        pass
      else:
        existente = carrinho.pega_produto_por_id(pacote['produto'].id)
        if existente is None:
          carrinho.incluir_produto({'produto': pacote['produto'], 'quantidade': pacote['quantidade']})
        else:
          existente['quantidade'] += pacote['quantidade']

  def devolver(self):
    self.lista_carrinhos()
    cpf = self.__tela_carrinho.pega_cpf()
    carrinho = self.pega_carrinho_por_cpf(cpf)
    while carrinho is None and cpf != 0:  # Não encontrou um carrinho para cpf cpf e não recebeu cód de saída
      self.__tela_carrinho.mostra_mensagem(f"Não há carrinho para o CPF {cpf}, você inseriu o valor correto?")
      cpf = self.__tela_carrinho.pega_cpf()
      if cpf == 0:
          break
      carrinho = self.pega_carrinho_por_cpf(cpf)
    if cpf != 0:  # Se não houver código de saída
      if (carrinho is not None): # Verifica se o carrinho existe e exibe os produtos deste
        self.listar_produtos(carrinho) # Os produtos são listados aqui

        
        """while produto is None and id != 0:
            id = self.__tela.pega_id()
            if id == 0:
                break
            produto = self.pega_produto_por_id(id)"""
            
        while True:
          id = self.__tela_carrinho.pega_id_produto()
          if id == 0:
            break
          try:
            pacote = carrinho.pega_produto_por_id(id)
            indice_pacote = carrinho.produtos.index(pacote)
            pacote = carrinho.produtos.pop(indice_pacote)
            resultado = self.__controlador_sistema.controlador_produto.retornar_produto(pacote) # Aqui retorna para o controlador do produto
            if resultado is not None:
              raise TypeError
            else:
              self.__tela_carrinho.mostra_mensagem("Produto retornado com sucesso!")
              break
          except IndexError:
            self.__tela_carrinho.mostra_mensagem(f"Não há produto com id {id} neste carrinho. Você inseriu o valor correto?\
              Você também pode inserir '0' para voltar")
          except TypeError:
            self.__tela_carrinho.mostra_mensagem("Ocorreu um erro ao remover o pacote, o pacote foi perdido!")
      else:
        self.__tela_carrinho.mostra_mensagem("Não existe carrinho atrelado a este CPF.")

  # Prepara os dados em uma lista de dicionários no formato: [
  # {'cliente': Cliente, 'produto': [produto, produto,...]}
  # {'cliente': Cliente, 'produto': [produto, produto,...]}
  # {'cliente': Cliente, 'produto': [produto, produto,...]}
  # ...]
  def lista_carrinhos(self):
    if len(self.__carrinho_DAO.get_all()) == 0: #Verifica se há carrinhos registrados
      self.__tela_carrinho.mostra_mensagem("Não há carrinho registrado!")
    else:
      lista_de_carrinhos = []
      for carrinho in self.__carrinho_DAO.get_all():
        produtos_listados_em_dict = []
        total = 0
        if len(carrinho.produtos) != 0:
          for produto in carrinho.produtos:
            subtotal = produto['produto'].preco*produto['quantidade']
            total += subtotal
            produtos_listados_em_dict.append({'nome': produto['produto'].nome,
                             'id': produto['produto'].id,
                             'preco': produto['produto'].preco,
                             'quantidade': produto['quantidade'],
                             'subtotal': subtotal})

          lista_de_carrinhos.append({'nome': carrinho.cliente.nome,
                                    'cpf': carrinho.cliente.cpf,
                                    'produtos': produtos_listados_em_dict,
                                    'total': total})
        else:
          lista_de_carrinhos.append({'nome': carrinho.cliente.nome,
                                    'cpf': carrinho.cliente.cpf,
                                    'produtos': 0})

      self.__tela_carrinho.listar_carrinhos(lista_de_carrinhos)
    return

  def excluir_carrinho(self):
    self.lista_carrinhos(produtos=False)
    cpf = self.__tela_carrinho.pega_cpf()
    carrinho = self.pega_carrinho_por_cpf(cpf)
    while carrinho is None and cpf != 0:
      self.__tela_carrinho.mostra_mensagem(f"Não há carrinho para o CPF {cpf}, você inseriu o valor correto?")
      cpf = self.__tela_carrinho.pega_cpf()
      if cpf == 0:
          break
      carrinho = self.pega_carrinho_por_cpf(cpf)
    if cpf != 0:
      if (carrinho is not None):
        self.__carrinho_DAO.remove(carrinho.cliente.cpf)
        self.__tela_carrinho.mostra_mensagem("Carrinho removido com sucesso!")
      else:
        self.__tela_carrinho.mostra_mensagem("Não existe carrinho atrelado a este CPF.")

  def listar_produtos(self, carrinho: Carrinho):

    subtotal = 0
    total = 0
    produtos = []
    try:
      if (carrinho is None) or not isinstance(carrinho, Carrinho):
        raise IndexError
    except IndexError:
      self.__tela_carrinho.mostra_mensagem(f"Não há carrinho registrado para este número")
    else:
      if len(carrinho.produtos) == 0:
        self.__tela_carrinho.mostra_mensagem("Este carrinho está vazio, adicione alguns produtos!")
      else:
        for pacote in carrinho.produtos:
            subtotal = pacote['produto'].preco*pacote['quantidade']
            produtos.append({'nome': pacote['produto'].nome,
                             'id': pacote['produto'].id,
                             'preco': pacote['produto'].preco,
                             'quantidade': pacote['quantidade'],
                             'subtotal': subtotal})
          
            total += subtotal
        self.__tela_carrinho.mostra_carrinho({'nome': carrinho.cliente.nome,
                                              'cpf': carrinho.cliente.cpf},
                                              produtos,
                                              total)
        return total

  def finalizar_carrinho(self):
    self.lista_carrinhos()
    cpf = self.__tela_carrinho.pega_cpf()
    carrinho = self.pega_carrinho_por_cpf(cpf)
    while carrinho is None and cpf != 0:
      self.__tela_carrinho.mostra_mensagem(f"Não há carrinho para o CPF {cpf}, você inseriu o valor correto?")
      cpf = self.__tela_carrinho.pega_cpf()
      if cpf == 0:
          break
      carrinho = self.pega_carrinho_por_cpf(cpf)
    if cpf != 0:
      total = self.listar_produtos(carrinho)
      dados = {'cliente': carrinho.cliente, 'gasto': total} # Pacote que é enviado ao cliente.
      self.__carrinho_DAO.remove(carrinho.cliente.cpf)
      self.__tela_carrinho.mostra_mensagem("Carrinho finalizado com sucesso e pagamento feito!")
      self.__controlador_sistema.controlador_cliente.registrar_compra(dados) # Entrega pacote ao cliente

  def finalizar(self):
    self.__controlador_sistema.abre_tela()

  def abre_tela(self):
        lista_opcoes = {1: self.incluir_carrinho, 2: self.comprar, 3: self.devolver, 4: self.lista_carrinhos, 5: self.finalizar_carrinho, 0: self.retornar}

        continua = True
        while continua:
            lista_opcoes[self.__tela_cliente.tela_opcoes()]()
