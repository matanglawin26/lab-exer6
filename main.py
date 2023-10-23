class CheckError:
    def parse_bits(self):
        while len(self.data) > 0:
            self.bits.append(self.data[:self.bit_length])
            self.data = self.data[self.bit_length:]


class SimpleParity:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.codeword = None
        self.dataword = None
        self.simulate()

    def simulate(self):
        self.sender()
        self.receiver()

    def sender(self):
        self.codeword = self.encoder()

    def receiver(self):
        self.dataword = self.decoder()

    def encoder(self):
        dataword_sum = sum(
            # Gets the sum of the dataword bits
            map(lambda x: int(x), filter(lambda x: len(x), self.a)))
        if dataword_sum % 2 == 0:  # Generate Parity Bit
            codeword = self.a + '0'
        else:
            codeword = self.a + '1'

        return codeword

    def decoder(self):
        codeword_sum = sum(
            # Gets the sum of the codeword bits
            map(lambda x: int(x), filter(lambda x: len(x), self.b)))

        if codeword_sum % 2 == 0:
            syndrome = 0  # or False
        else:
            syndrome = 1  # or True

        return "Discarded" if syndrome else "Accepted"

    def __str__(self):
        return 'Codeword:%s\nData word: %s' % (self.codeword, self.dataword)


class TwoDParity(CheckError):
    def __init__(self, data):
        self.data = data
        self.error_count = 0
        self.bit_length = 9
        self.bits = []
        self.simulate()

    def simulate(self):
        self.parse_bits()
        self.get_row_sum()
        self.get_col_sum()

    def get_row_sum(self):
        for row in self.bits:
            parity_bit = int(row[-1])
            dataword_sum = sum(
                # Gets the sum of the codeword bits
                map(lambda x: int(x), filter(lambda x: len(x), row[:-1])))

            # Checks if the parity bit correctly corresponds to the dataword
            if (dataword_sum % 2 == 0 and parity_bit == 1) or (dataword_sum % 2 != 0 and parity_bit == 0):
                self.error_count += 1

    def get_col_sum(self):
        parity_row = self.bits[-1]
        for col in range(8):  # Since datawords are 8 bits
            col_sum = 0

            for row in self.bits[:-1]:
                col_sum += int(row[col])

            if (col_sum % 2 == 0 and int(parity_row[col]) == 1) or (col_sum % 2 != 0 and int(parity_row[col]) == 0):
                self.error_count += 1

    def __str__(self):
        return 'Error count: %s' % (self.error_count)


class Checksum(CheckError):
    def __init__(self, data):
        self.data = data
        self.bit_length = 8
        self.bits = []
        self.checksum = ''
        self.sum = ''
        self.simulate()

    def simulate(self):
        self.parse_bits()
        self.checksum = self.get_sum(self.bits[:-1])
        self.sum = self.get_sum([self.bits[-1], self.checksum])

    def get_sum(self, bits):
        while len(bits) > 1:
            bit_sum = self.add_bits(bits[0], bits[1])
            if len(bit_sum) > self.bit_length:
                bits[0], bits[1] = bit_sum[:8][::-1], bit_sum[8:].zfill(8)
            else:
                bits = [bit_sum[::-1]] + bits[2:]

        return bit_sum[::-1]

    def add_bits(self, row_1, row_2):
        bit_sum = ''
        carry = 0
        for col in range(self.bit_length):
            col_sum = int(row_1[self.bit_length-col-1]) + \
                int(row_2[self.bit_length-col-1]) + carry

            if col_sum < 2:
                carry = 0
                bit_sum += str(col_sum)
            else:
                carry = 1
                if col_sum % 2 == 0:
                    bit_sum += '0'
                else:
                    bit_sum += '1'

        if carry:
            bit_sum += '1'

        return bit_sum

    def __str__(self):
        return 'Accept data' if self.sum == '11111111' else 'Reject Data'


class CRC:
    def __init__(self, data, keyword):
        self.keyword = keyword
        self.data = data[len(self.keyword) - 1:]
        self.remainder = data[:len(self.keyword) - 1]
        self.simulate()

    def simulate(self):
        kw_len = len(self.keyword)

        while len(self.data) > 0:
            self.remainder += self.data[0]
            self.data = self.data[1:]
            if self.remainder[0] == '1':
                self.remainder = self.get_xor(self.keyword)
            else:
                zero_bits = '0' * kw_len
                self.remainder = self.get_xor(zero_bits)

    def get_xor(self, curr_bits):
        kw_len = len(self.keyword)
        xor = ''
        for i in range(1, kw_len):
            xor += str(int(self.remainder[i]) ^ int(curr_bits[i]))

        return xor

    def __str__(self):
        return 'Accept data' if self.remainder == '000' else 'Reject data'


def get_result():
    p = int(input())

    if p == 1:
        a = input()
        b = input()
        return SimpleParity(a, b)
    elif p == 2:
        data = input()
        return TwoDParity(data)
    elif p == 3:
        data = input()
        return Checksum(data)
    elif p == 4:
        data = input()
        keyword = input()
        return CRC(data, keyword)


def main():
    result = get_result()

    print(result)

    return


main()
