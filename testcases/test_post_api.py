#帖子模块接口自动化测试用例（含 YAML 数据驱动）
from pathlib import Path

import pytest
import yaml

from api.post_api import post_api
from common.assert_util import AssertUtil as A

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "posts.yaml"


def load_post_cases():
    #从 YAML 数据文件读取参数化用例（数据与代码分离）
    with open(DATA_FILE, encoding="utf-8") as f:
        return yaml.safe_load(f)["get_post_cases"]


class TestPostAPI:
    #帖子模块：列表过滤 / 详情查询 / 新增 / 更新 / 删除#

    def test_get_posts_filter_by_user(self):
        #按 userId 过滤帖子：结果全部属于该用户
        resp = post_api.get_posts(userId=1)
        A.assert_status_code(resp, 200)
        A.assert_all_items_match(resp, "userId", 1)

    @pytest.mark.smoke
    def test_get_post_detail(self):
        #查询帖子详情：返回 200，标题非空
        resp = post_api.get_post(1)
        A.assert_status_code(resp, 200)
        A.assert_json_field(resp, "title")
        assert resp.json()["title"], "帖子标题为空"

    @pytest.mark.parametrize(
        "case", load_post_cases(), ids=lambda c: c["id"]
    )
    def test_get_post_by_id_parametrized(self, case):
        #数据驱动：按 YAML 用例批量查询帖子详情（含 404 场景）#
        resp = post_api.get_post(case["post_id"])
        A.assert_status_code(resp, case["expected_status"])
        if case["expected_status"] == 200:
            A.assert_json_field(resp, "id", case["post_id"])

    def test_create_post(self):
        #发布帖子：返回 201，id 由服务端生成#
        payload = {"title": "接口自动化测试", "body": "pytest + requests 数据驱动", "userId": 1}
        resp = post_api.create_post(payload)
        A.assert_status_code(resp, 201)
        A.assert_json_field(resp, "id")

    def test_update_post(self):
        #更新帖子：返回 200，title 被更新#
        resp = post_api.update_post(1, {"title": "新标题", "userId": 1})
        A.assert_status_code(resp, 200)
        A.assert_json_field(resp, "title", "新标题")

    def test_delete_post(self):
        #删除帖子：返回 200#
        resp = post_api.delete_post(1)
        A.assert_status_code(resp, 200)
