# tool_template_python

[![Docker Image CI](https://github.com/VForWaTer/tool_template_python/actions/workflows/docker-image.yml/badge.svg)](https://github.com/VForWaTer/tool_template_python/actions/workflows/docker-image.yml)
[![DOI](https://zenodo.org/badge/558416591.svg)](https://zenodo.org/badge/latestdoi/558416591)

This is the template for a generic containerized Python tool following the [Tool Specification](https://vforwater.github.io/tool-specs/) for reusable research software using Docker.

This template can be used to generate new Github repositories from it.


## Datasets

| **Dataset**       | **Provider**                 | **Variables**                                                                                                                                                                                                                                                                                                                    | **Start year**         | **End year** | **Temporal<br>resolution** | **Spatial<br>resolution** | **Coverage** | **CRS**                                  | **TOOL_RUN** | **URL**                                                                                                      |
|-------------------|------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------|--------------|----------------------------|---------------------------|--------------|------------------------------------------|--------------|--------------------------------------------------------------------------------------------------------------|
| HYRAS             | German Weather Service (DWD) | - Precipitation<br>- Radiation<br>- Humidity<br>- Mean temperature<br>- Max temperature<br>- Min temperature                                                                                                                                                                                                                     | 1931 (Precip.)<br>1951 | 2020         | 1 day                      | 1 km² (Precip.)<br>5 km²  | Germany      | ETRS89-extended / LCC Europe (EPSG:3034) | hyras        | [link](https://opendata.dwd.de/climate_environment/CDC/grids_germany/daily/hyras_de/)                        |
| RADKLIM-RW        | German Weather Service (DWD) | - Precipitation                                                                                                                                                                                                                                                                                                                  | 2001                   | 2023         | 1 hour                     | 1 km²                     | Germany      | RADOLAN-grid                             | radklim_rw   | [link](https://opendata.dwd.de/climate_environment/CDC/grids_germany/hourly/radolan/reproc/2017_002/netCDF/) |
| Hostrada          | German Weather Service (DWD) | - Cloud cover<br>- Wind speed and direction (at 10m height)<br>- Near-surface air and dew point temperature (at 2m height)<br>- Relative humidity (at 2m height)<br>- Water vapor mixing ratio (at 2m height)<br>- Air pressure at station height and sea level<br>- Global shortwave radiation<br>- Urban heat island intensity | 1995                   | 2024         | 1 hour                     | 1 km²                     | Germany      | ETRS89-extended / LCC Europe (EPSG:3034) | hostrada     | [link](https://opendata.dwd.de/climate_environment/CDC/grids_germany/hourly/hostrada/)                       |
| E-Obs             | Copernicus                   | - Mean temperature<br>- Minimum temperature<br>- Maximum temperature<br>- Precipitation<br>- Sea level pressure<br>- Relative humidity<br>- Wind speed<br>- Global radiation                                                                                                                                                     | 1950                   | 2024         | 1 day                      | 0.1° x 0.1°               | Europe       | WGS84 (EPSG:4326)                        |              | [link](https://surfobs.climate.copernicus.eu/dataaccess/access_eobs.php)                                     |
| DWD soil moisture | German Weather Service (DWD) | - soil moisture                                                                                                                                                                                                                                                                                                                  | 1991                   | 2024         | 1 day                      | 1 km²                     | Germany      | Gauss Krüger 3. meridian strip.          |              | [link](https://opendata.dwd.de/climate_environment/CDC/grids_germany/daily/soil_moist/)                      |


## How generic?

Tools using this template can be run by the [toolbox-runner](https://github.com/hydrocode-de/tool-runner). 
That is only convenience, the tools implemented using this template are independent of any framework.

The main idea is to implement a common file structure inside container to load inputs and outputs of the 
tool. The template shares this structures with the [R template](https://github.com/vforwater/tool_template_r),
[NodeJS template](https://github.com/vforwater/tool_template_node) and [Octave template](https://github.com/vforwater/tool_template_octave), 
but can be mimiced in any container.

Each container needs at least the following structure:

```
/
|- in/
|  |- parameters.json
|- out/
|  |- ...
|- src/
|  |- tool.yml
|  |- run.py
```

* `parameters.json` are parameters. Whichever framework runs the container, this is how parameters are passed.
* `tool.yml` is the tool specification. It contains metadata about the scope of the tool, the number of endpoints (functions) and their parameters
* `run.py` is the tool itself, or a Python script that handles the execution. It has to capture all outputs and either `print` them to console or create files in `/out`

## How to build the image?

You can build the image from within the root of this repo by
```
docker build -t tbr_python_tempate .
```

Use any tag you like. If you want to run and manage the container with [toolbox-runner](https://github.com/hydrocode-de/tool-runner)
they should be prefixed by `tbr_` to be recognized. 

Alternatively, the contained `.github/workflows/docker-image.yml` will build the image for you 
on new releases on Github. You need to change the target repository in the aforementioned yaml.

## How to run?

This template installs the json2args python package to parse the parameters in the `/in/parameters.json`. This assumes that
the files are not renamed and not moved and there is actually only one tool in the container. For any other case, the environment variables
`PARAM_FILE` can be used to specify a new location for the `parameters.json` and `TOOL_RUN` can be used to specify the tool to be executed.
The `run.py` has to take care of that.

To invoke the docker container directly run something similar to:
```
docker run --rm -it -v /path/to/local/in:/in -v /path/to/local/out:/out -e TOOL_RUN=foobar tbr_python_template
```

Then, the output will be in your local out and based on your local input folder. Stdout and Stderr are also connected to the host.

With the [toolbox runner](https://github.com/hydrocode-de/tool-runner), this is simplyfied:

```python
from toolbox_runner import list_tools
tools = list_tools() # dict with tool names as keys

foobar = tools.get('foobar')  # it has to be present there...
foobar.run(result_path='./', foo_int=1337, foo_string="Please change me")
```
The example above will create a temporary file structure to be mounted into the container and then create a `.tar.gz` on termination of all 
inputs, outputs, specifications and some metadata, including the image sha256 used to create the output in the current working directory.

## What about real tools, no foobar?

Yeah. 

1. change the `tool.yml` to describe your actual tool
2. add any `pip install` or `apt-get install` needed to the dockerfile
3. add additional source code to `/src`
4. change the `run.py` to consume parameters and data from `/in` and useful output in `out`
5. build, run, rock!

