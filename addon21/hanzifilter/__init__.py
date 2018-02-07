import itertools

# import the main window object (mw) from aqt
from aqt import mw

# import the "show info" tool from utils.py
from aqt.utils import showInfo

# import all of the Qt GUI library
from aqt.qt import *

from .utils import *

from .FieldSelector import FieldSelector
from .ActionGrid import ActionGrid
from .FieldBox import SourceBox, DestinationBox


class MyForm(QDialog):
    def __init__(self):
        # Here, you should call the inherited class' init, which is QDialog
        QDialog.__init__(self, mw, Qt.Window)
        mw.setupDialogGC(self)

        self.mw = mw
        self.parent = mw
        self.col = self.mw.col

        self.hanzi = None
        self.queries = None
        self.action_field = None

        v1 = QVBoxLayout()
        v1.addWidget(SourceBox(self.col, self.source_field_selected))
        v1.addWidget(DestinationBox(self.col, self.destination_field_selected))
        self.actiongrid = ActionGrid(self.col)
        v1.addWidget(self.actiongrid)
        v1.setContentsMargins(12, 12, 12, 12)
        self.setLayout(v1)
        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Hanzi Filter')
        self.show()

        # take the focus away from the first input area when starting up,
        # as users tend to accidentally type into the template
        self.setFocus()

    def source_field_selected(self, deck_name, note_name, field):
        cids = self.col.findCards('deck:"{}" note:"{}" (is:review OR is:learn)'.format(deck_name, note_name))
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


chinese_menu = None
for action in mw.form.menuTools.actions():
    menu = action.menu()
    if menu is not None and action.text() == 'Chinese tools':
        chinese_menu = menu
if chinese_menu is None:
    chinese_menu = QMenu('Chinese tools')
    mw.form.menuTools.addSeparator()
    mw.form.menuTools.addMenu(chinese_menu)

action = QAction('Hanzi Filter', mw)
action.triggered.connect(MyForm)
chinese_menu.addAction(action)
