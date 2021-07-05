import click
import asyncio
from stocks import get_codes
from xueqiu import main, sort_result, print_result

def mode2word(mode):
    d = {
        "r": "最近4个交易日有过涨停，st除外，科创板除外，前一个交易日不涨停,今日不涨停",
        "1": "昨日涨停，st除外，科创板除外"
    }

    if mode in d:
        return d[mode]
    else:
        raise Exception(f'模式{mode}不存在')
result = []

@click.command()
@click.option('-date', help="明天的日期")
@click.option('-mode', help="模式")
def cli(date, mode):

    if not date:
        raise Exception('缺少日期')
    if not mode:
        raise Exception('选择一个模式, r或1')
    word = mode2word(mode)
    print(word)
    main(word, date)

if __name__ == '__main__':
    cli()