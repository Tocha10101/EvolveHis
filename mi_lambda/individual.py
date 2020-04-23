from tests import quadratic_sum, sergei_function
class Individual():

    individ_id = 0
    def __init__(self, init_params=None):
        self.arguments = init_params['arguments']
        self.sigmas = init_params['sigmas']
        Individual.individ_id += 1
        self.pers_id = Individual.individ_id
        self.fitness_func = sergei_function
        self.value = self.fitness_func(self.arguments)

    def __repr__(self):
        return f"ID: {self.pers_id}, value: {self.value}\narguments: {self.arguments}"

    def __lt__(self, other):
        return self.value < other.value