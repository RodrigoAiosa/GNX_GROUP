import random
import os

def carregar_frases():
    """Carrega as frases do arquivo frases.txt"""
    try:
        with open('data/frases.txt', 'r', encoding='utf-8') as f:
            frases = [linha.strip() for linha in f if linha.strip()]
        return frases
    except FileNotFoundError:
        # Arquivo não encontrado, usar lista padrão
        return [
            "Profissional com expertise em Python para automação de processos e análise de dados.",
            "Especialista em SQL com capacidade de extrair, manipular e analisar grandes volumes de dados.",
            "Domínio avançado em Power BI para criação de dashboards interativos e relatórios gerenciais.",
            "Ampla experiência em Excel, incluindo fórmulas avançadas, macros e VBA.",
            "Especialista em automação de processos com Python, reduzindo tempo de execução de tarefas.",
            "Profissional de Business Intelligence com foco em transformar dados em insights acionáveis.",
            "Experiência em integração de sistemas utilizando Python e APIs para automação de fluxos.",
            "Criação de soluções em Power BI que facilitam a visualização e monitoramento de KPIs.",
            "Especialista em otimização de bancos de dados SQL, garantindo performance e integridade.",
            "Desenvolvimento de automações em Python para web scraping e processamento de dados.",
            "Habilidade em criar modelos preditivos utilizando Python, Pandas e NumPy.",
            "Criação de relatórios automatizados em Excel com VBA, reduzindo erros manuais.",
            "Experiência em implementação de soluções de BI com Power BI e SQL.",
            "Especialista em automação de e-mails e relatórios com Python.",
            "Desenvolvimento de dashboards em Power BI com atualização automática.",
            "Profissional com forte capacidade analítica e resolução de problemas complexos.",
            "Automação de planilhas Excel com Python para processamento massivo de dados.",
            "Criação de pipelines de dados usando SQL e Python para ETL.",
            "Especialista em visualização de dados com Power BI.",
            "Combinação de habilidades em Python, SQL, Power BI e Excel."
        ]

def carregar_departamentos():
    """Carrega os departamentos do arquivo departamentos.txt"""
    try:
        with open('data/departamentos.txt', 'r', encoding='utf-8') as f:
            departamentos = [linha.strip() for linha in f if linha.strip()]
        return departamentos
    except FileNotFoundError:
        return [
            "Recursos Humanos (RH)",
            "Compras ou Suprimentos",
            "Gerência Executiva",
            "Marketing",
            "Vendas",
            "Trade Marketing",
            "Desenvolvimento de Negócios",
            "Outros"
        ]

def carregar_segmentos():
    """Carrega os segmentos do arquivo segmentos.txt"""
    try:
        with open('data/segmentos.txt', 'r', encoding='utf-8') as f:
            segmentos = [linha.strip() for linha in f if linha.strip()]
        return segmentos
    except FileNotFoundError:
        return [
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

def get_random_frase(frases):
    """Retorna uma frase aleatória"""
    return random.choice(frases) if frases else ""

def get_random_departamento(departamentos):
    """Retorna um departamento aleatório"""
    return random.choice(departamentos) if departamentos else ""

def get_random_segmento(segmentos):
    """Retorna um segmento aleatório"""
    return random.choice(segmentos) if segmentos else ""
