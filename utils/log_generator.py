from datetime import datetime
import os

def gerar_arquivo_log_tabela(dados_envio, status_envio, mensagem_retorno=""):
    """Gera um arquivo de log com colunas separadas por ;"""
    data_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
    data_hora_formatada = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    nome_arquivo_txt = f"log_envio_{data_hora}.log"
    
    # Garantir que o diretório logs existe
    os.makedirs('logs', exist_ok=True)
    
    caminho_completo = os.path.join('logs', nome_arquivo_txt)
    
    with open(caminho_completo, 'w', encoding='utf-8') as f:
        # Cabeçalho com separador ;
        cabecalho = [
            "Data/Hora do Envio",
            "Status",
            "Nome",
            "Email",
            "Telefone",
            "Empresa",
            "Departamento",
            "Segmento",
            "Mensagem"
        ]
        
        # Escrever cabeçalho
        f.write(";".join(cabecalho) + "\n")
        
        # Dados da tabela
        mensagem = dados_envio.get('Mensagem', '')
        # Limpar quebras de linha e caracteres especiais
        mensagem = mensagem.replace('\n', ' ').replace('\r', ' ')
        # Truncar se for muito longa (opcional)
        if len(mensagem) > 100:
            mensagem = mensagem[:97] + "..."
        
        linha_dados = [
            data_hora_formatada,
            status_envio,
            dados_envio.get('Nome', ''),
            dados_envio.get('Email', ''),
            dados_envio.get('Telefone', ''),
            dados_envio.get('Empresa', ''),
            dados_envio.get('Departamento', ''),
            dados_envio.get('Segmento', ''),
            mensagem
        ]
        
        f.write(";".join(linha_dados) + "\n")
    
    return nome_arquivo_txt
