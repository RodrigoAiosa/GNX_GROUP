# Arquivo de inicialização do módulo utils
from .form_handler import preencher_formulario_api
from .log_generator import gerar_arquivo_log_tabela
from .data_manager import (
    carregar_frases,
    carregar_departamentos,
    carregar_segmentos,
    get_random_frase,
    get_random_departamento,
    get_random_segmento
)

__all__ = [
    'preencher_formulario_api',
    'gerar_arquivo_log_tabela',
    'carregar_frases',
    'carregar_departamentos',
    'carregar_segmentos',
    'get_random_frase',
    'get_random_departamento',
    'get_random_segmento'
]
