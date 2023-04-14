# MSOEA

The code for MSOEA# Multi-Scenario Optimization Evolutionary Algorithm-MSOEA

This repository provides implementations for the [paper](https://ieeexplore.ieee.org/document/9910596):

> S. Jiang, G. G. Yen and Z. He, "A Multi-Scenario Optimization Evolutionary Algorithm Based on Transfer Framework," in IEEE Transactions on Evolutionary Computation, 2022, doi: 10.1109/TEVC.2022.3211643.

## Abstract

Multi-scenario optimization problems involve multiple scenarios to be optimized simultaneously, where each scenario corresponds to a multi-objective optimization problem with specific operating conditions. The goal is to find a group of public compromised optimal solutions achieving compromised optimal in every scenario. This type of optimization problems widely exists in real-world applications, but the research on it is few. In this paper, a multi-scenario optimization evolutionary algorithm based on transfer framework is proposed. In one iteration, for each scenario, its knee solutions are recognized as its transfer candidates and are used to construct a constraint hyperplane, which determines whether transfer candidates from other scenarios can be the transferable solutions in this underlying scenario. Then, among all transfer candidates, those accepted by all scenarios are identified as the public compromised optimal solutions and stored in archive. Afterwards, archive updating process is applied to guarantee the optimality of solutions in archive and control the size of archive. Finally, each scenario’s accepted transferable solutions are utilized in its offspring generation, thus achieving information transfer between different scenarios. Experimental results on a group of benchmark functions verify the superiority of the proposed design in terms of both optimality and computational efficiency over existing approaches.

## Parameter Setting

For Python Version: The parameter setting is in the 'Parameter.py', 'MSOEA_f.py'. To run this program, use 'execute.py'

```python
In Parameter.py:
f_num;     # NO.Objective
x_num;     # NO.Decision variables
scenarios; # NO.Scenarios

In MSOEA_f.py:
max_gen;   # NO.Generations
N;         # Size of population
NK;        # Size of selected knee solutions
pc;        # probability of crossover
pm;        # probability of mutation

# Notify: The benchmark problems should be written in a separate document 'Individual.py'.
```

## Citation

If you find our work and this repository useful. Please consider giving a star and citation.

Bibtex:

```
@ARTICLE{MSOEA,
         author={Jiang, Shanlin and Yen, Gary G. and He, Zhenan},
         journal={IEEE Transactions on Evolutionary Computation}, 
         title={A Multi-Scenario Optimization Evolutionary Algorithm Based on Transfer Framework}, 
         year={2022},
         volume={},
         number={},
         pages={1-1},
         doi={10.1109/TEVC.2022.3211643}}
```
