import os
import logging.config

BASE_DIR = os.path.dirname(os.getcwd())

#LOGLEVEL=os.environ.get('LOGLEVEL', 'DEBUG')
LOGLEVEL = "DEBUG"

LOGGING_DICT = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s :%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'logfile': {
            'level':LOGLEVEL,
            'class':'logging.FileHandler',
            'filename': BASE_DIR + "/application.log",
            'formatter' : 'standard',
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
        },
    },

    'loggers': {
        ' __main__':{
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'jobs': {
            'handlers': ['console', 'logfile'],
            'level': 'INFO',
            'propagate': True,
        },
        'backup': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'archive': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
            'propagate': True,
        }
                
    }
}

logging.config.dictConfig(LOGGING_DICT)