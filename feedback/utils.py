
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

def get_df_from_payload(payload):
    """Creates dataframe (with confidence) for use in analytics
    """
    list_of_dicts = generate_keypoint_dicts(payload)
    raw_df = pd.DataFrame(list_of_dicts)
    return raw_df.pivot(index='timestep', columns='part', values=['x', 'y', 'score'])

def is_confident_detection(df, confidence_threshold=0.8, variability_threshold=0.15, min_pct=0.5):
    """Determines if keypoint detection is passing confidence threshold
    """
    is_confident = (df['score'].mean() >= confidence_threshold)
    is_consistent = (df['score'].std() <= variability_threshold)
    result = is_confident & is_consistent
    observed_pct = result.sum() / result.count()
    return bool(observed_pct <= min_pct)

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

def transform_keypoint_payload(df):
    """Wrapper function that transforms dataframe into smoothed coordinates
    """
    df = strip_joint_likelihood(df)
    df = smooth_coordinate_positions(df)
    return df
