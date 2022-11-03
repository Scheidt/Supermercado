from entidade.produto import Produto
from limite.tela_produto import TelaProduto

class ControladorProduto():

    def __init__(self, controlador_sistema) -> None:
        self.__controlador_sistema = controlador_sistema
        self.__produtos = [] # nome: str, id: int, preco: float, unidade: str
        if False:
            self.__produtos =[{'produto': Produto("Shampoo", 1, 9.95, "Unidade(s)"), 'estoque': 100}, 
                            {'produto': Produto("Batata", 2, 5.99, "Kg"), 'estoque': 300.01},
                            {'produto': Produto("Tomate", 3, 7.60, "Kg"), 'estoque': 200.00},
                            {'produto': Produto("Azeite 500ml", 4, 21.90, "Unidade(s)"), 'estoque': 100},
                            {'produto': Produto("Energético 355ml", 5, 9.99, "Unidade(s)"), 'estoque': 400},
                            {'produto': Produto("Revista Mônica©", 6, 15.00, "Unidade(s)"), 'estoque': 999}]
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
                    5: self.ordenar_id,
                    6: self.estocar}
        while True:  
            opção = self.__tela.tela_opcoes()
            if opção == 0:
                break
            funcao_escolhida = switcher[opção]
            funcao_escolhida()


    def pega_produto_por_id(self, id: int, verif = False):
        try:
            for pacote in self.__produtos:
                if (pacote['produto'].id == id):
                    return pacote
            else:
                raise KeyError
        except KeyError:
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
        for produto in self.__produtos:
            if produto['produto'].nome == dados['nome']: # Se já existe produto com esse nome, o estoque inserido é adicionado no produto
                produto['estoque'] += dados['estoque']
                break
        else:
            id = len(self.__produtos)+1
            try:
                if id > self.__produtos[-1]['produto'].id:
                    pass
                elif id <= self.__produtos[-1]['produto'].id:
                    id = self.__produtos[-1]['produto'].id + 1
            except IndexError:
                pass
            self.__produtos.append({'produto': Produto(dados["nome"], id, dados["preco"], dados["unidade"]),
                                    'estoque': dados["estoque"]})
    
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
            i = self.__produtos.index(produto) 
            dados = self.__tela.entrar_dados_produto()
            if dados["unidade"] in ("Unidade", "Unitário", "Unidades", "unidade", "unitário", "unidades"):
                dados["unidade"] = "Unidade(s)"
                dados["estoque"] = round(dados["estoque"])
            self.__produtos[i] = ({'produto': Produto(dados["nome"], produto['produto'].id, dados["preco"], dados["unidade"]),
                                    'estoque': dados["estoque"]})

    def listar_produtos(self, esgotados= True):
        self.__tela.mostra_mensagem("------------------- Informações dos Produtos Registrados -------------------")
        self.__tela.mostra_mensagem(f"{'Nome: ':20}{'Id: ':^5}   {'Preço: ':^7}{'Unidade: ':^18}{'Quantidade: ':^9} ")
        for pacote in self.__produtos:
            if esgotados == False and pacote['estoque'] == 0:
                pass
            else:
                self.__tela.listar({"nome": pacote['produto'].nome, 
                                    "id": pacote['produto'].id,      
                                    "preco": pacote['produto'].preco,
                                    "estoque": pacote['estoque'],
                                    "unidade": pacote['produto'].unidade
                                    })

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
            self.__produtos.remove(produto)
            del produto
            self.__tela.mostra_mensagem("Produto deletado com sucesso!")

    def ordenar_id(self):
        for i in range(len(self.__produtos)):
            self.__produtos[i]['produto'].id = i+1

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
                else:
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
            indice = self.__produtos.index(self.pega_produto_por_id(id, verif=True))
        except ValueError: # Entra aqui quando não há um produto com id igual
            for produto in self.__produtos:
                if produto['produto'].nome == pacote['produto'].nome: # Não há produto com id igual mas há com o mesmo nome.
                    produto['estoque'] += pacote['quantidade']
                    break
            else: # Não há nem mesmo id nem mesmo nome
                ids_possiveis.append(len(self.__produtos)+1)
                try:
                    ids_possiveis.append(self.__produtos[-1]['produto'].id +1)
                except IndexError:
                    pass
                ids_possiveis.sort(reverse=True)
                pacote['produto'].id = ids_possiveis[0]
                self.__produtos.append({'produto': pacote['produto'],
                                        'estoque': pacote['quantidade']})
                return None
        else:  # Se há produto com a mesma ID
            if self.__produtos[indice]['produto'].unidade == "Unidade(s)":
                self.__produtos[indice]['estoque'] += round(pacote['quantidade'])
                return None
            else:
                self.__produtos[indice]['estoque'] += pacote['quantidade']
                return None

    def finalizar(self):
        self.__controlador_sistema.abre_tela()
