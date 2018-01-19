from aqt.qt import *


class FieldSelector(QWidget):
    """A FieldSelector allows the user to select a deck, and a field of one of its note types."""
    def __init__(self, col, callback):
        """
        Creates a new FieldSelector.

        :param col: Anki Collection object
        :param callback: function to call when
        """
        QWidget.__init__(self)
        self.col = col
        self.callback = callback

        # Keep a list of decks
        decks = col.decks.all()
        self.deck_ids, self.deck_names = zip(*sorted([(deck['id'], deck['name']) for deck in decks],
                                                     key=lambda a: a[1]))

        # Blank for now, will be set depending on the deck chosen
        self.model_ids = []
        self.model_fields = []

        # The layout object
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(3)

        # Initialize the drop down menus
        self.deck_combobox = QComboBox(self)
        self.deck_combobox.setStyleSheet("combobox-popup: 0;")
        self.deck_combobox.setMinimumContentsLength(30)
        self.note_combobox = QComboBox(self)
        self.field_combobox = QComboBox(self)

        self.deck_combobox.addItems(self.deck_names)

        # Set the event listeners
        self.deck_combobox.currentIndexChanged.connect(self.deck_selected)
        self.note_combobox.currentIndexChanged.connect(self.note_selected)
        self.field_combobox.currentIndexChanged.connect(self.field_selected)

        # Add to layout
        for combobox, label in ((self.deck_combobox, 'Deck'),
                                (self.note_combobox, 'Note type'),
                                (self.field_combobox, 'Field')):
            vertical_layout = QVBoxLayout()
            vertical_layout.addWidget(QLabel(label))
            vertical_layout.addWidget(combobox)
            layout.addLayout(vertical_layout)
        self.setLayout(layout)

    def deck_selected(self, deck_index):
        did = self.deck_ids[deck_index]
        self.model_ids = []
        self.model_fields = []
        model_names = []
        for cid in self.col.decks.cids(did):
            card = self.col.getCard(cid)
            model = card.model()
            if model['id'] in self.model_ids:
                continue
            self.model_ids.append(model['id'])
            self.model_fields.append([field['name'] for field in model['flds']])
            model_names.append(model['name'])

        self.note_combobox.clear()
        self.note_combobox.addItems(model_names)

    def note_selected(self, note_index):
        self.field_combobox.clear()
        if note_index >= 0:
            self.field_combobox.addItems(self.model_fields[note_index])

    def field_selected(self, field_index):
        field = self.field_combobox.currentText()
        deck_name = self.deck_combobox.currentText()
        note_name = self.note_combobox.currentText()

        if '' in (field, note_name):
            return

        self.callback(deck_name, note_name, field)
