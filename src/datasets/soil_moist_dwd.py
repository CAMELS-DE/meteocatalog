import os
import requests
import tarfile
from glob import glob

import pandas as pd
import xarray as xr

from json2args import get_parameter, logger


def ascii_to_netcdf(start_year: int, end_year: int, mode: str):
    
    # get the years
    years = range(start_year, end_year+1)

    # only use dates for which the data is available
    years = [y for y in years if y >= 1991 and y <= 2024]

    # if mode is append, check which years already exist and remove them from the list
    if mode == "append":
        # check for existing monthly .nc files
        years_exist = [
            y for y in years 
            if all(os.path.exists(f"/out/dwd_soil_moist/soil_moisture/{y}/grids_germany_daily_soil_moist_{y}{month:02d}.nc") for month in range(1, 13))
        ]
        years = [y for y in years if y not in years_exist]

        if not years:
            logger.info("No new years to convert from ASCII to netCDF with mode `append`.")
            return
        
    for year in years:
        for month in range(1, 13):
            # Find the .asc files for the year and month
            asc_files = sorted(glob(f"/out/dwd_soil_moist/soil_moisture/{year}/grids_germany_daily_soil_moist_{year}{month:02d}*.asc"))

            # List to hold DataArrays for each day
            daily_data = []

            # Read daily .asc files of the month
            for file_path in asc_files:
                # Extract date from file name (assuming file name includes YYYYMMDD format)
                date_str = os.path.basename(file_path).split(".")[0].split("_")[-1]
                date = pd.to_datetime(date_str, format="%Y%m%d")

                # Read .asc file as Dataset
                ds = xr.open_dataset(file_path)

                # Assign date coords
                ds = ds.assign_coords(time=[date])

                # Extract the main data variable, rename it, and drop extra dimensions
                da = ds["band_data"].rename("soil_moisture").squeeze(drop=True)

                # Expand time dimension
                da = da.expand_dims(time=[date])

                # Add to monthly data list
                daily_data.append(da)

            # Combine daily DataArrays for the month and save to .nc file
            # for month_str, daily_arrays in monthly_data.items():
            #     monthly_dataset = xr.concat(daily_arrays, dim="time")
            monthly_dataset = xr.concat(daily_data, dim="time")

            # Make it a DataSet
            monthly_dataset = monthly_dataset.to_dataset()

            # Remove unnecessary coordinates and variables
            if "band" in monthly_dataset.dims:
                monthly_dataset = monthly_dataset.squeeze("band", drop=True)
            if "spatial_ref" in monthly_dataset:
                monthly_dataset = monthly_dataset.drop_vars("spatial_ref")

            # Set attributes for the dataset
            monthly_dataset.attrs = {
                "title": "Daily Soil Moisture Data",
                "summary": "Daily soil moisture data collected over Germany, stored with daily temporal resolution.",
                "Conventions": "CF-1.8",
                "source": "Generated from ASCII files",
                "crs": "EPSG:31467",
                "institution": "German Weather Service (DWD)",
                "history": f"Converted from ASCII to netCDF on {pd.Timestamp.now().strftime('%Y-%m-%d')}"
                }

            # Set attributes for the data variable
            monthly_dataset.soil_moisture.attrs = {
                "long_name": "Plant Available Water Content (% NFK)",
                "units": "%"
            }

            # Save to .nc file
            output_file = f"/out/dwd_soil_moist/soil_moisture/{year}/grids_germany_daily_soil_moist_{year}{month:02d}.nc"
            monthly_dataset.to_netcdf(output_file, encoding={"time": {"units": "days since 1900-01-01", "calendar": "gregorian", "dtype": "i4"}})

            # Remove the .asc files of the month
            for file_path in asc_files:
                os.remove(file_path)

def download_dwd_soil_moisture(start_year: int, end_year: int, mode: str, ascii_to_netcdf: bool):
    """
    Download the soil moisture data from the DWD Climate Data Center.
    
    """
    # create the directory
    os.makedirs("/out/dwd_soil_moist/soil_moisture", exist_ok=True)

    # get the years
    years = range(start_year, end_year+1)

    # only use dates for which the data is available
    years = [y for y in years if y >= 1991 and y <= 2024]

    # if mode is append, check which years already exist and remove them from the list
    if mode == "append":
        if ascii_to_netcdf:
            # check for existing monthly .nc files
            years_exist = [
                y for y in years 
                if all(os.path.exists(f"/out/dwd_soil_moist/soil_moisture/{y}/grids_germany_daily_soil_moist_{y}{month:02d}.nc") for month in range(1, 13))
            ]
        else:
            # check for existing .asc files, we only check if the 1st of each month is there
            years_exist = [
                y for y in years 
                if all(os.path.exists(f"/out/dwd_soil_moist/soil_moisture/{y}/grids_germany_daily_soil_moist_{y}{month:02d}01.asc") for month in range(1, 13))
            ]

        # remove the existing years from the list
        years = [y for y in years if y not in years_exist]

        if not years:
            logger.info("No new years to download with mode `append`.")
            return

    # log
    logger.info(f"Downloading soil moisture data for the years: {years}")

    # download the data for each year
    for year in years:
        # create the year directory
        os.makedirs(f"/out/dwd_soil_moist/soil_moisture/{year}", exist_ok=True)

        # download the data for each month
        for month in range(1, 13):
            url = f"https://opendata.dwd.de/climate_environment/CDC/grids_germany/daily/soil_moist/grids_germany_daily_soil_moist_{year}{month:02d}.tgz"
        
            response = requests.get(url)
            with open(f"/out/dwd_soil_moist/soil_moisture/{year}/grids_germany_daily_soil_moist_{year}{month:02d}.tgz", "wb") as f:
                f.write(response.content)

            with tarfile.open(f"/out/dwd_soil_moist/soil_moisture/{year}/grids_germany_daily_soil_moist_{year}{month:02d}.tgz", "r:gz") as tar:
                tar.extractall(f"/out/dwd_soil_moist/soil_moisture/{year}/")

            # remove the tar.gz files
            os.remove(f"/out/dwd_soil_moist/soil_moisture/{year}/grids_germany_daily_soil_moist_{year}{month:02d}.tgz")

def download_dwd_soil_moist():
    """
    Download the soil moisture dataset from the DWD Climate Data Center.  
    DWD soil moisture is a dataset of daily soil moisture data for Germany, with a spatial 
    resolution of 1 km.

    """
    # get the parameters
    parameters = get_parameter()

    # create the directory
    os.makedirs("/out/dwd_soil_moist", exist_ok=True)

    # download the data
    download_dwd_soil_moisture(parameters["start_year"], parameters["end_year"], parameters["mode"], parameters["ascii_to_netcdf"])

    # log
    logger.info(f"Download DWD soil moisture data completed.")

    if parameters["ascii_to_netcdf"]:
        ascii_to_netcdf(parameters["start_year"], parameters["end_year"], parameters["mode"])

        # log
        logger.info("Converted downloaded ascii files to netcdf files.")

    # file permissions
    os.system("chmod -R 777 /out/dwd_soil_moist")
    