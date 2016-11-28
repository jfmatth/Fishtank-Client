import configmanager
import backup


def LoadDefaults(cfg):
    pass
    
if __name__=="__main__":
    cfg = configmanager.ConfigManager(".")

    if cfg.settings.get("DefaultsLoaded") !=True:
        LoadDefaults(cfg)


