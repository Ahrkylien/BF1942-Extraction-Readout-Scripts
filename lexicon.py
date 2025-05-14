import struct


def read_i(f, n=1, force_list=False):
    res = struct.unpack('I' * n, f.read(4 * n))
    if n == 1 and not force_list:
        return res[0]
    return res


def get_lexicon_data(file_path):
    try:
        with open(file_path, 'rb') as f:
            number_of_entries = read_i(f)
            number_of_columns = read_i(f)
            lexi_strings = f.read().decode("UTF-16 LE", 'ignore').split('\x00')
            lexi_dict = {lexi_strings[i * number_of_columns]:
                         lexi_strings[1 + i * number_of_columns:number_of_columns + i * number_of_columns]
                         for i in range(number_of_entries)}
            # Note: 38 unknown bytes in tail
            return lexi_dict
    except Exception:
        return False


def get_lexicon_entry(lexicon_dict, name, column=0):
    try:
        for name_lex in lexicon_dict:
            if name_lex.lower() == name.lower():
                return lexicon_dict[name_lex][column]
    except Exception:
        pass
    return name
