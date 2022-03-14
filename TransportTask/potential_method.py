import copy
from data_structure import TransportTask, OneLineEquation
from algorithms import calculate_function

# У нас есть point, там хранится номер строки и номер колонки
# Вот эти константы удобны, когда мы хотим достать из point номер строки или номер колонки
LINE = 0
COL = 1
directions = [[-1, 0], [0, 1], [0, -1], [1, 0]]  # up right left  down


def potential_method(task: TransportTask, start_plan):
    """
    Метод потенциалов для транспортной задачи

    :param task: Условия транспортной задачи в закрытом виде
    :param start_plan: Начальный план
    :return: Оптимальный план
    """
    plan = copy.deepcopy(start_plan)
    filled_needed = len(task.v_exporter) + len(task.v_importer) - 1

    while True:
        if filled_needed != get_filled_count(plan):
            raise "Неправильное начальное заполнение!"

        v_export_pot, v_import_pot = solve_linear_system(task, plan)
        if check_optimal(v_export_pot, v_import_pot, plan, task.m_cost):
            print("END")
            break
        else:
            print("CONTINUE")
            print(calculate_function(plan, task.m_cost))

            working_point = find_new_working_point(v_export_pot, v_import_pot, plan, task.m_cost)
            print("Новая изменяемая точка: ", working_point)

            plan = change_plan(plan, working_point)
            print("Новый план: ")
            for line in plan:
                print(line)
    return plan


def change_plan(plan, start_point):
    """
    Меняем план.
    От стартовой точки находится цикл пересчета, точки в цикле чередуются +-+- (начиная от стартовой)
    Среди минусовых находится минимум
    Минимум должен обнулиться (для этого надо пересчитать точки плана из цикла пересчета)
        и точка минимума стать нерабочей
    """
    cycle = fynd_cycle(plan, start_point)
    is_minus = True
    for i in range(len(cycle)):
        if is_minus:
            cycle[i].append("-")
        else:
            cycle[i].append("+")
        is_minus = not is_minus

    print("Ломаная пути, не считая начальной точки: ", cycle)
    minimum, min_point = find_min(cycle, plan)
    plan[start_point[LINE]][start_point[COL]] = minimum

    for point in cycle:
        if point[2] == '-' and point[LINE] == min_point[LINE] and point[COL] == min_point[COL]:
            plan[point[LINE]][point[COL]] = '*'
        elif point[2] == "-":
            plan[point[LINE]][point[COL]] -= minimum
        else:
            plan[point[LINE]][point[COL]] += minimum

    return plan


def find_min(way, plan):
    print(way[0])
    min_value = plan[way[0][LINE]][way[0][COL]]
    min_point = [way[0][LINE], way[0][COL]]
    for point in way:
        if point[2] == '-':
            if plan[point[LINE]][point[COL]] < min_value:
                min_point = [point[LINE], point[COL]]
                min_value = plan[point[LINE]][point[COL]]
    return min_value, min_point


def fynd_cycle(plan, start_point):
    """
    Функция ищет цикл пересчета.
    Такой цикл существует и единственен
    Цикл пересчета - это особый проход по клеткам, есть некоторые правила, как его составить
    Подробнее см. в отчете
    """
    for direction in directions:
        next_point = step(start_point, direction)
        find, cycle = walk(next_point, direction, plan, start_point, set(), start_point)
        if find:
            return cycle
    return


def walk(point, current_direction, plan, starting_point, visited, prev_point):
    point_id = get_point_id(point, len(plan[0]))
    if point[LINE] < 0 or point[COL] < 0 or point[LINE] >= len(plan) or point[COL] >= len(
            plan[0]) or (point_id in visited):  # Вышли за границу
        return False, []
    visited.add(point_id)
    # Если точка оказалась нерабочей, то просто идем дальше
    if plan[point[LINE]][point[COL]] == '*':
        if is_equal(point, starting_point):  # Вернулись в исходную позицию
            return True, []
        next_point = step(point, current_direction)
        find, cycle = walk(next_point, current_direction, plan, starting_point, visited, point)
        if find:
            return find, cycle
        visited.remove(point_id)
    else:
        for direction in directions:
            next_point = step(point, direction)
            if is_equal(next_point, prev_point):
                continue
            find, cycle = walk(next_point, direction, plan, starting_point, visited, point)
            # Добавляем в цикл пересчета только те точки, в которых меняем направление
            if not is_equal(direction, current_direction):
                cycle.append(point)
            if find:
                return find, cycle
        visited.remove(point_id)

    return False, []


def is_equal(point, point_2):
    return point[LINE] == point_2[LINE] and point[COL] == point_2[COL]


def get_point_id(point, hor_size):
    return point[LINE] * hor_size + point[COL]


def step(point, direction):
    return [point[LINE] + direction[LINE], point[COL] + direction[COL]]


def find_new_working_point(v_export_pot, v_import_pot, plan, m_cost):
    """
    Находит новую рабочую(изменяемая) точку, от которой будем строить алгоритм пересчета
    (i, j) = argmax_ij(u_i + v_j - c_ij)
    """
    maximum = 0
    point = [0, 0]
    for i in range(len(plan)):
        for j in range(len(plan[0])):
            if plan[i][j] == '*':
                if (v_import_pot[j] + v_export_pot[i] - m_cost[i][j]) > maximum:
                    maximum = abs(v_import_pot[j] + v_export_pot[i] - m_cost[i][j])
                    point = [i, j]
    return point


def solve_linear_system(task: TransportTask, plan):
    """
    Находит векторы потенциалов U и V, решая систему линейных уравнений.
    Вектор U соответствует вектору экспорта
    Вектор V соответствует вектору импорта
    """
    system = []
    for i in range(len(plan)):
        for j in range(len(plan[0])):
            if plan[i][j] != '*':
                new_eq = OneLineEquation("u_" + str(i), "v_" + str(j), task.m_cost[i][j])
                system.append(new_eq)
    for elem in system:
        print(elem)

    # Поскольку у нас n + m переменных и ВСЕГДА только n + m - 1 уравнений, одну переменную можно выбрать любой
    result = {'u_0': 0}
    solved = False
    while not solved:
        solved = update_system(result, system)

    print(result)
    return convert_to_vectors(result)


def convert_to_vectors(result: dict):
    """
    :param result: Здесь записаны значения потенциалов U и V
    :return: вектор потенциалов экспорта (U) и вектор потенциалов импорта (V)
    """
    keys, values = list(result.keys()), list(result.values())
    importers, exporters = [], []
    for i in range(len(keys)):
        if keys[i][0] == 'u':
            exporters.append([int(keys[i].split('_')[1]), values[i]])
        else:
            importers.append([int(keys[i].split('_')[1]), values[i]])
    exporters.sort(key=lambda x: x[0])
    importers.sort(key=lambda x: x[0])
    v_export_pot = [elem[1] for elem in exporters]
    v_import_pot = [elem[1] for elem in importers]
    return v_export_pot, v_import_pot


def update_system(result, system):
    solved = True
    for eq in system:
        if not eq.solved:
            if eq.var_1_sym in result:
                result[eq.var_2_sym] = eq.solve(eq.var_1_sym, result[eq.var_1_sym])
                solved = False
                continue
            if eq.var_2_sym in result:
                result[eq.var_1_sym] = eq.solve(eq.var_2_sym, result[eq.var_2_sym])
                solved = False
                continue
    return solved


def get_filled_count(plan):
    count = 0
    for line in plan:
        for elem in line:
            if elem != '*':
                count += 1
    return count


def check_optimal(v_export, v_import, plan, m_cost):
    for i in range(len(plan)):
        for j in range(len(plan[0])):
            if plan[i][j] == '*':
                if v_import[j] + v_export[i] > m_cost[i][j]:
                    return False
    return True
