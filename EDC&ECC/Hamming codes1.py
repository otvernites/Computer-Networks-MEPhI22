import re


# control bits (min)
def least_check_bit(block):
    s1 = int(block[2])
    for i in range(4, len(block), 2):
        s1 = s1 ^ int(block[i])
    return s1


# rest control bits
def check_bit(block, num):
    subsequence_length = 2**num
    s1 = int(block[subsequence_length])

    for i in range(subsequence_length-1, len(block), subsequence_length*2):
        k = 0
        for j in range(subsequence_length):
            if i == subsequence_length-1 and k == 0 or i == subsequence_length-1 and k == 1:
                k += 1
                continue
            else:
                if i+k < len(block):
                    s1 = s1 ^ int(block[i+k])
                    k += 1
    return s1


# error code calculation (one error bit)
def error_checking(block, count_check_bits):
        s = []
        s.append(least_check_bit(block))  # first
        for i in range(1, count_check_bits):
            s.append(check_bit(block, i))  # rest
        return s


# getting indexes of control bits
def get_control_id(count_check_bits):
    control_id = []
    for i in range(count_check_bits):
        control_id.append(2 ** i - 1)
    return control_id


# placement of a number in an X-digit grid
def adding_zeros(code_blocks, block_len):
    last_id = len(code_blocks) - 1
    zeros_to_fill = block_len - len(code_blocks[last_id])
    zeros = "".zfill(zeros_to_fill)
    code_blocks[last_id] += zeros


def decoding(code_blocks, block_len, count_check_bits):
    decoded = []

    for block in code_blocks:

        s = error_checking(block, count_check_bits)  # control bits
        err_place = -1

        for i in range(count_check_bits):
            if s[i] != int(block[2**i - 1]):
                err_place += 2**i  # determining the location of the error

        # invert wrong bit
        if err_place != -1:
            if block[err_place] == '0':
                new_block = block[:err_place] + '1' + block[err_place+1:]
            else:
                new_block = block[:err_place] + '0' + block[err_place+1:]
        else:
            new_block = block

        # remove control bits
        control_id = get_control_id(count_check_bits)
        tmp = ""
        for i in range(block_len):
            if i not in control_id:
                tmp += new_block[i]
        decoded.append(tmp)

    # split the message into octets
    symbols = "".join(decoded)
    word_len = 8
    code_words = [int(symbols[i:i + word_len], 2) for i in range(0, len(symbols), word_len)]
    for i in range(len(code_words)):  # transfer to ASCII-symbols
        code_words[i] = chr(code_words[i])
    return(''.join(code_words))


def encoding(num, block_len, count_check_bits):
    num = str(num)
    numbers = []
    for digit in num:
        tmp = ord(digit)
        numbers.append(format(int(tmp), '0>8b'))  # put the symbols in an eight-digit grid

    # blocks of information without control bits
    s = "".join(numbers)
    lenght = block_len - count_check_bits
    code_blocks = [s[i:i + lenght] for i in range(0, len(s), lenght)]
    # if the bit width of the last block is less than the desired
    adding_zeros(code_blocks, lenght)

    tmp_arr = []  # temporary array for intermediate calculations

    # adding control bits (fill with zeros first)
    control_id = get_control_id(count_check_bits)
    for block in code_blocks:
        new_block = block
        for i in range(block_len):
            if i in control_id:
                new_block = new_block[:i] + '0' + new_block[i:]
        tmp_arr.append(new_block)

    encoded_response = []

    # recalculate control bits
    for block in tmp_arr:
        new_control_bits = error_checking(block, count_check_bits)
        new_block = block
        counter_for_control_bits = 0
        for i in range(block_len):
            if i in control_id:
                if new_block[i] != str(new_control_bits[counter_for_control_bits]):
                    new_block = new_block[:i] + str(new_control_bits[counter_for_control_bits]) + new_block[i+1:]
                counter_for_control_bits += 1
        encoded_response.append(new_block[::-1])

    # split the message into octets
    symbols = "".join(encoded_response)
    word_len = 8
    code_words = [symbols[i:i + word_len] for i in range(0, len(symbols), word_len)]
    # if the bit width of the last block is less than the desired
    adding_zeros(code_words, word_len)
    code_words = [int(symb, 2) for symb in code_words]  # decimal conversion
    return(code_words)


if __name__ == "__main__":
    block_len = 27
    numbers = []

    with open("Numbers.txt", "r") as text:
        for number in text:
            tmp_nums = re.findall(r'\d+', number)
            for num in tmp_nums:
                numbers.append(format(int(num), '0>8b'))  # put the numbers in an eight-digit grid

    s = "".join(numbers)
    # data blocks of given length encoded in Hamming code
    code_blocks = [s[i:i + block_len] for i in range(0, len(s), block_len)]

    # number of check bits
    sqr = 1
    count_check_bits = 0
    while sqr <= block_len:
        sqr = sqr * 2
        count_check_bits += 1

    # if the bit width of the last block is less than the desired
    adding_zeros(code_blocks, block_len)

    code_blocks = [s[::-1] for s in code_blocks]  # lower digits - on the left

    message = decoding(code_blocks, block_len, count_check_bits)
    print(message)
    answer = encoding(9033457 * 3300596, block_len, count_check_bits)
    print(answer)

