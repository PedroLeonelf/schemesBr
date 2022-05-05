
import pytest
import Similiarity as sim

import Entidade as entity

import Parser 


from GrafoValorado import *


def test_any_exemple(vect1, ligacoes1, vect2 = None, ligacoes2 = None):
    graph1 = Grafo()
    graph2 = Grafo()
    if vect2 == None:
        for entity in vect1:
            if entity.getAtributos() == []:
                entity.setAtributo('None')
            graph1.adiciona(entity)
        for ligacao in ligacoes1:
            graph1.adicionaAresta(ligacao[0], ligacao[1], ligacao[2], ligacao[3])
    else:
        for entity1, entity2 in zip(vect1, vect2):
            if entity1.getAtributos() == []:
                entity1.setAtributo('None')
            if entity2.getAtributos() == []:
                entity2.setAtributo('None')
            graph1.adiciona(entity1)
            graph2.adiciona(entity2)
        print(graph1,graph2)
        for ligacao1,ligacao2 in zip(ligacoes1, ligacoes2):
            graph1.adicionaAresta(ligacao1[0], ligacao1[1], ligacao1[2], ligacao1[3])
            graph2.adicionaAresta(ligacao2[0], ligacao2[1], ligacao2[2], ligacao2[3])
    
    if vect2 == None:
        assert sim.graphSimiliarity(graph1, graph1) == 100
    else:
        assert sim.graphSimiliarity(graph1, graph2) > 0
    
    

    
    




def test_example1():#Graph similarity is 100.0% time:1.3883669296900432
    entidade1 = entity.Entidade(["Proprietario", "key CPF", "Nome", "Email"])
    entidade2 = entity.Entidade(["Imovel", "Nome", "Localização", "Aluguel"])
    entidade3 = entity.Entidade(["Corretor", "Imobiliaria", 'Especialização'])
    entidade4 = entity.Entidade(["Inquilino", "key cpf", "Nome", "Aluguel_em_dia"])

    entidades = [entidade1, entidade2, entidade3, entidade4]

    ligacoes = []

    ligacoes.append(['Proprietario', "Imovel", '1:1', '1:n'])
    ligacoes.append(['Imovel', 'Inquilino', '1:1', '1:n'])
    ligacoes.append(['Inquilino', 'Corretor', '1:1', '1:1'])
    ligacoes.append(['Proprietario', 'Corretor', '1:1', '1:n'])

    test_any_exemple(entidades, ligacoes)

    
def test_example2():
    entidade1 = entity.Entidade(["Proprietario", "key CPF", "Nome", "Email"])
    entidade2 = entity.Entidade(["Imovel", "Nome", "Localização", "Aluguel"])
    entidade3 = entity.Entidade(["Corretor", "Imobiliaria", 'Especialização'])
    entidade4 = entity.Entidade(["Inquilino", "key cpf", "Nome", "Aluguel_em_dia"])

    entidade5 = entity.Entidade(["Dono", "key RG", "Nome", "EnderecoDeEmail"])
    entidade6 = entity.Entidade(["Propriedade", "NomeDoEstabelecimento", "Localização", "Condominio"])
    entidade7 = entity.Entidade(["Corretor", "Imobiliaria", 'Especialidade'])
    entidade8 = entity.Entidade(["Morador", "key cpf", "Nome", "Condominio_em_dia"])


    graph = Grafo()
    graph2 = Grafo()
    graph.adiciona(entidade1)
    graph.adiciona(entidade2)
    graph.adiciona(entidade3)
    graph.adiciona(entidade4)
    graph2.adiciona(entidade5)
    graph2.adiciona(entidade6)
    graph2.adiciona(entidade7)
    graph2.adiciona(entidade8)

    graph.adicionaAresta(entidade1, entidade2, '1:1', '1:n')
    graph.adicionaAresta(entidade2, entidade4, '1:1', '1:n')
    graph.adicionaAresta(entidade4, entidade3, '1:1', '1:1')
    graph.adicionaAresta(entidade1, entidade3, '1:1', '1:n')

    graph2.adicionaAresta(entidade5, entidade6, '1:1', '1:n')
    graph2.adicionaAresta(entidade6, entidade8, '1:1', '1:n')
    graph2.adicionaAresta(entidade8, entidade7, '1:1', '1:1')
    graph2.adicionaAresta(entidade5, entidade7, '1:1', '1:n')

    assert sim.graphSimiliarity(graph, graph2) == 100.0





def teste1_exemplo1(): # 100% similiarity, 4.12 sem abreviação 5.04 com abreviação
    entidade1 = entity.Entidade(["Empregado", 'key RG', 'nome', 'data-ingresso', 'salario'])
    entidade2 = entity.Entidade(["Degustador"])
    entidade3 = entity.Entidade(["Editor"])
    entidade4 = entity.Entidade(["Livro", 'titulo', 'key ISBN'])
    entidade5 = entity.Entidade(["Cozinheiro", 'key nome-fantasia', 'restaurantes [0,n]', ])
    entidade6 = entity.Entidade(["Receita", "key codigo", 'nome', 'data', 'categoria [1,n]', 'descricao-preparo', 'num-porcoes'])
    entidade7 = entity.Entidade(["Ingrediente", 'key nome', 'descrição', 'quantidade', 'medida'])

    entidades1 = [entidade1, entidade2, entidade3, entidade4, entidade5, entidade6, entidade7]

    ligacoes1 = []
    ligacoes1.append(['Empregado', 'Cozinheiro', '1:1', '0:1'])
    ligacoes1.append(['Empregado', 'Degustador', '1:1', '0:1'])
    ligacoes1.append(['Empregado', 'Editor', '1:1', '0:1'])
    ligacoes1.append(['Editor', 'Livro', '1:1', '0:n'])
    ligacoes1.append(['Livro', 'Receita', '0:N', '1:n'])
    ligacoes1.append(['Cozinheiro', 'Receita', '1:1', '1:n'])
    ligacoes1.append(['Degustador', 'Receita', '0:n', '1:n'])
    ligacoes1.append(['Receita', 'Ingrediente', '1:1', '1:n'])
    test_any_exemple(entidades1, ligacoes1)


def teste1(): #Graph similarity is 97.0% time:3.042292058467865 

    entidade1 = entity.Entidade(["Empregado", 'key RG', 'nome', 'data-ingresso', 'salario'])
    entidade2 = entity.Entidade(["Degustador"])
    entidade3 = entity.Entidade(["Editor"])
    entidade4 = entity.Entidade(["Livro", 'titulo', 'key ISBN'])
    entidade5 = entity.Entidade(["Cozinheiro", 'key nome-fantasia', 'restaurantes [0,n]', ])
    entidade6 = entity.Entidade(["Receita", "key codigo", 'nome', 'data', 'categoria [1,n]', 'descricao-preparo', 'num-porcoes'])
    entidade7 = entity.Entidade(["Ingrediente", 'key nome', 'descrição', 'quantidade', 'medida'])

    entidades1 = [entidade1, entidade2, entidade3, entidade4, entidade5, entidade6, entidade7]

    ligacoes1 = []
    ligacoes1.append(['Empregado', 'Cozinheiro', '1:1', '0:1'])
    ligacoes1.append(['Empregado', 'Degustador', '1:1', '0:1'])
    ligacoes1.append(['Empregado', 'Editor', '1:1', '0:1'])
    ligacoes1.append(['Editor', 'Livro', '1:1', '0:n'])
    ligacoes1.append(['Livro', 'Receita', '0:N', '1:n'])
    ligacoes1.append(['Cozinheiro', 'Receita', '1:1', '1:n'])
    ligacoes1.append(['Degustador', 'Receita', '0:n', '1:n'])
    ligacoes1.append(['Receita', 'Ingrediente', '1:1', '1:n'])

    entidade1 = entity.Entidade(["Funcionario", 'key Registro-Geral', 'nome-funcionario', 'data-ingresso', 'salario-func'])
    entidade2 = entity.Entidade(["Provador"])
    entidade3 = entity.Entidade(["Editor_livro"])
    entidade4 = entity.Entidade(["Livro_receita", 'titulo-livro', 'key International_Standard_Book_Number'])
    entidade5 = entity.Entidade(["Chefe_de_cozinha", 'key nome-fantasia', 'restaurantes [0,n]', ])
    entidade6 = entity.Entidade(["Receita", "key id", 'nome-da-receita', 'data_receita', 'categoria_receita [1,n]', 'preparo_descricao', 'porcoes-numero'])
    entidade7 = entity.Entidade(["Componente", 'key nome-componente', 'descrição_componente', 'qtd_componente', 'medida_componente'])

    entidades2 = [entidade1, entidade2, entidade3, entidade4, entidade5, entidade6, entidade7]

    ligacoes2 = []
    ligacoes2.append(['Funcionario', 'Chefe_de_cozinha', '1:1', '0:1'])
    ligacoes2.append(['Funcionario', 'Provador', '1:1', '0:1'])
    ligacoes2.append(['Funcionario', 'Editor_livro', '1:1', '0:1'])
    ligacoes2.append(['Editor_livro', 'Livro_receita', '1:1', '0:n'])
    ligacoes2.append(['Livro_receita', 'Receita', '0:N', '1:n'])
    ligacoes2.append(['Chefe_de_cozinha', 'Receita', '1:1', '1:n'])
    ligacoes2.append(['Provador', 'Receita', '0:n', '1:n'])
    ligacoes2.append(['Receita', 'Componente', '1:1', '1:n'])

    test_any_exemple(entidades1, ligacoes1, entidades2, ligacoes2)


def teste2():
    # time:1.8175164739290872
    # Graph similarity is 54.0%
    #76 without estructure limitation
    entidade1 = entity.Entidade(['Socio', 'key num-matricula', 'endereco', 'telefone (0,n)', 'data-nasc', 'data-pagamento'])
    entidade2 = entity.Entidade(['Remido'])
    entidade3 = entity.Entidade(['Não Remido', 'data-pagamento'])
    entidade4 = entity.Entidade(['Dependente', 'key nome', 'data-nascimento'])
    entidade5 = entity.Entidade(['Filho'])
    entidade6 = entity.Entidade(['Conjuge'])

    entidades1 = [entidade1, entidade2, entidade3, entidade4, entidade5, entidade6]

    ligacoes1 = []

    ligacoes1.append(['Socio', 'Remido', '1:1', '0:1'])
    ligacoes1.append(['Socio', 'Não Remido', '1:1', '0:1'])
    ligacoes1.append(['Socio', 'Dependente', '1:1', '0:n'])
    ligacoes1.append(['Dependente', 'Filho', '1:1', '0:n'])
    ligacoes1.append(['Dependente', 'Conjuge', '1:1', '0:1'])

    entidade1 = entity.Entidade(["Funcionario", 'key Registro-Geral', 'nome-funcionario', 'data-ingresso', 'salario-func'])
    entidade2 = entity.Entidade(["Provador"])
    entidade3 = entity.Entidade(["Editor_livro"])
    entidade4 = entity.Entidade(["Livro_receita", 'titulo-livro', 'key International_Standard_Book_Number'])
    entidade5 = entity.Entidade(["Chefe_de_cozinha", 'key nome-fantasia', 'restaurantes [0,n]', ])
    entidade6 = entity.Entidade(["Receita", "key id", 'nome-da-receita', 'data_receita', 'categoria_receita [1,n]', 'preparo_descricao', 'porcoes-numero'])
    entidade7 = entity.Entidade(["Componente", 'key nome-componente', 'descrição_componente', 'qtd_componente', 'medida_componente'])

    entidades2 = [entidade1, entidade2, entidade3, entidade4, entidade5, entidade6, entidade7]

    ligacoes2 = []
    ligacoes2.append(['Funcionario', 'Chefe_de_cozinha', '1:1', '0:1'])
    ligacoes2.append(['Funcionario', 'Provador', '1:1', '0:1'])
    ligacoes2.append(['Funcionario', 'Editor_livro', '1:1', '0:1'])
    ligacoes2.append(['Editor_livro', 'Livro_receita', '1:1', '0:n'])
    ligacoes2.append(['Livro_receita', 'Receita', '0:N', '1:n'])
    ligacoes2.append(['Chefe_de_cozinha', 'Receita', '1:1', '1:n'])
    ligacoes2.append(['Provador', 'Receita', '0:n', '1:n'])
    ligacoes2.append(['Receita', 'Componente', '1:1', '1:n'])

    test_any_exemple(entidades1, ligacoes1, entidades2, ligacoes2)

def teste_artigo(): # 74
    entidade1 = entity.Entidade(['Comprador', 'CPF', 'ID', 'Endereco'])
    entidade2 = entity.Entidade(['Compra', 'ID', 'data', 'total'])
    entidade3 = entity.Entidade(['Item', 'id', 'Nome', 'qtd', 'preco'])

    entidades1 = [entidade1, entidade2, entidade3]

    ligacoes1 = []

    ligacoes1.append(['Comprador', 'Compra', '1:1', '0:N'])
    ligacoes1.append(['Compra', 'Item', '1:1', '0:N'])



    entidade1 = entity.Entidade(['Cliente', 'cod_cliente', 'nome', 'telefone', 'vip'])
    entidade2 = entity.Entidade(['nota_fiscal', 'cod_nota', 'dt_nota', 'tot_nota'])
    entidade3 = entity.Entidade(['prod_vendido', 'cod_produto', 'nome_prod', 'quantidade'])

    entidades2 = [entidade1, entidade2, entidade3]

    ligacoes2 = []

    ligacoes2.append(['Cliente', 'nota_fiscal', '1:1', '1:N'])
    ligacoes2.append(['nota_fiscal', 'prod_vendido', '1:1', '1:N'])



    # entidade1 = entity.Entidade('')
    # entidade2 = entity.Entidade('')
    # entidade3 = entity.Entidade('')
    # entidade4 = entity.Entidade('')
    # entidade5 = entity.Entidade('')
    # entidade6 = entity.Entidade('')

    # entidades2 = [entidade1, entidade2, entidade3, entidade4, entidade5, entidade6]

    # ligacoes2 = []

    # ligacoes2.append()
    # ligacoes2.append()
    # ligacoes2.append()
    # ligacoes2.append()
    # ligacoes2.append()
    # ligacoes2.append()

    test_any_exemple(entidades1, ligacoes1, entidades2, ligacoes2)


def retorna_modelo(arquivo):
    parser = Parser.Parser()
    with open(arquivo,'r+') as file:
        parser.setLinhas(file.readlines())
    parser.traduzLinhas()
    return parser.getModelo()

def getGrafo(modelo):
    grafo = Grafo()
    for entidade in modelo.getEntidades():
        if entidade.getAtributos() == []:
            entidade.setAtributo('None')
        grafo.adiciona(entidade)
    
    for relation in modelo.getRelacionamentos():
        entidade1, entidade2 = relation.getEntidadesRelacionadas()
        grafo.adicionaAresta(entidade1.getNome(), entidade2.getNome(), entidade1.getCardinalidade(), entidade2.getCardinalidade())
    return grafo

def teste_arquivos(arq1, arq2):
    sim.graphSimiliarity(getGrafo(retorna_modelo(arq1)), getGrafo(retorna_modelo(arq2)))

# teste_artigo()

# teste_arquivos('codigo modelos/exemplo1', 'codigo modelos/exemplo1') # 100
# teste_arquivos('codigo modelos/exemplo1', 'codigo modelos/exemplo2') # 98
# teste_arquivos('codigo modelos/exemplo1', 'codigo modelos/exemplo3') # 94
# teste_arquivos('codigo modelos/exemplo1', 'codigo modelos/exemplo4') # 93
# teste_arquivos('codigo modelos/exemplo1', 'codigo modelos/exemplo5') # 85
# teste_arquivos('codigo modelos/exemplo1', 'codigo modelos/exemplo6') # 84 
# teste_arquivos('codigo modelos/exemplo1', 'codigo modelos/exemplo7') # 81
# teste_arquivos('codigo modelos/exemplo1', 'codigo modelos/exemplo8') # 77
# teste_arquivos('codigo modelos/exemplo1', 'codigo modelos/exemplo9') # 69
# teste_arquivos('codigo modelos/exemplo1', 'codigo modelos/exemplo10')# 62
# teste_arquivos('codigo modelos/exemplo1', 'codigo modelos/exemplo11')

# teste_arquivos('modelosTarefas/atividades/gabarito.txt', 'modelosTarefas/atividades/1.txt') # 88
# teste_arquivos('modelosTarefas/atividades/gabarito.txt', 'modelosTarefas/atividades/2.txt') # 93
# teste_arquivos('modelosTarefas/atividades/gabarito.txt', 'modelosTarefas/atividades/3.txt') # 87
# teste_arquivos('modelosTarefas/atividades/gabarito.txt', 'modelosTarefas/atividades/4.txt') # 81 min
# teste_arquivos('modelosTarefas/atividades/gabarito.txt', 'modelosTarefas/atividades/5.txt') # 88
# teste_arquivos('modelosTarefas/atividades/gabarito.txt', 'modelosTarefas/atividades/6.txt') # 87
# teste_arquivos('modelosTarefas/atividades/gabarito.txt', 'modelosTarefas/atividades/7.txt') # 90
# teste_arquivos('modelosTarefas/atividades/gabarito.txt', 'modelosTarefas/atividades/8.txt') # 92
# teste_arquivos('modelosTarefas/atividades/gabarito.txt', 'modelosTarefas/atividades/9.txt') # 87
# teste_arquivos('modelosTarefas/atividades/gabarito.txt', 'modelosTarefas/atividades/10.txt')# 94 
# teste_arquivos('modelosTarefas/atividades/gabarito.txt', 'modelosTarefas/atividades/11.txt')# 84
# teste_arquivos('modelosTarefas/atividades/gabarito.txt', 'modelosTarefas/atividades/12.txt')# 86
# teste_arquivos('modelosTarefas/atividades/gabarito.txt', 'modelosTarefas/atividades/13.txt')# 90
# teste_arquivos('modelosTarefas/atividades/gabarito.txt', 'modelosTarefas/atividades/14.txt')# 90
# teste_arquivos('modelosTarefas/atividades/gabarito.txt', 'modelosTarefas/atividades/15.txt')# 98 max
# teste_arquivos('modelosTarefas/atividades/gabarito.txt', 'modelosTarefas/atividades/16.txt')# 88
# teste_arquivos('modelosTarefas/atividades/gabarito.txt', 'modelosTarefas/atividades/17.txt')# 88
# teste_arquivos('modelosTarefas/atividades/gabarito.txt', 'modelosTarefas/atividades/18.txt')# 88
# teste_arquivos('modelosTarefas/atividades/gabarito.txt', 'modelosTarefas/atividades/19.txt')# 82
# teste_arquivos('modelosTarefas/atividades/gabarito.txt', 'modelosTarefas/atividades/20.txt')# 83
# teste_arquivos('modelosTarefas/atividades/gabarito.txt', 'modelosTarefas/atividades/21.txt')# 88
# teste_arquivos('modelosTarefas/atividades/gabarito.txt', 'modelosTarefas/atividades/22.txt')# 92
# teste_arquivos('modelosTarefas/atividades/gabarito.txt', 'modelosTarefas/atividades/23.txt')# 

teste_arquivos('textos/specialization1', 'textos/specialization2')
