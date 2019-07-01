import sys
import pandas as pd
from gensim_lda import gensim_lda_product

from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette
from PyQt5.QtCore import Qt, QRect

def load_item():

    df = pd.read_csv('../clean_dataset.csv', sep = ';', encoding='latin-1')
    product_df = df[['productid']]
    most_reviwed_products = product_df['productid'].value_counts()[:10]

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

        self.initUI()

    def initUI(self):
        grid = QGridLayout()

        grid.addWidget(self.create_Sentiment_Analysis(), 0, 0)
        grid.addWidget(self.create_Base_Aspect_SA(), 0, 1)

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

    def create_Base_Aspect_SA(self):
            groupBox = QGroupBox("Based-Aspect Sentiment Analysis")
            
            self.product_label = QLabel(self)
            self.product_label.setText('Prodotto:')
            
            self.product_id = QComboBox(self)
            product_list = load_item()
            for item in product_list:
                self.product_id.addItem(item)

            self.button_run = QPushButton('Run', self)
            self.button_run.setToolTip('Run')
            self.button_run.clicked.connect(self.on_click_run)

            self.progress_bar = QProgressBar(self)
            self.progress_bar.setGeometry(QRect(250, 450, 450, 25))
            self.progress_bar.setValue(0)

            vbox = QVBoxLayout()
            vbox.addWidget(self.product_label)
            vbox.addWidget(self.product_id)
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

        gensim_lda_product('B000G6RYNE', self.basa_execution, **parameters)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    palette = QPalette()
    palette.setColor(QPalette.Base, Qt.gray)
    app.setPalette(palette)
    ex = App()
    sys.exit(app.exec_())