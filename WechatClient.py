from werobot.client import Client


class WechatClient(Client):
    def __init__(self, config):
        super(WechatClient, self).__init__(config)

    # 微信新建草稿箱
    def create_draft(self, articles):
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/draft/add",
            data={"articles": articles}
        )

    # 微信发布草稿箱
    def publish_draft(self, media_id):
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/freepublish/submit",
            data={"media_id": media_id}
        )
    # 获取发布列表

    def get_publish_list(self, offset, count, no_content=0):
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/freepublish/batchget",
            data={"offset": offset, "count": count, "no_content": no_content}
        )
