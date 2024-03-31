import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QSlider,
    QSpinBox,
    QVBoxLayout,
)


class HoughTransformGroupBox(QGroupBox):
    def __init__(self, title):
        super().__init__(title)
        self.title = title
        self.hough_transform = None  # Reference to the associated Noise effect

        self.initUI()

    def initUI(self):
        # Vertical layout for the main content
        self.main_layout = QVBoxLayout()

        # Horizontal layout for label and combo box
        self.hough_type_hbox = QHBoxLayout()
        self.hough_type_label = QLabel("HT Type")
        self.hough_type_combo_box = QComboBox()
        self.hough_type_combo_box.addItems(["Line", "Circle", "Ellipse"])
        self.hough_type_hbox.addWidget(self.hough_type_label)
        self.hough_type_hbox.addWidget(self.hough_type_combo_box)

        # Attributes for the Circle Detection
        self.line_attributes_vbox = QVBoxLayout()
        self.line_threshold_hbox = QHBoxLayout()
        self.line_threshold_label = QLabel("Threshold")
        self.line_threshold_slider = QSlider(Qt.Horizontal)
        self.line_threshold_slider.setRange(0, 800)
        self.line_threshold_slider.setValue(101)
        self.line_threshold_spinbox = QSpinBox()
        self.line_threshold_spinbox.setRange(0, 800)
        self.line_threshold_spinbox.setValue(101)
        self.line_threshold_slider.valueChanged.connect(
            self.line_threshold_spinbox.setValue
        )
        self.line_threshold_spinbox.valueChanged.connect(
            self.line_threshold_slider.setValue
        )
        self.line_threshold_hbox.addWidget(self.line_threshold_slider)
        self.line_threshold_hbox.addWidget(self.line_threshold_spinbox)

        self.line_attributes_vbox.addWidget(self.line_threshold_label)
        self.line_attributes_vbox.addLayout(self.line_threshold_hbox)

        # Attributes for the Circle Detection
        self.circle_attributes_vbox = QVBoxLayout()
        self.min_radius_hbox = QHBoxLayout()
        self.min_radius_label = QLabel("Min Radius")
        self.min_radius_slider = QSlider(Qt.Horizontal)
        self.min_radius_slider.setRange(0, 800)
        self.min_radius_slider.setValue(10)
        self.min_radius_spinbox = QSpinBox()
        self.min_radius_spinbox.setRange(0, 800)
        self.min_radius_spinbox.setValue(10)
        self.min_radius_slider.valueChanged.connect(self.min_radius_spinbox.setValue)
        self.min_radius_spinbox.valueChanged.connect(self.min_radius_slider.setValue)
        self.min_radius_hbox.addWidget(self.min_radius_slider)
        self.min_radius_hbox.addWidget(self.min_radius_spinbox)

        self.max_radius_hbox = QHBoxLayout()
        self.max_radius_label = QLabel("Max Radius")
        self.max_radius_slider = QSlider(Qt.Horizontal)
        self.max_radius_slider.setRange(0, 800)
        self.max_radius_slider.setValue(80)
        self.max_radius_spinbox = QSpinBox()
        self.max_radius_spinbox.setRange(0, 800)
        self.max_radius_spinbox.setValue(80)
        self.max_radius_slider.valueChanged.connect(self.max_radius_spinbox.setValue)
        self.max_radius_spinbox.valueChanged.connect(self.max_radius_slider.setValue)
        self.max_radius_hbox.addWidget(self.max_radius_slider)
        self.max_radius_hbox.addWidget(self.max_radius_spinbox)

        self.accumulator_threshold_hbox = QHBoxLayout()
        self.accumulator_threshold_label = QLabel("Accumulator Threshold")
        self.accumulator_threshold_slider = QSlider(Qt.Horizontal)
        self.accumulator_threshold_slider.setRange(0, 800)
        self.accumulator_threshold_slider.setValue(52)
        self.accumulator_threshold_spinbox = QSpinBox()
        self.accumulator_threshold_spinbox.setRange(0, 800)
        self.accumulator_threshold_spinbox.setValue(52)
        self.accumulator_threshold_slider.valueChanged.connect(
            self.accumulator_threshold_spinbox.setValue
        )
        self.accumulator_threshold_spinbox.valueChanged.connect(
            self.accumulator_threshold_slider.setValue
        )
        self.accumulator_threshold_hbox.addWidget(self.accumulator_threshold_slider)
        self.accumulator_threshold_hbox.addWidget(self.accumulator_threshold_spinbox)

        self.min_dist_hbox = QHBoxLayout()
        self.min_dist_label = QLabel("Min Distance")
        self.min_dist_slider = QSlider(Qt.Horizontal)
        self.min_dist_slider.setRange(0, 800)
        self.min_dist_slider.setValue(30)
        self.min_dist_spinbox = QSpinBox()
        self.min_dist_spinbox.setRange(0, 800)
        self.min_dist_spinbox.setValue(30)
        self.min_dist_slider.valueChanged.connect(self.min_dist_spinbox.setValue)
        self.min_dist_spinbox.valueChanged.connect(self.min_dist_slider.setValue)
        self.min_dist_hbox.addWidget(self.min_dist_slider)
        self.min_dist_hbox.addWidget(self.min_dist_spinbox)

        self.circle_attributes_vbox.addWidget(self.min_radius_label)
        self.circle_attributes_vbox.addLayout(self.min_radius_hbox)
        self.circle_attributes_vbox.addWidget(self.max_radius_label)
        self.circle_attributes_vbox.addLayout(self.max_radius_hbox)
        self.circle_attributes_vbox.addWidget(self.accumulator_threshold_label)
        self.circle_attributes_vbox.addLayout(self.accumulator_threshold_hbox)
        self.circle_attributes_vbox.addWidget(self.min_dist_label)
        self.circle_attributes_vbox.addLayout(self.min_dist_hbox)

        # Add the layouts to the main layout
        self.main_layout.addLayout(self.hough_type_hbox)
        self.update_hough_options(0)  # Set default options for Line Detection

        # Set the main layout of the group box
        self.setLayout(self.main_layout)

    def update_hough_options(self, index):
        if index == 0:  # Line
            self.main_layout.addLayout(self.line_attributes_vbox)
        elif index == 1:  # Circle
            self.main_layout.addLayout(self.circle_attributes_vbox)
        elif index == 2:  # Ellipse
            pass