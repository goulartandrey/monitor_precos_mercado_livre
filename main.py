from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import date

#Input do produto desejado pelo usuário
produto_escolha = input('Qual produto você deseja?')

#Requisição do site mercado livre
headers = {'User-Agent': 'Mozilla/5.0'}
site = f"https://lista.mercadolivre.com.br/{produto_escolha}"
content = requests.get(site, headers=headers)

#Parseando a pagina HTML com o BeautifulSoup
soup = BeautifulSoup(content.text, 'html.parser')

#Encontrando todos os produtos da pagina
lista_produtos = soup.findAll('div', attrs={'class':'ui-search-result'})

#Criando listas vazias para adicionar os dados posteriormente
produtos = []
links = []
precos = []

#Percorrendo os itens da lista de produtos
for i in lista_produtos:
    try:
        nome = i.find('h2', attrs={'class':'ui-search-item__title'}).text
        link = i.find('a', attrs={'class':'ui-search-result__content'})['href']
        preco = i.find('span', attrs={'class':'price-tag-fraction'}).text

    except:
        nome = i.find('h2', attrs={'class': 'ui-search-item__title'}).text
        link = i.find('a', attrs={'class': 'ui-search-item__group__element'})['href']
        preco = i.find('span', attrs={'class': 'price-tag-fraction'}).text

        produtos.append(nome)
        links.append(link)
        precos.append(preco)
    else:
        produtos.append(nome)
        links.append(link)
        precos.append(preco)

#Zipando as listas produtos, links e preços
dados = list(zip(produtos, links, precos))

#Criando o DataFrame com os dados obtidos
df = pd.DataFrame(dados, columns=['PRODUTO', 'LINK', 'PRECO'])

#Exportando o DataFrame para excel com a data de hoje
data = date.today().strftime('%b-%d-%Y')
df.to_excel(rf'C:\Users\goula\desktop\pesquisa{data}.xlsx', index=False)