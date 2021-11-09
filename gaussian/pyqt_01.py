#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
app = QApplication([])
window = QWidget()
layout = QVBoxLayout()

Top_butt = QPushButton('Top')
layout.addWidget( Top_butt )
Bott_butt = QPushButton('Bottom')
layout.addWidget( Bott_butt )

def on_Top_butt_clicked():
    print("top was pressed")
    
def on_Bott_butt_clicked():
    print("bott was pressed")

Top_butt.clicked.connect( on_Top_butt_clicked )
Bott_butt.clicked.connect( on_Bott_butt_clicked )

window.setLayout(layout)
window.show()
app.exec()
