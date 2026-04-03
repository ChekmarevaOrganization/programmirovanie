def rel_calc(f1, f2):
    def load(path):
        with open(path, encoding='utf-8') as f:
            lines = [l.strip() for l in f if l.strip()]
        if not lines:
            raise ValueError("Файл пуст")
        h = [x.strip() for x in lines[0].split(',')]
        r = [tuple(x.strip() for x in l.split(',')) for l in lines[1:]]
        return h, r

    def show(h, r, name=""):
        print(f"\nРезультат: {name}")
        if not r:
            print("  (пусто)")
            return
        print("  " + " | ".join(f"{x:<12}" for x in h))
        print("  " + "-" * (len(h) * 13))
        for row in r:
            print("  " + " | ".join(f"{str(v):<12}" for v in row))

    a = load(f1)
    b = load(f2)
    def union():
        if set(a[0]) != set(b[0]):
            raise ValueError("Схемы не совпадают")
        idx = [b[0].index(x) for x in a[0]]
        rb = [tuple(r[i] for i in idx) for r in b[1]]
        return a[0], list(set(a[1]) | set(rb))

    def intersect():
        if set(a[0]) != set(b[0]):
            raise ValueError("Схемы не совпадают")
        idx = [b[0].index(x) for x in a[0]]
        rb = [tuple(r[i] for i in idx) for r in b[1]]
        return a[0], list(set(a[1]) & set(rb))

    def diff():
        if set(a[0]) != set(b[0]):
            raise ValueError("Схемы не совпадают")
        idx = [b[0].index(x) for x in a[0]]
        rb = [tuple(r[i] for i in idx) for r in b[1]]
        return a[0], list(set(a[1]) - set(rb))

    def cart():
        return a[0] + b[0], [x + y for x in a[1] for y in b[1]]

    def select():
        cond = input("  Условие: ").strip()
        if not cond:
            return a[0], a[1]
        res = []
        for row in a[1]:
            ctx = dict(zip(a[0], row))
            for k, v in ctx.items():
                try:
                    ctx[k] = int(v)
                except ValueError:
                    pass
            if bool(eval(cond, {"__builtins__": {}}, ctx)):
                res.append(row)
        return a[0], res

    def proj():
        cols = [x.strip() for x in input("  Столбцы (через запятую): ").split(',')]
        if not set(cols).issubset(set(a[0])):
            raise ValueError("Несуществующие столбцы")
        idx = [a[0].index(c) for c in cols]
        return cols, list({tuple(r[i] for i in idx) for r in a[1]})

    def join():
        common = set(a[0]) & set(b[0])
        if not common:
            raise ValueError("Нет общих столбцов")
        ia = [a[0].index(c) for c in common]
        ib = [b[0].index(c) for c in common]
        rh = a[0] + [x for x in b[0] if x not in common]
        rr = [ra + tuple(rb[i] for i, h in enumerate(b[0]) if h not in common)
              for ra in a[1] for rb in b[1]
              if tuple(ra[i] for i in ia) == tuple(rb[i] for i in ib)]
        return rh, rr

    def div():
        if not set(b[0]).issubset(set(a[0])):
            raise ValueError("Столбцы B не входят в A")
        xa = [x for x in a[0] if x not in b[0]]
        if not xa:
            raise ValueError("Все столбцы общие")
        ix = [a[0].index(x) for x in xa]
        y_in_a = [y for y in a[0] if y in b[0]]
        y_idx_b = [b[0].index(y) for y in y_in_a]
        y_combos = {tuple(r[i] for i in y_idx_b) for r in b[1]}
        res = [x_val for x_val in {tuple(r[i] for i in ix) for r in a[1]}
               if all(tuple(x_val) + y in a[1] for y in y_combos)]
        return xa, res

    ops = {
        '1': ('Объединение', union),
        '2': ('Пересечение', intersect),
        '3': ('Вычитание', diff),
        '4': ('Декартово произведение', cart),
        '5': ('Выборка', select),
        '6': ('Проекция', proj),
        '7': ('Соединение', join),
        '8': ('Деление', div)
    }

    print("\nДоступные операции:")
    for k, (name, _) in ops.items():
        print(f"  {k} — {name}")
    print("  0 / exit — выход")

    while True:
        c = input("\nВыбор: ").strip().lower()
        if c in ('0', 'exit', 'quit'):
            break
        if c not in ops:
            print("Неверный ввод")
            continue
        try:
            title, fn = ops[c]
            show(*fn(), title)
        except Exception as e:
            print(f"Ошибка: {e}")

if __name__ == "__main__":
    rel_calc('set1.txt', 'set2.txt')
