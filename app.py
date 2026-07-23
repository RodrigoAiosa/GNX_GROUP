import streamlit as st
import requests
import random
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime
import json
import os

# Configuração da página Streamlit
st.set_page_config(
    page_title="Automação GNX Group",
    page_icon="🤖",
    layout="wide"
)

# Título do app
st.title("🤖 Automação de Formulário - GNX Group")
st.markdown("---")

# Lista de frases sobre habilidades
FRASES_HABILIDADES = [
    "Profissional com expertise em Python para automação de processos e análise de dados, transformando tarefas repetitivas em soluções eficientes.",
    "Especialista em SQL com capacidade de extrair, manipular e analisar grandes volumes de dados para tomada de decisão estratégica.",
    "Domínio avançado em Power BI para criação de dashboards interativos e relatórios gerenciais de alto impacto.",
    "Ampla experiência em Excel, incluindo fórmulas avançadas, macros e VBA para otimização de planilhas complexas.",
    "Especialista em automação de processos com Python, reduzindo tempo de execução de tarefas em até 70%.",
    "Profissional de Business Intelligence com foco em transformar dados em insights acionáveis para o negócio.",
    "Experiência em integração de sistemas utilizando Python e APIs para automação de fluxos de trabalho.",
    "Criação de soluções em Power BI que facilitam a visualização e monitoramento de KPIs críticos.",
    "Especialista em otimização de bancos de dados SQL, garantindo performance e integridade dos dados.",
    "Desenvolvimento de automações em Python para web scraping, extração e processamento de dados estruturados.",
    "Habilidade em criar modelos preditivos e análises estatísticas utilizando Python e bibliotecas como Pandas e NumPy.",
    "Criação de relatórios automatizados em Excel com VBA, reduzindo erros manuais e aumentando a produtividade.",
    "Experiência em implementação de soluções de BI com Power BI e SQL para suporte à alta gestão.",
    "Especialista em automação de e-mails e relatórios com Python, otimizando a comunicação interna.",
    "Desenvolvimento de dashboards em Power BI com atualização automática via APIs e bancos de dados.",
    "Profissional com forte capacidade analítica e resolução de problemas complexos usando Python.",
    "Automação de planilhas Excel com Python, permitindo processamento massivo de dados com eficiência.",
    "Criação de pipelines de dados usando SQL e Python para ETL (Extract, Transform, Load).",
    "Especialista em visualização de dados com Power BI, criando narrativas visuais que impulsionam decisões.",
    "Combinação de habilidades em Python, SQL, Power BI e Excel para soluções completas em dados e automação."
]

def get_random_departamento():
    """Retorna um departamento aleatório"""
    departamentos = [
        "Recursos Humanos (RH)",
        "Compras ou Suprimentos",
        "Gerência Executiva",
        "Marketing",
        "Vendas",
        "Trade Marketing",
        "Desenvolvimento de Negócios",
        "Outros"
    ]
    return random.choice(departamentos)

def get_random_segmento():
    """Retorna um segmento aleatório"""
    segmentos = [
        "Indústria",
        "Logística e Transporte",
        "Varejo",
        "Setor de alimentos e restaurantes",
        "Eventos e Entretenimento",
        "Hotelaria e Turismo",
        "Call Centers",
        "Setor de saúde e bem-estar",
        "Educação",
        "Tecnologia da Informação",
        "Serviços Financeiros",
        "Outros"
    ]
    return random.choice(segmentos)

def get_random_frase():
    """Retorna uma frase aleatória sobre habilidades"""
    return random.choice(FRASES_HABILIDADES)

def extrair_csrf_token(html):
    """Extrai o token CSRF do HTML da página"""
    soup = BeautifulSoup(html, 'html.parser')
    
    # Tenta encontrar o token CSRF
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

def gerar_arquivo_log(dados_envio, status_envio, mensagem_retorno=""):
    """Gera um arquivo de log com todos os dados enviados"""
    data_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
    data_hora_formatada = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Estrutura do log
    log = {
        "data_hora_envio": data_hora_formatada,
        "timestamp_unix": int(time.time()),
        "status_envio": status_envio,
        "mensagem_retorno": mensagem_retorno,
        "dados_enviados": dados_envio
    }
    
    # Nome do arquivo
    nome_arquivo = f"log_envio_{data_hora}.json"
    
    # Salvar como JSON
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        json.dump(log, f, ensure_ascii=False, indent=4)
    
    # Também salvar como TXT para fácil leitura
    nome_arquivo_txt = f"log_envio_{data_hora}.txt"
    with open(nome_arquivo_txt, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("LOG DE ENVIO DE FORMULÁRIO - GNX GROUP\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Data/Hora do Envio: {data_hora_formatada}\n")
        f.write(f"Timestamp UNIX: {int(time.time())}\n")
        f.write(f"Status: {status_envio}\n")
        if mensagem_retorno:
            f.write(f"Mensagem: {mensagem_retorno}\n")
        f.write("\n" + "-" * 80 + "\n")
        f.write("DADOS ENVIADOS:\n")
        f.write("-" * 80 + "\n")
        for campo, valor in dados_envio.items():
            f.write(f"{campo}: {valor}\n")
        f.write("\n" + "=" * 80 + "\n")
        f.write("FIM DO LOG\n")
        f.write("=" * 80 + "\n")
    
    return nome_arquivo, nome_arquivo_txt, log

def preencher_formulario_api(nome, email, telefone, empresa):
    """Preenche o formulário usando requests (POST direto)"""
    try:
        # URL do formulário
        url = "https://gnxgroup.com.br/solucoes/temporarios/"
        
        st.info("🌐 Acessando o site para obter o token...")
        
        # Headers para a requisição inicial
        headers_initial = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        
        # Faz a requisição inicial para obter o token
        session = requests.Session()
        response = session.get(url, headers=headers_initial)
        response.raise_for_status()
        
        # Extrai o token CSRF
        token = extrair_csrf_token(response.text)
        
        # Seleciona departamento e segmento aleatoriamente
        departamento = get_random_departamento()
        segmento = get_random_segmento()
        mensagem = get_random_frase()
        
        st.info("📝 Preparando dados do formulário...")
        
        # Dados do formulário
        form_data = {
            'form_fields[nome]': nome,
            'form_fields[email]': email,
            'form_fields[telefone]': telefone,
            'form_fields[empresa]': empresa,
            'form_fields[departamento]': departamento,
            'form_fields[segmento]': segmento,
            'form_fields[mensagem_profissional]': mensagem,
        }
        
        # Adiciona token se encontrado
        if token:
            form_data['_wpnonce'] = token
        
        # Headers para o POST
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
        
        # Prepara os dados para o log
        dados_para_log = {
            'Nome': nome,
            'Email': email,
            'Telefone': telefone,
            'Empresa': empresa,
            'Departamento': departamento,
            'Segmento': segmento,
            'Mensagem': mensagem,
            'Token_CSRF': token if token else 'Não encontrado'
        }
        
        # Envia o POST
        post_response = session.post(
            url,
            data=form_data,
            headers=headers_post,
            allow_redirects=True
        )
        
        # Verifica se foi bem-sucedido
        if post_response.status_code == 200:
            # Tenta encontrar o botão e clicar via JavaScript
            soup = BeautifulSoup(post_response.text, 'html.parser')
            
            # Procura por mensagens de sucesso
            success_messages = soup.find_all(['div', 'p', 'span'], 
                                           text=re.compile(r'(sucesso|success|enviado|obrigado|agradecimento)', re.I))
            
            if success_messages:
                mensagem_retorno = "Formulário enviado com sucesso!"
                status_envio = "SUCESSO"
            else:
                mensagem_retorno = "Formulário enviado (verifique se recebeu o email de confirmação)"
                status_envio = "ENVIADO"
            
            # Gerar arquivo de log
            nome_json, nome_txt, log_completo = gerar_arquivo_log(
                dados_para_log, 
                status_envio, 
                mensagem_retorno
            )
            
            return {
                "status": "sucesso",
                "departamento": departamento,
                "segmento": segmento,
                "mensagem": mensagem,
                "detalhe": mensagem_retorno,
                "log_json": nome_json,
                "log_txt": nome_txt,
                "log_completo": log_completo
            }
        else:
            # Mesmo com erro, gerar log
            dados_para_log = {
                'Nome': nome,
                'Email': email,
                'Telefone': telefone,
                'Empresa': empresa,
                'Departamento': departamento,
                'Segmento': segmento,
                'Mensagem': mensagem,
                'Token_CSRF': token if token else 'Não encontrado'
            }
            
            mensagem_erro = f"Erro {post_response.status_code}: {post_response.text[:200]}"
            nome_json, nome_txt, log_completo = gerar_arquivo_log(
                dados_para_log, 
                "ERRO", 
                mensagem_erro
            )
            
            return {
                "status": "erro",
                "mensagem_erro": mensagem_erro,
                "log_json": nome_json,
                "log_txt": nome_txt,
                "log_completo": log_completo
            }
            
    except requests.exceptions.RequestException as e:
        dados_para_log = {
            'Nome': nome,
            'Email': email,
            'Telefone': telefone,
            'Empresa': empresa,
            'Departamento': 'N/A',
            'Segmento': 'N/A',
            'Mensagem': 'N/A',
            'Token_CSRF': 'N/A'
        }
        mensagem_erro = f"Erro de conexão: {str(e)}"
        nome_json, nome_txt, log_completo = gerar_arquivo_log(
            dados_para_log, 
            "ERRO_CONEXAO", 
            mensagem_erro
        )
        
        return {
            "status": "erro",
            "mensagem_erro": mensagem_erro,
            "log_json": nome_json,
            "log_txt": nome_txt,
            "log_completo": log_completo
        }
    except Exception as e:
        mensagem_erro = f"Erro inesperado: {str(e)}"
        return {
            "status": "erro",
            "mensagem_erro": mensagem_erro
        }

def main():
    # Sidebar para configurações
    st.sidebar.header("⚙️ Configurações")
    
    # Inputs do usuário
    nome = st.sidebar.text_input("Nome:", value="Rodrigo Aiosa")
    email = st.sidebar.text_input("Email:", value="rodrigoaiosa@gmail.com")
    telefone = st.sidebar.text_input("Telefone:", value="11977019335")
    empresa = st.sidebar.text_input("Empresa:", value="Sky Data Soluction")
    
    # Botão para executar
    if st.sidebar.button("🚀 Executar Automação", type="primary", use_container_width=True):
        if not nome or not email or not telefone or not empresa:
            st.error("⚠️ Por favor, preencha todos os campos!")
        else:
            with st.spinner("Executando automação... Aguarde!"):
                # Executar automação via API
                resultado = preencher_formulario_api(nome, email, telefone, empresa)
                
                if resultado["status"] == "sucesso":
                    st.success("✅ Formulário enviado com sucesso!")
                    
                    # Mostrar detalhes do preenchimento
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("📋 Departamento Selecionado", resultado["departamento"])
                        st.metric("🏢 Segmento Selecionado", resultado["segmento"])
                        if "detalhe" in resultado:
                            st.info(f"ℹ️ {resultado['detalhe']}")
                    
                    with col2:
                        st.text_area("💬 Mensagem Enviada", resultado["mensagem"], height=150)
                    
                    # Mostrar informações do log
                    if "log_completo" in resultado:
                        st.markdown("---")
                        st.subheader("📄 Log de Envio")
                        
                        # Exibir o log formatado
                        log_data = resultado["log_completo"]
                        col_log1, col_log2 = st.columns(2)
                        with col_log1:
                            st.json(log_data)
                        
                        with col_log2:
                            st.info(f"📁 Arquivos gerados:")
                            if "log_json" in resultado:
                                st.code(f"✅ {resultado['log_json']}", language="bash")
                            if "log_txt" in resultado:
                                st.code(f"✅ {resultado['log_txt']}", language="bash")
                            
                            # Botão para download do log JSON
                            if "log_json" in resultado:
                                with open(resultado["log_json"], 'r', encoding='utf-8') as f:
                                    json_content = f.read()
                                st.download_button(
                                    label="📥 Baixar Log (JSON)",
                                    data=json_content,
                                    file_name=resultado["log_json"],
                                    mime="application/json"
                                )
                            
                            # Botão para download do log TXT
                            if "log_txt" in resultado:
                                with open(resultado["log_txt"], 'r', encoding='utf-8') as f:
                                    txt_content = f.read()
                                st.download_button(
                                    label="📥 Baixar Log (TXT)",
                                    data=txt_content,
                                    file_name=resultado["log_txt"],
                                    mime="text/plain"
                                )
                    
                    st.balloons()
                else:
                    st.error(f"❌ Erro ao enviar formulário: {resultado['mensagem_erro']}")
                    
                    # Mostrar log mesmo em caso de erro
                    if "log_completo" in resultado:
                        st.markdown("---")
                        st.subheader("📄 Log de Erro")
                        st.json(resultado["log_completo"])
                        
                        if "log_json" in resultado:
                            with open(resultado["log_json"], 'r', encoding='utf-8') as f:
                                json_content = f.read()
                            st.download_button(
                                label="📥 Baixar Log de Erro (JSON)",
                                data=json_content,
                                file_name=resultado["log_json"],
                                mime="application/json"
                            )
    
    # Botão para gerar uma frase aleatória
    st.sidebar.markdown("---")
    st.sidebar.subheader("📝 Gerador de Frases")
    if st.sidebar.button("🔄 Gerar Frase Aleatória"):
        frase = get_random_frase()
        st.sidebar.info(frase)
    
    # Informações adicionais
    st.sidebar.markdown("---")
    st.sidebar.info("""
    **Como funciona:**
    1. Preencha seus dados
    2. Clique em "Executar Automação"
    3. O sistema preencherá automaticamente o formulário
    4. Os campos 'Departamento' e 'Segmento' são sorteados aleatoriamente
    5. Um arquivo de log é gerado com todos os dados enviados
    """)
    
    # Área principal
    st.header("📊 Sobre a Automação")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🏷️ Total de Departamentos", "8", delta="opções")
    with col2:
        st.metric("🏢 Total de Segmentos", "12", delta="opções")
    with col3:
        st.metric("💬 Total de Frases", f"{len(FRASES_HABILIDADES)}", delta="variações")
    
    st.markdown("---")
    
    # Mostrar algumas frases de exemplo
    st.subheader("💡 Exemplos de Frases sobre Habilidades")
    with st.expander("Ver lista de frases"):
        for i, frase in enumerate(FRASES_HABILIDADES[:10], 1):
            st.write(f"{i}. {frase}")
        if len(FRASES_HABILIDADES) > 10:
            st.write(f"... e mais {len(FRASES_HABILIDADES) - 10} frases disponíveis")
    
    # Exemplo de log
    st.markdown("---")
    st.subheader("📋 Exemplo de Log Gerado")
    with st.expander("Ver exemplo do formato do log"):
        exemplo_log = {
            "data_hora_envio": "2024-01-15 14:30:25",
            "timestamp_unix": 1705339825,
            "status_envio": "SUCESSO",
            "mensagem_retorno": "Formulário enviado com sucesso!",
            "dados_enviados": {
                "Nome": "Rodrigo Aiosa",
                "Email": "rodrigoaiosa@gmail.com",
                "Telefone": "11977019335",
                "Empresa": "Sky Data Soluction",
                "Departamento": "Marketing",
                "Segmento": "Tecnologia da Informação",
                "Mensagem": "Profissional com expertise em Python para automação de processos...",
                "Token_CSRF": "abc123def456"
            }
        }
        st.json(exemplo_log)
    
    # Requisitos
    st.markdown("---")
    st.subheader("📦 Requisitos do Sistema")
    codigo_requisitos = """
    streamlit>=1.28.0
    requests>=2.31.0
    beautifulsoup4>=4.12.0
    lxml>=4.9.0
    """
    st.code(codigo_requisitos, language="bash")
    
    st.caption("Desenvolvido com ❤️ usando Python, Requests e Streamlit")

if __name__ == "__main__":
    main()
