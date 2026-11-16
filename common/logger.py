#日志封装：控制台 + 滚动文件双输出，便于失败用例定位
import logging
from logging.handlers import RotatingFileHandler

from config.settings import LOG_DIR, LOG_FILE

LOG_DIR.mkdir(parents=True, exist_ok=True)


def get_logger(name="api_test") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:          # 防止重复添加 handler
        return logger
    logger.setLevel(logging.DEBUG)

    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(message)s"
    )

    # 控制台输出（INFO 及以上）
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(fmt)

    # 滚动文件输出（单文件 5MB，保留 3 个备份）
    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(fmt)

    logger.addHandler(console)
    logger.addHandler(file_handler)
    return logger


log = get_logger()
