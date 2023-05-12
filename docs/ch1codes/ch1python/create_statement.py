
def enrich_performance(performance):
    res = performance.copy()
    res['play'] = play_for(performance)
    res['amount'] = amount_for(performance)
    res['volume_credits'] = volume_credits_for(performance)
    return res


def create_statement(invoice, play):

    statement_data = {
        'customer': invoice['customer'],
        'performances': list(map(enrich_performance, invoice['performances']))
    }
    statement_data['total_amount'] = total_amount(statement_data)
    statement_data['total_volume_credits'] = total_volume_credits(statement_data)
