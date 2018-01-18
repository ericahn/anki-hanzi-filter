from aqt.qt import *

from .ActionBox import ActionBox


class ActionGrid(QWidget):
    def __init__(self, col):
        QWidget.__init__(self)

        self.query = self.my_filter = self.field = None
        self.good_cids = []
        self.col = col

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(3)

        layout.addWidget(QLabel('Seen'), 0, 1)
        layout.addWidget(QLabel('Not seen yet'), 0, 2)
        layout.addWidget(QLabel('Known, suspended'), 1, 0)
        layout.addWidget(QLabel('Unknown, unsuspended'), 2, 0)

        self.actionboxes = {}
        for seen in range(2):
            for suspend in range(2):
                row = suspend + 1
                col = seen + 1
                key = (('Seen', 'Unseen')[seen], ('Suspended', 'Unsuspended')[suspend])
                actionbox = ActionBox(self.col, suspend, self.recalculate)
                self.actionboxes[key] = actionbox
                layout.addWidget(actionbox, row, col)

        self.setLayout(layout)

    def update_filtering(self, queries, my_filter, field):
        self.queries = queries
        self.my_filter = my_filter
        self.field = field
        for seen in ('Seen', 'Unseen'):
            for suspend in ('Suspended', 'Unsuspended'):
                key = seen, suspend
                self.actionboxes[key].update_filtering(queries[key], my_filter, field)

    def recalculate(self):
        if not (self.queries and self.my_filter and self.field):
            return
        self.update_filtering(self.queries, self.my_filter, self.field)