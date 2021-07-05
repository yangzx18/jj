from wencai import wencai_search
import pickle
from datetime import datetime

def is_today(date):
    now = str(datetime.now()).split(' ')[0]
    return now == date

def get_codes(word):
    try:
        with open('s.pkl','rb') as f:
            data = pickle.load(f)
            date = data[word]['date']
            if not is_today(date):
                raise Exception('刷新股票列表')
            return data[word]
    except:
        s = "昨日涨停，st除外，科创板除外"
        res = wencai_search(word)
        
        try:
            data = res['data']['data']
        except:
            # print(res)
            raise Exception("error:查询结果错误或为空")

        # cur_timestamp = after_minuters(0)
        stocks = [ v['hqCode'] for v in data ]
        d = dict()
        d[word] = dict()
        d2 = d[word]
        d2['data'] = stocks
        d2['date'] = str(datetime.now()).split(' ')[0]
        with open('s.pkl','wb') as f:
            pickle.dump(d, f)


        return d2

if __name__ == '__main__':
    codes = get_codes()
    get_codes()
    print(codes)
