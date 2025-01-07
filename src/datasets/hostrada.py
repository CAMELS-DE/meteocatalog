import os
import requests
import calendar

from json2args import get_parameter, logger


def generate_filename(variable: str, year: int, month: int) -> str:
    """
    Generate the filename based on the variable, year, and month.

    """
    abbreviations = {
        "cloud_cover": "clt",
        "wind_speed": "sfcWind",
        "wind_direction": "sfcWind_direction",
        "air_temperature_mean": "tas",
        "dew_point_temperature": "tdew",
        "relative_humidity": "hurs",
        "water_vapor_mixing_ratio": "mixr",
        "air_pressure_sea_level": "psl",
        "air_pressure_surface": "ps",
        "global_shortwave_radiation": "rsds",
        "urban_heat_island_intensity": "uhi"
    }
    abbreviation = abbreviations[variable]
    last_day = calendar.monthrange(year, month)[1]
    return f"{abbreviation}_1hr_HOSTRADA-v1-0_BE_gn_{year}{month:02d}0100-{year}{month:02d}{last_day}23.nc"

def download_hostrada_variable(variable: str, start_year: int, end_year: int, mode: str):
    """
    Generalized function to download hostrada variables.
        
    """
    # create the directory
    os.makedirs(f"/out/hostrada/{variable}", exist_ok=True)

    # get the years
    years = range(start_year, end_year + 1)

    # only use dates for which the data is available
    years = [y for y in years if y >= 1995 and y <= 2024]

    # if mode is append, check which years already exist and remove them from the list
    if mode == "append":
        years_exist = [
            y for y in years
            if all(os.path.exists(f"/out/hostrada/{variable}/{y}/{generate_filename(variable, y, month)}") for month in range(1, 13))  # check that all 12 months exist
        ]
        years = [y for y in years if y not in years_exist]

        if not years:
            logger.info(f"No new years to download for {variable} with mode `append`.")
            return

    # log
    logger.info(f"Downloading {variable} data for the years: {years}")

    # download the data for each year
    for year in years:
        # create the year directory
        os.makedirs(f"/out/hostrada/{variable}/{year}", exist_ok=True)

        # download the data for each month
        for month in range(1, 13):
            filename = generate_filename(variable, year, month)

            url = f"https://opendata.dwd.de/climate_environment/CDC/grids_germany/hourly/hostrada/{variable}/{filename}"

            # Check if the URL exists
            head_response = requests.head(url)
            if head_response.status_code != 200:
                logger.info(f"Data for '{url}' is not available, check if the url is correct.")
                continue

            response = requests.get(url)
            with open(f"/out/hostrada/{variable}/{year}/{filename}", "wb") as f:
                f.write(response.content)

def download_hostrada():
    """
    Download the hostrada dataset from the DWD Climate Data Center.

    """
    # get the parameters
    parameters = get_parameter()

    # get the variables
    variables = parameters["variables"]

    if variables == "all":
        variables = [
            "cloud_cover", "wind_speed", "wind_direction", "air_temperature_mean", 
            "dew_point_temperature", "relative_humidity", "water_vapor_mixing_ratio", 
            "air_pressure_sea_level", "air_pressure_surface", "global_shortwave_radiation", 
            "urban_heat_island_intensity"
        ]
    else:
        variables = [variables]

    # create the directory
    os.makedirs("/out/hostrada", exist_ok=True)

    for variable in variables:
        download_hostrada_variable(variable, parameters["start_year"], parameters["end_year"], parameters["mode"])

    # log
    logger.info(f"Download of hostrada variables {variables} completed.")

    # file permissions
    os.system("chmod -R 777 /out/hostrada")