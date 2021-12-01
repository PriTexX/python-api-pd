MONTHS = {
    'Янв': 1,
    'Фев': 2,
    'Мар': 3,
    'Апр': 4,
    'Май': 5,
    'Июн': 6,
    'Июл': 7,
    'Авг': 8,
    'Сен': 9,
    'Окт': 10,
    'Ноя': 11,
    'Дек': 12,
}


def getMonth(monthNum: int) -> str:
    for k, v in MONTHS.items():
        if v == monthNum:
            return k
