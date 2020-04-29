from optimization import Optimization
import argparse



parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                    description='''\
Evolutionary algorithm / Evolutionary algorithm with a trained heuristic
------------------------------------------------------------------------''')

parser.add_argument('-th', '--train_heuristic', action='store_true', default=False,
                    help="trains a heuristic and adds it to he algorithm")

# update the functions you have
parser.add_argument('-f', '--function', action='store', type=int, default=1,
                    help="defines the fitness function type: \
                    (1  Bent Cigar Function), \
                    (2 - UNABLE OPTION (official function deleted), \
                    (3 - Zakharov Function), \
                    (4 - Rosenbrock Function), \
                    (5 - Rastrigin Function), \
                    (6 - Schaffer F7 Function), \
                    (7 - Bi-Rastrigin Function), \
                    (8 - Step Rastrigin Function), \
                    (9 - Levy Function), \
                    (10 - Schwefel Function)")
parser.add_argument('-sm', '--success_mark', action='store', type=float, default=1000,
                    help="defines the margin of error "
                            "after which the algorithm decides "
                            "that the found solution is sufficient "
                            "and stops "
                            "must be between 0 and 100"
                            "at 0 the algorithm will run until the max number of generations")
parser.add_argument('-d', '--dimension', action='store', type=int, default=2,
                    help='defines number of dimensions in the fitness function')
parser.add_argument('-l', '--lambd', action='store', type=int, default=90, help='defines number of parents chosen')
parser.add_argument('-mu', '--mu', action='store', type=int, default=200, help='defines size of the population')

args = parser.parse_args()



if __name__ == '__main__':
    inits = {
        'dim': args.dimension,
        'mu': args.mu,
        'lambd': args.lambd,
        'function_num': args.function,
        'generation_limit': args.success_mark,
        'heur_available': args.train_heuristic,
        'starting_generation': 0
    }

    optimization = Optimization(inits)
    optimization.main()

    read_data = optimization.restore_data('data.json')
    optimization.main()
