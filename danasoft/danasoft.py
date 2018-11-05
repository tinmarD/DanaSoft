import sys
import logging
import datetime
from PyQt4.QtGui import QApplication
from mainview import MainWindow
from config import *


if not os.path.exists(LOG_DIR_PATH):
    os.mkdir(LOG_DIR_PATH)

# Log to a file called danasoft_20102018_10h42.log
datetime_str = datetime.datetime.now().strftime('%d%m%Y-%Hh%M')
logging.basicConfig(filename=os.path.join(LOG_DIR_PATH, 'danasoft_{}.log'.format(datetime_str)), level=logging.DEBUG,
                    format='%(asctime)s.%(msecs)03d %(message)s {%(module)s} [%(funcName)s] ')
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)


# Logs uncaught exceptions to the log file, ignore KeyboardInterrupt
# (see : StackOverflow - logging-uncaught-exceptions-in-python)
def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_exception


def main(fullscreen, fill_subject):
    app = QApplication(sys.argv)
    # Create main window
    logging.info("DANASOFT - start")
    window = MainWindow(app, fullscreen, fill_subject)
    window.starttimer()
    if fullscreen:
        window.showFullScreen()
    else:
        window.setFixedSize(MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)
        window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    fullscreen, fill_subject = True, False
    if len(sys.argv) >= 2:
        try:
            fullscreen = bool(int(sys.argv[1]))
        except:
            print('Wrong fullscreen argument {}'.format(sys.argv[1]))
    if len(sys.argv) >= 3:
        try:
            fill_subject = bool(sys.argv[2])
        except:
            print('Wrong fullscreen argument {}'.format(sys.argv[2]))
    main(fullscreen, fill_subject)
