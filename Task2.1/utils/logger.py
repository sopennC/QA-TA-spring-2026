import logging

import allure


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
    return logger


def log_response(response, logger: logging.Logger | None = None):
    msg = f"{response.request.method} {response.url} {response.status_code}\nBody: {response.text[:500]}"
    if logger:
        logger.debug(msg)
    allure.attach(msg, name="Response", attachment_type=allure.attachment_type.TEXT)
