def get_objects(img):
    field_width, field_height = img.shape[:2]
    cell_shape = field_width/10,  field_height/8
    
    colors = color_coords(img)
    objects = []
    for color in colors:
        img_coor = color[:-1]
        field_coor = change_coord_sys(img_coor, cell_shape)
        objects.append([color[-1], img_coor, field_coor])