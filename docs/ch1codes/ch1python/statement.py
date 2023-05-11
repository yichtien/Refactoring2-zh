import locale
import math


def statement(invoice, plays):
    def amount_for(performance) -> float:

        if play['type'] == 'tragedy':
            this_amount = 40000
            if performance['audience'] > 30:
                this_amount += 1000 * (performance['audience'] - 30)
        elif play['type'] == 'comedy':
            this_amount = 30000
            if performance['audience'] > 20:
                this_amount += 10000 + 500 * (performance['audience'] - 20)
            this_amount += 300 * performance['audience']
        else:
            raise RuntimeError(f'unknown type: {play["type"]}')
        return this_amount

    total_amount = 0
    volume_credits = 0
    result = f'Statement for {invoice["customer"]}\n'
    locale.setlocale(locale.LC_ALL, 'en_US')
    for perf in invoice['performances']:
        play = plays[perf['playID']]

        this_amount = amount_for(perf)
        # add volume credits
        volume_credits += max(perf['audience'] - 30, 0)
        # add extra credit for every ten comedy attendees
        if "comedy" == play['type']:
            volume_credits += math.floor(perf['audience'] / 5)

        # print line for this order
        result += f'  {play["name"]}: {locale.currency(this_amount / 100)} ({perf["audience"]} seats)\n'
        total_amount += this_amount

    result += f'Amount owed is {locale.currency(total_amount / 100, grouping=True)}\n'
    result += f'You earned {volume_credits} credits\n'
    return result
