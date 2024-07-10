import sys
import asyncio
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit
from main import SyncManager
import configparser
import qasync

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.text_widget = QTextEdit()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PyQt5 Window with Text Widget')
        self.setGeometry(500, 400, 800, 600)

        layout = QVBoxLayout()
        layout.addWidget(self.text_widget)

        self.setLayout(layout)

    @staticmethod
    async def run_sync_manager(note_field):
        config = configparser.ConfigParser()
        config.read('config.ini')
        sync_manager = SyncManager(config, note_field)
        sync_manager.init_paths()
        if not sync_manager.error:
            await sync_manager.track_created_files()



def main():
    app = QApplication(sys.argv)
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    ex = MyApp()
    ex.show()

    with loop:
        loop.call_soon(asyncio.create_task, ex.run_sync_manager(ex.text_widget))
        sys.exit(loop.run_forever())


if __name__ == '__main__':
    main()
