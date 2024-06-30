
def to_money(value):
    return "{:,.2f}".format(value).replace(',', 'X').replace('.', ',').replace('X', '.')

def hoteis():
    pass