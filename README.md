# meteocatalog

`meteocatalog` is a Docker container with functionalities to download different (mostly meteorological) datasets from sources like the German Weather Service (DWD) or Copernicus.  
The downloaded data is mostly unchanged and organized in a well-structured way.  

`meteocatalog` is built based on the [tool-specs](https://github.com/VForWaTer/tool-specs), a specification that allows standardization of inputs for dockerized tools. Parameters for running `meteocatalog` are defined in `in/input.json` and described in `src/tool.yml`.

Please be not intimidated by the use of Docker or the tool-specs, the execution of the tool is simple and is described here, you only need a working Docker installation on your computer.

## Datasets

`meteocatalog` supports downloading a variety and growing amount of meteorological and environmental datasets, currently available datasets are listed in the table below.

| **Dataset**       | **Provider**                 | **Variables**                                                                                                                                                                                                                                                                                                                    | **Start year**         | **End year** | **Temporal<br>resolution** | **Spatial<br>resolution** | **Coverage** | **CRS**                                  | **TOOL_RUN** | **URL**                                                                                                      |
|-------------------|------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------|--------------|----------------------------|---------------------------|--------------|------------------------------------------|--------------|--------------------------------------------------------------------------------------------------------------|
| HYRAS             | German Weather Service (DWD) | - Precipitation<br>- Radiation<br>- Humidity<br>- Mean temperature<br>- Max temperature<br>- Min temperature                                                                                                                                                                                                                     | 1931 (Precip.)<br>1951 | 2020         | 1 day                      | 1 km² (Precip.)<br>5 km²  | Germany      | ETRS89-extended / LCC Europe (EPSG:3034) | hyras        | [link](https://opendata.dwd.de/climate_environment/CDC/grids_germany/daily/hyras_de/)                        |
| RADKLIM-RW        | German Weather Service (DWD) | - Precipitation                                                                                                                                                                                                                                                                                                                  | 2001                   | 2023         | 1 hour                     | 1 km²                     | Germany      | RADOLAN-grid                             | radklim_rw   | [link](https://opendata.dwd.de/climate_environment/CDC/grids_germany/hourly/radolan/reproc/2017_002/netCDF/) |
| Hostrada          | German Weather Service (DWD) | - Cloud cover<br>- Wind speed and direction (at 10m height)<br>- Near-surface air and dew point temperature (at 2m height)<br>- Relative humidity (at 2m height)<br>- Water vapor mixing ratio (at 2m height)<br>- Air pressure at station height and sea level<br>- Global shortwave radiation<br>- Urban heat island intensity | 1995                   | 2024         | 1 hour                     | 1 km²                     | Germany      | ETRS89-extended / LCC Europe (EPSG:3034) | hostrada     | [link](https://opendata.dwd.de/climate_environment/CDC/grids_germany/hourly/hostrada/)                       |
| E-Obs             | Copernicus                   | - Mean temperature<br>- Minimum temperature<br>- Maximum temperature<br>- Precipitation<br>- Sea level pressure<br>- Relative humidity<br>- Wind speed<br>- Global radiation                                                                                                                                                     | 1950                   | 2024         | 1 day                      | 0.1° x 0.1°               | Europe       | WGS84 (EPSG:4326)                        |              | [link](https://surfobs.climate.copernicus.eu/dataaccess/access_eobs.php)                                     |
| DWD soil moisture | German Weather Service (DWD) | - soil moisture                                                                                                                                                                                                                                                                                                                  | 1991                   | 2024         | 1 day                      | 1 km²                     | Germany      | Gauss Krüger 3. meridian strip.          |              | [link](https://opendata.dwd.de/climate_environment/CDC/grids_germany/daily/soil_moist/)                      |


## How to build the image?

You can build the image from within the root of this repo by
```
docker build -t meteocatalog .
```

## How to run?

Set the parameters for the datasets you want to download via the file `in/input.json` according to the specification in `src/tool.yml`.
This template installs the json2args python package to parse the parameters in the `/in/parameters.json`.

To invoke the docker container directly run something similar to:
```
docker run --rm -it -v ./in:/in -v /path/to/local/out:/out -e TOOL_RUN=init_meteocatalog meteocatalog
```
Replace `/path/to/local/out` with the destination where you want to store the downloaded data and set the environment variable `TOOL_RUN` depending on which dataset you want to download, `init_meteocatalog` will download all the available datasets at once (this requires lots of free disk space).  
