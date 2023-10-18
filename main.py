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


class TwoDParity:
    def __init__(self, data):
        self.data = data
        self.error_count = 0
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

    def parse_bits(self):
        while len(self.data) > 0:
            self.bits.append(self.data[:9])
            self.data = self.data[9:]

    def __str__(self):
        return 'Error count: %s' % (self.error_count)


class Checksum:
    def __init__(self, data, keyword):
        self.data = data
        self.keyword = keyword


class CRC:
    def __init__(self):
        pass


def get_result():
    # p = int(input())
    p = 2
    if p == 1:
        # a = input()
        # b = input()
        a = '10010010'
        b = '100100101'
        return SimpleParity(a, b)
    elif p == 2:
        data = '101100111101010111010110100110101011100101111'
        return TwoDParity(data)
    elif p == 3:
        return
    elif p == 4:
        return


def main():
    result = get_result()

    print(result)

    return


main()
