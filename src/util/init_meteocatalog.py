from datasets import eobs, hostrada, hyras, radklim_rw, soil_moist_dwd

from json2args import logger


def download_all():
    """
    Download all datasets available in the first release of meteocatalog.  
    These datasets are:
    - HYRAS
    - Radklim RW
    - HOSTRADA
    - DWD soil moisture
    - E-OBS

    """
    logger.info(f"Running the HYRAS downloading tool.")
    hyras.download_hyras()

    logger.info(f"Running the Radklim RW downloading tool.")
    radklim_rw.download_radklim()

    logger.info(f"Running the HOSTRADA downloading tool.")
    hostrada.download_hostrada()

    logger.info(f"Running the DWD soil moisture downloading tool.")
    soil_moist_dwd.download_dwd_soil_moist()

    logger.info(f"Running the E-OBS downloading tool.")
    eobs.download_eobs()
