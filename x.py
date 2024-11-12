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
    dim_sizes = [0] * dim_count
    for i in range(len(parents)):
        dim_sizes[i] = net.get_outcome_count(parents[i])
    dim_sizes[-1] = net.get_outcome_count(node_handle)
    
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

def query_cpt_with_indices(cpt_dict, parent_values, original_cpt, dim_sizes, net, node_handle):
    """
    Queries a CPT dictionary for both 'True' and 'False' outcomes of a node,
    including the indices of these values in the original CPT.

    Parameters:
    - cpt_dict: The CPT dictionary.
    - parent_values: A list of tuples [(parent_id, parent_value), ...].
    - original_cpt: The original CPT list from the network.
    - dim_sizes: Dimension sizes for navigating the CPT.

    Returns:
    - A dictionary with outcomes as keys, each containing a tuple with (probability, index).
    """
    outcomes = ['True', 'False']
    results = {}
    
    for outcome in outcomes:
        # Build the query key
        query_key = (tuple(parent_values), outcome)
        
        # Check if the key is in the CPT dictionary
        if query_key in cpt_dict:
            prob = cpt_dict[query_key]
            
            # Convert parent values and outcome to coordinates
            coords = []
            for (parent_id, parent_value) in parent_values:
                parent_handle = next((p for p in net.get_parents(node_handle) if net.get_node_id(p) == parent_id), None)
                parent_outcome_idx = net.get_outcome_ids(parent_handle).index(parent_value)
                coords.append(parent_outcome_idx)
            
            outcome_idx = net.get_outcome_ids(node_handle).index(outcome)
            coords.append(outcome_idx)
            
            # Calculate the original index based on these coordinates
            original_index = coords_to_index(coords, dim_sizes)
            
            # Store both the probability and its index in the results
            results[outcome] = (prob, original_index)
        else:
            results[outcome] = ("Configuration not found", None)
    
    return results

# Load and process the network
net = pysmile.Network()
net.read_file("Brain_Tumor.xdsl")

# Load the original CPT for a specific node
node_handle = "ISC"
original_cpt = net.get_node_definition(node_handle)

# Define dimension sizes for the CPT
dim_sizes = [net.get_outcome_count(parent) for parent in net.get_parents(node_handle)] + [net.get_outcome_count(node_handle)]

# Get the CPT dictionary
SH_CPT = get_cpt_dict(net, node_handle)

# Query the CPT for both 'True' and 'False' outcomes given a specific parent configuration
parent_values = [('MC', 'True')]
result = query_cpt_with_indices(SH_CPT, parent_values, original_cpt, dim_sizes, net, node_handle)

print("Probabilities and original indices for outcomes given parent configuration:")
print(result)
