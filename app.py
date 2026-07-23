import streamlit as st
from utils.form_handler import preencher_formulario_api, preencher_formulario_selenium
from utils.data_manager import (
    carregar_frases,
    carregar_departamentos,
    carregar_segmentos,
    get_random_frase,
    get_random_departamento,
    get_random_segmento
)
from datetime import datetime
import os
import time

# Configuração da página
st.set_page_config(
    page_title="Automação GNX Group",
    page_icon="🤖",
    layout="wide"
)

# Carregar CSS personalizado
def load_css():
    try:
        with open('static/style.css', 'r', encoding='utf-8') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except:
        pass

# Carregar CSS
load_css()

# Título do app
st.title("🤖 Automação de Formulário - GNX Group")
st.markdown("---")

# Inicializar dados
frases = carregar_frases()
departamentos = carregar_departamentos()
segmentos = carregar_segmentos()

def main():
    # Sidebar para configurações
    st.sidebar.header("⚙️ Configurações")
    
    # Inputs do usuário
    nome = st.sidebar.text_input("Nome:", value="Rodrigo Aiosa")
    email = st.sidebar.text_input("Email:", value="rodrigoaiosa@gmail.com")
    telefone = st.sidebar.text_input("Telefone:", value="11977019335")
    empresa = st.sidebar.text_input("Empresa:", value="Sky Data Solution")
    
    # Configurações de execução
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔄 Configurações de Execução")
    
    # Número de vezes para executar
    num_execucoes = st.sidebar.number_input(
        "Número de execuções:",
        min_value=1,
        max_value=100,
        value=1,
        step=1,
        help="Quantas vezes o formulário será preenchido"
    )
    
    # Modo de visualização
    st.sidebar.subheader("👁️ Modo de Visualização")
    modo_visualizacao = st.sidebar.radio(
        "Selecione o modo:",
        ["📡 API (rápido, sem navegador)", "🌐 Navegador (ver preenchimento)"],
        index=0,
        help="API: mais rápido, sem abrir navegador. Navegador: mostra o preenchimento em tempo real"
    )
    
    # Tempo entre execuções
    if num_execucoes > 1:
        tempo_entre = st.sidebar.slider(
            "Tempo entre execuções (segundos):",
            min_value=1,
            max_value=30,
            value=5,
            step=1,
            help="Aguardar este tempo entre cada execução"
        )
    else:
        tempo_entre = 0
    
    # Botão para executar
    if st.sidebar.button("🚀 Executar Automação", type="primary", use_container_width=True):
        if not nome or not email or not telefone or not empresa:
            st.error("⚠️ Por favor, preencha todos os campos!")
        else:
            # Verificar se é modo navegador
            usar_selenium = "Navegador" in modo_visualizacao
            
            if usar_selenium:
                # Verificar se o Chrome está disponível
                try:
                    from selenium import webdriver
                    from selenium.webdriver.chrome.options import Options
                    st.info("🌐 Modo navegador selecionado - O Chrome será aberto para visualização")
                except ImportError:
                    st.error("❌ Selenium não está instalado. Execute: pip install selenium webdriver-manager")
                    st.stop()
            
            # Container para os resultados
            resultados_container = st.container()
            
            with resultados_container:
                st.subheader(f"📊 Executando {num_execucoes} vez(es)...")
                
                # Barra de progresso
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Lista para armazenar todos os logs
                todos_logs = []
                execucoes_sucesso = 0
                execucoes_erro = 0
                
                for i in range(num_execucoes):
                    status_text.text(f"🔄 Execução {i+1} de {num_execucoes}")
                    
                    # Selecionar valores aleatórios
                    departamento = get_random_departamento(departamentos)
                    segmento = get_random_segmento(segmentos)
                    mensagem = get_random_frase(frases)
                    
                    try:
                        if usar_selenium:
                            # Modo com Selenium (visual)
                            resultado = preencher_formulario_selenium(
                                nome, 
                                email, 
                                telefone, 
                                empresa,
                                departamento,
                                segmento,
                                mensagem
                            )
                        else:
                            # Modo API (rápido)
                            resultado = preencher_formulario_api(
                                nome, 
                                email, 
                                telefone, 
                                empresa,
                                departamento,
                                segmento,
                                mensagem
                            )
                        
                        if resultado["status"] == "sucesso":
                            execucoes_sucesso += 1
                            if "log_txt" in resultado:
                                log_path = os.path.join('logs', resultado["log_txt"])
                                if os.path.exists(log_path):
                                    with open(log_path, 'r', encoding='utf-8') as f:
                                        log_content = f.read()
                                    todos_logs.append({
                                        "execucao": i+1,
                                        "status": "✅ SUCESSO",
                                        "departamento": departamento,
                                        "segmento": segmento,
                                        "log": log_content
                                    })
                            
                            # Mostrar no log de execução
                            with st.expander(f"📋 Execução {i+1} - SUCESSO", expanded=(i==0)):
                                st.success(f"✅ Formulário enviado com sucesso!")
                                st.write(f"**Departamento:** {departamento}")
                                st.write(f"**Segmento:** {segmento}")
                                st.write(f"**Mensagem:** {mensagem[:100]}...")
                        else:
                            execucoes_erro += 1
                            with st.expander(f"❌ Execução {i+1} - ERRO", expanded=(i==0)):
                                st.error(f"❌ Erro: {resultado.get('mensagem_erro', 'Erro desconhecido')}")
                    
                    except Exception as e:
                        execucoes_erro += 1
                        with st.expander(f"❌ Execução {i+1} - ERRO", expanded=(i==0)):
                            st.error(f"❌ Erro inesperado: {str(e)}")
                    
                    # Atualizar barra de progresso
                    progress_bar.progress((i + 1) / num_execucoes)
                    
                    # Aguardar entre execuções
                    if i < num_execucoes - 1 and tempo_entre > 0:
                        status_text.text(f"⏳ Aguardando {tempo_entre} segundos para próxima execução...")
                        time.sleep(tempo_entre)
                
                # Resumo final
                status_text.text("✅ Execuções concluídas!")
                
                st.markdown("---")
                st.subheader("📊 Resumo das Execuções")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("📦 Total de Execuções", num_execucoes)
                with col2:
                    st.metric("✅ Sucessos", execucoes_sucesso, delta=f"{execucoes_sucesso/num_execucoes*100:.0f}%")
                with col3:
                    st.metric("❌ Erros", execucoes_erro, delta=f"{execucoes_erro/num_execucoes*100:.0f}%")
                
                # Gerar arquivo consolidado com todos os logs
                if todos_logs and num_execucoes > 1:
                    st.markdown("---")
                    st.subheader("📄 Log Consolidado")
                    
                    # Gerar arquivo consolidado
                    data_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
                    nome_consolidado = f"log_consolidado_{data_hora}.log"
                    
                    with open(nome_consolidado, 'w', encoding='utf-8') as f:
                        # Cabeçalho
                        f.write("Data/Hora do Envio;Status;Nome;Email;Telefone;Empresa;Departamento;Segmento;Mensagem\n")
                        
                        # Para cada execução, adicionar uma linha
                        for log_info in todos_logs:
                            # Extrair dados do log
                            linhas = log_info["log"].strip().split('\n')
                            if len(linhas) > 1:
                                # Pular cabeçalho e pegar dados
                                dados_linha = linhas[1] if len(linhas) > 1 else ""
                                f.write(dados_linha + "\n")
                    
                    with open(nome_consolidado, 'r', encoding='utf-8') as f:
                        conteudo_consolidado = f.read()
                    
                    st.download_button(
                        label="📥 Baixar Log Consolidado (Todas as execuções)",
                        data=conteudo_consolidado,
                        file_name=nome_consolidado,
                        mime="text/plain",
                        use_container_width=True
                    )
                    
                    # Mostrar prévia
                    with st.expander("📋 Prévia do Log Consolidado"):
                        st.code(conteudo_consolidado[:500] + ("..." if len(conteudo_consolidado) > 500 else ""))
                
                st.balloons()
    
    # Botão para gerar uma frase aleatória
    st.sidebar.markdown("---")
    st.sidebar.subheader("📝 Gerador de Frases")
    if st.sidebar.button("🔄 Gerar Frase Aleatória"):
        frase = get_random_frase(frases)
        st.sidebar.info(frase)
    
    # Informações adicionais
    st.sidebar.markdown("---")
    st.sidebar.info("""
    **Como funciona:**
    1. Preencha seus dados
    2. Configure o número de execuções
    3. Escolha o modo (API ou Navegador)
    4. Clique em "Executar Automação"
    5. Acompanhe o progresso em tempo real
    """)
    
    # Estatísticas
    st.header("📊 Sobre a Automação")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🏷️ Total de Departamentos", len(departamentos), delta="opções")
    with col2:
        st.metric("🏢 Total de Segmentos", len(segmentos), delta="opções")
    with col3:
        st.metric("💬 Total de Frases", len(frases), delta="variações")
    
    st.caption("Desenvolvido com ❤️ usando Python, Requests e Streamlit")

if __name__ == "__main__":
    # Criar diretórios necessários
    os.makedirs('logs', exist_ok=True)
    main()
