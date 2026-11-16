from api.base_api import BaseAPI


class PostAPI(BaseAPI):
    #帖子模块接口操作集合

    def get_posts(self, **params):
        #查询帖子列表，支持过滤参数
        return self.client.get("/posts", params=params or None)

    def get_post(self, post_id):
        #查询帖子详情
        return self.client.get(f"/posts/{post_id}")

    def create_post(self, payload):
        #发布帖子
        return self.client.post("/posts", json=payload)

    def update_post(self, post_id, payload):
        #更新帖子
        return self.client.put(f"/posts/{post_id}", json=payload)

    def delete_post(self, post_id):
        #删除帖子
        return self.client.delete(f"/posts/{post_id}")


post_api = PostAPI()
