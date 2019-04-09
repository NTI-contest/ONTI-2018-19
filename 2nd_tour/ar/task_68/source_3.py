def find_field_edges(frame, aruko_params):
    center = (frame.shape[1]//2, frame.shape[0]//2)
    corners, ids, rejectedImgPoints = aruko_params
    
    ids = [id_[0] for id_ in ids]
    ids_coros = dict(zip(ids, corners))
    #углы к которым мы преобразуем изображение
    warped_size = [[0,0], [0, 10*30-1], [30*8 - 1, 10*30-1], [30*8-1, 0]]
    # очередь Aruko маркеров, для того чтобы в дальнейшем правильно развернуть сетку.
    marker_id_order = [5,6,8,7]
    
    coords_towarp = []
    field_edges = []
    frame = {}    
    bag = 0
    for k, i in enumerate(marker_id_order):
        try:
            smcorner = sorted(ids_coros[i][0], key = lambda coor: dist(coor, center))
            frame[i] = (smcorner[0][0],smcorner[0][1])
            coords_towarp.append(warped_size[k])
            field_edges.append(list(frame[i]))
        except:
            bag = 1
            continue
    return (len(list(frame.keys())), field_edges, coords_towarp)