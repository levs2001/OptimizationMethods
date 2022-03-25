import loader
import data_structure as ds
from algorithms import north_west_method, calculate_function
from potential_method import potential_method

if __name__ == '__main__':
    with loader.Loader("problems/our_problem_fines.txt") as data:
        m_cost, v_exporter, v_importer = data
    task = ds.TransportTask(m_cost, v_exporter, v_importer, "problems/our_fines.txt")

    start_plan = north_west_method(task)
    print("Start plan: ")
    for line in start_plan:
        print(line)

    print("Cost matrix: ")
    for line in task.m_cost:
        print(line)

    print("Vector exporter: ", task.v_exporter)
    print("Vector importer: ", task.v_importer)
    print("Start cost (for start plan) : ", calculate_function(start_plan, task.m_cost))

    res_plan = potential_method(task, start_plan)
    print()
    print("Result cost: ", calculate_function(res_plan, task.m_cost))
