
# coding: utf-8

# In[2]:


import requests as req
from bs4 import BeautifulSoup as bs

url = 'https://www.rank2traffic.com/stackoverflow.com' # Because Stack Overflow is God.

session = req.Session() # Começando a sessão, como se estivesse abrindo o browser
# Os headers fazem o Python fingir ser um browser comum, para evitar que o site bloqueie ele
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,/;q=0.8"}
ref = session.get(url, headers=headers) # Aqui ele abre o site e puxa o código-fonte
soup = bs(ref.text, "html.parser") # E transforma o código em texto (método .text) e logo depois em um objeto BeautifulSoup

# Extraindo a tabela
tab = soup.find('table', {'id':"myTab1-table"}) # método .find: encontre a primeira tabela com id 'myTab1-table'
rows=list() # para salvar as linhas da tabela
for row in tab.findAll("tr"):
    try:
        rows.append(row.findAll("td")[1].string.replace(" ","").replace("\n",""))# a segunda coluna (índice 1) é a que interessa
    except IndexError: # na primeira linha, não tem índice 1. então coloque o nome do site 
        rows.append(url[-17:])
        
# Extraindo dados complementares de uso
meta = soup.findAll('div',{'class':'infobox-data'})[1:] # método .findAll: Encontre TODOS nessas condições, e retorne uma lista
for box in meta:
    rows.append(box.find('span').string)
    rows.append(box.find('div').string)

# Extraindo percentual de acessos por país
tab = soup.find('table', {'class':"table table-hover table-condensed"})
try: 
    for row in tab.findAll("tr"):
        try:
            rows.append(row.findAll("td")[0].string)
            rows.append(row.findAll("td")[1].string)
        except IndexError:
            rows.append('Paises')
except AttributeError:
    rows.append('Supondo, sem info oficial')
    rows.append('100%')

import pandas as pd
df = pd.DataFrame(rows)
df.to_excel("StackOverflow.xlsx")


