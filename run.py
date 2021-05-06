from pingan import Fund
from wasabi import msg
from prettytable import PrettyTable

if __name__ == '__main__':
    stocks = {}
    money = float(input('投资金额（元）：'))
    fund_codes = input('基金代码（多个基金以空格分隔）：')
    with msg.loading("正在从平安证券加载数据中..."):
        funds = [Fund(x.strip()) for x in fund_codes.split(' ')]

    fund_table = PrettyTable()
    fund_table.title = '基金列表'
    fund_table.field_names = ['基金代码', '成立日期', '基金资产', '基金全称']
    fund_data = [x.base() for x in funds]
    fund_table.add_rows(fund_data)
    print(fund_table)

    fund_count = len(funds)
    for fund in funds:
        for stock in fund.stocks:
            if stocks.get(stock.code):
                stocks[stock.code].proportion += float(stock.proportion) / fund_count
            else:
                stocks[stock.code] = stock
                stocks[stock.code].proportion = float(stocks[stock.code].proportion) / fund_count
    total_money = 0
    sorted_stocks = sorted(stocks.values(), key=lambda item: item.proportion, reverse=True)
    stock_table = PrettyTable()
    stock_table.title = '股票列表'
    stock_table.field_names = ['股票代码', '股票名称', '占净值比例', '买入金额']
    stock_table.align['占净值比例'] = 'r'
    stock_table.align['买入金额'] = 'r'
    for stock in sorted_stocks:
        cost = int(money * stock.proportion / fund_count / 100)
        total_money += cost
        stock_table.add_row([stock.code, stock.name, f'{stock.proportion / fund_count:.02f}%', f'{cost:.02f}'])
    print(stock_table)
    msg.good(f'总计买入: {total_money:.02f} 元，剩余 {money - total_money:.02f} 元，建议存入余额宝/余利宝/零钱通等。')
    msg.warn('以上信息仅供参考，股市有风险，请理性投资！')
