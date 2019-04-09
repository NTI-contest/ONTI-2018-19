def change_coord_sys(obj, cell_shape):
    x = obj[0]//cell_shape[0]
    y = obj[1]//cell_shape[1]
    return (x,y)