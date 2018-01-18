import itertools

# import the main window object (mw) from aqt
from aqt import mw

# import the "show info" tool from utils.py
from aqt.utils import showInfo

# import all of the Qt GUI library
from aqt.qt import *

from .FieldSelector import FieldSelector
from .ActionGrid import ActionGrid


def unique(l):
    found = set()
    for x in l:
        if x not in found:
            yield x
            found.add(x)


def is_hanzi(c):
    return len(c) == 1 and 0x4e00 <= ord(c) <= 0x9fff


def only_hanzi(l):
    return list(filter(is_hanzi, unique(l)))


def create_filter(hanzi):
    hanzi = set(hanzi)

    def my_filter(text):
        for c in text:
            if is_hanzi(c) and c not in hanzi:
                return False
        return True

    return my_filter


class MyForm(QDialog):
    def __init__(self, parent=None):
        # Here, you should call the inherited class' init, which is QDialog
        QDialog.__init__(self, parent or mw, Qt.Window)
        mw.setupDialogGC(self)

        self.mw = mw or aqt.mw
        self.parent = parent or mw
        self.col = self.mw.col

        self.hanzi = None
        self.queries = None
        self.action_field = None

        v1 = QVBoxLayout()
        v1.addWidget(FieldSelector(self.col, self.source_field_selected))
        v1.addWidget(FieldSelector(self.col, self.destination_field_selected))
        self.actiongrid = ActionGrid(self.col)
        v1.addWidget(self.actiongrid)
        v1.setContentsMargins(12, 12, 12, 12)
        self.setLayout(v1)
        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Pizza title')
        self.show()

        # take the focus away from the first input area when starting up,
        # as users tend to accidentally type into the template
        self.setFocus()

    def source_field_selected(self, deck_name, note_name, field):
        cids = self.col.findCards('deck:"{}" note:"{}" is:review'.format(deck_name, note_name))
        candidates = [self.col.getCard(cid).note()[field] for cid in cids]
        self.hanzi = only_hanzi(candidates)
        self.update_actions()

    def destination_field_selected(self, deck_name, note_name, field):
        self.action_field = field
        query_base = 'deck:"{}" note:"{}"'.format(deck_name, note_name)
        self.queries = {}
        for seen, suspended in itertools.product(*itertools.repeat([True, False], 2)):
            query = query_base
            query += ' ' + ('' if seen else '-') + 'is:review'
            query += ' ' + ('' if suspended else '-') + 'is:suspended'
            self.queries[('Seen', 'Unseen')[not seen],
                         ('Suspended', 'Unsuspended')[not suspended]] = query
        self.update_actions()

    def update_actions(self):
        if None in (self.hanzi, self.queries, self.action_field):
            return
        self.actiongrid.update_filtering(self.queries, create_filter(self.hanzi), self.action_field)


action = QAction('Hanzi Filter', mw)

# set it to call testFunction when it's clicked
action.triggered.connect(lambda: MyForm())

# and add it to the tools menu
mw.form.menuTools.addAction(action)
