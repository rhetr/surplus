import signal
import sys
from PyQt6.QtWidgets import QApplication

from .surplus import handler, Surplus
# from .config import config


def main() -> int:
    for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGQUIT]:
        signal.signal(sig, handler)
    app = QApplication(sys.argv)

    # style = open(config.settings['Stylesheet'], 'r').read()
    # app.setStyleSheet(style)
    app.aboutToQuit.connect(handler)

    main = Surplus()
    main.show()
    sys.exit(app.exec())
