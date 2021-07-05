import asyncio
import aiohttp
from stocks import get_codes
from cons import get_timestamp, xueqiu_header

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
    url = "https://stock.xueqiu.com/v5/stock/chart/kline.json"

    async with session.get(url, params=params) as response:
        try:
            data = await response.json()
            return data
        except:
            print(f'获取{code}失败')



class saver:
    def __init__(self, date, mode):
        self._date = date
        self._mode = mode
        self._count = 238
        self._batch_size = 8
        self._cur_i = 0
        self._count = 238

    def select(self, data):
        max_v_down, max_v_up = 0, 0
        items = data['data']['item']
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

    async def predict_one(self, code):
        data = await get1min(self.session, code, self._date, -self._count)
        # if find(data):
        #     print(data['data']['symbol'])
        self.select(data)
        if self._cur_i < self._l:
            code = self._codes[self._cur_i]

            self._cur_i = self._cur_i + 1
            await self.predict_one(code)

    async def predict_mul(self):

        num_codes = len(self._codes)
        self._l = num_codes
        batch = batch_size
        if num_codes < self._batch_size:
            batch = num_codes

        tasks = []
        count = get_count()
        print('count', count)
        for i in range(batch):
            tasks.append(self.predict_one(session, self._codes[i]))
        ### codes不全局
        self._cur_i = batch  ### 恢复
        await asyncio.wait(tasks)


    async def main_task(self, batch_size, codes):
        self.session = aiohttp.ClientSession(headers=xueqiu_header)
        await self.predict_mul(codes, batch_size)
        await self.session.close()

    def start(self):
        loop = asyncio.get_event_loop()
        codes = get_codes(word)['data']
        self._codes = codes
        print('codes len', len(codes))
        task = self.main_task()
        loop.run_until_complete(task)
    