from optimization import Optimization


def main():

    inits = {
        'arguments': None,
        'sigmas': None,
        'dim': 1,
        'lmbd': 90,
        'mu': 200,
        'initial_len': 200
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