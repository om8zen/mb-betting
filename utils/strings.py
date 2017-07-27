def str_money(money):
    cents = int(abs(money) % 100)
    return "{sign}${dollars}.{cents}".format(
        sign = "-" if money < 0 else "",
        dollars = abs(int(money / 100.)),
        cents = ("0" if cents < 10 else "") + str(cents)
        )

def str_list(list_):
    return list_[0] if len(list_) == 1 else (", ".join(list_[:-1]) + " & " + list_[-1])
