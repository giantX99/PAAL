from cmath import sqrt

def get_real_xyz(y1, z1, y2, z2, cam_dist):
    #get yr:
    if y1 == y2:
        yr = y1
    else:
        print("Height not well calibrated")
    
    #get zr:
    zr = sqrt(((2*(z1)**2)+(2*(z2)**2)-((cam_dist)**2))/4)

    #get xr:
    s = (z1+z2+cam_dist)/2
    h = 2*sqrt(s*(s-z1)*(s-z2)*(s-cam_dist))/cam_dist
    r = 0
    xr = 0
    if z1 > z2:
        r = sqrt((z2**2)-(h**2))
        xr = -((cam_dist/2)-r)
    if z1 < z2:
        r = sqrt((z1**2)-(h**2))
        xr = ((cam_dist/2)-r)

    return(xr, yr, zr)