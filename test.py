from cec17_functions import cec17_test_func

def retrieve(filename):
	with open(filename, 'r') as f:
		data = [] # all the individs_args
		for line in f:
			individ_data = [float(el) for el in line.split()]
			data.append(individ_data)
	return data



# solution vectors
xes = retrieve('input_data/M_10_D10.txt')
dim = 10



# number of objective functions
mx = 1

# the number of chosen function
func_num = 3


# pointer for the calculated fitness
fitness = [0]

# breakpoint()

for el in xes:
    fitness = [0]
    cec17_test_func(el, fitness, dim, mx, func_num)
    print(fitness[0])

vect = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
cec17_test_func(vect, fitness, dim, mx, func_num)

print(fitness[0])