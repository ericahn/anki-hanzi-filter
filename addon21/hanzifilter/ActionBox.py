from aqt.qt import *


class ActionBox(QWidget):
    def __init__(self, col, suspending, on_action):
        QWidget.__init__(self)
        self.col = col
        self.suspending = suspending
        self.on_action = on_action

        self.query = self.my_filter = self.field = None
        self.good_cids = []

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(3)

        self.label = QLabel()
        self.button = QPushButton('Suspend' if suspending else 'Unsuspend')
        self.button.clicked.connect(self.take_action)

        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def update_filtering(self, query, my_filter, field):
        self.query = query
        self.my_filter = my_filter
        self.field = field
        self.redraw()

    def take_action(self):
        if self.suspending:
            action = self.col.sched.suspendCards
        else:
            action = self.col.sched.unsuspendCards
        action(self.good_cids)
        self.on_action()

    def redraw(self):
        cids = self.col.findCards(self.query)
        if not (self.query and self.my_filter and self.field):
            return
        field_values = [self.col.getCard(cid).note()[self.field] for cid in cids]
        self.good_cids = []
        for cid, field_value in zip(cids, field_values):
            if self.suspending ^ self.my_filter(field_value):
                self.good_cids.append(cid)
        print(self.query)
        print(len(self.good_cids))
        if len(self.good_cids) > 0:
            print(self.col.getCard(self.good_cids[0]).note()[self.field])
        print()
        self.label.setText('# cards: {}'.format(len(self.good_cids)))
        self.button.setFlat(len(self.good_cids) == 0)
