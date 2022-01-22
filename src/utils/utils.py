def is_num(string):
    for c in string:
        if c not in "0123456789":
            return False
    return True
