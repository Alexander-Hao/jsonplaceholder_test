#用户模块接口自动化测试用例
import pytest

from api.user_api import user_api
from common.assert_util import AssertUtil as A


class TestUserAPI:
    #用户模块：列表查询 / 详情查询 / 新增 / 更新 / 删除

    @pytest.mark.smoke
    def test_get_users_list(self, request_logger):
        #查询用户列表：返回 200，默认返回 10 条记录
        request_logger("查询用户列表")
        resp = user_api.get_users()
        A.assert_status_code(resp, 200)
        A.assert_list_length(resp, 10)

    @pytest.mark.smoke
    def test_get_user_detail(self):
        #查询用户详情：返回 200，name 非空且 id 正确
        resp = user_api.get_user(1)
        A.assert_status_code(resp, 200)
        A.assert_json_field(resp, "id", 1)
        A.assert_json_field(resp, "name")

    def test_get_user_not_found(self):
        #查询不存在的用户：返回 404
        resp = user_api.get_user(99999)
        A.assert_status_code(resp, 404)

    @pytest.mark.parametrize(
        "user_id,expected_name",
        [
            (1, "Leanne Graham"),
            (2, "Ervin Howell"),
        ],
        ids=["user_id_1", "user_id_2"],
    )
    def test_get_user_parametrized(self, user_id, expected_name):
        #数据驱动：一次运行批量校验不同用户的姓名
        resp = user_api.get_user(user_id)
        A.assert_status_code(resp, 200)
        A.assert_json_field(resp, "name", expected_name)

    def test_create_user(self):
        #新增用户：返回 201，服务端生成 id
        payload = {"name": "Test User", "username": "tester", "email": "tester@example.com"}
        resp = user_api.create_user(payload)
        A.assert_status_code(resp, 201)
        A.assert_json_field(resp, "id")

    def test_update_user(self):
        #更新用户：返回 200，name 字段被更新
        resp = user_api.update_user(1, {"name": "Updated Name"})
        A.assert_status_code(resp, 200)
        A.assert_json_field(resp, "name", "Updated Name")

    def test_delete_user(self):
        #删除用户：返回 200
        resp = user_api.delete_user(1)
        A.assert_status_code(resp, 200)
