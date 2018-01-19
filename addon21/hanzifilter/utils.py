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
