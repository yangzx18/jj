import aiohttp
import json
import asyncio
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

result = []

base = 0
test = 0

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
async def get1min(session, code, date, count=-238):
    _code = code
    if code.startswith("6"):
        _code = "SH" + code
    else:
        _code = "SZ" + code

    _begin = get_timestamp(date)
    params = {
        "symbol": _code,
        "begin": _begin,
        "period": "1m",
        "type": "before",
        "count": count,
    }
    global test
    if test == 0:
        print(params)
        test += 1
    url = "https://stock.xueqiu.com/v5/stock/chart/kline.json"

    async with session.get(url, params=params) as response:
        try:
            data = await response.json()
            return data
        except:
            print(f'获取{code}失败')
            
def find(data):
    max_v_down, max_v_up = 0, 0
    items = data['data']['item']
    # print(data)
    try:
        yestoday, today = items[:240+base], items[240+base:]
        # print('长度', len(yestoday), len(today))
        yestoday_v, today_v = [ v[1] for v in yestoday ], [ v[1] for v in today ]
        max_yestoday_v, max_today_v = max(yestoday_v), max(today_v)
        global result
        if max_today_v * 2 > max_yestoday_v:
            t = [data['data']['symbol'],max_yestoday_v / 1000000, max_today_v / 1000000, today[-1][5]] ## 5是close
            result.append(t)
    except:
        print(data['data']['symbol'], len(yestoday), len(today))

async def predict_one(session, code, codes, date, count):
    data = await get1min(session, code, date, count)
    # if find(data):
    #     print(data['data']['symbol'])
    find(data)
    global cur_i, l

    if cur_i < l:
        code = codes[cur_i]

        cur_i = cur_i + 1
        await predict_one(session, code, codes, date, count)

async def predict_mul(codes, batch_size, session, date):
    global cur_i, l

    num_codes = len(codes)
    l = num_codes
    batch = batch_size
    if num_codes < batch_size:
        batch = num_codes

    tasks = []
    count = get_count()
    global base
    count = base + count
    print('count', count)
    for i in range(batch):
        tasks.append(predict_one(session, codes[i], codes, date, -count))
    ### codes不全局
    cur_i = batch  ### 恢复
    await asyncio.wait(tasks)

async def main_task(batch_size, codes, date):
    session = aiohttp.ClientSession(headers=xueqiu_header)
    await predict_mul(codes, batch_size, session, date)
    await session.close()
def sort_result(result, mode):
    if mode == 1:
        r = sorted(result, key=lambda x: float(x[2]*x[3]))
    else:
        r = sorted(result, key=lambda x: float(x[2]/x[1]))
    r.reverse()
    return r

def print_result(result):
    # print(result)
    url_headers = "https://xueqiu.com/S/"
    for r in result:
        code = r[0]
        url = url_headers + code
        print(url, '\t', f'{round(r[1], 3)}'.rjust(6), f'{round(r[2], 3)}'.rjust(8), f'{r[3]:7}'.rjust(6))


def main(word, date):
    from stocks import get_codes
    global result
    loop = asyncio.get_event_loop()
    codes = get_codes(word)['data']
    print('codes len', len(codes))
    task = main_task(8, codes, date)
    loop.run_until_complete(task)

    print('-'*22, '按成交额输出', '-'*22)
    result = sort_result(result, 1)
    print_result(result)
    print('-'*22, '按量比输出', '-'*22)
    result = sort_result(result, 2)
    print_result(result)
# if __name__ == '__main__':
    