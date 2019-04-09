def warp_by_4markers(frame, aruko_params):
    angle_count, field_edges, coords_towarp = find_field_edges(frame, aruko_params)
    rows, cols = (10*30-1, 30*8-1)
    
    if angle_count == 4:
        coords_towarp = np.float32([coords_towarp[:]])
        field_edges = np.float32([field_edges[:]])
        M = cv2.getPerspectiveTransform(field_edges, coords_towarp)
        warped_img = cv2.warpPerspective(frame,M,(cols,rows))
        return warped_img
        
    return warped_img