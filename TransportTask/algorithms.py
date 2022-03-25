from data_structure import TransportTask


def north_west_method(in_task: TransportTask):
    """
    Создает начальный план методом Северо-Западного угла.

    Начальный план - матрица, задающая количество перевезенного груза из i-ый в j-ый пункт
    До конца функции под начальным планом подразумевается task.m_cost (так удобно работать)
    Звездочками(*) обозначаются незаполненные клетки
    """
    task = copy_task(in_task)
    point = [0, 0]  # Наше местоположение в таблице, первый элемент строка, второй столбец

    while point[0] < len(task.v_exporter) and point[1] < len(task.v_importer):
        possible_max = min(task.v_exporter[point[0]], task.v_importer[point[1]])

        # Если мы полностью закрыли импортера и экспортера
        if task.v_exporter[point[0]] == task.v_importer[point[1]]:
            # Такая хитрая проверка условий нужна для того, чтобы всегда получать m + n - 1 заполненных клеток
            if point[1] < len(task.v_importer) - 1:  # Есть место справа
                close_column(task.m_cost, point[0], point[1], possible_max)
                close_line(task.m_cost, point[0], point[1] + 1, 0)
            elif point[0] < len(task.v_exporter) - 1:  # Если есть место снизу.
                close_line(task.m_cost, point[0], point[1], possible_max)
                close_column(task.m_cost, point[0] + 1, point[1], 0)
            else:  # Видимо мы в правом нижнем углу
                task.m_cost[point[0]][point[1]] = possible_max

            point[0] += 1
            point[1] += 1

        # Если мы закрываем импортера (столбец)
        elif possible_max == task.v_importer[point[1]]:
            close_column(task.m_cost, point[0], point[1], possible_max)
            point[1] += 1
            task.v_exporter[point[0]] -= possible_max

        # Закрываем экспортера (строку)
        else:
            close_line(task.m_cost, point[0], point[1], possible_max)
            point[0] += 1
            task.v_importer[point[1]] -= possible_max

        # Отладка
        # print(task.m_cost)
        # print("\n")

    return task.m_cost.copy()


def close_line(m_good_count, point_i, point_j, good_count):
    """
    Ставит в [point_i, point_j] новое количество груза и обнуляет элементы строки, идущие после point.

    :param m_good_count: Матрица количества груза, перевозимого из пункт i в пункт j
    :param point_i: Текущая строка в методе СЗУ
    :param point_j: Текущий столбец в методе СЗУ
    :param good_count: Количество груза, которое нужно поставить в [point_i, point_j]
    """
    if point_i >= len(m_good_count) or point_j >= len(m_good_count[0]):
        return
    if point_j < len(m_good_count[0]) - 1:
        for j in range(point_j + 1, len(m_good_count[0])):
            m_good_count[point_i][j] = '*'
    m_good_count[point_i][point_j] = good_count


def close_column(m_good_count, point_i, point_j, good_count):
    if point_i >= len(m_good_count) or point_j >= len(m_good_count[0]):
        return
    if point_i < len(m_good_count) - 1:
        for i in range(point_i + 1, len(m_good_count)):
            m_good_count[i][point_j] = '*'
    m_good_count[point_i][point_j] = good_count


def copy_task(in_task: TransportTask):
    return TransportTask(in_task.m_cost, in_task.v_exporter, in_task.v_importer)


def calculate_function(plan, m_cost):
    result = 0
    for i in range(len(plan)):
        for j in range(len(plan[i])):
            if plan[i][j] != '*':
                result += plan[i][j] * m_cost[i][j]
    return result
