import os
import requests
import tarfile

from json2args import get_parameter, logger


def download_radklim_precipitation(start_year: int, end_year: int, mode: str):
    """
    Download the precipitation data of the Radklim RW dataset from the DWD Climate Data Center.
    
    """
    # create the directory
    os.makedirs("/out/radklim_rw/precipitation", exist_ok=True)

    # get the years
    years = range(start_year, end_year+1)

    # only use dates for which the data is available
    years = [y for y in years if y >= 2001 and y <= 2023]

    # if mode is append, check which years already exist and remove them from the list
    if mode == "append":
        years_exist = [
            y for y in years 
            if all(os.path.exists(f"/out/radklim_rw/precipitation/{y}/RW_2017.002_{y}{month:02d}.nc") for month in range(1, 13)) # check that all 12 months exist
        ]
        years = [y for y in years if y not in years_exist]

        if not years:
            logger.info("No new years to download with mode `append`.")
            return

    # log
    logger.info(f"Downloading precipitation data for the years: {years}")

    # download the data for each year
    for year in years:
        # from https://opendata.dwd.de/climate_environment/CDC/grids_germany/hourly/radolan/reproc/2017_002/netCDF/readme.txt: use different URL for 2021
        if year == 2021:
            url = "https://opendata.dwd.de/climate_environment/CDC/grids_germany/hourly/radolan/reproc/2017_002/netCDF/supplement/RW2017.002_2021_netcdf_supplement.tar.gz"
        else:
            url = f"https://opendata.dwd.de/climate_environment/CDC/grids_germany/hourly/radolan/reproc/2017_002/netCDF/{year}/RW2017.002_{year}_netcdf.tar.gz"
        
        response = requests.get(url)
        with open(f"/out/radklim_rw/precipitation/RW2017.002_{year}_netcdf.tar.gz", "wb") as f:
            f.write(response.content)

        with tarfile.open(f"/out/radklim_rw/precipitation/RW2017.002_{year}_netcdf.tar.gz", "r:gz") as tar:
            tar.extractall(f"/out/radklim_rw/precipitation")

        # remove the tar.gz files
        os.remove(f"/out/radklim_rw/precipitation/RW2017.002_{year}_netcdf.tar.gz")

def download_radklim():
    """
    Download the Radklim RW preciptitation dataset from the DWD Climate Data Center.  
    Radklim RW is a dataset of hourly precipitation data for Germany, with a spatial resolution of 1 km.

    """
    # get the parameters
    parameters = get_parameter()

    # create the directory
    os.makedirs("/out/radklim_rw", exist_ok=True)

    # download the data
    download_radklim_precipitation(parameters["start_year"], parameters["end_year"], parameters["mode"])

    # log
    logger.info(f"Download Radklim RW precipitation data completed.")

    # file permissions
    os.system("chmod -R 777 /out/radklim_rw")
    