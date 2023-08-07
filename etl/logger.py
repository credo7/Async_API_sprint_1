import logging
from logging.handlers import RotatingFileHandler

from etl.config import LOG_LEVEL

# Set up the logger
logger = logging.getLogger('etl_application')
logger.setLevel(LOG_LEVEL)

# INFO-level handler
fh = RotatingFileHandler('logs/etl_logs.log')
formatter = logging.Formatter(
    '%(asctime)s %(levelname)-4s [%(filename)s:%(lineno)s]  %(message)s'
)
fh.setFormatter(formatter)
logger.addHandler(fh)

# ERROR-level handler
fh_error = RotatingFileHandler('logs/etl_errors.log')
formatter_error = logging.Formatter(
    '%(asctime)s %(levelname)-4s [%(filename)s:%(lineno)s]  %(message)s'
)
fh_error.setFormatter(formatter_error)
fh_error.setLevel(LOG_LEVEL)
logger.addHandler(fh_error)
