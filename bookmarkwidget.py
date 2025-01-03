import json
import os
import warnings

from PySide6 import QtCore
from PySide6.QtCore import QDir, QFileInfo, QStandardPaths, Qt, QUrl
from PySide6.QtGui import QIcon, QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QMenu, QMessageBox, QTreeView

_url_role = Qt.UserRole + 1

# .jsonブックマーク・ファイルからの読み込み／.jsonブックマーク・ファイルへの書き込みに使われる形式です。
_default_bookmarks = [
    ['お気に入り'],
    ['https://www.jobridge.info/', 'Jobridge'],
    ['https://social-bridge.co.jp/college/', 'SB Career College'],
    ['https://social-bridge.co.jp/', 'Social Bridge'],
    ['https://sbkunren.xsrv.jp/202408java/jikosyoukai/30/nasuportal/', 'NasuPortal'],
]


def _config_dir():
    location = QStandardPaths.writableLocation(QStandardPaths.ConfigLocation)
    return f'{location}/QtForPythonBrowser'


_bookmark_file = 'bookmarks.json'


def _create_folder_item(title):
    result = QStandardItem(title)
    result.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
    return result


def _create_item(url, title, icon):
    result = QStandardItem(title)
    result.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
    result.setData(url, _url_role)
    if icon is not None:
        result.setIcon(icon)
    return result


# 配列の配列からモデルを作成する。
def _create_model(parent, serialized_bookmarks):
    result = QStandardItemModel(0, 1, parent)
    last_folder_item = None
    for entry in serialized_bookmarks:
        if len(entry) == 1:
            last_folder_item = _create_folder_item(entry[0])
            result.appendRow(last_folder_item)
        else:
            url = QUrl.fromUserInput(entry[0])
            title = entry[1]
            icon = QIcon(entry[2]) if len(entry) > 2 and entry[2] else None
            last_folder_item.appendRow(_create_item(url, title, icon))
    return result


# モデルを配列の配列にシリアライズし、その過程でアイコンをディレクトリ下の.pngファイルに書き出す。
def _serialize_model(model, directory):
    result = []
    folder_count = model.rowCount()
    for f in range(0, folder_count):
        folder_item = model.item(f)
        result.append([folder_item.text()])
        item_count = folder_item.rowCount()
        for i in range(0, item_count):
            item = folder_item.child(i)
            entry = [item.data(_url_role).toString(), item.text()]
            icon = item.icon()
            if not icon.isNull():
                icon_sizes = icon.availableSizes()
                largest_size = icon_sizes[len(icon_sizes) - 1]
                w = largest_size.width()
                icon_file_name = f'{directory}/icon{f:02}_{i:02}_{w}.png'
                icon.pixmap(largest_size).save(icon_file_name, 'PNG')
                entry.append(icon_file_name)
            result.append(entry)
    return result


# ツールバーやメニューを永続化し、ポップアップする機能を備えたドックウィジェットで使用するツリービューとしてのブックマーク。
class BookmarkWidget(QTreeView):
    """Provides a tree view to manage the bookmarks."""

    open_bookmark = QtCore.Signal(QUrl)
    open_bookmark_in_new_tab = QtCore.Signal(QUrl)
    changed = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self.setRootIsDecorated(False)
        self.setUniformRowHeights(True)
        self.setHeaderHidden(True)
        self._model = _create_model(self, self._read_bookmarks())
        self.setModel(self._model)
        self.expandAll()
        self.activated.connect(self._activated)
        self._model.rowsInserted.connect(self._changed)
        self._model.rowsRemoved.connect(self._changed)
        self._model.dataChanged.connect(self._changed)
        self._modified = False

    def _changed(self):
        self._modified = True
        self.changed.emit()

    def _activated(self, index):
        item = self._model.itemFromIndex(index)
        self.open_bookmark.emit(item.data(_url_role))

    def _action_activated(self, index):
        action = self.sender()
        self.open_bookmark.emit(action.data())

    def _tool_bar_item(self):
        return self._model.item(0, 0)

    def _other_item(self):
        return self._model.item(1, 0)

    def add_bookmark(self, url, title, icon):
        self._other_item().appendRow(_create_item(url, title, icon))

    def add_tool_bar_bookmark(self, url, title, icon):
        self._tool_bar_item().appendRow(_create_item(url, title, icon))

    # parent_itemの下にあるブックマークを、アクションのリストを持つQMenu/QToolBarのようなtarget_objectに同期します。既存のアクションを更新し、必要であれば新しいアクションを追加し、不要なアクションを非表示にする。
    def _populate_actions(self, parent_item, target_object, first_action):
        if parent_item is None:
            print("Warning: parent_item is None")
        return
        
        existing_actions = target_object.actions()
        existing_action_count = len(existing_actions)
        a = first_action
        row_count = parent_item.rowCount()
        for r in range(0, row_count):
            item = parent_item.child(r)
            title = item.text()
            icon = item.icon()
            url = item.data(_url_role)
            if a < existing_action_count:
                action = existing_actions[a]
                if (title != action.toolTip()):
                    action.setText(BookmarkWidget.short_title(title))
                    action.setIcon(icon)
                    action.setToolTip(title)
                    action.setData(url)
                    action.setVisible(True)
            else:
                short_title = BookmarkWidget.short_title(title)
                action = target_object.addAction(icon, short_title)
                action.setToolTip(title)
                action.setData(url)
                action.triggered.connect(self._action_activated)
            a = a + 1
        while a < existing_action_count:
            existing_actions[a].setVisible(False)
            a = a + 1

    def populate_tool_bar(self, tool_bar):
        self._populate_actions(self._tool_bar_item(), tool_bar, 0)

    def populate_other(self, menu, first_action):
        self._populate_actions(self._other_item(), menu, first_action)

    def _current_item(self):
        index = self.currentIndex()
        if index.isValid():
            item = self._model.itemFromIndex(index)
            if item.parent():  # トップレベル項目を除く。
                return item
        return None

    def context_menu_event(self, event):
        context_menu = QMenu()
        open_in_new_tab_action = context_menu.addAction("Open in New Tab")
        remove_action = context_menu.addAction("Remove...")
        current_item = self._current_item()
        open_in_new_tab_action.setEnabled(current_item is not None)
        remove_action.setEnabled(current_item is not None)
        chosen_action = context_menu.exec(event.globalPos())
        if chosen_action == open_in_new_tab_action:
            self.open_bookmarkInNewTab.emit(current_item.data(_url_role))
        elif chosen_action == remove_action:
            self._remove_item(current_item)

    def _remove_item(self, item):
        message = f"Would you like to remove \"{item.text()}\"?"
        button = QMessageBox.question(self, "Remove", message,
        QMessageBox.Yes | QMessageBox.No)
        if button == QMessageBox.Yes:
            item.parent().removeRow(item.row())

    def write_bookmarks(self):
        if not self._modified:
            return
        dir_path = _config_dir()
        native_dir_path = QDir.toNativeSeparators(dir_path)
        directory = QFileInfo(dir_path)
        if not directory.isDir():
            print(f'Creating {native_dir_path}...')
            if not QDir(directory.absolutePath()).mkpath(directory.fileName()):
                warnings.warn(f'Cannot create {native_dir_path}.',
                RuntimeWarning)
                return
        serialized_model = _serialize_model(self._model, dir_path)
        bookmark_file_name = os.path.join(native_dir_path, _bookmark_file)
        print(f'Writing {bookmark_file_name}...')
        with open(bookmark_file_name, 'w') as bookmark_file:
            json.dump(serialized_model, bookmark_file, indent=4)

    def _read_bookmarks(self):
        bookmark_file_name = os.path.join(QDir.toNativeSeparators(_config_dir()),
        _bookmark_file)
        if os.path.exists(bookmark_file_name):
            print(f'Reading {bookmark_file_name}...')
            return json.load(open(bookmark_file_name))
        return _default_bookmarks

    # ブックマークアクションの短いタイトルを返す。"Qt | Cross Platform...」 -> "Qt」
    @staticmethod
    def short_title(t):
        i = t.find(' | ')
        if i == -1:
            i = t.find(' - ')
        return t[0:i] if i != -1 else t