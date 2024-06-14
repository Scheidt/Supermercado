import PySimpleGUI as sg
from entidade.produto import Produto
from limite.tela_produto import TelaProduto
from excecao.produtonaoencontrado import ProdutoNaoEncontradoException
from DAOs.produtoDAO import ProdutoDAO

class ControladorProduto():

    def __init__(self, controlador_sistema) -> None:
        self.__controlador_sistema = controlador_sistema
        self.__produtos_DAO = ProdutoDAO()
        self.__tela = TelaProduto()

    def menu(self):
        """
        print("1 - Incluir Produto")
        print("2 - Alterar Produto")
        print("3 - Listar Produtos")
        print("4 - Excluir Produto")
        print("0 - Retornar")
        """
        switcher = {0: self.finalizar,
                    1: self.incluir_produto,
                    2: self.alterar_produto,
                    3: self.listar_produtos,
                    4: self.excluir_produto,
                    5: self.estocar}
        while True:  
            opção = self.__tela.tela_opcoes()
            if opção == 0:
                break
            funcao_escolhida = switcher[opção]
            funcao_escolhida()


    def pega_produto_por_id(self, id: int, verif = False):
        try:
            if self.__produtos_DAO.get(id) is not None:
                return self.__produtos_DAO.get(id)
            else:
                raise ProdutoNaoEncontradoException
        except ProdutoNaoEncontradoException:
            if id == 0:
                return None
            if verif == False:
                self.__tela.mostra_mensagem(f"Não há produto com id {id}. Você inseriu o valor correto? "\
                                            f"Você também pode digitar '0' para voltar ao menu.")

    def incluir_produto(self):
        dados = self.__tela.entrar_dados_produto()
        if dados['unidade'] in ("Unidade", "Unitário", "Unidades", "unidade", "unitário", "unidades"):  # Padroniza o unitário e arredonda estoque se for
            dados['unidade'] = "Unidade(s)"
            dados['estoque'] = round(dados["estoque"])
        for produto in self.__produtos_DAO.get_all():
            if produto['produto'].nome == dados['nome']: # Se já existe produto com esse nome, o estoque inserido é adicionado no produto
                produto['estoque'] += dados['estoque']
                break
        else:
            id = len(self.__produtos_DAO.get_all())+1 # Essas próximas linhas servem para pegar o maior número para ser ID do produto
            try:
                if id > list(self.__produtos_DAO.get_all())[-1]['produto'].id:
                    pass
                elif id <= list(self.__produtos_DAO.get_all())[-1]['produto'].id:
                    id = list(self.__produtos_DAO.get_all())[-1]['produto'].id + 1
            except IndexError:
                pass
            self.__produtos_DAO.add({'produto': Produto(dados["nome"], id, dados["preco"], dados["unidade"]),
                                    'estoque': dados["estoque"]})
            self.__tela.mostra_mensagem("Produto registrado com sucesso!")
    
    def alterar_produto(self):
        self.listar_produtos()
        id = self.__tela.pega_id()
        produto = self.pega_produto_por_id(id)
        while produto is None and id != 0:
            id = self.__tela.pega_id()
            if id == 0:
                break
            produto = self.pega_produto_por_id(id)
        if id != 0:
            dados = self.__tela.entrar_dados_produto()
            if dados is None:
                return
            if dados["unidade"] in ("Unidade", "Unitário", "Unidades", "unidade", "unitário", "unidades"):
                dados["unidade"] = "Unidade(s)"
                dados["estoque"] = round(dados["estoque"])
            id = produto['produto'].id
            self.__produtos_DAO.remove(id)
            print (dados)
            print (produto)
            self.__produtos_DAO.add = ({'produto': Produto(dados["nome"], id, dados["preco"], dados["unidade"]),
                                    'estoque': dados["estoque"]})
            self.__tela.mostra_mensagem("Produto alterado com sucesso!")

    def listar_produtos(self, esgotados= True):
        lista_de_produtos = []
        if len(self.__produtos_DAO.get_all()) != 0:
            for pacote in self.__produtos_DAO.get_all():
                if esgotados == False and pacote['estoque'] == 0:
                    pass
                else:
                    lista_de_produtos.append({"nome": pacote['produto'].nome, 
                                              "id": pacote['produto'].id,      
                                              "preco": pacote['produto'].preco,
                                              "estoque": pacote['estoque'],
                                              "unidade": pacote['produto'].unidade
                                            })
            self.__tela.listar_produtos(lista_de_produtos)
        else:
            self.__tela.listar_produtos(None)

    def excluir_produto(self):
        self.listar_produtos()
        id = self.__tela.pega_id()
        produto = self.pega_produto_por_id(id)
        while produto is None and id != 0:
            id = self.__tela.pega_id()
            if id == 0:
                break
            produto = self.pega_produto_por_id(id)
        if produto == None:
            self.__tela.mostra_mensagem(f"O produto com o id {id} não existe")
        else:
            self.__produtos_DAO.remove(produto['produto'].id)
            del produto
            self.__tela.mostra_mensagem("Produto deletado com sucesso!")

    """def ordenar_id(self):
        for i in range(len(self.__produtos)):
            self.__produtos[i]['produto'].id = i+1"""

    def estocar(self):
        self.listar_produtos()
        id = self.__tela.pega_id()
        produto = self.pega_produto_por_id(id)
        while produto is None and id != 0:
            id = self.__tela.pega_id()
            if id == 0:
                break
            produto = self.pega_produto_por_id(id)
        if id != 0:
            quantidade = self.__tela.interacao_estoque("estocar", produto['produto'].nome)
            if produto['produto'].unidade == "Unidade(s)":
                self.pega_produto_por_id(id)['estoque'] += round(quantidade)
            else:
                self.pega_produto_por_id(id)['estoque'] += quantidade

    def comprar(self): # Retorna uma lista na forma (Produto, quantia) ou ValueError caso não houver estoque suficiente
        self.listar_produtos(esgotados=False)
        id = self.__tela.pega_id()
        produto = self.pega_produto_por_id(id)
        while produto is None and id != 0:
            id = self.__tela.pega_id()
            if id == 0:
                break
            produto = self.pega_produto_por_id(id)
        if id != 0:
            if produto['estoque'] == 0:
                self.__tela.mostra_mensagem("Este produto está esgotado, por favor, tente novamente mais tarde!")
            else:
                quantidade = self.__tela.interacao_estoque("comprar", produto['produto'].nome)
                if produto['produto'].unidade == "Unidade(s)": # Produto Unitário
                    if produto['estoque'] < round(quantidade): # Produto unitário sem estoque suficiente
                        quantidade = produto['estoque']
                        produto['estoque'] = 0
                        self.__tela.mostra_mensagem("Não há estoque suficiente, todo o estoque possível foi adicionado ao carrinho.")
                        return {'produto': produto['produto'],
                                'quantidade': round(quantidade)}
                    else: # 
                        self.pega_produto_por_id(id)['estoque'] -= round(quantidade)
                        return {'produto': produto['produto'],
                                'quantidade': round(quantidade)}
                else: # Produto não unitário
                    if produto['estoque'] < quantidade:
                        quantidade = produto['estoque']
                        produto['quantidade'] = 0
                        self.__tela.mostra_mensagem("Não há estoque suficiente, todo o estoque possível foi adicionado ao carrinho.")
                        return {'produto': produto['produto'],
                                'quantidade': round(quantidade)}
                    else:
                        produto['estoque'] -= quantidade
                        return {'produto': produto['produto'], 
                                'quantidade': quantidade}

    def retornar_produto(self, pacote: dict): # Recebe um pacote no formato (Produto, quantidade)
        id = pacote['produto'].id
        ids_possiveis = [id]
        try:
            produto = self.__produtos_DAO.get(id)
            if produto is None:
                raise ValueError
        except: # Entra aqui quando não há um produto com id igual
            for produto in self.__produtos_DAO.get_all():
                if produto['produto'].nome == pacote['produto'].nome: # Não há produto com id igual mas há com o mesmo nome.
                    produto['estoque'] += pacote['quantidade']
                    break
            else: # Não há nem mesmo id nem mesmo nome
                ids_possiveis.append(len(self.__produtos_DAO.get_all())+1)
                try:
                    ids_possiveis.append(self.__produtos_DAO.get_all()[-1]['produto'].id +1)
                except IndexError:
                    pass
                ids_possiveis.sort(reverse=True)
                pacote['produto'].id = ids_possiveis[0]
                self.__produtos_DAO.add(ids_possiveis[0], {'produto': pacote['produto'],
                                        'estoque': pacote['quantidade']})
                return None
        else:  # Se há produto com a mesma ID
            if produto['produto'].unidade == "Unidade(s)":
                produto['estoque'] += round(pacote['quantidade'])
                return None
            else:
                produto['estoque'] += pacote['quantidade']
                return None

    def finalizar(self):
        self.__controlador_sistema.abre_tela()

    def abre_tela(self):
        lista_opcoes = {1: self.incluir_produto, 2: self.alterar_produto, 3: self.listar_produtos, 4: self.excluir_produto, 5: self.ordenar_id, 6: self.estocar, 0: self.retornar}

        continua = True
        while continua:
            lista_opcoes[self.__tela_cliente.tela_opcoes()]()
