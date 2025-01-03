import sys
from bookmarkwidget import BookmarkWidget
from browsertabwidget import BrowserTabWidget
from downloadwidget import DownloadWidget
from findtoolbar import FindToolBar
from webengineview import WebEngineView
from PySide6 import QtCore
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QAction, QKeySequence, QIcon
from PySide6.QtWidgets import (QApplication, QDockWidget, QLabel, QLineEdit, QMainWindow, QToolBar)
from PySide6.QtWebEngineCore import QWebEngineDownloadRequest, QWebEnginePage

main_windows = []

def create_main_window():
    """利用可能な画面解像度の75％を使用してMainWindowを作成します。"""
    main_win = MainWindow()
    main_windows.append(main_win)
    available_geometry = main_win.screen().availableGeometry()
    main_win.resize(available_geometry.width() * 2 / 3,
    available_geometry.height() * 2 / 3)
    main_win.show()
    return main_win

def create_main_window_with_browser():
    """BrowserTabWidgetを持つMainWindowを作成します。"""
    main_win = create_main_window()
    return main_win.add_browser_tab()

StyleSheet = '''
QMenuBar {
    background-color: #c7b2de;
    font-size: 28px;
}
QMenu {
    background-color: #87e7b0;
    font-size: 28px;
}
QLabel {
    background-color: #87e7b0;
    font-size: 28px;
}
QLineEdit {
    background-color: #c7b2de;
    font-size: 28px;
}
QToolBar {
    background-color: #c7b2de;
    font-size: 28px;
}
BookmarkWidget {
    background-color: #c7b2de;
    font-size: 28px;
}
'''

class MainWindow(QMainWindow):
    """ウェブブラウジング体験を提供します。BookmarkWidget、BrowserTabWidget、DownloadWidgetを含む親ウィンドウを提供します。"""

    def __init__(self):
        super().__init__()

        self.setWindowTitle('ジョブラウザ')

        self._tab_widget = BrowserTabWidget(create_main_window_with_browser)
        self._tab_widget.enabled_changed.connect(self._enabled_changed)
        self._tab_widget.download_requested.connect(self._download_requested)
        self.setCentralWidget(self._tab_widget)
        self.connect(self._tab_widget, QtCore.SIGNAL("url_changed(QUrl)"),
        self.url_changed)

        self._bookmark_dock = QDockWidget()
        self._bookmark_dock.setWindowTitle('お気に入り')
        self._bookmark_widget = BookmarkWidget()
        self._bookmark_widget.open_bookmark.connect(self.load_url)
        self._bookmark_widget.open_bookmark_in_new_tab.connect(self.load_url_in_new_tab)
        self._bookmark_dock.setWidget(self._bookmark_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self._bookmark_dock)

        self._find_tool_bar = None

        self._actions = {}
        self._create_menu()

        self._tool_bar = QToolBar()
        self.addToolBar(self._tool_bar)
        for action in self._actions.values():
            if not action.icon().isNull():
                self._tool_bar.addAction(action)

        self._addres_line_edit = QLineEdit()
        self._addres_line_edit.setClearButtonEnabled(True)
        self._addres_line_edit.returnPressed.connect(self.load)
        self._tool_bar.addWidget(self._addres_line_edit)
        self._zoom_label = QLabel()
        self.statusBar().addPermanentWidget(self._zoom_label)
        self._update_zoom_label()

        self._bookmarksToolBar = QToolBar()
        self.addToolBar(Qt.TopToolBarArea, self._bookmarksToolBar)
        self.insertToolBarBreak(self._bookmarksToolBar)
        self._bookmark_widget.changed.connect(self._update_bookmarks)
        self._update_bookmarks()

        self.setStyleSheet(StyleSheet)

    def _update_bookmarks(self):
        self._bookmark_widget.populate_tool_bar(self._bookmarksToolBar)
        self._bookmark_widget.populate_other(self._bookmark_menu, 3)

    def _create_menu(self):
        file_menu = self.menuBar().addMenu("&ファイル")
        exit_action = QAction(QIcon.fromTheme("application-exit"), "&終了",
        self, shortcut="Ctrl+Q", triggered=qApp.quit)
        file_menu.addAction(exit_action)

        navigation_menu = self.menuBar().addMenu("&ナビゲーション")

        style_icons = ':/qt-project.org/styles/commonstyle/images/'
        back_action = QAction(QIcon.fromTheme("go-previous",
        QIcon(style_icons + 'left-32.png')),
        "戻る", self,
        shortcut=QKeySequence(QKeySequence.Back),
        triggered=self._tab_widget.back)
        self._actions[QWebEnginePage.Back] = back_action
        back_action.setEnabled(False)
        navigation_menu.addAction(back_action)
        forward_action = QAction(QIcon.fromTheme("go-next",
        QIcon(style_icons + 'right-32.png')),
        "進む", self,
        shortcut=QKeySequence(QKeySequence.Forward),
        triggered=self._tab_widget.forward)
        forward_action.setEnabled(False)
        self._actions[QWebEnginePage.Forward] = forward_action

        navigation_menu.addAction(forward_action)
        reload_action = QAction(QIcon(style_icons + 'refresh-32.png'),
        "更新", self,
        shortcut=QKeySequence(QKeySequence.Refresh),
        triggered=self._tab_widget.reload)
        self._actions[QWebEnginePage.Reload] = reload_action
        reload_action.setEnabled(False)
        navigation_menu.addAction(reload_action)

        navigation_menu.addSeparator()

        new_tab_action = QAction("新しいタブを開く", self,
        shortcut='Ctrl+T',
        triggered=self.add_browser_tab)
        navigation_menu.addAction(new_tab_action)

        close_tab_action = QAction("現在のタブを閉じる", self,
        shortcut="Ctrl+W",
        triggered=self._close_current_tab)
        navigation_menu.addAction(close_tab_action)

        navigation_menu.addSeparator()

        history_action = QAction("閲覧履歴", self,
        triggered=self._tab_widget.show_history)
        navigation_menu.addAction(history_action)

        edit_menu = self.menuBar().addMenu("&編集")

        find_action = QAction("検索する", self,
        shortcut=QKeySequence(QKeySequence.Find),
        triggered=self._show_find)
        edit_menu.addAction(find_action)

        edit_menu.addSeparator()
        undo_action = QAction("取り消す", self,
        shortcut=QKeySequence(QKeySequence.Undo),
        triggered=self._tab_widget.undo)
        self._actions[QWebEnginePage.Undo] = undo_action
        undo_action.setEnabled(False)
        edit_menu.addAction(undo_action)

        redo_action = QAction("やり直す", self,
        shortcut=QKeySequence(QKeySequence.Redo),
        triggered=self._tab_widget.redo)
        self._actions[QWebEnginePage.Redo] = redo_action
        redo_action.setEnabled(False)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        cut_action = QAction("切り取る", self,
        shortcut=QKeySequence(QKeySequence.Cut),
        triggered=self._tab_widget.cut)
        self._actions[QWebEnginePage.Cut] = cut_action
        cut_action.setEnabled(False)
        edit_menu.addAction(cut_action)

        copy_action = QAction("写し取る", self,
        shortcut=QKeySequence(QKeySequence.Copy),
        triggered=self._tab_widget.copy)
        self._actions[QWebEnginePage.Copy] = copy_action
        copy_action.setEnabled(False)
        edit_menu.addAction(copy_action)

        paste_action = QAction("貼り付ける", self,
        shortcut=QKeySequence(QKeySequence.Paste),
        triggered=self._tab_widget.paste)
        self._actions[QWebEnginePage.Paste] = paste_action
        paste_action.setEnabled(False)
        edit_menu.addAction(paste_action)

        edit_menu.addSeparator()

        select_all_action = QAction("すべて選択する", self,
        shortcut=QKeySequence(QKeySequence.SelectAll),
        triggered=self._tab_widget.select_all)
        self._actions[QWebEnginePage.SelectAll] = select_all_action
        select_all_action.setEnabled(False)
        edit_menu.addAction(select_all_action)

        self._bookmark_menu = self.menuBar().addMenu("&お気に入り")
        add_bookmark_action = QAction("&お気に入りに追加する", self,
        triggered=self._add_bookmark)
        self._bookmark_menu.addAction(add_bookmark_action)
        add_tool_bar_bookmark_action = QAction("&お気に入りをツールバーに追加する", self,
        triggered=self._add_tool_bar_bookmark)
        self._bookmark_menu.addAction(add_tool_bar_bookmark_action)
        self._bookmark_menu.addSeparator()

        tools_menu = self.menuBar().addMenu("&ツール")
        download_action = QAction("ダウンロードを開く", self,
        triggered=DownloadWidget.open_download_directory)
        tools_menu.addAction(download_action)

        window_menu = self.menuBar().addMenu("&ウィンドウ")

        window_menu.addAction(self._bookmark_dock.toggleViewAction())

        window_menu.addSeparator()

        zoom_in_action = QAction(QIcon.fromTheme("zoom-in"),
        "ページを拡大する", self,
        shortcut=QKeySequence(QKeySequence.ZoomIn),
        triggered=self._zoom_in)
        window_menu.addAction(zoom_in_action)
        zoom_out_action = QAction(QIcon.fromTheme("zoom-out"),
        "ページを縮小する", self,
        shortcut=QKeySequence(QKeySequence.ZoomOut),
        triggered=self._zoom_out)
        window_menu.addAction(zoom_out_action)

        reset_zoom_action = QAction(QIcon.fromTheme("zoom-original"),
        "ページを等倍にする", self,
        shortcut="Ctrl+0",
        triggered=self._reset_zoom)
        window_menu.addAction(reset_zoom_action)

        about_menu = self.menuBar().addMenu("&その他")
        about_action = QAction("このブラウザについて", self,
        shortcut=QKeySequence(QKeySequence.HelpContents),
        triggered=qApp.aboutQt)
        about_menu.addAction(about_action)
        
        self.setStyleSheet(StyleSheet)

    def add_browser_tab(self):
        return self._tab_widget.add_browser_tab()

    def _close_current_tab(self):
        if self._tab_widget.count() > 1:
            self._tab_widget.close_current_tab()
        else:
            self.close()

    def close_event(self, event):
        main_windows.remove(self)
        event.accept()

    def load(self):
        url_string = self._addres_line_edit.text().strip()
        if url_string:
            self.load_url_string(url_string)

    def load_url_string(self, url_s):
        url = QUrl.fromUserInput(url_s)
        if (url.isValid()):
            self.load_url(url)

    def load_url(self, url):
        self._tab_widget.load(url)

    def load_url_in_new_tab(self, url):
        self.add_browser_tab().load(url)

    def url_changed(self, url):
        self._addres_line_edit.setText(url.toString())

    def _enabled_changed(self, web_action, enabled):
        action = self._actions[web_action]
        if action:
            action.setEnabled(enabled)

    def _add_bookmark(self):
        index = self._tab_widget.currentIndex()
        if index >= 0:
            url = self._tab_widget.url()
            title = self._tab_widget.tabText(index)
            icon = self._tab_widget.tabIcon(index)
            self._bookmark_widget.add_bookmark(url, title, icon)

    def _add_tool_bar_bookmark(self):
        index = self._tab_widget.currentIndex()
        if index >= 0:
            url = self._tab_widget.url()
            title = self._tab_widget.tabText(index)
            icon = self._tab_widget.tabIcon(index)
            self._bookmark_widget.add_tool_bar_bookmark(url, title, icon)

    def _zoom_in(self):
        new_zoom = self._tab_widget.zoom_factor() * 1.5
        if (new_zoom <= WebEngineView.maximum_zoom_factor()):
            self._tab_widget.set_zoom_factor(new_zoom)
            self._update_zoom_label()

    def _zoom_out(self):
        new_zoom = self._tab_widget.zoom_factor() / 1.5
        if (new_zoom >= WebEngineView.minimum_zoom_factor()):
            self._tab_widget.set_zoom_factor(new_zoom)
            self._update_zoom_label()

    def _reset_zoom(self):
        self._tab_widget.set_zoom_factor(1)
        self._update_zoom_label()

    def _update_zoom_label(self):
        percent = int(self._tab_widget.zoom_factor() * 100)
        self._zoom_label.setText(f"{percent}%")

    def _download_requested(self, item):
        # 新しいダウンロードを開く前に古いダウンロードを削除する。
        for old_download in self.statusBar().children():
            if (type(old_download).__name__ == 'DownloadWidget' and
                old_download.state() != QWebEngineDownloadRequest.DownloadInProgress):
                self.statusBar().removeWidget(old_download)
                del old_download

        item.accept()
        download_widget = DownloadWidget(item)
        download_widget.remove_requested.connect(self._remove_download_requested,
        Qt.QueuedConnection)
        self.statusBar().addWidget(download_widget)

    def _remove_download_requested(self):
        download_widget = self.sender()
        self.statusBar().removeWidget(download_widget)
        del download_widget

    def _show_find(self):
        if self._find_tool_bar is None:
            self._find_tool_bar = FindToolBar()
            self._find_tool_bar.find.connect(self._tab_widget.find)
            self.addToolBar(Qt.BottomToolBarArea, self._find_tool_bar)
        else:
            self._find_tool_bar.show()
            self._find_tool_bar.focus_find()

    def write_bookmarks(self):
        self._bookmark_widget.write_bookmarks()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = create_main_window()
    initial_urls = sys.argv[1:]
    if not initial_urls:
        initial_urls.append('https://sbkunren.xsrv.jp/202408java/jikosyoukai/30/nasuportal/')
    for url in initial_urls:
        main_win.load_url_in_new_tab(QUrl.fromUserInput(url))
    exit_code = app.exec()
    main_win.write_bookmarks()
    sys.exit(exit_code)