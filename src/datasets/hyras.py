import os
import requests

from json2args import get_parameter, logger


def download_hyras_precipitation(start_year: int, end_year: int, mode: str):
    """
    Download the precipitation data of the HYRAS dataset from the DWD Climate Data Center.
    
    """
    # create the directory
    os.makedirs("/out/hyras/precipitation", exist_ok=True)

    # get the years
    years = range(start_year, end_year+1)

    # only use dates for which the data is available
    years = [y for y in years if y >= 1931 and y <= 2020]

    # if mode is append, check which years already exist and remove them from the list
    if mode == "append":
        years_exist = [y for y in years if os.path.exists(f"/out/hyras/precipitation/pr_hyras_1_{y}_v5-0_de.nc")]
        years = [y for y in years if y not in years_exist]

    # log
    logger.info(f"Downloading precipitation data for the years: {years}")

    # download the data for each year
    for year in years:
        url = f"https://opendata.dwd.de/climate_environment/CDC/grids_germany/daily/hyras_de/precipitation/pr_hyras_1_{year}_v5-0_de.nc"
        response = requests.get(url)
        with open(f"/out/hyras/precipitation/pr_hyras_1_{year}_v5-0_de.nc", "wb") as f:
            f.write(response.content)

def download_hyras_global_radiation(start_year: int, end_year: int, mode: str):
    """
    Download the global radiation data of the HYRAS dataset from the DWD Climate Data Center.
    
    """
    # create the directory
    os.makedirs("/out/hyras/global_radiation", exist_ok=True)

    # get the years
    years = range(start_year, end_year+1)

    # only use dates for which the data is available
    years = [y for y in years if y >= 1951 and y <= 2020]

    # if mode is append, check which years already exist and remove them from the list
    if mode == "append":
        years_exist = [y for y in years if os.path.exists(f"/out/hyras/global_radiation/rsds_hyras_5_{y}_v3-0_de.nc")]
        years = [y for y in years if y not in years_exist]

    # log
    logger.info(f"Downloading global radiation data for the years: {years}")

    # download the data for each year
    for year in years:
        url = f"https://opendata.dwd.de/climate_environment/CDC/grids_germany/daily/hyras_de/radiation_global/rsds_hyras_5_{year}_v3-0_de.nc"
        response = requests.get(url)
        with open(f"/out/hyras/global_radiation/rsds_hyras_5_{year}_v3-0_de.nc", "wb") as f:
            f.write(response.content)

def download_hyras_humidity(start_year: int, end_year: int, mode: str):
    """
    Download the humidity data of the HYRAS dataset from the DWD Climate Data Center.
    
    """
    # create the directory
    os.makedirs("/out/hyras/humidity", exist_ok=True)

    # get the years
    years = range(start_year, end_year+1)

    # only use dates for which the data is available
    years = [y for y in years if y >= 1951 and y <= 2020]

    # if mode is append, check which years already exist and remove them from the list
    if mode == "append":
        years_exist = [y for y in years if os.path.exists(f"/out/hyras/humidity/hurs_hyras_5_{y}_v5-0_de.nc")]
        years = [y for y in years if y not in years_exist]

    # log
    logger.info(f"Downloading humidity data for the years: {years}")

    # download the data for each year
    for year in years:
        url = f"https://opendata.dwd.de/climate_environment/CDC/grids_germany/daily/hyras_de/humidity/hurs_hyras_5_{year}_v5-0_de.nc"
        response = requests.get(url)
        with open(f"/out/hyras/humidity/hurs_hyras_5_{year}_v5-0_de.nc", "wb") as f:
            f.write(response.content)

def download_hyras_mean_air_temperature(start_year: int, end_year: int, mode: str):
    """
    Download the mean air temperature data of the HYRAS dataset from the DWD Climate Data Center.
    
    """
    # create the directory
    os.makedirs("/out/hyras/air_temperature_mean", exist_ok=True)

    # get the years
    years = range(start_year, end_year+1)

    # only use dates for which the data is available
    years = [y for y in years if y >= 1951 and y <= 2020]

    # if mode is append, check which years already exist and remove them from the list
    if mode == "append":
        years_exist = [y for y in years if os.path.exists(f"/out/hyras/air_temperature_mean/tas_hyras_5_{y}_v5-0_de.nc")]
        years = [y for y in years if y not in years_exist]

    # log
    logger.info(f"Downloading mean air temperature data for the years: {years}")

    # download the data for each year
    for year in years:
        url = f"https://opendata.dwd.de/climate_environment/CDC/grids_germany/daily/hyras_de/air_temperature_mean/tas_hyras_5_{year}_v5-0_de.nc"
        response = requests.get(url)
        with open(f"/out/hyras/air_temperature_mean/tas_hyras_5_{year}_v5-0_de.nc", "wb") as f:
            f.write(response.content)

def download_hyras_max_air_temperature(start_year: int, end_year: int, mode: str):
    """
    Download the maximum air temperature data of the HYRAS dataset from the DWD Climate Data Center.
    
    """
    # create the directory
    os.makedirs("/out/hyras/air_temperature_max", exist_ok=True)

    # get the years
    years = range(start_year, end_year+1)

    # only use dates for which the data is available
    years = [y for y in years if y >= 1951 and y <= 2020]

    # if mode is append, check which years already exist and remove them from the list
    if mode == "append":
        years_exist = [y for y in years if os.path.exists(f"/out/hyras/air_temperature_max/tasmax_hyras_5_{y}_v5-0_de.nc")]
        years = [y for y in years if y not in years_exist]

    # log
    logger.info(f"Downloading maximum air temperature data for the years: {years}")

    # download the data for each year
    for year in years:
        url = f"https://opendata.dwd.de/climate_environment/CDC/grids_germany/daily/hyras_de/air_temperature_max/tasmax_hyras_5_{year}_v5-0_de.nc"
        response = requests.get(url)
        with open(f"/out/hyras/air_temperature_max/tasmax_hyras_5_{year}_v5-0_de.nc", "wb") as f:
            f.write(response.content)

def download_hyras_min_air_temperature(start_year: int, end_year: int, mode: str):
    """
    Download the minimum air temperature data of the HYRAS dataset from the DWD Climate Data Center.
    
    """
    # create the directory
    os.makedirs("/out/hyras/air_temperature_min", exist_ok=True)

    # get the years
    years = range(start_year, end_year+1)

    # only use dates for which the data is available
    years = [y for y in years if y >= 1951 and y <= 2020]
    
    # if mode is append, check which years already exist and remove them from the list
    if mode == "append":
        years_exist = [y for y in years if os.path.exists(f"/out/hyras/air_temperature_min/tasmin_hyras_5_{y}_v5-0_de.nc")]
        years = [y for y in years if y not in years_exist]

    # log
    logger.info(f"Downloading minimum air temperature data for the years: {years}")

    # download the data for each year
    for year in years:
        url = f"https://opendata.dwd.de/climate_environment/CDC/grids_germany/daily/hyras_de/air_temperature_min/tasmin_hyras_5_{year}_v5-0_de.nc"
        response = requests.get(url)
        with open(f"/out/hyras/air_temperature_min/tasmin_hyras_5_{year}_v5-0_de.nc", "wb") as f:
            f.write(response.content)

def download_hyras():
    """
    Download variables of the HYRAS dataset from the DWD Climate Data Center:
    - Precipitation
    - Global radiation
    - Humidity
    - Mean air temperature
    - Maximum air temperature
    - Minimum air temperature

    For most variables, a netCDF file with the entire temporal range is available,  
    but this scripts downloads the data in yearly files, to be able to handle read
    parts of the data at a time when working with it.

    """
    # get the parameters
    parameters = get_parameter()

    # get the variables
    variables = parameters["variables"]

    if variables == "all":
        variables = ["precipitation", "radiation_global", "humidity", "air_temperature_mean", "air_temperature_max", "air_temperature_min"]
    else:
        variables = [variables]

    # create the directory
    os.makedirs("/out/hyras", exist_ok=True)

    for variable in variables:
        if variable == "precipitation":
            download_hyras_precipitation(parameters["start_year"], parameters["end_year"], parameters["mode"])
        elif variable == "radiation_global":
            download_hyras_global_radiation(parameters["start_year"], parameters["end_year"], parameters["mode"])
        elif variable == "humidity":
            download_hyras_humidity(parameters["start_year"], parameters["end_year"], parameters["mode"])
        elif variable == "air_temperature_mean":
            download_hyras_mean_air_temperature(parameters["start_year"], parameters["end_year"], parameters["mode"])
        elif variable == "air_temperature_max":
            download_hyras_max_air_temperature(parameters["start_year"], parameters["end_year"], parameters["mode"])
        elif variable == "air_temperature_min":
            download_hyras_min_air_temperature(parameters["start_year"], parameters["end_year"], parameters["mode"])

    # log
    logger.info(f"Download of HYRAS variables {variables} completed.")

    # file permissions
    os.system("chmod -R 777 /out/hyras")
    