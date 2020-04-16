
def bar_make(value: int, gap: int, fill_char: str = '█', empty_char: str = ' ', point_mode: bool = False, length: int = 10):
    bar = ''

    percentage = (value/gap) * length

    if point_mode:
        for i in range(0, length + 1):
            if i == round(percentage):
                bar += fill_char
            else:
                bar += empty_char
        return bar

    for i in range(1, 11):
        if i <= percentage:
            bar += fill_char
        else:
            bar += empty_char
    return bar