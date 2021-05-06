import requests


class PingAnUtils:

    @staticmethod
    def get_fund_by_code(code):
        api = 'https://m.stock.pingan.com/omm/http/pss/queryPublicDetail'
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        form_data = {
            "code": code
        }
        return requests.post(api, headers=headers, data=form_data).json()


class Stock:
    # 股票代码
    code = ''
    # 股票名称
    name = ''
    # 占净值比例
    proportion = 0.0

    def __init__(self, code, name, proportion):
        self.code = code
        self.name = name
        self.proportion = proportion


class Fund:
    # 基金代码
    code = ''
    # 基金全称
    fullName = ''
    # 成立日期
    setupDate = ''
    # 资产规模
    unitTotal = ''
    # 管理银行
    custodianBank = ''
    # 持仓股票
    stocks = []

    def __init__(self, code):
        self.code = code
        resp = PingAnUtils.get_fund_by_code(code)
        self.fullName = resp['fullName']
        self.setupDate = resp['setupDate']
        self.unitTotal = resp['unitTotal']
        self.custodianBank = resp['custodianBank']
        for stock in resp['stocks']:
            self.stocks.append(Stock(stock['stockPrtStockCode'], stock['stockPrtStockName'], stock['stockPrtstkvaluetonav']))

    def base(self):
        return [self.code, self.setupDate, self.unitTotal, self.fullName]
