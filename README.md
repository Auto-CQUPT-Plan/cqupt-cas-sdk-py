# cqupt-cas-sdk-py

> 重庆邮电大学 统一身份认证平台 SDK

> 本项目是 Auto CQUPT Plan 的一部分

> [!warning]
> 
> 本项目仅供学习，请勿用于非法用途，否则后果自负！！！

## 1. 项目简介

`cqupt-cas-sdk-py`是由 `python` 编写的 **重庆邮电大学统一身份认证中心SDK**, 实现了登录功能.

## 2. 使用

- 安装

你可以使用uv来安装这个库
```shell
uv add "cqupt-cas @ git+https://github.com/Auto-CQUPT-Plan/cqupt-cas-sdk-py.git"
```

- 使用

**参数说明：**

| 参数     | 说明            |
| -------- | --------------- |
| username | 用户账号        |
| password | 密码            |
| service  | 要登陆服务的URL |



```python
from cqupt_cas import Client

cas_client = Client("id", "passwd", "https://i.cqupt.edu.cn")

ticket = cas_client.ticket
```
即可拿到带有 `ticket` 的认证url


你也可以使用异步版本的实现

```python
from cqupt_cas import AsyncClient

cas_client = AsyncClient("id", "passwd", "https://i.cqupt.edu.cn")

ticket = await cas_client.ticket()
```