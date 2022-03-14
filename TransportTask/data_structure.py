class TransportTask:
    def __init__(self, in_m_cost, in_v_exporter, in_v_importer, fine_filename=None):
        self.m_cost = []
        for line in in_m_cost:
            self.m_cost.append(line.copy())
        self.v_exporter = in_v_exporter.copy()  # Количестве груза в каждом пункте хранения
        self.v_importer = in_v_importer.copy()  # Потребности в грузе в пунктах потребления
        self.fine_filename = fine_filename  # Имя файла, где должны быть прописаны штрафы (при необходимости)
        self.make_closed()
        #
        # Как выглядит таблица? c00     c01      c02.... exporter0
        #                       c10     c11      c12 ....exporter1
        #                         ...
        #                       cn0     cn1      cn2 ... exportern
        #                      importer0 importer1 .....

    def make_closed(self):
        sum_export = 0
        sum_import = 0
        for elem in self.v_exporter:
            sum_export += elem
        for elem in self.v_importer:
            sum_import += elem
        if sum_import == sum_export:
            return
        elif sum_export < sum_import:
            print("You enter task with fines!")
            if self.fine_filename is not None:
                fine_file = open(self.fine_filename, "r")
                line = fine_file.readline()
                fines = [int(x) for x in line.split()]
                fine_file.close()
                self.add_fines(fines, sum_export, sum_import)
            else:
                raise "Your task with fines, but no fine_file!"

        else:
            raise "Your task isn't close and isn't for fines!"

    def add_fines(self, fines, sum_export, sum_import):
        self.m_cost.append(fines)
        self.v_exporter.append(sum_import - sum_export)


class OneLineEquation:
    def __init__(self, var_1_sym, var_2_sym, summ):
        self.var_1_sym = var_1_sym
        self.var_2_sym = var_2_sym
        self.var_1_val = 0
        self.var_2_val = 0
        self.sum = summ
        self.solved = False

    def __str__(self):
        return self.var_1_sym + "+" + self.var_2_sym + "=" + str(self.sum)

    def solve(self, in_var_sym, in_var_value):
        self.solved = True
        if in_var_sym == self.var_1_sym:
            self.var_1_val = in_var_value
            self.var_2_val = -in_var_value + self.sum
            return self.var_2_val
        else:
            self.var_2_val = in_var_value
            self.var_1_val = -in_var_value + self.sum
            return self.var_1_val
