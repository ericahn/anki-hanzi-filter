from aqt.qt import *

from .utils import *

from .FieldSelector import FieldSelector


class FieldBox(QGroupBox):
    def __init__(self, title, infowidget, col, callback):
        QGroupBox.__init__(self, title)
        self.col = col
        self.callback = callback

        layout = QVBoxLayout()
        self.field_selector = FieldSelector(col, self.my_callback)
        self.infowidget = infowidget
        layout.addWidget(self.field_selector)
        layout.addWidget(self.infowidget)
        self.setLayout(layout)

    def my_callback(self, deck_name, note_name, field):
        self.callback(deck_name, note_name, field)


class SourceBox(FieldBox):
    def __init__(self, *args):
        FieldBox.__init__(self, 'Source field', QLabel(), *args)

    def my_callback(self, deck_name, note_name, field):
        cids = self.col.findCards('deck:"{}" note:"{}" (is:review OR is:learn)'.format(deck_name, note_name))
        candidates = [self.col.getCard(cid).note()[field] for cid in cids]
        hanzi = only_hanzi(candidates)
        if len(hanzi) < 10:
            examples = ', '.join(hanzi)
        else:
            examples = ', '.join(hanzi[:4]) + ', ..., ' + ', '.join(hanzi[-4:])
        self.infowidget.setText('Found {} seen hanzi: {}'.format(len(hanzi), examples))
        self.callback(deck_name, note_name, field)


class DestinationBox(FieldBox):
    def __init__(self, *args):
        FieldBox.__init__(self, 'Destination field', FieldValueList(), *args)

    def my_callback(self, deck_name, note_name, field):
        cids = self.col.findCards('deck:"{}" note:"{}"'.format(deck_name, note_name))
        candidates = [self.col.getCard(cid).note()[field] for cid in cids]
        sentences = list(unique(candidates))
        self.infowidget.update(sentences)
        self.callback(deck_name, note_name, field)


class FieldValueList(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel('Found 0 sentences')
        self.list = QListWidget()
        layout.addWidget(self.label)
        layout.addWidget(self.list)
        self.setLayout(layout)

    def update(self, sentences):
        self.label.setText('Found {} sentence'.format(len(sentences)) + ('' if len(sentences) == 1 else 's'))
        self.list.clear()
        self.list.addItems(sentences)
