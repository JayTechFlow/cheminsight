import sys
import requests
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QFileDialog,
    QVBoxLayout,
    QMessageBox,
)
from PyQt5.QtCore import Qt

import matplotlib.pyplot as plt

API_URL = "http://127.0.0.1:8000/api/upload/"


class ChemInsightDesktop(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ChemInsight Desktop")
        self.setGeometry(300, 200, 500, 450)

        layout = QVBoxLayout()

        title = QLabel("ChemInsight Desktop Application")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:16px; font-weight:bold;")
        layout.addWidget(title)

        self.file_label = QLabel("No CSV file selected")
        self.file_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.file_label)

        self.upload_btn = QPushButton("Select & Upload CSV")
        self.upload_btn.clicked.connect(self.select_file)
        layout.addWidget(self.upload_btn)

        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignTop)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv)",
        )

        if file_path:
            self.file_label.setText(f"Selected file:\n{file_path}")
            self.upload_to_api(file_path)

    def upload_to_api(self, file_path):
        try:
            with open(file_path, "rb") as f:
                response = requests.post(API_URL, files={"file": f})

            if response.status_code != 200:
                QMessageBox.critical(self, "Error", "Failed to upload CSV")
                return

            data = response.json()

            # Show summary
            summary = (
                f"Total Equipment: {data['total_equipment']}\n"
                f"Avg Flowrate: {round(data['avg_flowrate'], 2)}\n"
                f"Avg Pressure: {round(data['avg_pressure'], 2)}\n"
                f"Avg Temperature: {round(data['avg_temperature'], 2)}"
            )

            self.result_label.setText(summary)

            # Plot chart
            self.plot_chart(data["type_distribution"])

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def plot_chart(self, type_distribution):
        equipment_types = list(type_distribution.keys())
        counts = list(type_distribution.values())

        plt.figure(figsize=(6, 4))
        plt.bar(equipment_types, counts, color="steelblue")
        plt.xlabel("Equipment Type")
        plt.ylabel("Count")
        plt.title("Equipment Type Distribution")
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChemInsightDesktop()
    window.show()
    sys.exit(app.exec_())
