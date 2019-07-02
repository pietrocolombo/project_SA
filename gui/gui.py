import sys
import subprocess
import pandas as pd
from gensim_lda import gensim_lda_product
from download_image import perfromScraping

from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QPixmap, QIntValidator
from PyQt5.QtCore import Qt, QRect

def load_item(product_number = 10):

    df = pd.read_csv('../data/clean_dataset.csv', sep = ';', encoding='latin-1')
    product_df = df[['productid']]
    most_reviwed_products = product_df['productid'].value_counts()[:product_number]

    return list(most_reviwed_products.index)

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Amazon Food Reviews'
        self.left = 10
        self.top = 10
        self.width = 540
        self.height = 400
        self.basa_execution = 0
        self.product_image = 'AmazonImages/B002QWP89S.jpg'

        self.initUI()

    def initUI(self):
        grid = QGridLayout()

        grid.addWidget(self.create_Sentiment_Analysis(), 0, 0)
        grid.addWidget(self.create_parameters_Base_Aspect_SA(), 0, 1)
        grid.addWidget(self.create_Base_Aspect_SA(), 1, 1)

        self.setLayout(grid)
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.show()

    def create_Sentiment_Analysis(self):
            groupBox = QGroupBox("Sentiment Analysis")

            vbox = QVBoxLayout()
            vbox.addStretch(1)
            groupBox.setLayout(vbox)

            return groupBox

    def create_parameters_Base_Aspect_SA(self):
        groupBox = QGroupBox("Parameters for Based-Aspect SA")

        self.topic_number_label = QLabel(self)
        self.topic_number_label.setText('Numero di topic:')
        self.topic_number = QLineEdit(self)
        self.topic_number.setMaxLength(2)
        self.topic_number.setValidator(QIntValidator())

        self.topic_limit_label = QLabel(self)
        self.topic_limit_label.setText('Limite massimo di topic:')
        self.topic_limit = QLineEdit(self)
        self.topic_limit.setValidator(QIntValidator())
        self.topic_limit.setMaxLength(2)
        self.topic_limit.setText('10')

        self.product_number_label = QLabel(self)
        self.product_number_label.setText('Numero di prodotti disponibili:')
        self.product_number = QLineEdit(self)
        self.product_number.setValidator(QIntValidator())
        self.product_number.setMaxLength(2)
        self.product_number.setText('10')

        self.button_parameters = QPushButton('Aggiorna prodotti', self)
        self.button_parameters.setToolTip('Aggiorna prodotti')
        self.button_parameters.clicked.connect(self.on_click_update_products)

        self.button_reset = QPushButton('Reset', self)
        self.button_reset.setToolTip('Reset')
        self.button_reset.clicked.connect(self.on_click_reset)

        self.execution_label = QLabel(self)
        self.execution_label.setText('Numero di esecuzioni:')
        self.execution = QLineEdit(self)
        self.execution.setText(str(self.basa_execution))
        self.execution.setReadOnly(True)

        vbox = QVBoxLayout()
        vbox.addWidget(self.topic_number_label)
        vbox.addWidget(self.topic_number)
        vbox.addWidget(self.topic_limit_label)
        vbox.addWidget(self.topic_limit)
        vbox.addWidget(self.product_number_label)
        vbox.addWidget(self.product_number)
        vbox.addWidget(self.button_parameters)
        vbox.addWidget(self.button_reset)
        vbox.addWidget(self.execution_label)
        vbox.addWidget(self.execution)

        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox

    def on_click_update_products(self):

        if not self.product_number.text() == 10:
            self.product_combobox.clear()
            product_list = load_item(int(self.product_number.text()))
            for item in product_list:
                self.product_combobox.addItem(item)

    def on_click_reset(self):

        self.basa_execution = 0

        self.topic_number.setText('')
        self.topic_limit.setText('10')
        self.product_number.setText('10')
        self.execution.setText(str(self.basa_execution))

        self.product_combobox.clear()
        product_list = load_item()
        for item in product_list:
            self.product_combobox.addItem(item)
        self.product_combobox.setCurrentIndex(0)
        self.update_image()

        subprocess.call('rm lda_model/*',  shell=True)

    def update_image(self):

        #perfromScraping(str(self.product_combobox.currentText()))
        self.product_image = f'AmazonImages/{str(self.product_combobox.currentText())}.jpg'
        pixmap = QPixmap(self.product_image)
        pixmap_resized = pixmap.scaled(125, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
        self.immage_original.setPixmap(pixmap_resized)

    def create_Base_Aspect_SA(self):
        groupBox = QGroupBox("Based-Aspect Sentiment Analysis")
        
        self.product_label = QLabel(self)
        self.product_label.setText('Prodotto:')
        
        self.product_combobox = QComboBox(self)
        product_list = load_item()
        for item in product_list:
            self.product_combobox.addItem(item)
        self.product_combobox.setCurrentIndex(0)
        self.product_combobox.currentTextChanged.connect(self.update_image)

        self.immage_original = QLabel(self)
        pixmap = QPixmap(self.product_image)
        pixmap_resized = pixmap.scaled(125, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        self.immage_original.setPixmap(pixmap_resized)
        self.immage_original.setAlignment(Qt.AlignCenter)

        self.button_run = QPushButton('Run', self)
        self.button_run.setToolTip('Run')
        self.button_run.clicked.connect(self.on_click_run)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(QRect(250, 450, 450, 25))
        self.progress_bar.setValue(0)

        vbox = QVBoxLayout()
        vbox.addWidget(self.product_label)
        vbox.addWidget(self.product_combobox)
        vbox.addWidget(self.immage_original)
        vbox.addWidget(self.button_run)
        vbox.addWidget(self.progress_bar)

        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox

    def on_click_run(self):
        def update_progress_bar(value):
            self.progress_bar.setValue(value)
            QApplication.processEvents()

        self.basa_execution += 1

        parameters = {}
        parameters["on_update"] = update_progress_bar
        
        product_id = str(self.product_combobox.currentText())
        if self.topic_number.text():
            topic_number = int(self.topic_number.text())
            gensim_lda_product(product_id, self.basa_execution, start = topic_number, limit = topic_number + 1, **parameters)
        else:
            topic_limit = int(self.topic_limit.text())
            gensim_lda_product(product_id, self.basa_execution, limit = topic_limit, **parameters)
        
        self.execution.setText(str(self.basa_execution))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    palette = QPalette()
    palette.setColor(QPalette.Base, Qt.gray)
    app.setPalette(palette)
    ex = App()
    sys.exit(app.exec_())