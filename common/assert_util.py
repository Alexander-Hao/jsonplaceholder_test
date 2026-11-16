import json


class AssertUtil:

    @staticmethod
    def assert_status_code(resp, expected: int):
        #断言 HTTP 状态码
        assert resp.status_code == expected, (
            f"状态码断言失败: 期望 {expected}，实际 {resp.status_code}，"
            f"响应体: {resp.text[:500]}"
        )

    @staticmethod
    def assert_json_field(resp, field: str, expected=None):
        #断言 JSON 字段存在，可选校验其值
        data = resp.json()
        assert field in data, (
            f"响应中缺少字段 {field}，实际响应体: "
            f"{json.dumps(data, ensure_ascii=False)[:500]}"
        )
        if expected is not None:
            assert data[field] == expected, (
                f"字段 {field} 断言失败: 期望 {expected!r}，实际 {data[field]!r}"
            )

    @staticmethod
    def assert_list_length(resp, expected_len: int):
        #断言响应是列表且长度符合预期
        data = resp.json()
        assert isinstance(data, list), f"响应不是列表: {type(data).__name__}"
        assert len(data) == expected_len, (
            f"列表长度断言失败: 期望 {expected_len}，实际 {len(data)}"
        )

    @staticmethod
    def assert_all_items_match(resp, field: str, expected_value):
        #断言列表中每条记录指定字段都等于预期值
        data = resp.json()
        assert isinstance(data, list) and data, "响应应为非空列表"
        assert all(item.get(field) == expected_value for item in data), (
            f"列表中存在 {field} 不等于 {expected_value!r} 的记录"
        )
