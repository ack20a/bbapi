import logging

def setup_logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # 文件处理器 - 错误级别
        # error_file_handler = logging.FileHandler('error.log')
        # error_file_handler.setFormatter(formatter)
        # error_file_handler.setLevel(logging.ERROR)
        # logger.addHandler(error_file_handler)
    
    return logger