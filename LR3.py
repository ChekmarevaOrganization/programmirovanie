import numpy as np
# Шкала Саати
print("Шкала Саати:")
print("1 - равная важность")
print("3 - умеренное превосходство")
print("5 - существенное превосходство")
print("7 - значительное превосходство")
print("9 - абсолютное превосходство")
print("2,4,6,8 - промежуточные значения\n")

# 1 Создание матрицы
def make_matrix(n, values):
    m = np.ones((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            m[i, j] = values[i][j - i]
            m[j, i] = 1.0 / values[i][j - i]
    return m

# 2 Нормализация и веса
def normalize(m):
    sums = m.sum(axis=0)
    norm = m / sums
    weights = norm.mean(axis=1)
    return weights

# 3 Ввод данных
def input_data():
    while True:
        n_crit = int(input("\nКоличество критериев (≥5): "))
        if n_crit >= 5:
            break
        print("Критериев должно быть не менее 5!")

    criteria = []
    print(f"\nВведите {n_crit} критериев:")
    for i in range(n_crit):
        crit = input(f"  Критерий {i + 1}: ")
        criteria.append(crit)

    # Ввод альтернатив
    while True:
        n_alt = int(input("\nКоличество альтернатив (≥3): "))
        if n_alt >= 3:
            break
        print("Альтернатив должно быть не менее 3")

    alternatives = []
    print(f"\nВведите {n_alt} альтернатив:")
    for i in range(n_alt):
        alt = input(f"  Альтернатива {i + 1}: ")
        alternatives.append(alt)

    return criteria, alternatives

# 4 Ввод матрицы попарных сравнений
def input_matrix(n, names, title):
    print(f"\n{title}")
    print("Введите значения по шкале Саати (1-9):")
    values = []
    for i in range(n):
        row = []
        for j in range(i, n):
            if i == j:
                row.append(1)
            else:
                while True:
                    try:
                        val = int(input(f"  {names[i]} против {names[j]} = "))
                        if 1 <= val <= 9:
                            row.append(val)
                            break
                        else:
                            print("Введите число от 1 до 9")
                    except ValueError:
                        print("Введите целое число")
        values.append(row)
    return values

def run():
    print("Метод анализа иерархий (МАИ)")
    # Ввод данных
    criteria, alternatives = input_data()
    n_crit = len(criteria)
    n_alt = len(alternatives)
    print("Сравнение критериев")
    # Матрица критериев
    crit_values = input_matrix(n_crit, criteria, "\nПопарное сравнение критериев:")
    crit_matrix = make_matrix(n_crit, crit_values)
    crit_weights = normalize(crit_matrix)
    print("\nВеса критериев:")
    for i, (c, w) in enumerate(zip(criteria, crit_weights)):
        print(f"  {i + 1}. {c}: {w:.3f} ({w * 100:.1f}%)")
    # Матрицы альтернатив по каждому критерию
    print("Сравнение альтернатив по критериям")
    alt_matrix = np.zeros((n_alt, n_crit))

    for k in range(n_crit):
        print(f"\nКритерий '{criteria[k]}'")
        alt_values = input_matrix(n_alt, alternatives, "")
        alt_mat = make_matrix(n_alt, alt_values)
        alt_weights = normalize(alt_mat)
        alt_matrix[:, k] = alt_weights
        print(f"Веса по критерию '{criteria[k]}':")
        for i, (a, w) in enumerate(zip(alternatives, alt_weights)):
            print(f"  {a}: {w:.3f}")

    # Глобальные веса
    print("Глобальные веса и решения")

    global_w = alt_matrix @ crit_weights

    print("\nРезультаты:")
    print(f"{'Альтернатива':<35}{'Вес':<12}{'%':<10}")

    sorted_idx = np.argsort(global_w)[::-1]
    for rank, idx in enumerate(sorted_idx, 1):
        alt = alternatives[idx]
        w = global_w[idx]
        print(f"{rank}. {alt:<33}{w:<12.3f}{w * 100:<10.1f}")

    best = alternatives[sorted_idx[0]]
    print(f"\nРекомендуемый выбор: {best}")

    return global_w
if __name__ == "__main__":
    run()