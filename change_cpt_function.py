import pysmile
import pysmile_license
import equation_solver
import numpy as np
epsilon=0.05
def update_cpt_with_epsilon(net,node_name):
    
    res=[]
    for i in range(4):
        cpt = net.get_node_definition(node_name)
        print(cpt)
        cpt[0]-=epsilon
        cpt[1]+=epsilon
        net.set_node_definition(node_name,cpt)
        #cpt = net.get_node_definition(node_name)
        #print(cpt)
        net.set_evidence("ISC","True")
        net.update_beliefs()
        beliefs = net.get_node_value("MC")
       # print(beliefs)
        res.append((cpt[0],beliefs[0]))
    return res

def round_list_to_2_decimals(values):
    res=[]
    for (x,y) in values:
        res.append((round(x,2),round(y,2)))
    return res
net = pysmile.Network()
        
net.read_file("Brain_Tumor.xdsl")
sample_values=update_cpt_with_epsilon(net,"ISC")
sample_values=round_list_to_2_decimals(sample_values)
coefficients = []
for (x,y) in sample_values:
    coefficients.append(equation_solver.get_coefficients_1_way(x,y))
coefficients.pop(0)

for (a,b,c,d) in coefficients:
    #ax+b -x*y*c-y*d=0
    #result = 0.75 * 0.993 - 0.001 - 0.75 * 0.48 - 0.48 * 0.786
    print  (a*0.993 - 0.001 + c + d* 0.786)
print(np.linalg.lstsq(coefficients,[0,0,0]))
#print(np.linalg.solve([[0.25,1],[0.3,1]],[0.375,0.38]))




