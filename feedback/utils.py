
import pandas as pd


def generate_keypoint_dicts(payload):
    """Transforms array of pose estimation keypoints 
    into generator of keypoint data
    """
    def is_valid_entry(entry):
        """Checks if each keypoint contains required fields
        """
        if not entry.get('keypoints'):
            ValueError('Payload missing keypoints field!')
        if not entry['keypoints']:
            ValueError('Keypoints field is empty!')
        return True

    for timestep, entry in enumerate(payload):
        assert is_valid_entry(entry), 'Not a valid entry!'
        for reading in entry['keypoints']:
            yield dict(
                x=reading['position']['x'],
                y=reading['position']['y'],
                part=reading['part'],
                score=reading['score'],
                timestep=timestep
            )

def strip_joint_likelihood(df):
    """Removes likelihood score from the keypoints data
    """
    df = df.loc[:, df.columns.get_level_values(level=0) != 'score']
    return df.astype(float)

def smooth_coordinate_positions(df, window=5):
    """Estimates the actual keypoint location (via rolling window)
    NOTE: Should be using Kalman filters for this
    https://pykalman.github.io/
    """
    return df.rolling(window=window, center=True, min_periods=1).median()

def transform_keypoint_payload(payload):
    """Wrapper function that transforms javascript payload
    into python dataframe
    """
    list_of_dicts = generate_keypoint_dicts(payload)
    raw_df = pd.DataFrame(list_of_dicts)
    df = raw_df.pivot(index='timestep', columns='part', values=['x', 'y', 'score'])
    df = strip_joint_likelihood(df)
    df = smooth_coordinate_positions(df)
    return df
