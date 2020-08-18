from fake_useragent import UserAgent

def getHeader():
    ua = UserAgent()
    return {    'User-Agent': ua.random,
                'accept-language': 'zh-CN'}