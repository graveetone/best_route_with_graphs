class UASortingService:
    def __init__(self, l):
        self.list_ = l

    def call(self, comparator=None):
        ua_alphabet = 'абвгґдеєжзиіїйклмнопрстуфхцчшщьюя'
        ua_comparator = lambda s: [ua_alphabet.index(c) for c in s.lower() if c in ua_alphabet]

        return sorted(self.list_, key=lambda obj: ua_comparator(comparator(obj)) if comparator else ua_comparator(obj))
