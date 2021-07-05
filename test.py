from xueqiu import xueqiu_header
import requests
from cons import get_timestamp

_begin = get_timestamp('20210629')

params = {
    "symbol": 'SH601216',
    "begin": _begin,
    "period": "1m",
    "type": "before",
    "count": -538,
}
url = "https://stock.xueqiu.com/v5/stock/chart/kline.json"



res = requests.get(url, headers=xueqiu_header, params=params).json()

print(len(res['data']['item']))