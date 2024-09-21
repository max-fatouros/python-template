import logging
import sys
import os
from datetime import datetime


from {{ cookiecutter.project_name }}.utils.constants import LOG_LEVEL
from {{ cookiecutter.project_name }}.utils.paths import LOG_DIR

class Logger:
    """
    https://stackoverflow.com/questions/14906764/how-to-redirect-stdout-to-both-file-and-console-with-scripting
    Writes the output from the print function to while still printing it to terminal
    """

    def __init__(self, file):
        self.terminal = sys.stdout
        self.log = open(file, 'w')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def close(self):
        self.log.close()
        sys.stdout = open('/dev/stdout', 'w')

    def flush(self):
        # this flush method is needed for python 3 compatibility.
        # this handles the flush command by doing nothing.
        # you might want to specify some extra behavior here.
        pass


class CustomFormatter(logging.Formatter):
    def __init__(self, *args, do_color=False, **kwargs):
        self.do_color = do_color

        super().__init__(*args, **kwargs)

    COLORS_BY_LEVEL = {
        logging.DEBUG: '34',  # Green
        logging.INFO: '26',  # Blue
        logging.WARNING: '220',  # Yellow
        logging.ERROR: '208',  # Orange
        logging.CRITICAL: '124',  # Red
    }

    def color_format(self, start_escape_code, end_escape_code):
        return f'%(asctime)s {start_escape_code}%(levelname)-8s{end_escape_code} %(module)s:%(lineno)s %(funcName)s :: %(message)s'

    def format(self, record: logging.LogRecord) -> str:
        start_escape_code = ''
        end_escape_code = ''

        if self.do_color:
            start_escape_code += (
                '\033[1;38;5;'
                + self.COLORS_BY_LEVEL[record.levelno]
                + 'm'
            )
            end_escape_code = '\033[m'

        formatter = logging.Formatter(
            self.color_format(
                start_escape_code,
                end_escape_code,
            ),
            datefmt='%H:%M:%S',
        )
        return formatter.format(record)


log = logging.getLogger()


log_file = os.path.join(
    LOG_DIR,
    f'{datetime.now().isoformat()}',
)

# >>> Prints to logs directory in project root
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(
    CustomFormatter(do_color=False),
)
# <<<

# >>> Prints to terminal
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(
    CustomFormatter(do_color=True),
)
# <<<

log.addHandler(stream_handler)
log.addHandler(file_handler)


# "specifies the lowest-severity log message a logger will handle"
log.setLevel(LOG_LEVEL)


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    log.critical(
        'Uncaught exception',
        exc_info=(exc_type, exc_value, exc_traceback),
    )


sys.excepthook = handle_exception
