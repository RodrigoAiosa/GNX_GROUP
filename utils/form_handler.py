import requests
import streamlit as st
from bs4 import BeautifulSoup
import re
from .log_generator import gerar_arquivo_log_tabela
import os
import time

def extrair_csrf_token(html):
    """Extrai o token CSRF do HTML da página"""
    soup = BeautifulSoup(html, 'html.parser')
    
    token_input = soup.find('input', {'name': '_wpnonce'})
    if token_input:
        return token_input.get('value', '')
    
    token_input = soup.find('input', {'id': '_wpnonce'})
    if token_input:
        return token_input.get('value', '')
    
    token_input = soup.find('input', {'type': 'hidden', 'name': re.compile(r'nonce|_wpnonce', re.I)})
    if token_input:
        return token_input.get('value', '')
    
    script_pattern = r'var\s+nonce\s*=\s*[\'"]([^\'"]+)[\'"]'
    script_match = re.search(script_pattern, html)
    if script_match:
        return script_match.group(1)
    
    return ''

def preencher_formulario_api(nome, email, telefone, empresa, departamento, segmento, mensagem):
    """Preenche o formulário usando requests (POST direto) - Modo API"""
    try:
        url = "https://gnxgroup.com.br/solucoes/temporarios/"
        
        st.info("🌐 Acessando o site para obter o token...")
        
        headers_initial = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        
        session = requests.Session()
        response = session.get(url, headers=headers_initial)
        response.raise_for_status()
        
        token = extrair_csrf_token(response.text)
        
        st.info("📝 Preparando dados do formulário...")
        
        form_data = {
            'form_fields[nome]': nome,
            'form_fields[email]': email,
            'form_fields[telefone]': telefone,
            'form_fields[empresa]': empresa,
            'form_fields[departamento]': departamento,
            'form_fields[segmento]': segmento,
            'form_fields[mensagem_profissional]': mensagem,
        }
        
        if token:
            form_data['_wpnonce'] = token
        
        headers_post = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://gnxgroup.com.br',
            'Referer': url,
            'Connection': 'keep-alive',
        }
        
        st.info("📤 Enviando formulário...")
        
        dados_para_log = {
            'Nome': nome,
            'Email': email,
            'Telefone': telefone,
            'Empresa': empresa,
            'Departamento': departamento,
            'Segmento': segmento,
            'Mensagem': mensagem
        }
        
        post_response = session.post(
            url,
            data=form_data,
            headers=headers_post,
            allow_redirects=True
        )
        
        if post_response.status_code == 200:
            soup = BeautifulSoup(post_response.text, 'html.parser')
            
            success_messages = soup.find_all(['div', 'p', 'span'], 
                                           text=re.compile(r'(sucesso|success|enviado|obrigado|agradecimento)', re.I))
            
            if success_messages:
                mensagem_retorno = "Formulário enviado com sucesso!"
                status_envio = "SUCESSO"
            else:
                mensagem_retorno = "Formulário enviado (verifique se recebeu o email de confirmação)"
                status_envio = "ENVIADO"
            
            nome_log = gerar_arquivo_log_tabela(dados_para_log, status_envio, mensagem_retorno)
            
            return {
                "status": "sucesso",
                "departamento": departamento,
                "segmento": segmento,
                "mensagem": mensagem,
                "detalhe": mensagem_retorno,
                "log_txt": nome_log
            }
        else:
            mensagem_erro = f"Erro {post_response.status_code}: {post_response.text[:200]}"
            nome_log = gerar_arquivo_log_tabela(dados_para_log, "ERRO", mensagem_erro)
            
            return {
                "status": "erro",
                "mensagem_erro": mensagem_erro,
                "log_txt": nome_log
            }
            
    except requests.exceptions.RequestException as e:
        dados_para_log = {
            'Nome': nome,
            'Email': email,
            'Telefone': telefone,
            'Empresa': empresa,
            'Departamento': 'N/A',
            'Segmento': 'N/A',
            'Mensagem': 'N/A'
        }
        mensagem_erro = f"Erro de conexão: {str(e)}"
        nome_log = gerar_arquivo_log_tabela(dados_para_log, "ERRO_CONEXAO", mensagem_erro)
        
        return {
            "status": "erro",
            "mensagem_erro": mensagem_erro,
            "log_txt": nome_log
        }
    except Exception as e:
        mensagem_erro = f"Erro inesperado: {str(e)}"
        return {
            "status": "erro",
            "mensagem_erro": mensagem_erro
        }

def preencher_formulario_selenium(nome, email, telefone, empresa, departamento, segmento, mensagem):
    """Preenche o formulário usando Selenium - Modo Visual"""
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        
        st.info("🌐 Iniciando navegador para visualização...")
        
        # Configurar Chrome
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1280,1024")
        # Remover headless para ver o navegador
        # chrome_options.add_argument("--headless")  # Comentado para ver o navegador
        
        # Iniciar driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        st.info("🌐 Abrindo o site...")
        driver.get("https://gnxgroup.com.br/solucoes/temporarios/")
        time.sleep(3)
        
        # Aguardar elementos
        wait = WebDriverWait(driver, 15)
        
        st.info("📝 Preenchendo o formulário...")
        
        # Preencher Nome
        nome_field = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='form-field-nome']")))
        nome_field.clear()
        nome_field.send_keys(nome)
        time.sleep(0.5)
        
        # Preencher Email
        email_field = driver.find_element(By.XPATH, "//*[@id='form-field-email']")
        email_field.clear()
        email_field.send_keys(email)
        time.sleep(0.5)
        
        # Preencher Telefone
        telefone_field = driver.find_element(By.XPATH, "//*[@id='form-field-telefone']")
        telefone_field.clear()
        telefone_field.send_keys(telefone)
        time.sleep(0.5)
        
        # Preencher Empresa
        empresa_field = driver.find_element(By.XPATH, "//*[@id='form-field-empresa']")
        empresa_field.clear()
        empresa_field.send_keys(empresa)
        time.sleep(0.5)
        
        # Selecionar Departamento
        st.info(f"📋 Selecionando departamento: {departamento}")
        departamento_select = driver.find_element(By.XPATH, "//*[@id='form-field-departamento']")
        for option in departamento_select.find_elements(By.TAG_NAME, "option"):
            if option.text == departamento:
                option.click()
                break
        time.sleep(0.5)
        
        # Selecionar Segmento
        st.info(f"📋 Selecionando segmento: {segmento}")
        segmento_select = driver.find_element(By.XPATH, "//*[@id='form-field-segmento']")
        for option in segmento_select.find_elements(By.TAG_NAME, "option"):
            if option.text == segmento:
                option.click()
                break
        time.sleep(0.5)
        
        # Preencher Mensagem
        st.info("💬 Preenchendo mensagem...")
        mensagem_field = driver.find_element(By.XPATH, "//*[@id='form-field-mensagem_profissional']")
        mensagem_field.clear()
        mensagem_field.send_keys(mensagem)
        time.sleep(1)
        
        # Clicar no botão de enviar
        st.info("📤 Enviando formulário...")
        try:
            submit_button = driver.find_element(By.XPATH, "//*[@id='contato']/div/div[2]/div[1]/div[2]/div/form/div/div[9]/button")
            submit_button.click()
            time.sleep(3)
        except:
            # Tentar encontrar o botão de outra forma
            submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
            submit_button.click()
            time.sleep(3)
        
        # Verificar se foi enviado
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        success_messages = soup.find_all(['div', 'p', 'span'], 
                                       text=re.compile(r'(sucesso|success|enviado|obrigado|agradecimento)', re.I))
        
        if success_messages:
            mensagem_retorno = "Formulário enviado com sucesso!"
            status_envio = "SUCESSO"
        else:
            mensagem_retorno = "Formulário enviado (verifique se recebeu o email de confirmação)"
            status_envio = "ENVIADO"
        
        # Fechar navegador
        driver.quit()
        
        # Gerar log
        dados_para_log = {
            'Nome': nome,
            'Email': email,
            'Telefone': telefone,
            'Empresa': empresa,
            'Departamento': departamento,
            'Segmento': segmento,
            'Mensagem': mensagem
        }
        
        nome_log = gerar_arquivo_log_tabela(dados_para_log, status_envio, mensagem_retorno)
        
        return {
            "status": "sucesso",
            "departamento": departamento,
            "segmento": segmento,
            "mensagem": mensagem,
            "detalhe": mensagem_retorno,
            "log_txt": nome_log
        }
        
    except Exception as e:
        try:
            driver.quit()
        except:
            pass
        return {
            "status": "erro",
            "mensagem_erro": f"Erro no Selenium: {str(e)}"
        }
