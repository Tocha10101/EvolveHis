"""
    Author: Anton Masiukevich
    Last modification data: 27.04.2020
    Github: https://github.com/Tocha10101
"""

from random import randint
import numpy
from numpy.random import uniform, normal
from math import e
from itertools import permutations
from individual import Individual

class Population():
    
    def __init__(self, init_params):

        self.dim = init_params['dim']
        self.lambd = init_params['lambda']
        self.mu = init_params['mu']

        self.function_num = init_params['function_num']
        self.heur_available = init_params['heur_available']

        self.individuals = self.generate_population()
        self.worst_ever = [self.get_worst(self.individuals)]
        self.best_ever = self.all_time_best()
        self.pool = []
        
    # a function that decides who lives and who dies
    def living_selector(self):

        # copies population to pool
        self.pool = self.individuals.copy()

        # produces the offsprings and adds them to a new generation
        new_generation, best, worst = self.produce()
        self.pool += new_generation

        self.pool.sort()
        self.worst_ever.append(worst)          # appends the worst offspring
        self.pool.remove(worst)

        # drops current self.individuals
        self.individuals = []
        
         # appends best among the offsprings and best ever
        if best is not self.pool[0]:

            self.individuals.append(best)
            self.pool.remove(best)
            
        self.individuals.append(self.pool[0])
        self.pool.remove(self.pool[0])        # appends best among the offsprings

        # the best of all the time remains only in individuals - no need to be chosen
        tickets = []
        for i in range(len(self.pool)):
            for j in range(len(self.pool) - i):
                tickets.append(self.pool[i].pers_id)
        
        numpy.random.shuffle(tickets)

        chosen = []
        for i in range(self.mu - 2):
            index = randint(0, len(tickets) - 1)
            for el in self.pool:
                if el.pers_id == tickets[index]:
                    chosen.append(el)
                    break
            # remove all the used tickets
            tickets = list(filter((tickets[index]).__ne__, tickets))

        self.individuals += chosen
        self.individuals.sort()


    def get_best(self, individs: list):
        best = individs[0]
        for el in individs:
            if el < best:
                best = el
        return best
    
    def all_time_best(self) -> Individual:
        return self.individuals[0]

    def find_closest_worst(self, ind_args):
        closest = self.worst_ever[0]
        min_dist = float('inf')
        for worst in self.worst_ever:
            dist = numpy.sqrt(sum([(ind_args[i] - worst.arguments[i]) ** 2 for i in range(len(worst.arguments))]))
            if dist < min_dist:
                min_dist = dist
                closest = worst
        return closest

    def get_worst(self, individs: list) -> Individual:
        worst = individs[0]
        for el in individs:
            if el > worst:
                worst = el
        return worst

    def euclid_dist(self, arguments: list) -> float:
        return numpy.sqrt(sum([el ** 2 for el in arguments]))

    def produce(self) -> (list, Individual, Individual):
        selected = self.selection()
        mothers, fathers = selected[::2], selected[1::2]
        offsprings = [] # r_population
        for mother, father in zip(mothers, fathers):
            # mutation here doesn't depend on chance
            child1_data, child2_data = self.mutation(*self.crossover(mother, father))
            if self.heur_available:
                child1_data['closest_worst'] = self.find_closest_worst(child1_data['arguments'])
                child2_data['closest_worst'] = self.find_closest_worst(child2_data['arguments'])
                
                # altering the children
                vect1 = [child1_data['arguments'][i] - child1_data['closest_worst'].arguments[i] for i in range(self.dim)]
                vect2 = [child2_data['arguments'][i] - child2_data['closest_worst'].arguments[i] for i in range(self.dim)]
                
                all_time_worst = self.get_worst(self.worst_ever)

                learning_rate1 = 40 * (self.best_ever.value - child1_data['closest_worst'].value) / (((self.best_ever.value - all_time_worst.value) * (self.euclid_dist(vect1) + 1) ** 2) * self.euclid_dist(vect1))
                
                learning_rate2 = 40 * (self.best_ever.value - child2_data['closest_worst'].value) / (((self.best_ever.value - all_time_worst.value) * (self.euclid_dist(vect2) + 1) ** 2) * self.euclid_dist(vect2))
                
                child1_data['arguments'] = [child1_data['arguments'][i] + vect1[i] * learning_rate1 for i in range(self.dim)]
                child2_data['arguments'] = [child2_data['arguments'][i] + vect2[i] * learning_rate2 for i in range(self.dim)]
            else:
                child1_data['closest_worst'] = None
                child2_data['closest_worst'] = None
            child1_data['function_num'] = self.function_num
            child2_data['function_num'] = self.function_num
            child1, child2 = Individual(child1_data), Individual(child2_data)
            offsprings.append(child1)
            offsprings.append(child2)
        return offsprings, self.get_best(offsprings), self.get_worst(offsprings)


    def selection(self):
        t_population = []
        for i in range(self.lambd):
            generated = randint(0, len(self.individuals) - 1)
            el = self.individuals[randint(0, generated)]
            t_population.append(el)
            self.individuals.remove(el)
        return t_population

    # interpolation crossover
    def crossover(self, mother: Individual, father: Individual):
        a = uniform(0, 1)
        child1_args = [a * mother.arguments[i] + (1 - a) * father.arguments[i] for i in range(len(father.arguments))]
        child2_args = [a * father.arguments[i] + (1 - a) * mother.arguments[i] for i in range(len(mother.arguments))]
        child1_sigmas = [a * mother.sigmas[i] + (1 - a) * father.sigmas[i] for i in range(len(father.sigmas))]
        child2_sigmas = [a * father.sigmas[i] + (1 - a) * mother.sigmas[i] for i in range(len(mother.sigmas))]
        return (child1_args, child1_sigmas), (child2_args, child2_sigmas)
        
    # standart mutation for mu + lambda
    def mutation(self, off1_data, off2_data):
        tau1 = 1 / numpy.sqrt(2 * self.dim)
        tau2 = 1 / numpy.sqrt(2 * numpy.sqrt(self.dim))
        sharing_rand = normal(0, 1)
        unique1, unique2 = normal(0, 1), normal(0, 1)

        sigmas_r1, sigmas_r2 = off1_data[1].copy(), off2_data[1].copy()
        for i in range(len(sigmas_r1)):
            sigmas_r1[i], sigmas_r2[i] = sigmas_r1[i] * e ** (tau1 * sharing_rand + tau2 * unique1), sigmas_r2[i] * e ** (tau1 * sharing_rand + tau2 * unique2)

        arguments1 = [off1_data[0][i] + unique1 * sigmas_r1[i] for i in range(len(off1_data[0]))]
        arguments2 = [off2_data[0][i] + unique1 * sigmas_r2[i] for i in range(len(off2_data[0]))]
        return {
            'arguments': arguments1,
            'sigmas': off1_data[1]
        },  {
            'arguments': arguments2,
            'sigmas': off2_data[1]
        }

    def generate_population(self):

        dim_offset = [j + 1 for j in range(self.dim)]
        numpy.random.shuffle(dim_offset)
        individs = []
        for i in range(self.mu):
            arguments, sigmas = [], []
            for j in range(self.dim):
                lower, upper = (i * dim_offset[j] % self.mu) * (200 / self.mu) - 100, (i * dim_offset[j] % self.mu + 1) * (200 / self.mu) - 100
                argument = uniform(upper, lower)
                sigma = uniform(0, 25)
                arguments.append(argument)
                sigmas.append(sigma)
            individs.append( Individual({
                'arguments': arguments,
                'sigmas': sigmas,
                'function_num': self.function_num,
                'closest_worst': None
                })
            )
        return individs
