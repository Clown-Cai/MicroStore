from qcloudsms_py import SmsSingleSender
import random
from django.core.cache import cache

from .settings import *

# 获取短信发送的发送器
ssender = SmsSingleSender(APP_ID, APP_KEY)

def send_sms(phone):
    code = _get_code()
    # 在缓存中记录code
    cache.set(phone, code)
    params = [code, EXP]
    try:
        result = ssender.send_with_param(
            NATIONCODE,
            phone,
            TEMPLATE_ID,
            params,           # 模板参数
            sign=SMS_SIGN,    # 发送者的签名
            extend="",        # 扩展字段
            ext=""
        )
        if result and result.get('result') == 0:
            return True
        return False
    except Exception as e:
        return False

# 生成短信验证码
def _get_code():
    code = ''
    for i in range(4):
        code += str(random.randint(0,9))
    return code