import logging


def get_logger(name: str):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.propagate = 0
        logger.addHandler(_stream_handler)
    return logger


_formatter = logging.Formatter("%(levelname)s:%(asctime)s:%(name)s:%(message)s")

_stream_handler = logging.StreamHandler()
_stream_handler.setFormatter(_formatter)

if not __debug__:
    logging.disable()
