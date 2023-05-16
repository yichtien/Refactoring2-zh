import locale

from docs.ch1codes.ch1python.create_statement import create_statement_data


def statement(invoice, plays):
    return render_plain_text(create_statement_data(invoice, plays))


def render_plain_text(data):
    result = f'Statement for {data["customer"]}\n'

    for perf in data['performances']:
        result += f'  {perf["play"]["name"]}: {usd(perf["amount"])} ({perf["audience"]} seats)\n'

    result += f'Amount owed is {usd(data["total_amount"])}\n'
    result += f'You earned {data["total_volume_credits"]} credits\n'
    return result


def html_statement(invoice, plays):
    return render_html(create_statement_data(invoice, plays))


def render_html(data):
    result = f'&lt;h1&gt;Statement for {data["customer"]}&lt;/h1&gt;\n'
    result += f'&lt;table&gt;\n'
    result += f'&lt;tr&gt;&lt;th&gt;play&lt;/th&gt;&lt;th&gt;seats&lt;/th&gt;&lt;th&gt;cost&lt;/th&gt;&lt;/tr&gt;'
    for perf in data['performances']:
        result += f'&lt;tr&gt;&lt;td&gt;{perf["play"]["name"]} &lt;/td &gt;&lt;td &gt;${perf.audience} &lt;/td&gt;'
        result += f'&lt;td&gt;{usd(perf["amount"])}&lt;/td&gt;&lt;/tr&gt;\n'
        result += '&lt;/table&gt;\n'
        result += f'&lt;p&gt;Amount owed is &lt;em&gt;{usd(data["total_amount"])}&lt;/em&gt;&lt;/p&gt;\n'
        result += f'&lt;p&gt;You earned&lt;em&gt;{data["total_volume_credits"]}&lt;/em&gt;credits&lt;/p&gt;\n'

    return result


def usd(number):
    locale.setlocale(locale.LC_ALL, 'en_US')
    return locale.currency(number / 100, grouping=True)
