import pysmile
import pysmile_license

def get_value_and_index_param(net, parameter):
    # Extract the target node and outcome
    node_name, outcome_value = list(parameter['probability'].items())[0]
    given_conditions = parameter['given']
    
    # Get the node handle and CPT data
    node_handle = net.get_node(node_name)
    cpt = net.get_node_definition(node_handle)
    parents = net.get_parents(node_handle)
    
    # Prepare dimension sizes for index mapping
    dim_sizes = [net.get_outcome_count(parent) for parent in parents] + [net.get_outcome_count(node_handle)]
    
    # Convert the given conditions and outcome to coordinates
    coords = []
    for parent in parents:
        parent_id = net.get_node_id(parent)
        if parent_id in given_conditions:
            outcome_id = net.get_outcome_ids(parent).index(given_conditions[parent_id])
            coords.append(outcome_id)
        else:
            return None, None  # Condition not met
    
    # Add the outcome coordinate
    outcome_idx = net.get_outcome_ids(node_handle).index(outcome_value)
    coords.append(outcome_idx)
    
    # Calculate the index in the original CPT
    index = sum(coord * dim for coord, dim in zip(coords, dim_sizes))
    
    # Retrieve the probability from the CPT
    probability = cpt[index] if index < len(cpt) else None
    return probability, index

def get_outcome_indices(net, parameter):
    # Extract the target node from parameter['probability']
    node_name = list(parameter['probability'].keys())[0]
    given_conditions = parameter['given']
    
    # Get the node handle, CPT data, and parent handles
    node_handle = net.get_node(node_name)
    cpt = net.get_node_definition(node_handle)
    parents = net.get_parents(node_handle)
    
    # Get the outcome counts for parents and the target node
    dim_sizes = [net.get_outcome_count(parent) for parent in parents] + [net.get_outcome_count(node_handle)]
    
    # Initialize a dictionary to store the outcome indices
    outcome_indices = {}
    
    # Generate all possible combinations of outcomes for parent nodes
    parent_outcomes = [net.get_outcome_ids(parent) for parent in parents]
    all_parent_combinations = product(*parent_outcomes)
    
    # For each combination of parent outcomes, calculate the index for each target node outcome
    for parent_combination in all_parent_combinations:
        # Convert given conditions to coordinates
        coords = []
        for i, parent in enumerate(parents):
            parent_id = net.get_node_id(parent)
            # If a given condition exists, match it
            if parent_id in given_conditions:
                outcome_id = net.get_outcome_ids(parent).index(given_conditions[parent_id])
                coords.append(outcome_id)
            else:
                # Otherwise, use the current combination outcome
                coords.append(net.get_outcome_ids(parent).index(parent_combination[i]))
        
        # For each outcome of the node, calculate the index
        for outcome_idx, outcome_value in enumerate(net.get_outcome_ids(node_handle)):
            full_coords = coords + [outcome_idx]
            index = sum(coord * dim for coord, dim in zip(full_coords, dim_sizes))
            outcome_indices[outcome_value] = index
    
    return outcome_indices

def product(*args):
    """Helper function to generate the Cartesian product of given lists."""
    if len(args) == 1:
        return ((x,) for x in args[0])
    else:
        result = []
        for x in args[0]:
            for y in product(*args[1:]):
                result.append((x,) + y)
        return result

