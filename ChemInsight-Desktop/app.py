import sys
import os
import requests

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QFileDialog,
    QVBoxLayout,
    QMessageBox,
    QFrame,
)
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


API_URL = "http://127.0.0.1:8000/api/upload/"


class ChartCanvas(FigureCanvas):
    def __init__(self):
        self.fig = Figure(figsize=(8.5, 5.2))
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)

    def plot(self, data):
        self.ax.clear()

        types = list(data.keys())
        counts = list(data.values())

        colors = [
            "#2563eb",
            "#16a34a",
            "#f97316",
            "#7c3aed",
            "#dc2626",
            "#0891b2",
            "#0ea5e9",
            "#22c55e",
        ]

        # Bar chart
        self.ax.bar(
            types,
            counts,
            color=colors[: len(types)],
            width=0.6,
        )

        # Axis titles
        self.ax.set_title("Equipment Type Distribution", fontsize=11)
        self.ax.set_xlabel("Equipment Type", fontsize=9)
        self.ax.set_ylabel("Count", fontsize=9)

        # Rotate labels to avoid overlap
        self.ax.tick_params(axis="x", labelrotation=30, labelsize=8)
        self.ax.tick_params(axis="y", labelsize=8)

        # Adjust layout for labels
        self.fig.subplots_adjust(bottom=0.28)

        self.draw()


class ChemInsightDesktop(QWidget):
    def __init__(self):
        super().__init__()

        # ===== Fixed window size =====
        self.setWindowTitle("ChemInsight Desktop")
        self.setFixedSize(820, 760)  # FIXED SIZE
        self.setStyleSheet("background-color:#f5f7fb;")

        main_layout = QVBoxLayout()
        main_layout.setSpacing(12)

        # ===== Header =====
        header = QLabel("ChemInsight – Desktop Analytics Tool")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet(
            "font-size:18px; font-weight:bold; color:#1e293b;"
        )
        main_layout.addWidget(header)

        # ===== Upload Card =====
        upload_card = QFrame()
        upload_card.setStyleSheet(
            "background:#ffffff; border-radius:8px; padding:12px;"
        )

        upload_layout = QVBoxLayout()
        upload_layout.setSpacing(8)

        self.file_label = QLabel("No CSV file selected")
        self.file_label.setStyleSheet("color:#334155;")
        upload_layout.addWidget(self.file_label)

        self.upload_btn = QPushButton("Select & Upload CSV")
        self.upload_btn.setStyleSheet(
            """
            QPushButton {
                background-color:#2563eb;
                color:white;
                padding:8px;
                border-radius:4px;
            }
            QPushButton:hover {
                background-color:#1d4ed8;
            }
            """
        )
        self.upload_btn.clicked.connect(self.select_file)
        upload_layout.addWidget(self.upload_btn)

        upload_card.setLayout(upload_layout)
        main_layout.addWidget(upload_card)

        # ===== Summary Card =====
        self.summary_label = QLabel("")
        self.summary_label.setStyleSheet(
            "background:#ffffff; padding:12px; border-radius:8px; color:#0f172a;"
        )
        self.summary_label.setMinimumHeight(110)
        self.summary_label.setAlignment(Qt.AlignTop)
        main_layout.addWidget(self.summary_label)

        # ===== Chart Card =====
        chart_card = QFrame()
        chart_card.setStyleSheet(
            "background:#ffffff; border-radius:8px; padding:10px;"
        )

        chart_layout = QVBoxLayout()
        self.chart = ChartCanvas()
        chart_layout.addWidget(self.chart)

        chart_card.setLayout(chart_layout)
        main_layout.addWidget(chart_card)

        self.setLayout(main_layout)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv)",
        )

        if file_path:
            file_name = os.path.basename(file_path)
            self.file_label.setText(f"Selected file: {file_name}")
            self.upload_to_api(file_path)

    def upload_to_api(self, file_path):
        try:
            with open(file_path, "rb") as f:
                response = requests.post(API_URL, files={"file": f})

            if response.status_code != 200:
                QMessageBox.critical(self, "Error", "CSV upload failed")
                return

            data = response.json()

            summary_text = (
                f"<b>Total Equipment:</b> {data['total_equipment']}<br>"
                f"<b>Avg Flowrate:</b> {round(data['avg_flowrate'], 2)}<br>"
                f"<b>Avg Pressure:</b> {round(data['avg_pressure'], 2)}<br>"
                f"<b>Avg Temperature:</b> {round(data['avg_temperature'], 2)}"
            )

            self.summary_label.setText(summary_text)
            self.chart.plot(data["type_distribution"])

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChemInsightDesktop()
    window.show()
    sys.exit(app.exec_())
