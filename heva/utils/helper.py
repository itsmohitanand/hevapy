import numpy as np


def _convert_np(value):
    if isinstance(value, np.ndarray):
        pass
    else:
        value = np.array(value).reshape(len(value), 1)
    return value
