from optimization import Optimization
import argparse

def main():

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='''\
    Evolutionary algorithm / Evolutionary algorithm with a trained heuristic
    ------------------------------------------------------------------------''')

    parser.add_argument('-th', '--train_heuristic', action='store_true', default=False,
                        help="trains a heuristic and adds it to he algorithm")
    parser.add_argument('-f', '--function', action='store', type=int, default=1,
                        help="defines the fitness function: "
                             " 0 - quadratic sum "
                             " 1 - sergei function ")
    parser.add_argument('-sm', '--success_mark', action='store', type=float, default=200000,
                        help="defines the margin of error "
                             "after which the algorithm decides "
                             "that the found solution is sufficient "
                             "and stops "
                             "must be between 0 and 100"
                             "at 0 the algorithm will run until the max number of generations")
    parser.add_argument('-g', '--generations', action='store', type=int, default=1000,
                        help='defines the max number of generations')
    parser.add_argument('-d', '--dimension', action='store', type=int, default=2,
                        help='defines number of dimensions in the fitness function')
    parser.add_argument('-l', '--lambd', action='store', type=int, default=90, help='defines number of parents chosen')
    parser.add_argument('-mu', '--mu', action='store', type=int, default=200, help='defines size of the population')


    args = parser.parse_args()

    inits = {
        'arguments': None,
        'sigmas': None,
        'dim': args.dimension,
        'lmbd': args.lambd,
        'mu': args.mu,
        'function_number': args.function,
        'success_mark': args.success_mark,
        'heur_available': args.train_heuristic
    }
    optimization = Optimization(inits)
    previous_best = None
    best = optimization.population.all_time_best()
    # by now generated the initial population
    generation = 0
    gens_since_last_best = 0
    # later make a better stop condition
    while generation < args.generations and (gens_since_last_best < 100 or generation < args.dimension*100):

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