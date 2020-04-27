from cec17_functions import cec17_test_func

class Individual():

    individ_id = 0
    # fitness_function = None
    def __init__(self, init_params=None):
        self.arguments = init_params['arguments']
        self.sigmas = init_params['sigmas']
        Individual.individ_id += 1
        self.pers_id = Individual.individ_id
        self.function_num = init_params['function_num']
        self.value = self.calc_fitness()
        self.closest_worst = init_params['closest_worst']           # think about better initialization

    def __repr__(self):
        return f"ID: {self.pers_id}, value: {self.value}\narguments: {self.arguments}"

    def __lt__(self, other):
        return self.value < other.value

    def calc_fitness(self):
        fitness_ptr = [0]
        cec17_test_func(self.arguments, fitness_ptr, len(self.arguments), 1, self.function_num)
        return fitness_ptr[0]