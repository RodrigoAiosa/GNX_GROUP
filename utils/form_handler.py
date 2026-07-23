import requests
import streamlit as st
from bs4 import BeautifulSoup
import re
from .log_generator import gerar_arquivo_log_tabela
import os

# URL do formulário alvo
URL_FORMULARIO = "https://gnxgroup.com.br/solucoes/temporarios/"

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
        url = URL_FORMULARIO
        
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
