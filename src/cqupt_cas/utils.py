import base64
import random

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from lxml import etree  # type: ignore


def random_string(length):
    """
    Code by AI
    生成随机字符串
    :param length: 字符串长度
    :return: 随机字符串
    """
    aes_chars = "ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678"
    aes_chars_len = len(aes_chars)
    result = ""
    for i in range(length):
        result += aes_chars[random.randint(0, aes_chars_len - 1)]
    return result


def aes_encrypt(password, salt) -> str:
    """
    Code by AI
    :param password: 明文密码
    :param salt: 盐值
    :return: 加密后的密码
    """
    try:
        # 1. 生成64个随机字符并与密码拼接
        random_str = random_string(64)
        password_str = random_str + password

        # 2. 使用盐值作为密钥（去除前后空格）
        key = salt.strip().encode("utf-8")
        # 确保密钥长度为16字节
        if len(key) < 16:
            key = key.ljust(16, b"\0")
        elif len(key) > 16:
            key = key[:16]

        # 3. 生成16个随机字符作为IV
        iv = random_string(16).encode("utf-8")

        # 4. 使用AES-CBC模式加密，PKCS7填充
        cipher = AES.new(key, AES.MODE_CBC, iv)
        # 填充数据
        padded_data = pad(password_str.encode("utf-8"), AES.block_size)
        # 加密
        encrypted = cipher.encrypt(padded_data)

        # 5. 编码为base64
        encrypted_base64 = base64.b64encode(encrypted).decode("utf-8")

        return encrypted_base64
    except Exception as e:
        print(f"CAS加密失败: {e}")
        raise e


def get_execution_and_salt(html: str) -> tuple[str, str]:
    execution_xpath = "//*[@id='execution']/@value"
    salt_xpath = "//*[@id='pwdEncryptSalt']/@value"

    html = etree.HTML(html)
    execution = html.xpath(execution_xpath)  # type: ignore
    salt = html.xpath(salt_xpath)  # type: ignore

    return execution[0], salt[0]
