import os

from PySide6.QtCore import (Qt)
from PySide6.QtGui import (QKeyEvent, QPixmap)
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QDialog)

class LabelSpreadsDialog(QDialog):
    def __init__(self, available_height, images, spreads):
        super().__init__()
        self.index = 0
        self.images = images 
        self.spreads = spreads
        self.index2page = {i: os.path.basename(image) for i, image in enumerate(images)}

        self.setWindowTitle("跨页标记预览")
        # self.setGeometry(APP.primaryScreen().availableGeometry())
        # self.setMaximumSize(APP.primaryScreen().availableSize())
        self.available_height = available_height

        layout = QHBoxLayout()
        self.setLayout(layout)
        
        label = QLabel()
        label2 = QLabel()
        self.label = label
        self.label2 = label2
        layout.addWidget(label)
        layout.addWidget(label2)
        label2.setText("非跨页")

        help_text = [
            "用 ←/→ 方向键切换页面。",
            "用空格键标记/取消跨页。",
            "如需整体偏移 1 页，请使用「跨页位移」选项。",
            "用回车键确认全部跨页。",
            "关闭窗口取消。",
        ]
        buttonLabel = QLabel('\n'.join(help_text))
        layout.addWidget(buttonLabel)
        # print(label.size())
        # print(label.maximumSize())
        # l, t, r, b = layout.getContentsMargins()
        
        #label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        pixmap = QPixmap(images[0]).scaledToHeight(self.available_height * 0.9)
        label.setPixmap(pixmap)
        #label.setScaledContents(True)
        
        #label2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # pixmap2 = QPixmap(images[0]).scaledToHeight(self.frameGeometry().height() - t - b - t - b)
        # label2.setPixmap(pixmap2)
        #label2.setScaledContents(True)
        #self.resize(pixmap2.width(), pixmap2.height())
    
    def keyReleaseEvent(self, event):
        # t = 20
        # b = 20
        if isinstance(event, QKeyEvent):
            if event.key() == Qt.Key.Key_Left:
                self.index = max(0, self.index - 1)
                if self.index2page[self.index] in self.spreads:
                    self.label2.setText('跨页')
                else:
                    self.label2.setText('非跨页')
                pixmap = QPixmap(self.images[self.index]).scaledToHeight(self.available_height * 0.9)
                self.label.setPixmap(pixmap)
                # pixmap2 = QPixmap(images[self.index]).scaledToHeight(self.frameGeometry().height() - t - b - t - b)
                # self.label2.setPixmap(pixmap2)
            elif event.key() == Qt.Key.Key_Right:
                self.index = min(self.index + 1, len(self.images) - 1)
                if self.index2page[self.index] in self.spreads:
                    self.label2.setText('跨页')
                else:
                    self.label2.setText('非跨页')
                
                pixmap = QPixmap(self.images[self.index]).scaledToHeight(self.available_height * 0.9)
                self.label.setPixmap(pixmap)
                # pixmap2 = QPixmap(images[self.index]).scaledToHeight(self.frameGeometry().height() - t - b - t - b)
                # self.label2.setPixmap(pixmap2)
            elif event.key() == Qt.Key.Key_Space:
                if self.label2.text() == "非跨页":
                    self.spreads.append(os.path.basename(self.images[self.index]))
                    self.label2.setText('跨页')
                else:
                    self.spreads.remove(os.path.basename(self.images[self.index]))
                    self.label2.setText('非跨页')
            elif event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
                self.accept()
            else:
                super().keyReleaseEvent(event)
        else:
            super().keyReleaseEvent(event)