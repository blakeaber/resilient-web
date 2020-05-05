
import numpy as np
import pandas as pd
from functools import partial

from feedback import logic


def lower_arm_down(input_df):
	result = input_df.apply(
		lambda row: logic.bodypart_is_down(row, 'leftWrist', 'leftElbow'), 
		axis=1
	).max()
	return int(result)

def lower_leg_angle_achieved(input_df):
	left_leg = input_df.apply(
		lambda row: logic.angle_between_joints(row, 'leftAnkle', 'leftKnee'), 
		axis=1
	).mean()
	right_leg = input_df.apply(
		lambda row: logic.angle_between_joints(row, 'leftAnkle', 'leftKnee'), 
		axis=1
	).mean()
	legs_angle = np.mean([left_leg, right_leg])
	return bool(int(50 <= legs_angle <= 70) or int(130 <= legs_angle <= 150))

def arms_straight(input_df, acceptable_threshold=10):
	pass

def knees_straight(input_df, acceptable_threshold=10):
	pass

def heels_and_hands_on_floor():
	# analyze minimum y-axis measurements and variability of angle / wrist
	# with respect to same. 
	pass
