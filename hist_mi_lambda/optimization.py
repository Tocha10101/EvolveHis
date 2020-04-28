from numpy.random import uniform, normal
from population import Population
from individual import Individual
from tests import Tests

class Optimization():

    def __init__(self, init_params):
        self.dim = init_params['dim']
        self.mu = init_params['mu']
        self.function_number = init_params['function_number']
        Individual.fitness_function = Tests(self.function_number).function

        initial = {
            'dim': self.dim,
            'heur_available': init_params['heur_available'],
            'individuals': self.generate_population(),
            'lambda': init_params['lmbd'],
            'mu': init_params['mu'],
            'function_num': self.function_number
        }
        self.population = Population(initial)

    def generate_population(self):
        individs = []
        for i in range(self.mu):
            arguments, sigmas = [], []
            for j in range(self.dim):
                # give it some use!!!
                argument = uniform(-100, 100)
                sigma = uniform(0, 25) 
                arguments.append(argument)
                sigmas.append(sigma)
            individs.append( Individual({
                'arguments': arguments,
                'sigmas': sigmas,
                'function_num': self.function_number,
                'closest_worst': None
                })
            )
        return individs
