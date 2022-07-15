import open3d as o3d
import os

def ply_2_pcd(ply_file, file_num):
    ply = o3d.io.read_point_cloud(ply_file)
    pcd_file_name = 'pcd_data_{}.pcd'.format(file_num)
    o3d.io.write_point_cloud(pcd_file_name, ply)
    print(pcd_file_name, 'saved.')

'''
pcd_folder = 'C:/Users/gian-/OneDrive/Documentos/PAAL/data/pcd/'
ply_folder = 'C:/Users/gian-/OneDrive/Documentos/PAAL/data/ply/'
ply_files = [ply for ply in os.listdir(ply_folder)]
file_num = 1
os.chdir(pcd_folder)
for ply in ply_files:
    ply_2_pcd(ply_folder+ply, file_num, pcd_folder)
    file_num += 1
'''