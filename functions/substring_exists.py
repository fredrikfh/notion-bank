def substring_exist(string, substrings):
    for substring in substrings:
        if string.find(substring) != -1:
            return True
    return False
