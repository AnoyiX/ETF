from pingan import Fund, zh_count

funds_code = ['001631', '001629', '501030', '004856']
money = 100000

if __name__ == '__main__':
    funds = []
    stocks = {}
    print('Your Money: ￥', money)
    print('Loading fund data...')
    print('----------------------------------------------------------------------------------------------------')
    print('|', '基金列表'.center(92), "|")
    print('----------------------------------------------------------------------------------------------------')
    print('| 基金代码  基金全称                                                        基金资产     成立日期  |')
    for code in funds_code:
        fund = Fund(code)
        fund.print_base()
        if fund.stocks:
            funds.append(fund)
    print('----------------------------------------------------------------------------------------------------')
    print('Data From 平安证券'.rjust(96))
    print('')
    fund_count = len(funds)
    for fund in funds:
        for stock in fund.stocks:
            if stocks.get(stock.code):
                stocks[stock.code].proportion += float(stock.proportion) / fund_count
            else:
                stocks[stock.code] = stock
                stocks[stock.code].proportion = float(stocks[stock.code].proportion) / fund_count
    print('----------------------------------------------------------------------------------------------------')
    print('|', '股票申购列表'.center(90), "|")
    print('----------------------------------------------------------------------------------------------------')
    print('| 股票名称                                                 股票代码      占净值比例       购入金额 |')
    total_money = 0
    sorted_stocks = sorted(stocks.values(), key=lambda item: item.proportion, reverse=True)
    for stock in sorted_stocks:
        cost = int(money * stock.proportion / fund_count / 100)
        # 选择投资金额大于 500 的股票
        if cost > 500:
            total_money += cost
            print('|', stock.name.ljust(52 - zh_count(stock.name)), stock.code.rjust(12), str('%.6f' % (stock.proportion / fund_count)).rjust(14), str(int(cost)).rjust(14), ' |')
    print('----------------------------------------------------------------------------------------------------')
    print('Author: Anoyi'.ljust(13), '合计: {} 元'.format(str(total_money)).rjust(83))
    print('')
    print('【注意】以上信息仅供参考，股市有风险，请理性投资！剩余零花钱 {} 元，建议存入余额宝/余利宝/零钱通等。'.format(int(money - total_money)))
    print('')
    print('')
