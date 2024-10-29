import pysmile
# pysmile_license is your license key
import pysmile_license
def hello_smile():
    node_handle="C"
    net = pysmile.Network()
    net.read_file("Brain_Tumor.xdsl")
    net.update_beliefs()
    beliefs = net.get_node_definition("C")
    print(beliefs)
    print(net.get_node_value("C"))
    print(net.get_value_indexing_parents("C"))
    print(net.get_value_indexing_parent_ids("C"))
    print(" Outcomes: " + " ".join(net.get_outcome_ids("C")))
    parent_ids = net.get_parent_ids(node_handle)
    if len(parent_ids) > 0:
        print(" Parents: " + " ".join(parent_ids))
    cpt = net.get_node_definition(node_handle)
    print(cpt)
    parents = net.get_parents(node_handle)
    dim_count = 1 + len(parents)
    dim_sizes = [0] * dim_count
    for i in range(0, dim_count - 1):
        dim_sizes[i] = net.get_outcome_count(parents[i])
        dim_sizes[len(dim_sizes) - 1] = net.get_outcome_count(node_handle)    




def sens_analysis(target_node,parameter):
    target_node_id=target_node.key
    parameter_node_id=parameter.key()
    net = pysmile.Network()
    net.read_file("Brain_Tumor.xdsl")
    beliefs = net.get_node_value("target_node_id")

def load_network(file_path):
    # Load the Bayesian network from a file
    net = pysmile.Network()
    net.read_file(file_path)
    return net

def print_outcome_probability(network, node1, outcome1, node2, outcome2):
    # Print probability for the specific outcome of node1
    try:
        outcome1_index = network.get_outcome_index(node1, outcome1)
        probability1 = network.get_node_value(node1)[outcome1_index]
        print(f"Probability of {node1} = '{outcome1}': {probability1:.4f}")
    except pysmile.SMILEException:
        print(f"Outcome '{outcome1}' not found for node '{node1}'")

    # Print probability for the specific outcome of node2
    try:
        outcome2_index = network.get_outcome_index(node2, outcome2)
        probability2 = network.get_node_value(node2)[outcome2_index]
        print(f"Probability of {node2} = '{outcome2}': {probability2:.4f}")
    except pysmile.SMILEException:
        print(f"Outcome '{outcome2}' not found for node '{node2}'")

hello_smile()