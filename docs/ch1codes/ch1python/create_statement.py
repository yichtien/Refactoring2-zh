import locale
import math


def create_statement_data(invoice, plays):
    def amount_for(performance) -> float:
        if play_for(performance)['type'] == 'tragedy':
            res = 40000
            if performance['audience'] > 30:
                res += 1000 * (performance['audience'] - 30)
        elif play_for(performance)['type'] == 'comedy':
            res = 30000
            if performance['audience'] > 20:
                res += 10000 + 500 * (performance['audience'] - 20)
            res += 300 * performance['audience']
        else:
            raise RuntimeError(f'unknown type: {play_for(performance)["type"]}')
        return res

    def play_for(performance):
        """用以移除变量 `play` """
        return plays[performance['playID']]

    def volume_credits_for(perf):
        # add volume credits
        res: int = 0
        res += max(perf['audience'] - 30, 0)
        # add extra credit for every ten comedy attendees
        if "comedy" == play_for(perf)['type']:
            res += math.floor(perf['audience'] / 5)
        return res

    def usd(number):
        locale.setlocale(locale.LC_ALL, 'en_US')
        #
        return locale.currency(number / 100, grouping=True)

    def total_volume_credits(data):
        res = 0
        for perf in data['performances']:
            res += perf['volume_credits']
        return res

    def total_amount(data):
        res = 0
        for perf in data['performances']:
            res += perf['amount']
        return res

    def enrich_performance(performance):
        res = performance.copy()
        res['play'] = play_for(performance)
        res['amount'] = amount_for(performance)
        res['volume_credits'] = volume_credits_for(performance)
        return res

    statement_data = {
        'customer': invoice['customer'],
        'performances': list(map(enrich_performance, invoice['performances']))
    }
    statement_data['total_amount'] = total_amount(statement_data)
    statement_data['total_volume_credits'] = total_volume_credits(statement_data)

    return statement_data
