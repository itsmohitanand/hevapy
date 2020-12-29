from typing import Union
import numpy as np


def _convert_2d_np(value: Union[list, np.ndarray]) -> np.ndarray:

    if isinstance(value, np.ndarray):
        if len(value.shape) == 1:
            value = value.reshape(value.shape[0], 1)
        else:
            pass
    else:
        value = np.array(value).reshape(len(value), 1)
    return value
