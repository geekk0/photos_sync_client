import sys
import asyncio
import configparser
import qasync

from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow


from main import SyncManager
from test_design import Ui_MainWindow


class MyApp(QMainWindow):  # make MyApp a subclass of QMainWindow

    singleton: 'MyApp' = None

    def __init__(self):
        super().__init__()
        self.init_paths()

        self.sync_task = None

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.init_ui()

        self.ui.choose_source_folder.clicked.connect(self.choose_folder_path)
        self.ui.choose_destination_folder.clicked.connect(self.choose_folder_path)
        self.ui.clear_button.clicked.connect(self.clear_log_view)
        self.ui.apply_settings.clicked.connect(self.apply_settings_change)

    def init_ui(self):
        self.setWindowTitle('Перемещение файлов на сервер')

        self.text_widget = self.ui.LogView
        font = self.text_widget.font()  # Get the current font
        font.setPointSize(12)  # Set the font size to your preferred value
        self.text_widget.setFont(font)  # Apply the font back to the widget

        font = self.ui.source_folder_path.font()
        font.setPointSize(12)
        self.ui.source_folder_path.setFont(font)
        self.ui.source_folder_path.setText(self.sync_manager.source_path)

        font = self.ui.destination_folder_path.font()
        font.setPointSize(12)
        self.ui.destination_folder_path.setFont(font)
        self.ui.destination_folder_path.setText(self.sync_manager.destination_path)

        font = self.ui.studio_name_input.font()
        font.setPointSize(12)
        self.ui.studio_name_input.setFont(font)
        self.ui.studio_name_input.setText(self.sync_manager.studio_name)


    def init_paths(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.sync_manager = SyncManager(config)
        self.sync_manager.init_settings()

    def choose_folder_path(self):
        options = QFileDialog.Options()
        folder_name = QFileDialog.getExistingDirectory(self, "Select Folder", "", options=options)

        if folder_name:
            sender = self.sender()
            if sender.objectName() == 'choose_source_folder':
                folder_path_element = self.ui.source_folder_path
            else:
                folder_path_element = self.ui.destination_folder_path
            try:
                folder_path_element.setText(folder_name)
                font = folder_path_element.font()
                font.setPointSize(12)
            except Exception as e:
                print(e)

    def apply_settings_change(self):
        try:
            self.sync_manager.save_settings(source_path=self.ui.source_folder_path.text(),
                                            destination_path=self.ui.destination_folder_path.text(),
                                            studio_name=self.ui.studio_name_input.toPlainText())
            self.init_paths()
            self.ui.tabWidget.setCurrentIndex(0)
            self.restart_monitoring()
        except Exception as e:
            print(e)

    def restart_monitoring(self):
        if self.sync_task:
            self.sync_task.cancel()  # Stop the current task
            self.sync_task = None
            self.init_paths()
            loop = asyncio.get_running_loop()
            loop.call_soon(
                lambda: setattr(self, 'sync_task', asyncio.create_task(self.run_sync_manager(self.text_widget))))
        else:
            self.sync_task = asyncio.create_task(self.run_sync_manager(self.text_widget))

    async def run_sync_manager(self, note_field):
        if not self.sync_manager.error:
            await self.sync_manager.track_created_files(note_field)

    def clear_log_view(self):
        self.ui.LogView.setText("")


    # def restart(self):
    #     self.close()  # Close the current window
    #     MyApp.singleton = MyApp()  # Create a new instance of MyApp
    #     MyApp.singleton.show()  # Show the new window
    #     MyApp.singleton.restart_monitoring()  # Restart the Watchdog observer



def main():
    app = QApplication(sys.argv)
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    ex = MyApp()
    ex.show()

    # with loop:
    #     loop.call_soon(asyncio.create_task, ex.run_sync_manager(ex.text_widget))
    #     sys.exit(loop.run_forever())

    with loop:
        # Schedule a callback that creates the task
        loop.call_soon(lambda: setattr(ex, 'sync_task', asyncio.create_task(ex.run_sync_manager(ex.text_widget))))
        sys.exit(loop.run_forever())


if __name__ == '__main__':
    main()
