from numpy.random import uniform, normal
from population import Population
from individual import Individual

class Optimization():

    def __init__(self, init_params):
        self.dim = init_params['dim']
        self.lmbd = init_params['lmbd']
        self.mu = init_params['mu']
        self.initial_len = init_params['initial_len']
        
        initial = {
            'dim': self.dim,
            'individuals': self.generate_population(),
            'lambda': self.lmbd,
            'mu': self.mu
        }
        self.population = Population(initial)

    def generate_population(self):
        individs = []
        for i in range(self.initial_len):
            arguments, sigmas = [], []
            for j in range(self.dim):
                # give it some use!!!
                argument = uniform(-100, 100)
                sigma = uniform(0, 25) 
                arguments.append(argument)
                sigmas.append(sigma)
            individs.append(Individual({'arguments': arguments, 'sigmas': sigmas}))
        return individs