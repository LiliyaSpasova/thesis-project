import pysmile
import pysmile_license
import coefficient_calculator
import numpy as np
from plots import plot_rational_functions
from linear_system_solver import solve_system
from cpt_querys  import *

def update_cpt_with_epsilon(net,parameter,target,epsilon):
    res=[]
    node_name, _ = list(parameter['probability'].items())[0]

    target_node_name, _ = list(parameter['probability'].items())[0]
    _,index=get_value_and_index_param(net,parameter)
    for i in range(4):
        cpt = net.get_node_definition(node_name)
        cpt[index]-=epsilon
        cpt[1]+=epsilon
        net.set_node_definition(node_name,cpt)
        
        target_node_name, target_given = target['probability'],target['given']
        for g in target_given:
            node=g[0]
            value=g[1]
            net.set_evidence(node,value)
        #net.set_evidence("ISC","True")
        net.update_beliefs()
        beliefs = net.get_node_value(target_node_name)
       # print(beliefs)
        res.append((cpt[0],beliefs[0]))
    return res

def round_point_values(values):
    res=[]
    for (x,y) in values:
        res.append((round(x,4),round(y,4)))
    return res
def round_plot_params(values):
    res=[]
    for (a,b,c,d) in values:
        res.append((round(a,4),round(b,4),round(c,4),round(d,4)))
    return res
net = pysmile.Network()
        
net.read_file("Brain_Tumor.xdsl")
plots_params=[]
plot_points=[]
epsilons=[0.1,0.12]
parameter = {'probability': {'ISC': 'False'}, 'given': {'MC': 'True'}}
target =  {'probability': {'MC': 'True'}, 'given': {'ISC': 'True'}}
for e in epsilons:
    points=update_cpt_with_epsilon(net,parameter,target,e)
    points=round_point_values(points)
    plot_points.append(points)
    coefficients = []
    for (x,y) in points:
         coefficients.append(coefficient_calculator.get_coefficients_1_way(x,y))
    plots_params.append(solve_system(coefficients))

plots_params.append([0.993,0.001,1,0.786])

plot_rational_functions(plots_params=round_plot_params(plots_params))



