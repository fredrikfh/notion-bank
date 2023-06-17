def substring_exist(string, substrings):
    """ Returns True if any of the substrings exist in the string """
    for substring in substrings:
        if string.find(substring) != -1:
            return True
    return False
