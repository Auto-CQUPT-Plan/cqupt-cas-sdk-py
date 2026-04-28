import aiohttp

from urllib.parse import quote
from .utils import aes_encrypt, get_execution_and_salt


class AsyncClient:
    BASE_URL = "https://ids.cqupt.edu.cn"

    HEADERS = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
    }

    async def __init__(self, username: str, password: str, service: str) -> None:
        self.username = username
        self.password = password
        self.service = service

        self.ticket = await self.__init()

    async def __login(
        self, username: str, password: str, execution: str, cookie: str, service: str
    ):
        url = "{}/authserver/login?service={}".format(self.BASE_URL, quote(service))

        parm = {
            "username": username,
            "password": password,
            "captcha": "",
            "_eventId": "submit",
            "cllt": "userNameLogin",
            "dllt": "generalLogin",
            "lt": "",
            "execution": execution,
        }

        async with aiohttp.ClientSession() as session:
            resp = await session.post(
                url=url,
                headers={**self.HEADERS, "Cookie": cookie},
                data=parm,
                allow_redirects=False,
            )

        if "该帐号已经被冻结" in await resp.text():
            raise Exception("该帐号已经被冻结")

        ticket = resp.headers.get("Location")
        if not ticket:
            raise Exception("登录失败")
        return ticket

    async def __init(self):
        # 登录流程:
        #     1. 第一次请求界面获取Cookie (route&jssid)
        #     2. 第二次请求界面, 携带第一次的Cookie获取execution和pwdEncryptSalt
        #     3. 第三次请求登录, 使用pwdEncryptSalt加密用户密码

        url = "{}/authserver/login?service={}".format(
            self.BASE_URL, quote(self.service)
        )

        session = aiohttp.ClientSession()

        resp = await session.get(url, headers=self.HEADERS)
        cookie = resp.headers["Set-Cookie"].split()
        html = await resp.text()

        cookie = cookie[0] + cookie[2]

        resp = await session.get(url, headers={**self.HEADERS, "Cookie": cookie})
        html = await resp.text()
        execution, pwdEncryptSalt = get_execution_and_salt(html)

        passwd = aes_encrypt(self.password, pwdEncryptSalt)

        await session.close()
        await self.__login(self.username, passwd, execution, cookie, self.service)
