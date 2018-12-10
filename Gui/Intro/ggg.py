def odd():
    funcs = []
    for c in 'abcdefg':
        funcs.append((lambda: c))  # поиск переменной c будет выполнен позднее
    return funcs  # не сохраняет текущее значение c


for func in odd():
    print(func(), end=' ')  # Опа!: выведет 7 символов g, а не a,b,c,... !
