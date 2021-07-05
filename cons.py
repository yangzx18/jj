import json
from datetime import datetime
def load_json(path):
    f = open(path, 'r')
    data = json.load(f)
    return data
xueqiu_cookie = load_json('/home/yangzx/cookies.json')['xueqiu']

xueqiu_header = {
    'Accept': 'application/json, text/plain, */*',
    
    'Cookie': xueqiu_cookie,
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/68.0.3440.106 Chrome/68.0.3440.106 Safari/537.36'
}
xueqiu_trade_url_real = 'https://stock.xueqiu.com/v5/stock/realtime/quotec.json'
xueqiu_trade_url = 'https://stock.xueqiu.com/v5/stock/quote.json'
xueqiu_pankou_url = 'https://stock.xueqiu.com/v5/stock/realtime/pankou.json'
xueqiu_trade_params = {
    "symbol": '',
    "extend": 'detail',
    '_' : '1582698548797'
}

def get_timestamp(date):

    y = int(date[:4])
    m = int(date[4:6])
    d = int(date[6:])

    d = datetime(y, m, d)
    stamp = d.timestamp()
    stamp = int(stamp * 1000)

    return stamp

def get_count(test=None):
    t1 = test or datetime.now()
    s = str(t1).split(' ')[1].split('.')[0].replace(':', '')
    s = int(str(s))
    if s < 93000:
        return 480
        # raise Exception('时间错误')
        
    elif s < 113000:
        t2 = datetime(t1.year, t1.month, t1.day, 9, 30, 0)
        r = t1 - t2
        return r.seconds // 60 + 240
        
    elif s < 130000:
        return 360 ## 240 + 120
    
    elif s < 150000:
        t3 = datetime(t1.year, t1.month, t1.day, 13, 0, 0)
        r = t1 - t3
        return r.seconds // 60 + 360 ## 240 + 120
    else:
        return 480