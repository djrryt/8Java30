import PySide6
from PySide6.QtWidgets import (QApplication,
                               QLabel,
                               QWidget)
import os
import sys

# PySide6のアプリ本体（ユーザがコーディングしていく部分）
class MainWindow(QWidget):
    def __init__(self, parent=None):
        # 親クラスの初期化
        super().__init__(parent)

        # ウィンドウタイトル
        self.setWindowTitle("PySide6で作ったアプリです。")

        # ラベルを表示するメソッド
        self.SetLabel()

        # ウィンドウサイズを指定（px単位）
        windowWidth = 1000  # ウィンドウの横幅
        windowHeight = 800  # ウィンドウの高さ
        
        # ウィンドウサイズの変更
        self.resize(windowWidth, windowHeight)
        
        # ウィンドウの位置とサイズを指定（px単位）
        xPos = 400  # x座標
        yPos = 500  # y座標
        windowWidth = 600   # ウィンドウの横幅
        windowHeight = 400  # ウィンドウの高さ
        
        # ウィンドウの位置とサイズの変更
        self.setGeometry(xPos, yPos, windowWidth, windowHeight)

    # ラベルは別のメソッドに分けました
    def SetLabel(self):
        # ラベルを使うことを宣言（引数のselfはウィンドウのことで、ウィンドウにラベルが表示されます）
        label = QLabel(self)
        
        # ラベルの見た目をQt Style Sheetで設定
        labelStyle = """QLabel {
            color:            #FF00AA;  /* 文字色 */
            font-size:        64px;     /* 文字サイズ */
            background-color: #FFAA00;  /* 背景色 */
        }"""
        
        # 見た目の設定をラベルに反映させる
        label.setStyleSheet(labelStyle)

        # ラベルに文字を指定
        label.setText("こんにちは。ラベルです。")

if __name__ == "__main__":
    # 環境変数にPySide6を登録
    dirname = os.path.dirname(PySide6.__file__)
    plugin_path = os.path.join(dirname, 'plugins', 'platforms')
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
    
    app = QApplication(sys.argv)    # PySide6の実行
    window = MainWindow()           # ユーザがコーディングしたクラス
    window.show()                   # PySide6のウィンドウを表示
    sys.exit(app.exec())            # PySide6の終了
