import requests

wencai_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/76.0.3809.100 Chrome/76.0.3809.100 Safari/537.36'
}

wen_url = 'http://www.iwencai.com/unifiedwap/unified-wap/result/get-stock-pick'

wencai_params = {
    "question": "",
    "perpage": 3000
}

def wencai_search(words):
    print('获取数据')
    try:
        wencai_params['question'] = words
        res = requests.get(wen_url,headers=wencai_headers,params=wencai_params)
        return res.json()
    except:
        raise Exception("问财获取失败")
