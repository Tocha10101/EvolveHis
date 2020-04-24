from optimization import Optimization
import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='''\
    Evolutionary algorithm / Evolutionary algorithm with a trained heuristic
    ------------------------------------------------------------------------''')

#parser.add_argument('-th', '--train_heuristic',  action='store_true',  default=False,
#                        help="trains a heuristic and adds it to he algorithm")
#parser.add_argument('-f', '--function', action='store', type=int, default=0,
#                        help="defines the fitness function:"
#                             "0 - quadratic sum"
#                             "1 - sergei function")
#parser.add_argument('-sm', '--success_mark', action='store', type=float, default=0,
#                        help="defines the margin of error"
#                             "after which the algorithm decides"
#                             "that the found solution is sufficient"
#                             "and stops"
#                             "must be between 0 and 100"
#                             "at 0 the algorithm will run until the max number of generations")
#parser.add_argument('-g', '--generations', action='store', type=int,
#                        help='defines the max number of generations')
parser.add_argument('-d', '--dimension', action='store', type=int, default=1, help='defines number of dimensions in the fitness function')
parser.add_argument('-l', '--lambd', action='store', type=int, default=90, help='defines algorithms lambda')
parser.add_argument('-mu', '--mu', action='store', type=int, default=200, help='defines algorithms mu')
parser.add_argument('-il', '--initial_length', action='store', default=200, type=int, help='defines size of an initial population')
args = parser.parse_args()

def main():

    inits = {
        'arguments': None,
        'sigmas': None,
        'dim': args.dimension,
        'lmbd': args.lambd,
        'mu': args.mu,
        'initial_len': args.initial_length
    }
    optimization = Optimization(inits)
    previous_best = None
    best = optimization.population.all_time_best()
    # by now generated the initial population
    generation = 0
    gens_since_last_best = 0
    # later make a better stop condition
    while generation < 1000 and gens_since_last_best < 100:

        # selection here (lambda individuals)
        # optimization.population.selection()

        # produces the offsprings
        
        optimization.population.living_selector()
        generation += 1

        previous_best = best

        best = optimization.population.all_time_best()

        if previous_best is best:
            gens_since_last_best += 1
        else:
            gens_since_last_best = 0
        
        print(f"Generation {generation}. Best: {best}")

    all_times_best = optimization.population.all_time_best()
    
    print(f"\n\nConverged with individual\nID: {all_times_best.pers_id}\nArguments: {all_times_best.arguments}\nValue: {all_times_best.value}")


if __name__ == '__main__':
    main()