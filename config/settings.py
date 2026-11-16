#全局配置：环境地址、超时、重试策略、报告/日志路径
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

BASE_URL = "https://jsonplaceholder.typicode.com"

# 请求超时（秒）
TIMEOUT = 10

# 失败重试策略：网络抖动时自动重试
RETRY_TIMES = 2
RETRY_INTERVAL = 0.5

# 输出目录
REPORT_DIR = BASE_DIR / "reports"
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "api_test.log"
