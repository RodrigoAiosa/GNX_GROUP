import streamlit as st
from utils.form_handler import preencher_formulario_api
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
    
    # Botão para executar
    if st.sidebar.button("🚀 Executar Automação", type="primary", use_container_width=True):
        if not nome or not email or not telefone or not empresa:
            st.error("⚠️ Por favor, preencha todos os campos!")
        else:
            with st.spinner("Executando automação... Aguarde!"):
                # Selecionar valores aleatórios
                departamento = get_random_departamento(departamentos)
                segmento = get_random_segmento(segmentos)
                mensagem = get_random_frase(frases)
                
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
                    
                    # Mostrar dados enviados
                    st.markdown("---")
                    st.subheader("📋 Dados Enviados")
                    
                    dados_exibicao = {
                        "Nome": nome,
                        "Email": email,
                        "Telefone": telefone,
                        "Empresa": empresa,
                        "Departamento": resultado["departamento"],
                        "Segmento": resultado["segmento"],
                        "Mensagem": resultado["mensagem"]
                    }
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Nome:** {dados_exibicao['Nome']}")
                        st.write(f"**Email:** {dados_exibicao['Email']}")
                        st.write(f"**Telefone:** {dados_exibicao['Telefone']}")
                        st.write(f"**Empresa:** {dados_exibicao['Empresa']}")
                    with col2:
                        st.write(f"**Departamento:** {dados_exibicao['Departamento']}")
                        st.write(f"**Segmento:** {dados_exibicao['Segmento']}")
                        st.write(f"**Mensagem:** {dados_exibicao['Mensagem'][:100]}...")
                    
                    # Botão para download do log
                    if "log_txt" in resultado:
                        st.markdown("---")
                        log_path = os.path.join('logs', resultado["log_txt"])
                        
                        if os.path.exists(log_path):
                            with open(log_path, 'r', encoding='utf-8') as f:
                                txt_content = f.read()
                            
                            st.text_area("📄 Prévia do Log (CSV com ;)", txt_content, height=150)
                            
                            st.download_button(
                                label="📥 Baixar Log (CSV com ;)",
                                data=txt_content,
                                file_name=resultado["log_txt"],
                                mime="text/plain",
                                use_container_width=True
                            )
                    
                    st.balloons()
                else:
                    st.error(f"❌ Erro ao enviar formulário: {resultado['mensagem_erro']}")
                    
                    if "log_txt" in resultado:
                        st.markdown("---")
                        st.subheader("📄 Log de Erro")
                        log_path = os.path.join('logs', resultado["log_txt"])
                        
                        if os.path.exists(log_path):
                            with open(log_path, 'r', encoding='utf-8') as f:
                                txt_content = f.read()
                            st.text_area("Conteúdo do Log", txt_content, height=150)
                            
                            st.download_button(
                                label="📥 Baixar Log de Erro",
                                data=txt_content,
                                file_name=resultado["log_txt"],
                                mime="text/plain",
                                use_container_width=True
                            )
    
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
    2. Clique em "Executar Automação"
    3. O sistema preencherá automaticamente o formulário
    4. Os campos 'Departamento' e 'Segmento' são sorteados aleatoriamente
    5. Um arquivo .log é gerado com colunas separadas por ;
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
