import os
import json
from tornado import web
from tornado import httpserver
from tornado import ioloop

global identify_config

class IdentifyHandler(web.RequestHandler):
    def get(self):
        request_body = self.request.body_arguments
        print(request_body)
        # request_body = json.loads(body)

        one_page = self.get_argument("one_page", 10)
        # page_no = self.get_argument("page_no", 0)
        print(one_page)
        root_path = identify_config["source_path"]
        img_list = []
        count = 0
        for img_file in os.listdir(root_path):
            if count == int(one_page):
                break
            img_path = root_path + img_file
            print(img_path)
            if "_" in img_file:
                continue
            img_list.append(img_path)
            count += 1

        # img_list = ["static/huaxi_captcha/157855723366602.jpg"]
        self.render("index.html", img_list=img_list, one_page=one_page, char_length=identify_config["count"])

    def post(self):
        img0 = self.get_argument("img0", "1")
        body = self.request.body
        print(body, img0)
        request_body = json.loads(body)
        print(request_body)

if __name__ == '__main__':
    with open("../conf/identify_config.json", "r") as f:
        identify_config = json.load(f)

    app = web.Application(handlers=[
        (r"/get", IdentifyHandler),
        (r"/submit", IdentifyHandler)
    ],
    template_path="templates",
    static_path="static")
    server = httpserver.HTTPServer(app)
    server.listen(9000)
    print("start on ", 9000)
    ioloop.IOLoop.current().start()
    # app.listen(address="0.0.0.0", port=9000)
