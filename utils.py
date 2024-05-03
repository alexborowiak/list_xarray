import os
import logging, sys
import cftime

import numpy as np
import xarray as xr

from typing import List, Union
logging.basicConfig(format="- %(message)s", filemode='w', stream=sys.stdout)
logger = logging.getLogger()


def get_notebook_logger():
    import logging, sys
    logging.basicConfig(format=" - %(message)s", filemode='w', stream=sys.stdout)
    logger = logging.getLogger()
    return logger


def change_logging_level(logginglevel: str):
    eval(f'logging.getLogger().setLevel(logging.{logginglevel})')
    
def change_logginglevel(logginglevel: str):
    change_logging_level(logginglevel)
    
    
change_logginglevel = change_logging_level





def convert_to_0_start_cftime(time, freq='Y'):
    """
    Convert time values to a new time range with a starting year of 0 (year 1 AD).

    This function takes an array of time values, adjusts them to start from year 0 (1 AD),
    and returns a new time range based on the adjusted values.

    Args:
        time (numpy.ndarray): Array of time values.
        freq (str, optional): Frequency string for the new time range. Default is 'Y' (yearly).

    Returns:
        pandas.DatetimeIndex: A new time range starting from year 0 with the adjusted time values.
    """

    t0, tf = np.take(time, [0, -1])

    # Define the new start time as year 0
    t0_new = cftime.datetime(1, 1, 1, 0, 0, 0, 0, calendar='gregorian')

    # Calculate the new end time based on the difference between the original end time and start time
    tf_new = t0_new + (tf - t0) if freq is None else None

    # Generate a new time range using xarray's cftime_range
    new_time = xr.cftime_range(start=t0_new, end=tf_new, periods=len(time), freq=freq)

    return new_time



def reset_time_to_0_start(ds: Union[xr.Dataset, xr.DataArray]) ->  Union[xr.Dataset, xr.DataArray]:
    """
    Reset the time values of an xarray Dataset or DataArray to start from year 0 (1 AD).

    This function takes an xarray Dataset or DataArray and adjusts its time values to start from year 0 (1 AD).

    Args:
        ds (Union[xr.Dataset, xr.DataArray]): The xarray Dataset or DataArray with time values to be reset.

    Returns:
        Union[xr.Dataset, xr.DataArray]: The input xarray Dataset or DataArray with adjusted time values.
    """

    # Call the convert_to_0_start_cftime function to adjust time values
    ds['time'] = convert_to_0_start_cftime(ds.time.values)
    return ds