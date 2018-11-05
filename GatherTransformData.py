#!/usr/bin/env python
# coding: utf-8

# In[6]:


from pydent import AqSession
session = AqSession("", "", "http://52.27.43.242")

def get_ops(name):
    op_type = session.OperationType.find_by_name("Transform Cells")
    ops = op_type.operations
    return ops

def get_op_ids(ops):
    op_ids = [ops[i].id for i in range(len(ops))]
    return op_ids

def get_fvs(op_ids):
    fvs = session.FieldValue.where({'parent_class': 'Operation', 'parent_id': op_ids, 'role': 'output'})
    return fvs
    
def get_fv_ids(fvs):
    fv_ids = [fvs[i].id for i in range(len(fvs))]
    return fv_ids

def get_wires(fvs_ids):
    wires = session.Wire.where({'from_id': fv_ids})
    return wires

def get_wire_end_ids(wires):
    wire_end_ids = [wires[i].to_id for i in range(len(wires))]
    return wire_end_ids

def get_inputs(wire_end_ids):
    inputs = session.FieldValue.where({'id': wire_end_ids})
    return inputs

def get_op_ids_from_inputs(inputs):
    next_op_ids = [inputs[i].parent_id for i in range(len(inputs))]
    return next_op_ids

# Valid Op IDS
check_plate_type_id = 28
transform_cells_type_id = 26


# In[15]:


# t_ops = get_ops("Transform Cells")
# t_op_ids = get_op_ids(t_ops)
# t_fvs = get_fvs(t_op_ids)
# t_fv_ids = get_fv_ids(t_fvs)
# t_wires = get_wires()
transforms = get_ops("Transform Cells")
checks = get_ops("Check Plate")


# In[18]:


associations = {}
for i in range(len(transforms)):
    for j in range(len(checks)):
        if(transforms[i].created_at == checks[j].created_at):
            associations[transforms[i]] = checks[j]
            break


# In[29]:


t_fvs = get_fvs(get_op_ids(transforms))
c_fvs = get_fvs(get_op_ids(checks))


# In[45]:


t_sample_ids = [t_fvs[i].child_sample_id for i in range(len(t_fvs))]
t_samples = session.Sample.where({'id': t_sample_ids, 'sample_type_id': 2})


# In[49]:


t_sample_fvs = session.FieldValue.where({'parent_id': t_sample_ids, 'name': 'Length', ''})


# In[75]:


c_item_ids = [c_fvs[i].child_item_id for i in range(len(c_fvs))]


# In[96]:


c_items = session.Item.find(c_item_ids[:400])


# In[95]:


[print(c_items[i].data) for i in range(len(c_items))]


# In[ ]:




