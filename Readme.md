# Evolutionary algorithm with deeper historical knowlegde
An implementation of (μ + λ) evolutionary algorithm with custom heuristic that uses information about the deeper ancestors than parents.
Tested on benchmark functions of the CEC-2017 Special Session and Competition on Single Objective Numerical Optimization Single Bound Constrained Real-Parameter Optimization.

### Instalation guide
Download all project files and open Linux Terminal in the main folder. Type and execute the following command:
```bash
gcc -fPIC -shared -lm -o cec17_test_func.so cec17_test_func.c
```
This compiles a C file into *cec17_test_func.so*, which will be used by the Python wrapper function in *cec17_function.py*.

Then, type
```bash
python main.py -h
```
or 
```bash
python main.py --help
```
to see the list of the running options.

## Adapter between C code and Python
Used [this code](https://github.com/lacerdamarcelo/cec17_python) to call C functions from Python.

## Original Implementation of benchmark functions (in C)
N. H. Awad, M. Z. Ali, J. J. Liang, B. Y. Qu and P. N. Suganthan, "Problem Definitions and Evaluation Criteria for the CEC 2017 Special Session and Competition on Single Objective Bound Constrained Real-Parameter Numerical Optimization," Technical Report, Nanyang Technological University, Singapore, November 2016
 
