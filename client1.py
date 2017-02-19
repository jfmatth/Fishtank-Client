import configmanager
import backup
import json
import os
import logging

DEFAULTWINDOWS = "defaults.json"

logger = logging.getLogger(__name__)

def LoadDefaults(cfg):
    logger.debug("Loading Defaults")
    s = json.loads(open(DEFAULTWINDOWS).read() )

    for k,v in s.items():
        cfg.settings[k] = v

    cfg.settings["DefaultsLoaded"] = True


if __name__=="__main__":
    cfg = configmanager.ConfigManager(".")

    if cfg.settings.get("DefaultsLoaded") !=True:
        LoadDefaults(cfg)