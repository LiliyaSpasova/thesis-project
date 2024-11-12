import pysmile
import pysmile_license

def get_cpt_dict(net, node_handle):
    """
    Serializes the CPT (Conditional Probability Table) of a node into a dictionary format
    where each entry is (parent configuration, outcome) -> probability.
    """
    cpt_dict = {}
    cpt = net.get_node_definition(node_handle)
    parents = net.get_parents(node_handle)
    
    dim_count = 1 + len(parents)
    dim_sizes = [net.get_outcome_count(parent) for parent in parents] + [net.get_outcome_count(node_handle)]
    
    coords = [0] * dim_count
    for elem_idx in range(len(cpt)):
        index_to_coords(elem_idx, dim_sizes, coords)
        
        # Create the parent configuration key
        parent_values = tuple(
            (net.get_node_id(parents[parent_idx]), net.get_outcome_id(parents[parent_idx], coords[parent_idx]))
            for parent_idx in range(len(parents))
        )
        
        # Set the probability for this configuration in the dictionary
        outcome = net.get_outcome_id(node_handle, coords[-1])
        prob = cpt[elem_idx]
        
        # Use (parent configuration, outcome) as the key
        cpt_dict[(parent_values, outcome)] = prob
    
    return cpt_dict

def index_to_coords(index, dim_sizes, coords):
    """
    Converts a linear index into multidimensional coordinates based on dimension sizes.
    """
    prod = 1
    for i in range(len(dim_sizes) - 1, -1, -1):
        coords[i] = (index // prod) % dim_sizes[i]
        prod *= dim_sizes[i]

def coords_to_index(coords, dim_sizes):
    """
    Converts multidimensional coordinates into a linear index based on dimension sizes.
    """
    index = 0
    factor = 1
    for i in range(len(dim_sizes) - 1, -1, -1):
        index += coords[i] * factor
        factor *= dim_sizes[i]
    return index

def query_cpt_with_indices(cpt_dict, parent_values, net, node_name):
    """
    Queries a CPT dictionary for all outcomes of a node, including the indices in the original CPT.
    
    Parameters:
    - cpt_dict: The CPT dictionary.
    - parent_values: A list of tuples [(parent_id, parent_value), ...].
    - net: The PySmile network object.
    - node_name: The name of the node to query.
    
    Returns:
    - A dictionary with outcomes as keys, each containing a tuple with (probability, index).
    """
    node_handle = net.get_node(node_name)
    dim_sizes = [net.get_outcome_count(parent) for parent in net.get_parents(node_handle)] + [net.get_outcome_count(node_handle)]
    
    # List all outcomes for the target node
    results = {}
    for outcome in net.get_outcome_ids(node_handle):
        # Build the query key for the (parent configuration, outcome)
        query_key = (tuple(parent_values), outcome)
        
        # Check if the key is in the CPT dictionary
        if query_key in cpt_dict:
            prob = cpt_dict[query_key]
            
            # Calculate the index in the original CPT for this outcome
            coords = []
            for parent_id, parent_value in parent_values:
                parent_handle = next(p for p in net.get_parents(node_handle) if net.get_node_id(p) == parent_id)
                coords.append(net.get_outcome_ids(parent_handle).index(parent_value))
            
            coords.append(net.get_outcome_ids(node_handle).index(outcome))
            original_index = coords_to_index(coords, dim_sizes)
            
            # Store the probability and its index in the results
            results[outcome] = (prob, original_index)
        else:
            results[outcome] = ("Configuration not found", None)
    
    return results

# Load and process the network
net = pysmile.Network()
net.read_file("Brain_Tumor.xdsl")

# Load the original CPT for a specific node
node_name = "SH"

# Get the CPT dictionary
SH_CPT = get_cpt_dict(net, net.get_node(node_name))

# Query the CPT for both 'True' and 'False' outcomes given a specific parent configuration
parent_values = [('B', 'True')]
result = query_cpt_with_indices(SH_CPT, parent_values, net, node_name)

print("Probabilities and original indices for outcomes given parent configuration:")
print(result)
