class_list = []

def dcr_register(cls):
    if hasattr(cls, 'bl_rna'):
        class_list.append(cls)
    return cls
