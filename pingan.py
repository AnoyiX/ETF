import requests


def zh_count(str):
    """
    统计中文个数
    """
    count = 0
    for s in str:
        if '\u4e00' <= s <= '\u9fa5':
            count += 1
    return count


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

    def print_details(self):
        print('-----------------------------------------------------------------------')
        print('| ', self.fullName.center(65 - zh_count(self.fullName)), ' |')
        print('-----------------------------------------------------------------------')
        print('| 基金代码', '{} |'.format(self.code).rjust(60))
        print('| 成立日期', '{} |'.format(self.setupDate).rjust(60))
        print('| 资产规模', '{} |'.format(self.unitTotal).rjust(60 - zh_count(self.unitTotal)))
        print('| 基金托管', '{} |'.format(self.custodianBank).rjust(60 - zh_count(self.custodianBank)))
        print('| ', ''.center(65), ' |')
        print('-----------------------------------------------------------------------')
        print('| ', '重仓持股'.center(61), ' |')
        print('-----------------------------------------------------------------------')
        print('| ', '股票名称'.ljust(30), '股票代码'.rjust(10), '占净值比例'.rjust(10), ' |')
        print('| ', ''.center(65), ' |')
        for stock in self.stocks:
            print('| ', stock.name.ljust(30 - zh_count(stock.name)), stock.code.rjust(18), stock.proportion.rjust(15), ' |')
        print('-----------------------------------------------------------------------')

    def print_base(self):
        print('| ', self.code.ljust(8), self.fullName.ljust(60 - zh_count(self.fullName)), self.unitTotal.rjust(11 - zh_count(self.unitTotal)), self.setupDate.rjust(12), ' |')


if __name__ == '__main__':
    Fund('001838').print_details()

