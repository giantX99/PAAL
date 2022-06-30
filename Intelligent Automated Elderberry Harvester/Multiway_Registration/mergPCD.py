import copy
import numpy as np
import open3d as o3d

# Visualize pointclouds before registration
def draw_registration_result(source, target, transformation):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    source_temp.paint_uniform_color([1, 0.706, 0]) #yellow
    target_temp.paint_uniform_color([0, 0.651, 0.929]) #blue
    source_temp.transform(transformation)
    o3d.visualization.draw_geometries([source_temp, target_temp])

# Registration initialization
def pairwise_registration(source, target):
    voxel_size = 0.05
    max_correspondence_distance_coarse = voxel_size * 15
    max_correspondence_distance_fine = voxel_size * 1.5
    print("Apply point-to-plane ICP")
    icp_coarse = o3d.pipelines.registration.registration_icp(
        source, target, max_correspondence_distance_coarse, np.identity(4),
        o3d.pipelines.registration.TransformationEstimationPointToPlane())
    icp_fine = o3d.pipelines.registration.registration_icp(
        source, target, max_correspondence_distance_fine,
        icp_coarse.transformation,
        o3d.pipelines.registration.TransformationEstimationPointToPlane())
    transformation_icp = icp_fine.transformation
    information_icp = o3d.pipelines.registration.get_information_matrix_from_point_clouds(
        source, target, max_correspondence_distance_fine,
        icp_fine.transformation)
    return transformation_icp, information_icp


def full_registration(pcds):
    pose_graph = o3d.pipelines.registration.PoseGraph()
    odometry = np.identity(4)
    pose_graph.nodes.append(o3d.pipelines.registration.PoseGraphNode(odometry))
    n_pcds = len(pcds)
    for source_id in range(n_pcds):
        for target_id in range(source_id + 1, n_pcds):
            transformation_icp, information_icp = pairwise_registration(
                pcds[source_id], pcds[target_id])
            print("Build o3d.registration.PoseGraph")
            if target_id == source_id + 1:  # odometry case
                odometry = np.dot(transformation_icp, odometry)
                pose_graph.nodes.append(
                    o3d.pipelines.registration.PoseGraphNode(np.linalg.inv(odometry)))
                pose_graph.edges.append(
                    o3d.pipelines.registration.PoseGraphEdge(source_id,
                                                   target_id,
                                                   transformation_icp,
                                                   information_icp,
                                                   uncertain=False))
            else:  # loop closure case
                pose_graph.edges.append(
                    o3d.pipelines.registration.PoseGraphEdge(source_id,
                                                   target_id,
                                                   transformation_icp,
                                                   information_icp,
                                                   uncertain=True))
    return pose_graph


# Merge 2 pointclouds (source, target) source to target and return the combined pointcloud.
def mergePCD(image1_pcd, image2_pcd):
    # Define parameters
    voxel_size = 0.02
    threshold = 0.02

    # homogeneous matrix of 1.pcd
    transformation_initial = np.asarray([[-0.999984,   -0.00399195 , 0.00400795 , 1.365   ],
                                         [0.00399195, -0.999984, 0.00400795, -2.092],
                                         [-0.00400795, 0.00399195, 0.999984, -1.63],
                                         [0., 0., 0., 1.]])

    # Perform the Initial alignment
    print("[INFO] Initial Alignment")
    evaluation = o3d.pipelines.registration.evaluate_registration(
        image1_pcd, image2_pcd, threshold, transformation_initial)
    print(evaluation)

    # Normalize both point clouds using Voxel sampling to get better results
    image1_pcd.voxel_down_sample(voxel_size=voxel_size)
    image2_pcd.voxel_down_sample(voxel_size=voxel_size)

    # Initialize the vertex information from the point clouds
    image1_pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
    image2_pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))

    # Perform ICP Point-to-Plane registration and find true Transformation matrix
    print("[INFO] Apply point-to-plane ICP")
    registered_images = o3d.pipelines.registration.registration_icp(
        image1_pcd, image2_pcd, threshold, transformation_initial,
        o3d.pipelines.registration.TransformationEstimationPointToPlane())
    print(registered_images)
    print("[INFO] Transformation Matrix:")
    print(registered_images.transformation)

    # Merge Point Clouds
    pcds = [image1_pcd, image2_pcd]
    print("[INFO] Full registration")

    with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug) as cm:
        pose_graph = full_registration(pcds)

    pcd_combined = o3d.geometry.PointCloud()
    pcd_combined = image1_pcd.transform(pose_graph.nodes[0].pose)
    pcd_combined += image2_pcd.transform(pose_graph.nodes[1].pose)
    pcd_combined_down = pcd_combined.voxel_down_sample(voxel_size=voxel_size)

    return pcd_combined_down

'''
main:
    image1_pcd = o3d.io.read_point_cloud("pcd_data_3.pcd") #yellow
    image2_pcd = o3d.io.read_point_cloud("pcd_data_2.pcd") #blue
    pcd_combined  = mergePCD(image1_pcd, image2_pcd)
    o3d.visualization.draw_geometries([pcd_combined])
'''