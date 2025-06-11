import logging
import os


log_dir = "logs"
log_filename = os.path.join(log_dir, "tracing.log")


def setup_logger(job_id: str) -> logging.Logger:

    # Create the logs directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)

    # Create a logger instance
    logger = logging.getLogger(job_id)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # Create a file handler to write logs to a file
        file_handler = logging.FileHandler(log_filename, encoding='utf-8')
        file_handler.setLevel(logging.INFO)

        # file_handler.stream = open(file_handler.stream.fileno(), mode='w', encoding='utf-8', closefd=False)

        # Create a formatter and set it for the file handler
        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s', datefmt='%m-%d %H:%M:%S')
        file_handler.setFormatter(formatter)

        # Add the file handler to the logger
        logger.addHandler(file_handler)
    return logger
