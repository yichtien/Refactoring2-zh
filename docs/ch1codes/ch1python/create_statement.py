import math
from functools import reduce


def create_statement_data(invoice, plays):
    def play_for(performance):
        """用以移除变量 `play` """
        return plays[performance['playID']]

    def total_volume_credits(data):
        res = reduce(lambda x, y: x + y['volume_credits'], data['performances'], 0)
        return res

    def total_amount(data):
        res = reduce(lambda x, y: x + y['amount'], data['performances'], 0)
        return res

    def enrich_performance(performance):
        res = performance.copy()
        calculator = create_performance_calculator(res, play_for(res))
        res['play'] = calculator.play
        res['amount'] = calculator.amount
        res['volume_credits'] = calculator.volume_credits
        return res

    statement_data = {
        'customer': invoice['customer'],
        'performances': list(map(enrich_performance, invoice['performances']))
    }
    statement_data['total_amount'] = total_amount(statement_data)
    statement_data['total_volume_credits'] = total_volume_credits(statement_data)

    return statement_data


class PerformanceCalculator:

    def __init__(self, performance, play):
        self._performance = performance
        self._play = play

    @property
    def performance(self):
        return self._performance

    @property
    def play(self):
        return self._play

    @property
    def amount(self) -> float:
        raise RuntimeError(f'subclass responsibility')

    @property
    def volume_credits(self):
        res: int = max(self.performance['audience'] - 30, 0)
        return res


class TragedyCalculator(PerformanceCalculator):

    @property
    def amount(self) -> float:
        res = 40000
        if self.performance['audience'] > 30:
            res += 1000 * (self.performance['audience'] - 30)
        return res


class ComedyCalculator(PerformanceCalculator):

    @property
    def amount(self) -> float:
        res = 30000
        if self.performance['audience'] > 20:
            res += 10000 + 500 * (self.performance['audience'] - 20)
        res += 300 * self.performance['audience']
        return res

    @property
    def volume_credits(self):
        return super().volume_credits + math.floor(self.performance['audience'] / 5)


def create_performance_calculator(performance, play):
    if play['type'] == 'tragedy':
        return TragedyCalculator(performance, play)
    elif play['type'] == 'comedy':
        return ComedyCalculator(performance, play)
    else:
        raise Exception(f'unknown type {play["type"]}')
