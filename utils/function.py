import hashlib


def md5_encode(str):
    """
    md5加密密码
    :param str:原始密码
    :return: 加密后的密码
    """
    return hashlib.md5(str.encode('utf-8')).hexdigest()
