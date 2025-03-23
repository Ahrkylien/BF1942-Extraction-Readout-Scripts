import struct


def read_i(f, n=1, forceList=False):
    res = struct.unpack('I' * n, f.read(4 * n))
    if n == 1 and not forceList:
        return res[0]
    return res


def getLexiconData(filePath):
    try:
        with open(filePath, 'rb') as f:
            numberOfEntries = read_i(f)
            numberOfColumns = read_i(f)
            lexiStrings = f.read().decode("UTF-16 LE", 'ignore').split('\x00')
            lexiDict = {lexiStrings[i * numberOfColumns]:
                        lexiStrings[1 + i * numberOfColumns:numberOfColumns + i * numberOfColumns]
                        for i in range(numberOfEntries)}
            # Note: 38 unknown bytes in tail
            return lexiDict
    except:
        return False


def getLexiconEntry(lexiconDict, name, column=0):
    try:
        for name_lex in lexiconDict:
            if name_lex.lower() == name.lower():
                return lexiconDict[name_lex][column]
    except:
        pass
    return name
