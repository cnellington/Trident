#!/usr/bin/env python
# coding: utf-8
# Caleb Ellington
# ellinc@uw.edu

# In[1]:


from pydent import AqSession
session = AqSession("", "", "http://52.27.43.242")


# In[2]:


# Get next operation ids method
def get_next_ops(op_ids):
    fvs = session.FieldValue.where({'parent_class': 'Operation', 'parent_id': op_ids, 'role': 'output'})
    fv_ids = [fvs[i].id for i in range(len(fvs))]

    wires = session.Wire.where({'from_id': fv_ids})
    wire_end_ids = [wires[i].to_id for i in range(len(wires))]

    inputs = session.FieldValue.where({'id': wire_end_ids})
    next_op_ids = [inputs[i].parent_id for i in range(len(inputs))]
    return next_op_ids


# In[3]:


# Get initial operation ids
op_type = session.OperationType.find_by_name("Transform Cells").id
transform_ops = session.Operation.where({'operation_type_id': op_type, 'status': 'done'})
transform_op_ids = [transform_ops[i].id for i in range(len(transform_ops))]


# In[4]:


# get next op ids
plate_cells_op_ids = get_next_ops(transform_op_ids)


# In[7]:


# Querying necessary data from operations
plate_fvs = session.FieldValue.where({'parent_class': 'Operation', 'parent_id': plate_cells_op_ids, 'role': 'output'})
fv_sample_ids = [plate_fvs[i].child_sample_id for i in range(len(plate_fvs))]
plasmid_fvs = session.FieldValue.where({'parent_id': fv_sample_ids, 'name': 'Length'})
fv_item_ids = [plate_fvs[i].child_item_id for i in range(len(plate_fvs))]
plates = session.DataAssociation.where({'parent_id': fv_item_ids, 'key': 'num_colonies'})


# In[8]:


# Get item and sample ids
id_colonies = {plates[i].parent_id: plates[i].object['num_colonies'] for i in range(len(plates))}
id_lengths = {plasmid_fvs[i].parent_id: plasmid_fvs[i].value for i in range(len(plasmid_fvs))}


# In[11]:


# Get axes
x_lengths = []
y_colonies = []
for i in range(len(plate_fvs)):
    try:
        length = id_lengths[plate_fvs[i].child_sample_id]
        colonies = id_colonies[plate_fvs[i].child_item_id]
        x_lengths.append(length)
        y_colonies.append(colonies)
    except:
        pass


# In[12]:


# Trim data with 0-length plasmids
trimmed_lengths = []
trimmed_colonies = []
for i in range(len(x_lengths)):
    if(x_lengths[i] == '' or float(x_lengths[i]) < 1):
        pass
    else:
        trimmed_lengths.append(float(x_lengths[i]))
        trimmed_colonies.append(float(y_colonies[i]))


# In[13]:


# Sort by x axis
x_axis, y_axis = (list(t) for t in zip(*sorted(zip(trimmed_lengths, trimmed_colonies))))


# In[14]:


# Gather Data
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
slope, intercept, r_value, p_value, std_err = stats.linregress(x_axis, y_axis)
print("slope: " + str(round(slope, 4)))
print("r value: " + str(round(r_value, 4)))
print("r squared value: " + str(round(r_value**2, 4)))
print("p value: " + str(round(p_value, 8)))
print("std err: " + str(round(std_err, 3)))
plt.scatter(x_axis, y_axis)
plt.plot(np.unique(x_axis), np.poly1d(np.polyfit(x_axis, y_axis, 1))(np.unique(x_axis)))
plt.title('Transformation Efficiency in Aquarium from Integrant Length')
plt.xlabel('Plasmid Length')
plt.ylabel('Colonies Produced')
plt.show()


# In[ ]:




