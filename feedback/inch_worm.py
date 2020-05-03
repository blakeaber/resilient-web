
import pickle
import numpy as np
import pandas as pd
from functools import partial

from feedback import logic


# with open('./analytics/events/inch_worm_start.pkl', 'rb') as f:
# 	START_INCH_WORM = pickle.load(f)
# 
# 
# with open('./analytics/events/inch_worm_end.pkl', 'rb') as f:
# 	END_INCH_WORM = pickle.load(f)


def knees_straight(row, joint1, joint2, joint3, joint4, acceptable_threshold=10):
    diff = logic.diff_between_joint_angles(row, joint1, joint2, joint3, joint4)
    return 0 <= diff <= acceptable_threshold


def heels_and_hands_on_floor():
    pass


# is_inchworm_start_position = partial(
#     logic.is_same_body_position, 
#     target_df=START_INCH_WORM
# )
# is_inchworm_end_position = partial(
#     logic.is_same_body_position, 
#     target_df=END_INCH_WORM
# )
