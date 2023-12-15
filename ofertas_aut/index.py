from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import pandas as pd


# Inicialize o driver do Selenium (neste exemplo, usaremos o Chrome)
driver = webdriver.Chrome()

# Abra a página da web desejada
driver.get(
    "https://localhost/ofertas/Ofertas/Ofertas/index.php?estilo=x4&tela=ofertas")

# Clica no avançado
element = driver.find_element(By.ID, "details-button")
element.click()

# vai para a pagina
element = driver.find_element(By.ID, "proceed-link")
element.click()

# seleciona banner
produtos = []

# lendo o csv
ofertas_df = pd.read_csv('#meu_rel', sep=';')

criaOfertas = ofertas_df[['MERCADORIA', 'ESTOQUE', 'RENTAB']]

criaOfertas['RENTAB'] = pd.to_numeric(
    criaOfertas['RENTAB'].str.replace(',', '.'), errors='coerce')
criaOfertas['MERCADORIA'] = criaOfertas['MERCADORIA'].str.split('-').str[0]

nova_lista_ofertas = criaOfertas[(criaOfertas['ESTOQUE'] > 30) & (
    criaOfertas['RENTAB'] > -10) & (criaOfertas['RENTAB'] <= 5)]

select_element = driver.find_element(By.ID, "cabecalho")
select = Select(select_element)
# Use select_by_value para selecionar o valor "fest_choco"
select.select_by_value("parceirao")

# Itera sobre a lista de produtos
for i, produto in enumerate(nova_lista_ofertas['MERCADORIA']):
    # Preenche o campo de busca correspondente ao índice atual
    num = i % 4 + 1  # Garante que o número varie de 1 a 4
    input_element = driver.find_element(By.ID, f"busca_produto_x4_{num}")
    input_element.clear()
    input_element.send_keys(Keys.RETURN)
    input_element.send_keys(produto)
    input_element.send_keys(Keys.RETURN)

    # Se todos os campos foram preenchidos, selecione a opção no rodapé e clique em salvar
    if num == 4 or i == len(nova_lista_ofertas) - 1:
        # Selecione a opção no rodapé
        select_element = driver.find_element(By.ID, "rodape")
        select = Select(select_element)
        input_element = driver.find_element(By.ID, f"vld_oferta")
        input_element.send_keys(Keys.RETURN)
        # Use select_by_value para selecionar o valor "pix_va"
        select.select_by_value("pix_va")
        # Clique em salvar
        element = driver.find_element(By.ID, "botaoSalvar")
        element.click()

nova_lista_ofertas.to_csv('Ofertas Geradas.csv', sep=';', index=False)
