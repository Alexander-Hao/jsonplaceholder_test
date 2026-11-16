#一键运行入口：执行全部用例并生成 HTML 报告
import subprocess
import sys

if __name__ == "__main__":
    sys.exit(subprocess.call([sys.executable, "-m", "pytest"]))
