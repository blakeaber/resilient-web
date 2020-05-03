
import numpy as np
from scipy import spatial
from functools import partial


# def is_same_body_position(input_df, target_df, loss_threshold=0.2):
#     """Checks whether candidate body position matches target
#     body position (using Procrustes linear transformation)
#     """
#     (normalized_gold_standard, normalized_input, loss) = spatial.procrustes(
#         target_df, 
#         input_df
#     )
#     return loss <= loss_threshold
    
def angle_between_joints(series, joint1, joint2):
    """
    series: pandas MultiIndex series
    joint1: 'wrist1'
    joint2: 'elbow1'
    """
    def slope_to_degrees(x_delta, y_delta):
        return np.rad2deg(np.arctan2(y_delta, x_delta))

    x_delta = series['x'][joint2] - series['x'][joint1]
    y_delta = series['y'][joint2] - series['y'][joint1]
    degree = slope_to_degrees(x_delta, y_delta)

#     return degree if degree > 0 else abs(degree) - 180
    return degree

def diff_between_joint_angles(row, joint1, joint2, joint3, joint4):
    """
    series: pandas MultiIndex series
    joint1: 'wrist1'
    joint2: 'elbow1'
    joint3: 'elbow1'
    joint4: 'shoulder1'
    """
    bodypart1 = np.abs(angle_between_joints(row, joint1, joint2))
    bodypart2 = np.abs(angle_between_joints(row, joint3, joint4))
    return np.abs(bodypart2 - bodypart1)

def bodypart_matches_degree(row, joint1, joint2, desired_degree, acceptable_threshold):
    degree_actual = np.abs(angle_between_joints(row, joint1, joint2))
    degree_expected = np.abs(desired_degree)
    min_acceptable = degree_expected - acceptable_threshold
    max_acceptable = degree_expected + acceptable_threshold
    return min_acceptable <= degree_actual <= max_acceptable

bodypart_is_vertical = partial(
    bodypart_matches_degree, 
    desired_degree=90, 
    acceptable_threshold=10
)
bodypart_is_horizontal = partial(
    bodypart_matches_degree, 
    desired_degree=180, 
    acceptable_threshold=10
)

