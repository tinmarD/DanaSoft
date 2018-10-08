import sys
from PyQt4.QtGui import QApplication
from mainview import MainWindow
from config import *


def main():
    app = QApplication(sys.argv)
    # Create main window
    window = MainWindow(app)
    window.starttimer()
    if FULLSCREEN:
        window.showFullScreen()
    else:
        window.setFixedSize(MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)
        window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
