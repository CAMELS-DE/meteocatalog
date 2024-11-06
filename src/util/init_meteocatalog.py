from datasets import eobs, hostrada, hyras, radklim_rw, soil_moist_dwd


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
    hyras.download_hyras()
    radklim_rw.download_radklim()
    hostrada.download_hostrada()
    soil_moist_dwd.download_dwd_soil_moist()
    eobs.download_eobs()
