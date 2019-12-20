from alipay import AliPay
import datetime

from .settings import *

alipay = AliPay(
    appid=APP_ID,
    app_notify_url=None,  # 默认回调url，一般为None
    # 应用私钥
    app_private_key_string=APP_PRIVATE_KEY_STRING,
    # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
    alipay_public_key_string=ALIPAY_PUBLIC_KEY_STRING,
    sign_type=SIGN_TYPE,  # RSA 或者 RSA2
    debug=DEBUG  # 默认False
)


# 生成支付链接
# 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
def get_paymentlink(subject, total_amount):
    out_trade_no = _get_out_trade_no()
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=out_trade_no,
        total_amount=total_amount,
        subject=subject,
        # 支付成功后，前台异步回调接口
        return_url=RETURN_URL,
        # 支付成功后，后台异步回调接口, 可选, 不填则使用默认notify url
        notify_url="https://example.com/notify"
    )
    PAYMENT_LINK = GATEWAY + order_string
    return PAYMENT_LINK


# 生成订单号
def _get_out_trade_no():
    trade_no = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    return trade_no
