from numpy.random import uniform, normal
from population import Population
from individual import Individual

class Optimization():

    def __init__(self, init_params):

        initial = {
            'dim': init_params['dim'],
            'heur_available': init_params['heur_available'],
            'lambda': init_params['lambd'],
            'mu': init_params['mu'],
            'function_num': init_params['function_num']
        }
        self.population = Population(initial)
        self.generation_limit = init_params['generation_limit']


    def main(self):

        best = self.population.all_time_best()
        generation = 0

        while generation < self.generation_limit:
            
            self.population.living_selector()

            best = self.population.all_time_best()
            
            print(f"Generation {generation}. Best: {best}")
            generation += 1

        all_times_best = self.population.all_time_best()
        
        print(f"\n\nConverged with individual\nID: {all_times_best.pers_id}\nArguments: {all_times_best.arguments}\nValue: {all_times_best.value}")
