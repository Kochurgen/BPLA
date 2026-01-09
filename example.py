import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QListWidget, QStackedWidget, QLabel,
    QPushButton
)
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QStackedWidget Example")
        self.setGeometry(100, 100, 600, 400)

        # Create main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # 1. Create the navigation list (QListWidget)
        self.list_widget = QListWidget()
        self.list_widget.insertItem(0, "Page 1: Welcome")
        self.list_widget.insertItem(1, "Page 2: Settings")
        self.list_widget.insertItem(2, "Page 3: Exit")
        # Connect the current row change signal to the stacked widget index change slot
        self.list_widget.currentRowChanged.connect(self.display_page)
        self.main_layout.addWidget(self.list_widget)

        # 2. Create the stacked widget (QStackedWidget)
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)

        # 3. Create the individual pages/widgets and add them to the stack
        self.page1 = self.create_page_one()
        self.page2 = self.create_page_two()
        self.page3 = self.create_page_three()  # Simple exit page

        self.stacked_widget.addWidget(self.page1)  # Index 0
        self.stacked_widget.addWidget(self.page2)  # Index 1
        self.stacked_widget.addWidget(self.page3)  # Index 2

    def create_page_one(self):
        widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Welcome to Page 1!")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        widget.setLayout(layout)
        return widget

    def create_page_two(self):
        widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel("This is Page 2: Settings.")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        button = QPushButton("Go to Page 1")
        button.clicked.connect(lambda: self.list_widget.setCurrentRow(0))
        layout.addWidget(button)
        widget.setLayout(layout)
        return widget

    def create_page_three(self):
        widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Click the button below to exit.")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        button = QPushButton("Exit Application")
        button.clicked.connect(QApplication.instance().quit)
        layout.addWidget(button)
        widget.setLayout(layout)
        return widget

    def display_page(self, index):
        """Changes the current visible page in the stacked widget."""
        self.stacked_widget.setCurrentIndex(index)  #


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())