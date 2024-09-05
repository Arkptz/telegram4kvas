import logging
from logging.handlers import RotatingFileHandler
import colorlog

logging.root.setLevel(logging.DEBUG)

# handler = RotatingFileHandler(
#     filename="/opt/etc/telegram4kvas/telegram4kvas_log.txt",
#     maxBytes=1 * 1024 * 1024,
#     backupCount=3,
#     encoding="UTF-8",
# )
color_log_format = "[%(asctime)s] [%(levelname)s] [%(funcName)s():%(lineno)s] [%(name)s] %(log_color)s %(message)s"
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
color_formatter = colorlog.ColoredFormatter(color_log_format, "%d/%m/%Y %H:%M:%S")
# handler.setFormatter(formatter)
# logging.root.addHandler(handler)
console_handler = colorlog.StreamHandler()
console_handler.setFormatter(color_formatter)
console_handler.setLevel(logging.INFO)
logging.root.addHandler(console_handler)
