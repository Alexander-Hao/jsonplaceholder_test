#用户模块接口封装（对应被测系统 /users 资源：查询/新增/更新/删除）
from api.base_api import BaseAPI


class UserAPI(BaseAPI):
    #用户模块接口操作集合

    def get_users(self, **params):
        #查询用户列表，支持过滤参数
        return self.client.get("/users", params=params or None)

    def get_user(self, user_id):
        #查询单个用户详情
        return self.client.get(f"/users/{user_id}")

    def create_user(self, payload):
        #新增用户 
        return self.client.post("/users", json=payload)

    def update_user(self, user_id, payload):
        #更新用户信息
        return self.client.put(f"/users/{user_id}", json=payload)

    def delete_user(self, user_id):
        #删除用户
        return self.client.delete(f"/users/{user_id}")


user_api = UserAPI()
