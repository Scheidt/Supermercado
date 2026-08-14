# Mercado P&P

Este repositório é um arquivo. O projeto é um sistema de supermercado com
interface gráfica: cadastro de produtos e clientes, carrinhos de compra, controle
de estoque e ranking de clientes por gasto. Foi um trabalho da disciplina de
Programação Orientada a Objetos na UFSC, entregue em novembro de 2022.

A branch `original` guarda o código exatamente como estava em 2022, com os
defeitos e os arquivos que não deveriam estar versionados. A `main` é o mesmo
projeto consertado hoje, em Python e dentro das mesmas restrições. O diff está em
[original...main](https://github.com/Scheidt/Supermercado/compare/original...main).

O post que conta essa história: (link a preencher quando publicar)

## Como rodar

```bash
python -m venv .venv
.venv\Scripts\activate        # Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

Requer Python 3.10 ou mais novo, com `tkinter` disponível (já vem no instalador
oficial do Windows e do macOS; no Debian/Ubuntu, `apt install python3-tk`).

A dependência é o **FreeSimpleGUI**, fork LGPL do PySimpleGUI 4.60.5. O projeto
original importava `PySimpleGUI`, que não instala mais: a linha 4.x foi retirada
do PyPI e a 5.x passou a exigir chave de licença. A API é a mesma.

## Testes

```bash
pip install pytest
python -m pytest
```

Os testes cobrem as entidades, os repositórios e os fluxos dos controladores,
incluindo um caso de regressão para cada defeito corrigido nesta revisão.

## Arquitetura

Quatro camadas, cada uma num pacote:

| Pacote        | Papel                                                                    |
| ------------- | ------------------------------------------------------------------------ |
| `entidade`    | Regras do domínio: `Produto`, `Cliente`, `Carrinho`, `ItemCarrinho`, `Unidade`, validação de CPF |
| `dao`         | Persistência em JSON, um arquivo por tipo, com escrita atômica            |
| `controlador` | Casos de uso; conversa com as entidades, os DAOs e as telas               |
| `limite`      | Telas FreeSimpleGUI; não conhecem entidades, só dicionários e primitivos  |

A dependência aponta sempre para dentro: `limite` não importa `entidade`
(exceto os tipos de valor `Unidade` e `cpf`, usados para formatar e validar na
entrada), e `entidade` não importa nada das outras camadas.

`ControladorSistema` cria os três controladores e passa a si mesmo para cada um,
que é como um controlador chega no outro (o carrinho precisa do produto para
descontar estoque, e do cliente para registrar a compra).

### Dados

A base fica em `dados/*.json`, criada na primeira execução e fora do controle de
versão. O formato anterior era pickle, trocado por JSON porque carregar um
pickle executa código do arquivo e porque renomear qualquer classe invalidava as
bases já gravadas.

## Estrutura

```
main.py                  ponto de entrada
entidade/
  cpf.py                 normalização e validação (dígitos verificadores)
  unidade.py             Enum das unidades de venda
  produto.py             produto e o próprio estoque
  cliente.py             cliente e o total gasto
  item_carrinho.py       linha do carrinho, com preço congelado na hora da compra
  carrinho.py            carrinho de um cliente
dao/
  abstract_dao.py        repositório genérico em JSON
  produto_dao.py cliente_dao.py carrinho_dao.py
controlador/
  controlador_sistema.py controlador_produto.py
  controlador_cliente.py controlador_carrinho.py
limite/
  tela_abstrata.py       janelas, formulários e conversões compartilhadas
  tela_sistema.py tela_produto.py tela_cliente.py tela_carrinho.py
```

## Notas de uso

- **CPF** é validado de verdade: 11 dígitos e dígitos verificadores conferidos.
  Pode ser digitado com ou sem pontuação. Ele identifica o cliente e não pode
  ser editado; para trocar de CPF, cadastre outro cliente.
- **Produto unitário** só aceita quantidade inteira, e a quantidade digitada é
  arredondada. Produtos em `Kg` e `L` aceitam fração.
- **Alterar produto** muda nome, preço e unidade. Estoque muda por *Estocar*,
  por compra e por devolução.
- Um produto que está em algum carrinho aberto não pode ser excluído, e um
  cliente com carrinho aberto também não. Do contrário a devolução não teria
  para onde repor o estoque.
