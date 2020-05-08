from numpy.random import uniform, normal
from population import Population
from individual import Individual
import json
import time

class Optimization():

    def __init__(self, init_params):

        self.dim = init_params['dim']
        self.lambd = init_params['lambda']
        self.mu = init_params['mu']
        self.function_num = init_params['function_num']

        initial = {
            'dim': init_params['dim'],
            'heur_available': init_params['heur_available'],
            'lambda': init_params['lambda'],
            'mu': init_params['mu'],
            'function_num': init_params['function_num']
        }
        self.population = Population(initial)
        self.generation_limit = init_params['generation_limit']
        self.current_generation = init_params['starting_generation']


    def main(self):

        best = self.population.all_time_best()
        # now we can start from
        previous_best = None
        change_iteration = self.current_generation
        tic = time.perf_counter()
        while  self.current_generation  < self.generation_limit:
            
            self.population.living_selector()

            best = self.population.all_time_best()

            if best is previous_best:
                change_iteration += 1
            else:
                previous_best = best
                change_iteration = 0
            
            print(f"Generation {self.current_generation}. Best: {best}")
             
            self.current_generation += 1    

        toc = time.perf_counter()
        all_times_best = self.population.all_time_best()
        
        print(f"\n\nConverged with individual\nID: {all_times_best.pers_id}\nArguments: {all_times_best.arguments}\nValue: {all_times_best.value}")
        return all_times_best, toc - tic, change_iteration

    def save_data(self, json_filename):
        data = {
            'dim': self.dim,
            'lambda': self.lambd,
            'mu': self.mu,
            'function_num': self.function_num,
            'generation_limit': self.generation_limit,
            'starting_generation': self.current_generation
        }

        population = {
            'individ_id': Individual.individ_id,
            'individuals': [],
            'worst_ever': []
        }

        for el in self.population.worst_ever:
            population['worst_ever'].append(el.toDict())
        
        for el in self.population.individuals:
            population['individuals'].append(el.toDict())

        data['population'] = population
        with open(json_filename, 'w') as jf:
            json.dump(data, jf, indent=4)
        return data

    def restore_data(self, json_filename):

        read_data = {}
        with open(json_filename, 'r') as jf:
            read_data = json.loads(jf.read())


        self.dim = read_data['dim']
        self.lambd = read_data['lambda']
        self.mu = read_data['mu']
        self.function_num = read_data['function_num']
        self.generation_limit = read_data['generation_limit']
        self.current_generation = read_data['starting_generation']


        Individual.individ_id = read_data['population']['individ_id']
        # population restoring
        restored_population = {}


        # restores worst_ever
        for el in read_data['population']['worst_ever']:
            # automaticly calculates fitness
            restored_worst_data = {
                'id': el['id'],
                'arguments': el['arguments'],
                'sigmas': el['sigmas'],
                'function_num': self.function_num
            }

            if el['closest_worst_id'] == -1:
                restored_worst_data['closest_worst'] = None
            else:
                for i in range(len(self.population.worst_ever)):
                    if self.population.worst_ever[i].pers_id == el['closest_worst_id']:
                        restored_worst_data['closest_worst'] = self.population.worst_ever[i]
                        break

            restored_worst = Individual(restored_worst_data)
            assert el['value'] == restored_worst.value
                
            self.population.worst_ever.append(restored_worst)

        for el in read_data['population']['individuals']:

            restored_individ_data = {
                'id': el['id'],
                'arguments': el['arguments'],
                'sigmas': el['sigmas'],
                'function_num': self.function_num
            }
            
            if el['closest_worst_id'] == -1:
                restored_individ_data['closest_worst'] = None
            else:
                for i in range(len(self.population.worst_ever)):
                    if self.population.worst_ever[i].pers_id == el['closest_worst_id']:
                        restored_individ_data['closest_worst'] = self.population.worst_ever[i]
                        break

            restored_individ = Individual(restored_individ_data)
            assert el['value'] == restored_individ.value

            self.population.individuals.append(restored_individ)

        return read_data