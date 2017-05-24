'''2016.12.25
專門處理String
'''


import string


abc123 = ''.join(map(chr, range(42)))
abc123_ = abc123.join(map(chr, range(43, 124)))
abc123_ = abc123_.join(map(chr, range(125, 127)))
abc123 = abc123.join(map(chr, range(43, 127)))


# str去中文
def no_chinese(input):
    delete = input.translate(str.maketrans('', '', abc123))
    output = input.translate(str.maketrans('', '', delete))
    return output


# str去中文以外
def no_abc123(input):
    output = input.translate(str.maketrans('', '', abc123))
    return output

# str去中文和'|'以外
def no_abc123_(input):
    output = input.translate(str.maketrans('', '', abc123_))
    return output

# main function
if __name__ == "__main__":
    string = 'vsij是你v34決定2:@我|的傷心%*'
    print(string)
    print(no_chinese(string))
    print(no_abc123(string))
    print(no_abc123_(string))
