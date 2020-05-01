"""
    Author: Anton Masiukevich
    Date of last modification: 27.04.2020
    Github: https://github.com/Tocha10101
"""

from cec17_functions import cec17_test_func

class Individual():

    individ_id = 0
    def __init__(self, init_params=None):
        self.arguments = init_params['arguments']
        self.sigmas = init_params['sigmas']
        Individual.individ_id += 1
        self.pers_id = Individual.individ_id
        self.function_num = init_params['function_num']
        self.value = self.calc_fitness()
        self.closest_worst = init_params['closest_worst']

    def __repr__(self):
        return f"ID: {self.pers_id}, value: {self.value}\narguments: {self.arguments}"

    def __lt__(self, other):
        return self.value < other.value

    def calc_fitness(self):
        fitness_ptr = [0]
        cec17_test_func(self.arguments, fitness_ptr, len(self.arguments), 1, self.function_num)
        return fitness_ptr[0]

    def describe(self):
        return {
            'value': self.value,
            'arguments': self.arguments
        }

    def toDict(self):

        individ_data = {
            'id': self.pers_id,
            'arguments': self.arguments,
            'sigmas': self.sigmas,
            'value': self.value,
        }
        if self.closest_worst:
            individ_data['closest_worst_id'] = self.closest_worst.pers_id
        else:
             individ_data['closest_worst_id'] = -1
        return individ_data
