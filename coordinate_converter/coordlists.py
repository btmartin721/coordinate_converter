class Coords:

    pos = r"positive"
    neg = r"negative"

    def __init__(self, whole_entry):
        self.whole_entry = whole_entry
        self.parts = []

    def add_parts(self, part):
        self.parts.append(part)
