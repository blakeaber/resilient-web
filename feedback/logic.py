
import numpy as np
from scipy import spatial
from functools import partial

    
def angle_between_joints(series, joint1, joint2):
    """
    series: pandas MultiIndex series
    joint1: 'wrist1'
    joint2: 'elbow1'
    """
    def slope_to_degrees(x_delta, y_delta):
        return np.rad2deg(np.arctan2(y_delta, x_delta) + np.pi)

    x_delta = series['x'][joint2] - series['x'][joint1]
    y_delta = series['y'][joint2] - series['y'][joint1]
    degree = slope_to_degrees(x_delta, y_delta)

    return degree

def diff_between_joint_angles(row, joint1, joint2, joint3, joint4):
    """
    series: pandas MultiIndex series
    joint1: 'wrist1'
    joint2: 'elbow1'
    joint3: 'elbow1'
    joint4: 'shoulder1'
    """
    bodypart1 = angle_between_joints(row, joint1, joint2)
    bodypart2 = angle_between_joints(row, joint3, joint4)
    return np.abs(bodypart2 - bodypart1)

def bodypart_matches_degree(row, joint1, joint2, degree_expected, acceptable_threshold):
    degree_actual = angle_between_joints(row, joint1, joint2)
    min_acceptable = degree_expected - acceptable_threshold
    max_acceptable = degree_expected + acceptable_threshold
    return min_acceptable <= degree_actual <= max_acceptable

bodypart_is_down = partial(
    bodypart_matches_degree, 
    degree_expected=90, 
    acceptable_threshold=10
)
bodypart_is_up = partial(
    bodypart_matches_degree, 
    degree_expected=270, 
    acceptable_threshold=10
)
bodypart_is_left = partial(
    bodypart_matches_degree, 
    degree_expected=360, 
    acceptable_threshold=10
)
bodypart_is_right = partial(
    bodypart_matches_degree, 
    degree_expected=180, 
    acceptable_threshold=10
)

