import pysmile
import pysmile_license
import coefficient_calculator
import numpy as np
from plots import *
from linear_system_solver import solve_system
from cpt_querys  import *
from get_distribution import *
import itertools
import random


def update_cpt_with_epsilon(net,parameters,target,num_variations):
    res=[]
    value_combinations=generate_value_combinations(parameters.__len__(),num_variations)

    target_node_name, target_node_value = target['probability']
    target_node_distribution=get_distribution(net,target)


    parameters_info =extract_parameters_info(parameters)
    for variation in value_combinations:
        coordinates=[]
        for param_index,p in enumerate(parameters_info):
            cpt = p['cpt']
            true_index=p['true_index']
            false_index=p['false_index']
            parameter_node_name=p['name']
            parameter_node_value=p['parameter_node_value']
            distribution=p['distribution']
            cpt[true_index]=variation[param_index]
            cpt[false_index]=1-variation[param_index]
            net.set_node_definition(parameter_node_name,cpt)
            coordinates.append(cpt[ distribution[parameter_node_value][1]])
        if 'given' in target:
            for  key, value in target['given']:
                net.set_evidence(key,value)
        net.update_beliefs()
        beliefs = net.get_node_value(target_node_name)
        coordinates.append(beliefs[0])
        res.append(tuple(coordinates))## change this beliefs index to 1 if the target value is false
    return res

def round_point_values(values):
    res=[]
    for val in values:
        val = val[:-1] + (round(val[-1], 4),)
        res.append(val)
    return res
def round_plot_params(values):
    res=[]
    for (a,b,c,d) in values:
        res.append((round(a,4),round(b,4),round(c,4),round(d,4)))
    return res
def calculate_variations_needed(parameters,target):
    num_parameters=parameters.__len__()
    res=pow(2,num_parameters)
    if 'given' in target:
        res=res*2
    return res

def extract_parameters_info(parameters):
    structured_data = []
    
    for parameter in parameters:
        # Extract parameter details
        parameter_node_name, parameter_node_value = parameter['probability']
    
        # Generate all combinations for the current node
        cpt = net.get_node_definition(parameter_node_name)  # Placeholder function call
        distribution = get_distribution(net, parameter)    # Placeholder function call
        _, true_index = distribution['True']
        _, false_index = distribution['False']
        
        # Save structured data for each combination
        structured_data.append({
                'name': parameter_node_name,
                'true_index': true_index,
                'false_index': false_index,
                'distribution':distribution,
                'parameter_node_value':parameter_node_value,
                'cpt': cpt  # Assuming you want the entire CPT structure
            })
    
    return structured_data

def generate_value_combinations(num_parameters,num_combinations):
    probability_values=[0.1,0.4,0.7,0.9]
    all_combinations = list(itertools.product(probability_values, repeat=num_parameters))
    
    # Check if num_combinations exceeds available combinations
    if num_combinations > len(all_combinations):
        raise ValueError(f"Requested {num_combinations} combinations, but only {len(all_combinations)} are available.")
    
    # Randomly select the desired number of combinations
    selected_combinations = random.sample(all_combinations, num_combinations)
    
    return selected_combinations

net = pysmile.Network()
        
net.read_file("Brain_Tumor.xdsl")
plots_params=[]
plot_points=[]


parameter_1 = {'probability': ('B', 'True'), 'given': [('MC', 'True')]}

parameter_2 = {'probability': ('ISC', 'True'), 'given': [('MC', 'True')]}

parameters=[parameter_1,parameter_2]
target =  {'probability': ('C', 'True')}

needed_variations=calculate_variations_needed(parameters,target)

points=update_cpt_with_epsilon(net,parameters,target,needed_variations)
points=round_point_values(points)
plot_points.append(points)
coefficients = []
if parameters.__len__()==1:
    for (x,y) in points:
        coefficients.append(coefficient_calculator.get_coefficients_1_way(x,y))
    plots_params.append(solve_system(coefficients))
    plot_rational_functions(plots_params=round_plot_params(plots_params),points=plot_points[0])
else:
    for (x,y,z) in points:
        coefficients.append(coefficient_calculator.get_coefficients_2_way(x,y,z))
    plots_params.append(solve_system(coefficients))
    plot_3d_rational_functions(plots_params=plots_params)


