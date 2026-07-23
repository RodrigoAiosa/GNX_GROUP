from datetime import datetime
import os

def gerar_arquivo_log_tabela(dados_envio, status_envio, mensagem_retorno=""):
    """Gera um arquivo de log em formato de tabela com colunas"""
    data_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
    data_hora_formatada = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    nome_arquivo_txt = f"log_envio_{data_hora}.txt"
    
    # Garantir que o diretório logs existe
    os.makedirs('logs', exist_ok=True)
    
    caminho_completo = os.path.join('logs', nome_arquivo_txt)
    
    with open(caminho_completo, 'w', encoding='utf-8') as f:
        # Cabeçalho
        f.write("=" * 200 + "\n")
        f.write("LOG DE ENVIO DE FORMULÁRIO - GNX GROUP\n")
        f.write(f"Data/Hora do Envio: {data_hora_formatada}\n")
        f.write(f"Status: {status_envio}\n")
        if mensagem_retorno:
            f.write(f"Mensagem: {mensagem_retorno}\n")
        f.write("=" * 200 + "\n\n")
        
        # Cabeçalho das colunas
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
        linha_cabecalho = "|"
        for col in cabecalho:
            linha_cabecalho += f" {col:<30} |"
        f.write(linha_cabecalho + "\n")
        
        # Linha de separação
        linha_sep = "|"
        for _ in cabecalho:
            linha_sep += f"{'-' * 32}|"
        f.write(linha_sep + "\n")
        
        # Dados da tabela
        mensagem = dados_envio.get('Mensagem', '')
        if len(mensagem) > 28:
            mensagem = mensagem[:25] + "..."
        
        linha_dados = "|"
        linha_dados += f" {data_hora_formatada:<30} |"
        linha_dados += f" {status_envio:<30} |"
        linha_dados += f" {dados_envio.get('Nome', ''):<30} |"
        linha_dados += f" {dados_envio.get('Email', ''):<30} |"
        linha_dados += f" {dados_envio.get('Telefone', ''):<30} |"
        linha_dados += f" {dados_envio.get('Empresa', ''):<30} |"
        linha_dados += f" {dados_envio.get('Departamento', ''):<30} |"
        linha_dados += f" {dados_envio.get('Segmento', ''):<30} |"
        linha_dados += f" {mensagem:<30} |"
        f.write(linha_dados + "\n")
        
        # Linha de fechamento
        f.write(linha_sep + "\n\n")
        f.write("=" * 200 + "\n")
        f.write("FIM DO LOG\n")
        f.write("=" * 200 + "\n")
    
    return nome_arquivo_txt
