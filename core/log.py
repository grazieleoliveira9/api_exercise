
import logging
import sys
from pathlib import Path

def setup_logger(name=__name__):
    """Configura e retorna um logger"""
    
    # Criar diretório de logs
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configurar formato
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Criar logger
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    
    # Handler para arquivo
    file_handler = logging.FileHandler(log_dir / 'app.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    # Handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # Adicionar handlers se não existirem
    if not log.handlers:
        log.addHandler(file_handler)
        log.addHandler(console_handler)
    
    return log

# Logger global padrão
log = setup_logger()