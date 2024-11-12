import os
import requests
import tarfile

from json2args import get_parameter, logger


def generate_filename(variable: str) -> str:
    """
    Generate the filename based on the variable.

    """
    abbreviations = {
        "precipitation": "rr",
        "radiation": "qq",
        "humidity": "hu",
        "mean_temperature": "tg",
        "max_temperature": "tx",
        "min_temperature": "tn",
        "air_pressure_sea_level": "pp",
        "wind_speed": "fg"
    }
    abbreviation = abbreviations[variable]
    return f"{abbreviation}_ens_mean_0.1deg_reg_v28.0e.nc"

def download_eobs_variable(variable: str, mode: str):
    """
    Generalized function to download eobs variables.

    """
    # create the directory
    os.makedirs(f"/out/eobs/{variable}", exist_ok=True)

    # if mode is append, check if data for the variable already exists
    if mode == "append":
            if os.path.exists(f"/out/eobs/{variable}/{generate_filename(variable)}"):
                logger.info(f"Data for {variable} already exists, no data is downloaded with mode `append`.")
                return

    # log
    logger.info(f"Downloading {variable} data.")

    # download the data
    filename = generate_filename(variable)

    url = f"https://knmi-ecad-assets-prd.s3.amazonaws.com/ensembles/data/Grid_0.1deg_reg_ensemble/{filename}"
    response = requests.get(url)
    with open(f"/out/eobs/{variable}/{filename}", "wb") as f:
        f.write(response.content)


def download_eobs():
    """
    Download the E-OBS dataset from Copernicus.

    """
    # get the parameters
    parameters = get_parameter()

    # get the variables
    variables = parameters["variables"]

    if variables == "all":
        variables = [
            "precipitation", "radiation", "humidity", "mean_temperature", "max_temperature", 
            "min_temperature", "air_pressure_sea_level", "wind_speed"
        ]
    else:
        variables = [variables]

    # create the directory
    os.makedirs("/out/eobs", exist_ok=True)

    for variable in variables:
        download_eobs_variable(variable, parameters["mode"])

    # log
    logger.info(f"Download of E-OBS variables {variables} completed.")

    # file permissions
    os.system("chmod -R 777 /out/eobs")
