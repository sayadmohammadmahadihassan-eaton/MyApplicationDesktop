'''
Library for my tool
Authon: Sayad Hassan
'''

class MyLibrary:
    '''Library for my tool'''
    def __init__(self):
        pass

    def strip_symbol_and_check_empty_space(self, line):
        '''
        Function to check for symbols and strip them. Also, if the pair
        includes an empty space or missing key/value, then add '_'.

        :return key, value: replaced symbols and space values.
        '''
        if len(line.split()) <= 2:
            parts = line.split(':')
            key = ''.join(filter(str.isdigit, parts[0].strip())) if parts[0].strip() else '_'
            value = ''.join(filter(str.isdigit, parts[1].strip())) if parts[1].strip() else '_'
            return key, value
        else:
            key, value = line.strip().split(None, 1)
            key = ''.join(filter(str.isdigit, key))
            value = ''.join(filter(str.isdigit, value))
            return key, value


    def read_key_value_pairs(self, txt_file):
        '''
        read a file to get key value from txt file.

        :return key_value_pairs: list of keys value pairs
        '''
        key_value_pairs = {}

        with open(txt_file, 'r', encoding='utf-8') as file:
            lines = file.read().strip().split('\n')
            for line in lines:
                # ignore empty line space and comment lines
                if line.strip() and not line.strip().startswith('#'):
                    key, value = self.strip_symbol_and_check_empty_space(line)
                    key_value_pairs[key] = value
        return key_value_pairs


    def read_keys(self, key_txt_file):
        '''
        read a file to filter only keys.

        :return keys, key_value_pair: list of keys and key value pair list
        '''
        keys = []
        key_value_pair = []
        with open(key_txt_file, 'r', encoding='utf-8') as text_file:
            lines = text_file.read().strip().split('\n')
            for line in lines:
                # ignore empty space and comment lines
                if line.strip() and not line.strip().startswith('#'):
                    key, value = self.strip_symbol_and_check_empty_space(line)
                    keys.append(key)
                    key_value_pair.append(f'{key} : {value}')

        return keys, key_value_pair

    def read_integer(self, txt_file):
        '''
        read a file to filter only keys.

        :return _integer: list of integers
        '''
        _integer = []
        with open(txt_file, 'r', encoding='utf-8') as text_file:
            lines = text_file.read().strip().split('\n')
            for line in lines:
                # ignore empty space and comment lines
                if line.strip() and not line.strip().startswith('#'):
                    _integer.append(line.strip())

        return _integer
    
    def read_links(self):
        '''
        read a file for links.

        :return _links: list of links
        '''
        _links = []
        with open('app.txt', 'r', encoding='utf-8') as text_file:
            lines = text_file.read().strip().split('\n')
            for line in lines:
                    _links.append(line.strip())

        return _links

if __name__=='__main__':
    m = MyLibrary()
    exe_app_links = m.read_links()
    app_list_top = ['prepare_eep_file_tool', 'com_files_with_given_keys_tool', 'hmi']
    app_list_top.extend(exe_app_links)
    print(app_list_top)
