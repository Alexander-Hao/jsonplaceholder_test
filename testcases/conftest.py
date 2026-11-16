import pytest

from common.logger import log


@pytest.fixture(scope="session", autouse=True)
def session_setup():
    #整个测试会话开始 / 结束时输出关键日志
    log.info("=" * 60)
    log.info("接口自动化测试会话开始")
    log.info("=" * 60)
    yield
    log.info("=" * 60)
    log.info("接口自动化测试会话结束")
    log.info("=" * 60)


@pytest.fixture()
def request_logger():
    #每个用例的日志记录器：记录用例名称与入参，便于失败定位
    def _log(case_name, **kwargs):
        log.info(f"[用例] {case_name} | 入参: {kwargs or '无'}")
    return _log


def pytest_html_report_title(report):
    #自定义 HTML 报告标题
    report.title = "API 接口自动化测试报告"
