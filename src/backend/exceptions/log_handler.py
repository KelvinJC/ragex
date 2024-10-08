import logging
from pathlib import Path


current_working_directory = Path.cwd()

def setup_logger(logger_name: str, log_file: str, log_level: int = logging.INFO) -> logging.Logger:
    """
    This function allows the system to create and write log data of the 
    system's operations.
    Args:
        logger_name (str): name of the log file to create
        log_file (str): the file path to the log file
        log_level (int): the value of the log type (debug, info, debug)
    """
    # create a log from a specified logger name
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(format)
    
    logger.addHandler(file_handler)
    return logger


def create_directory_and_log_file(dir_name: str, filename: str) -> Path:
    """
    this function creates a directory and a corresponding log file in it
    Args:
        dir_name (str): name of the directory
        file_name (str): name of the log file
    """
    new_path = current_working_directory.joinpath(dir_name)
    # create the directory path only once by checking if it exists
    new_path.mkdir(exist_ok=True)
    log_file_path = new_path.joinpath(filename)
    log_file_path.touch()

dir = "logs"
log_files = ["system.log", "user_ops.log", "llm_response.log" ]


for file in log_files:
    create_directory_and_log_file(dir, file)

system_logger = setup_logger('SystemLogger', f"{current_working_directory}/logs/system.log")
user_ops_logger = setup_logger('UserLogger', f"{current_working_directory}/logs/user_ops.log")
llm_response_logger = setup_logger('LLMResponse', f"{current_working_directory}/logs/llm_response.log")