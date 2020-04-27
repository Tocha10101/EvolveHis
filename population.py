from random import randint
import numpy
from numpy.random import uniform, normal
from math import e
from itertools import permutations
from individual import Individual
class Population():
    
    def __init__(self, init_params):

        self.dim = init_params['dim']
        self.individuals = init_params['individuals']
        self.lambd = init_params['lambda']
        self.mu = init_params['mu']
        self.worst_ever = [self.individuals[-1]]
        self.heur_available = init_params['heur_available']
        self.function_num = init_params['function_num']
        self.pool = []
        
    
    # a function that decides who lives and who dies
    def living_selector(self):

        # copies population to pool
        self.pool = self.individuals.copy()

        # produces the offsprings and adds them to a new generation
        new_generation, best, worst = self.produce()
        self.pool += new_generation

        self.pool.sort()

        self.worst_ever.append(worst)           # appends the worst offspring

        # drops current self.individuals
        self.individuals = []
        
        self.individuals.append(self.pool[0])   # appends best of all the time
        self.individuals.append(best)           # appends best among the offsprings
        self.pool.remove(best)
        self.pool.remove(worst)

        # the best of all the time remains only in individuals - no need to be chosen
        tickets = []
        for i in range(len(self.pool)):
            for j in range(len(self.pool) - i):
                tickets.append(self.pool[i].pers_id)
        
        # Only one permutation needed
        # make a better permutation here !!!!!
        for p in permutations(tickets):
            tickets = list(p)
            break

        chosen = []
        for i in range(self.mu - 2):
            index = randint(0, len(tickets) - 1)
            for el in self.pool:
                if el.pers_id == tickets[index]:
                    chosen.append(el)
                    break
            # remove all the used tickets
            tickets = list(filter((tickets[index]).__ne__, tickets))
        
        # for el in self.pool:
        #     if el in self.individuals:
        #         self.individuals.remove(el)
        self.individuals += chosen
        self.individuals.sort()

    # returns the best offspring (with MINIMUM value)
    def best_of_generation(self, offsprings):
        best = offsprings[0]
        for el in offsprings:
            if el < best:
                best = el
        return best

    def all_time_best(self):
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

    # returns the worst offspring(with MAXIMUM value)
    def worst_of_generation(self, offsprings):
        worst = offsprings[0]
        for el in offsprings:
            if el > worst:
                worst = el
        return worst

    def euclid_dist(self, arguments):
        return numpy.sqrt(sum([el ** 2 for el in arguments]))

    def produce(self):
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
                
                learning_rate1, learning_rate2 = numpy.maximum(40 - self.euclid_dist(vect1), 0) / self.euclid_dist(vect1), numpy.maximum(40 - self.euclid_dist(vect2), 0) /self.euclid_dist(vect2)
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
        return offsprings, self.best_of_generation(offsprings), self.worst_of_generation(offsprings)


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
        