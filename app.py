import streamlit as st
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import os
import subprocess
import sys

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

def install_chrome():
    """Instala o Chrome no ambiente do Streamlit Cloud"""
    try:
        # Verifica se o Chrome já está instalado
        result = subprocess.run(['google-chrome', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            st.info("✅ Chrome já está instalado")
            return True
    except:
        pass
    
    try:
        st.info("📦 Instalando Chrome...")
        # Para sistemas Linux (Ubuntu/Debian)
        subprocess.run(['apt-get', 'update'], check=True, capture_output=True)
        subprocess.run(['apt-get', 'install', '-y', 'wget', 'unzip'], check=True, capture_output=True)
        
        # Baixa e instala o Chrome
        subprocess.run(['wget', '-q', 'https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb'], check=True)
        subprocess.run(['dpkg', '-i', 'google-chrome-stable_current_amd64.deb'], check=True, capture_output=True)
        subprocess.run(['apt-get', 'install', '-f', '-y'], check=True, capture_output=True)
        
        # Limpa o arquivo .deb
        subprocess.run(['rm', 'google-chrome-stable_current_amd64.deb'], check=True)
        
        st.success("✅ Chrome instalado com sucesso!")
        return True
    except Exception as e:
        st.error(f"❌ Erro ao instalar Chrome: {str(e)}")
        return False

def setup_driver():
    """Configura o driver do Chrome com opções para ambiente headless"""
    try:
        # Instala o Chrome se necessário
        if not install_chrome():
            return None
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-setuid-sandbox")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Tenta usar o ChromeDriver com webdriver-manager
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            return driver
        except:
            # Fallback: tenta usar o ChromeDriver do sistema
            service = Service('/usr/local/bin/chromedriver')
            driver = webdriver.Chrome(service=service, options=chrome_options)
            return driver
            
    except Exception as e:
        st.error(f"❌ Erro ao configurar driver: {str(e)}")
        return None

def preencher_formulario(driver, nome, email, telefone, empresa):
    """Preenche o formulário com os dados fornecidos"""
    try:
        # Abrir a página
        st.info("🌐 Acessando o site...")
        driver.get("https://gnxgroup.com.br/solucoes/temporarios/")
        time.sleep(5)
        
        # Aguardar o carregamento dos elementos
        wait = WebDriverWait(driver, 20)
        
        # Preencher Nome
        st.info("📝 Preenchendo nome...")
        nome_field = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='form-field-nome']")))
        nome_field.clear()
        nome_field.send_keys(nome)
        
        # Preencher Email
        st.info("📧 Preenchendo email...")
        email_field = driver.find_element(By.XPATH, "//*[@id='form-field-email']")
        email_field.clear()
        email_field.send_keys(email)
        
        # Preencher Telefone
        st.info("📱 Preenchendo telefone...")
        telefone_field = driver.find_element(By.XPATH, "//*[@id='form-field-telefone']")
        telefone_field.clear()
        telefone_field.send_keys(telefone)
        
        # Preencher Empresa
        st.info("🏢 Preenchendo empresa...")
        empresa_field = driver.find_element(By.XPATH, "//*[@id='form-field-empresa']")
        empresa_field.clear()
        empresa_field.send_keys(empresa)
        
        # Selecionar Departamento (sorteio)
        st.info("🎲 Selecionando departamento...")
        departamento = get_random_departamento()
        departamento_select = driver.find_element(By.XPATH, "//*[@id='form-field-departamento']")
        for option in departamento_select.find_elements(By.TAG_NAME, "option"):
            if option.text == departamento:
                option.click()
                break
        
        # Selecionar Segmento (sorteio)
        st.info("🎲 Selecionando segmento...")
        segmento = get_random_segmento()
        segmento_select = driver.find_element(By.XPATH, "//*[@id='form-field-segmento']")
        for option in segmento_select.find_elements(By.TAG_NAME, "option"):
            if option.text == segmento:
                option.click()
                break
        
        # Preencher Mensagem com frase aleatória
        st.info("💬 Gerando mensagem...")
        mensagem = get_random_frase()
        mensagem_field = driver.find_element(By.XPATH, "//*[@id='form-field-mensagem_profissional']")
        mensagem_field.clear()
        mensagem_field.send_keys(mensagem)
        
        # Tentar enviar o formulário (opcional)
        try:
            st.info("📤 Enviando formulário...")
            submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
            submit_button.click()
            time.sleep(3)
        except:
            st.warning("⚠️ Não foi possível enviar o formulário automaticamente")
        
        return {
            "status": "sucesso",
            "departamento": departamento,
            "segmento": segmento,
            "mensagem": mensagem
        }
        
    except Exception as e:
        return {
            "status": "erro",
            "mensagem_erro": str(e)
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
                try:
                    # Configurar driver
                    driver = setup_driver()
                    
                    if driver is None:
                        st.error("❌ Não foi possível iniciar o driver. Verifique a instalação do Chrome.")
                    else:
                        # Executar automação
                        resultado = preencher_formulario(driver, nome, email, telefone, empresa)
                        
                        driver.quit()
                        
                        if resultado["status"] == "sucesso":
                            st.success("✅ Formulário preenchido com sucesso!")
                            
                            # Mostrar detalhes do preenchimento
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("📋 Departamento Selecionado", resultado["departamento"])
                                st.metric("🏢 Segmento Selecionado", resultado["segmento"])
                            
                            with col2:
                                st.text_area("💬 Mensagem Enviada", resultado["mensagem"], height=150)
                            
                            st.balloons()
                        else:
                            st.error(f"❌ Erro ao preencher o formulário: {resultado['mensagem_erro']}")
                        
                except Exception as e:
                    st.error(f"❌ Erro durante a execução: {str(e)}")
    
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
    
    # Requisitos
    st.markdown("---")
    st.subheader("📦 Requisitos do Sistema")
    codigo_requisitos = """
    streamlit>=1.28.0
    selenium>=4.15.0
    webdriver-manager>=4.0.1
    pandas>=2.1.3
    """
    st.code(codigo_requisitos, language="bash")
    
    st.caption("Desenvolvido com ❤️ usando Python, Selenium e Streamlit")

if __name__ == "__main__":
    main()
