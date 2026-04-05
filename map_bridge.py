from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot


class MapBridge(QObject):
    addressUpdated = pyqtSignal(str)

    @pyqtSlot(str)
    def updateAddress(self, address):
        self.addressUpdated.emit(address)
