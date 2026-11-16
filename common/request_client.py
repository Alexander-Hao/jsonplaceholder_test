#requests 统一封装：自动记录请求/响应日志、超时控制、失败重试。

import time

import requests

from common.logger import log
from config.settings import TIMEOUT, RETRY_TIMES, RETRY_INTERVAL


class RequestClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    def _request(self, method: str, url: str, **kwargs):
        full_url = url if url.startswith("http") else self.base_url + url
        kwargs.setdefault("timeout", TIMEOUT)

        last_exc = None
        for attempt in range(1, RETRY_TIMES + 1):
            try:
                resp = self.session.request(method, full_url, **kwargs)
                log.info(
                    f"[{method}] {full_url} -> {resp.status_code} | "
                    f"耗时 {resp.elapsed.total_seconds():.2f}s"
                )
                if resp.status_code >= 400:
                    log.warning(f"响应体(前500字符): {resp.text[:500]}")
                else:
                    log.debug(f"响应体(前500字符): {resp.text[:500]}")
                return resp
            except (requests.ConnectionError, requests.Timeout) as exc:
                last_exc = exc
                log.warning(
                    f"第 {attempt} 次请求失败: {exc.__class__.__name__}，"
                    f"{RETRY_INTERVAL}s 后重试"
                )
                time.sleep(RETRY_INTERVAL)
        raise last_exc

    def get(self, url, params=None, headers=None):
        return self._request("GET", url, params=params, headers=headers)

    def post(self, url, json=None, headers=None):
        return self._request("POST", url, json=json, headers=headers)

    def put(self, url, json=None, headers=None):
        return self._request("PUT", url, json=json, headers=headers)

    def delete(self, url, headers=None):
        return self._request("DELETE", url, headers=headers)
