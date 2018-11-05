#!/usr/bin/env python
# coding: utf-8

# In[2]:


from pydent import AqSession
session = AqSession("ellinc", "GoHuskies2020!", "http://52.27.43.242")


# In[73]:


transform = session.OperationType.find_by_name("Transform Cells")


# In[4]:


ops = transform.operations


# In[15]:


op_ids = [ops[i].id for i in range(len(ops))]


# In[40]:


fvs = session.FieldValue.where({'parent_class': 'Operation', 'parent_id': op_ids, 'role': 'output'})


# In[41]:


fv_ids = [fvs[i].id for i in range(len(fvs))]
print(fv_ids[0])


# In[38]:


plate_wires = session.Wire.where({'from_id': fv_ids})
plate_2wire_to_ids = [plate_wires[i].to_id for i in range(len(plate_wires))]
check_plate_wires = session.Wire.where({'from_id': plate_wire_to_ids})


# In[48]:


next_op = session.Wire.where({'from_id': fvs[0].id})
op = session.Sample.where({'id': next_op[0].to_id})
print(op)


# In[3]:


# Get next operation ids
def get_next_ops(op_ids):
    fvs = session.FieldValue.where({'parent_class': 'Operation', 'parent_id': op_ids, 'role': 'output'})
    fv_ids = [fvs[i].id for i in range(len(fvs))]

    wires = session.Wire.where({'from_id': fv_ids})
    wire_end_ids = [wires[i].to_id for i in range(len(wires))]

    inputs = session.FieldValue.where({'id': wire_end_ids})
    next_op_ids = [inputs[i].parent_id for i in range(len(inputs))]
    return next_op_ids

op_type = session.OperationType.find_by_name("Transform Cells").id
transform_ops = session.Operation.where({'operation_type_id': op_type, 'status': 'done'})
transform_op_ids = [transform_ops[i].id for i in range(len(transform_ops))]


# In[4]:


plate_cells_op_ids = get_next_ops(transform_op_ids)
check_plate_op_ids = get_next_ops(plate_cells_op_ids)


# In[5]:


check_plate_type_id = 28
transform_cells_type_id = 26


# In[6]:


print(len(transform_op_ids))
print(len(plate_cells_op_ids))
print(len(check_plate_op_ids))


# In[7]:


plate_fvs = session.FieldValue.where({'parent_class': 'Operation', 'parent_id': plate_cells_op_ids, 'role': 'output'})
fv_item_ids = [plate_fvs[i].child_item_id for i in range(len(plate_fvs))]


# In[8]:


plates = session.DataAssociation.where({'parent_id': fv_item_ids, 'key': 'num_colonies'})


# In[9]:


print(plates[0])


# In[10]:


fv_sample_ids = [plate_fvs[i].child_sample_id for i in range(len(plate_fvs))]
plasmid_fvs = session.FieldValue.where({'parent_id': fv_sample_ids, 'name': 'Length'})


# In[11]:


print(plasmid_fvs[3])


# In[12]:


print(len(plate_fvs))
print(len(plates))
print(len(plasmid_fvs))


# In[13]:


id_colonies = {}
id_lengths = {}
id_colonies = {plates[i].parent_id: plates[i].object['num_colonies'] for i in range(len(plates))}
id_lengths = {plasmid_fvs[i].parent_id: plasmid_fvs[i].value for i in range(len(plasmid_fvs))}


# In[14]:


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


# In[15]:


print(len(x_lengths))
print(len(y_colonies))


# In[16]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
plt.plot(x_lengths, y_colonies)
plt.show()


# In[20]:


trimmed_lengths = []
trimmed_colonies = []
for i in range(len(x_lengths)):
    if(x_lengths[i] == '' or float(x_lengths[i]) < 1):
        pass
    else:
        trimmed_lengths.append(float(x_lengths[i]))
        trimmed_colonies.append(float(y_colonies[i]))
        


# In[21]:


x_axis, y_axis = (list(t) for t in zip(*sorted(zip(trimmed_lengths, trimmed_colonies))))


# In[22]:


print(len(x_axis))
print(len(y_axis))


# In[23]:


plt.plot(x_axis, y_axis)
plt.show()


# In[32]:


import statistics
print("length stdev: " + str(statistics.stdev(x_axis)))
print("colonies stdev: " + str(statistics.stdev(y_axis)))


# In[33]:


print("length mean: " + str(statistics.mean(x_axis)))
print("colonies mean: " + str(statistics.mean(y_axis)))


# In[34]:


print("length median: " + str(statistics.median(x_axis)))
print("colonies median: " + str(statistics.median(y_axis)))


# In[35]:


print("length mode: " + str(statistics.mode(x_axis)))
print("colonies mode: " + str(statistics.mode(y_axis)))


# In[36]:


plt.scatter(x_axis, y_axis)
plt.show()


# In[37]:


import numpy as np


# In[39]:


plt.scatter(x_axis, y_axis)
plt.plot(np.unique(x_axis), np.poly1d(np.polyfit(x_axis, y_axis, 1))(np.unique(x_axis)))
plt.show()


# In[42]:


from scipy import stats


# In[43]:


slope, intercept, r_value, p_value, std_err = stats.linregress(x_axis, y_axis)


# In[50]:


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


P[C|n]
P[C|n1<n<n2]
Geometric function for each cluster, find mean and stdev
make plot of lengths and mean with stderr and stdev

f_l = [100,1000]

