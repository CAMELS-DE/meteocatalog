import os
from datetime import datetime as dt
from pprint import pprint

from json2args import get_parameter, logger

from datasets import hyras


# parse parameters
parameters = get_parameter()

# check if a toolname was set in env
toolname = os.environ.get("TOOL_RUN", "").lower()

# switch the tool
if toolname == "hyras":
    # log
    logger.info(f"Running the HYRAS downloading tool.")
    
    # write parameters to STDOUT.log
    pprint(parameters)

    # run the tool
    hyras.download_hyras()
    

# In any other case, it was not clear which tool to run
else:
    raise AttributeError(f"Either no TOOL_RUN environment variable available, or '{toolname}' is not valid.\n")
