import json


# FUNÇÕES SOLICITADAS:
def ler_banco(arquivo):
    try:
        with open(arquivo, 'r', encoding='utf-8') as banco_json:
            banco = json.load(banco_json)
    except FileNotFoundError:
        print(f'O arquivo "{arquivo}" não foi encontrado nesse diretório')
    return banco


def corrigir_nomes(banco):
    entrada = 'øß¢æ'
    saida = 'obca'
    tabela = str.maketrans(entrada, saida)

    for dado in banco:
        decod = dado['name']
        dado['name'] = decod.translate(tabela)
    return banco


def corrigir_precos(banco):
    for dado in banco:
        preco = str(dado['price'])
        preco = float(preco)
        dado['price'] = preco
    return banco


def corrigir_quantidade(banco):
    nBanco = list()
    nDado = dict()
    for dado in banco:
        if 'quantity' not in dado:
            dado['id'] = dado['id']
            dado['name'] = dado['name']
            dado['quantity'] = 0
            dado['price'] = dado['price']
            dado['category'] = dado['category']

    for dados in banco:
        nDado['id'] = dados['id']
        nDado['name'] = dados['name']
        nDado['quantity'] = dados['quantity']
        nDado['price'] = dados['price']
        nDado['category'] = dados['category']
        nBanco.append(nDado.copy())
    return nBanco


def exportar_banco(banco):
    with open('saida.json', 'w', encoding='utf-8') as saida_banco:
        json.dump(banco, saida_banco, indent=4, ensure_ascii=False)


def listagem_produtos(banco):
    listaOrdenada = sorted(banco, key=lambda k: (k['category'], k['id']))
    print('-' * 130)
    print('LISTA ORDENADA POR CATEGORIA E ID:'.center(130))
    print('-' * 130)
    for prod in listaOrdenada:
        print(f'NOME: {prod["name"]:.<80} ID: {prod["id"]}  CATEGORIA: {prod["category"]}')


def estoque_categoria(banco):
    dictCategoria = {'Panelas': 0, 'Eletrodomésticos': 0, 'Eletrônicos': 0, 'Acessórios': 0}
    for k in dictCategoria.keys():
        for dado in banco:
            if dado['category'] == k:
                dictCategoria[k] += dado['quantity']

    print('-' * 35)
    print('VALOR DO ESTOQUE POR CATEGORIA:'.center(35))
    print('-' * 35)
    for k, v in dictCategoria.items():
        print(f'{k:.<20}{v:>3}')


# PROGRAMA PRINCIPAL:
try:
    banco = ler_banco('broken-database.json')
except UnboundLocalError:
    print('Não foi possível ler o arquivo!')
else:
    banco = corrigir_nomes(banco)
    banco = corrigir_precos(banco)
    banco = corrigir_quantidade(banco)
    exportar_banco(banco)
try:
    banco = ler_banco('saida.json')
except UnboundLocalError:
    print('Não foi possível ler o arquivo')
else:
    listagem_produtos(banco)
    estoque_categoria(banco)
