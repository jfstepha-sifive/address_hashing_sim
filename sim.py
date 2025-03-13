def reverse(str):
    return str[::-1]

class numberWithEcc:
    def __init__(self, value, address=0, odd_parity=True):
        self.address = address
        self.odd_parity = odd_parity
        self.address_bits = 8
        self.data_bits = 32
        self.hamming_bits = 6

        # init values will get overwritten
        self.in_value = 0
        self.ecc = 0
        self.parity = 0
        self.dw = 0
        self.num_ones = 0
        self.address_parity = 0
        self.write(value, address) # calculate ecc, parity

    def count_ones(self):
        self.num_ones = bin(self.dw).count('1') + bin(self.ecc).count('1') + bin(self.parity).count('1') 

    def calculate_parity(self, odd=True):
        self.parity = bin(self.in_value).count('1') % 2
        # print(f"even parity: bin:{bin(self.in_value)} count {bin(self.in_value).count('1')} parity:", self.parity)
        if odd:
            self.parity = 1 - self.parity
    def calculate_address_parity(self, odd=False):
        self.address_parity = bin(self.address).count('1') % 2
        if odd:
            self.address_parity = 1 - self.address_parity

    def write(self, value, address=0):
        self.set_data(value)
        self.calc_ecc()
        self.calculate_parity(self.odd_parity)
        self.address = address
        self.calculate_address_parity()
        self.dw = self.in_value ^ (address*2 + self.address_parity)
        self.count_ones()
    
    def set_data(self, value):
        self.in_value = value

    def inject_sb_error(self, bit_pos):
        self.dw ^= 1 << bit_pos

    def inject_db_error(self, bit_pos):
        self.dw ^= 3 << bit_pos

    # hamming codes copied from https://www.geeksforgeeks.org/hamming-code-implementation-in-python/
    def posRedundantBits(self, data, r, pchar='0'):
    
        # Redundancy bits are placed at the positions
        # which correspond to the power of 2.
        j = 0
        k = 1
        m = len(data)
        res = ''
    
        # If position is power of 2 then insert '0'
        # Else append the data
        for i in range(1, m + r+1):
            if(i == 2**j):
                res = res + pchar
                j += 1
            else:
                res = res + data[-1 * k]
                k += 1
    
        # The result is reversed since positions are
        # counted backwards. (m + r+1 ... 1)
        return res[::-1]
    
    def calcParityBits(self, arr, r):
        n = len(arr)
    
        # For finding rth parity bit, iterate over
        # 0 to r - 1
        for i in range(r):
            val = 0
            for j in range(1, n + 1):
    
                # If position has 1 in ith significant
                # position then Bitwise OR the array value
                # to find parity bit value.
                if(j & (2**i) == (2**i)):
                    val = val ^ int(arr[-1 * j])
                    # -1 * j is given since array is reversed
    
            # String Concatenation
            # (0 to n - 2^r) + parity bit + (n - 2^r + 1 to n)
            arr = arr[:n-(2**i)] + str(val) + arr[n-(2**i)+1:]
        return arr
    
    def detectError(self, arr, nr):
        n = len(arr)
        res = 0
    
        # Calculate parity bits again
        for i in range(nr):
            val = 0
            for j in range(1, n + 1):
                if(j & (2**i) == (2**i)):
                    val = val ^ int(arr[-1 * j])
    
            # Create a binary no by appending
            # parity bits together.
    
            res = res + val*(10**i)
    
        # Convert binary to decimal
        return int(str(res), 2)

    def getHamming(self,arr, r):
        #print("\n")
        #print(f"getting hamming bits from {arr} ")
        res = ''
        arr_rev = arr[::-1]
    
        # Calculate parity bits again
        for i in range(r):
            pos = 2**i - 1
            bit = arr_rev[pos]
            res += bit
            #print(f"bit {i} position {pos} bit {bit}: res={res}")
    
        # Convert binary to decimal
        return res
    
    def calc_ecc(self):
        data_str = "{:032b}".format(self.in_value)
        arrx = self.posRedundantBits(data_str,r=6, pchar="x")
        arr = self.posRedundantBits(data_str,r=6, pchar="0")
        arr2 = self.calcParityBits(arr, r=6)
        h = self.getHamming(arr2, r=6)
        self.ecc = int(h, 2)

    def print_monia_order(self, header=True, print_hex=False):
        self.print(header, print_hex, True)

    def print(self, header=True, print_hex=False, monia_order=False):
        if print_hex:
            print("\ninput value: ", self.in_value, "0x{:08x}".format(self.in_value))
            print("\naddress: ", self.address, "0x{:08x}".format(self.address))
        if header:
            if monia_order:
                print("**** don't believe this order, it is probably broken! **** ")
                print("value: ", self.in_value, "0x{:08x}".format(self.in_value))
                print("address   datapart1_.......data_part2......_hammng_p  DW:datapart1_.......data_part2......_hammng_p")
                print("aaaaaaaaap ddddddddd_ddddddddddddddddddddddd_pppppp_p     ddddddddd_ddddddddddddddddddddddd_pppppp_p")
                print("aaaaaaaaaa 000000000_11111111112222222222333_000013_p     000000000_11111111112222222222333_000013_p")
                print("123456789p 123456789_01234567890123456789012_124862_p     123456789_01234567890123456789012_124862_p  ones")
            else:
                print("\n")
                # print("address    p_hammng_..........datapart2...._datapart1  DW:p_hammng_..........datapart2...._datapart1")
                h1 = "address" + " " * (self.address_bits - len("address") + 2)
                h1 += "p_hamm" + "." * (self.hamming_bits - len("p_hamm") + 2) + "_"
                h1 += "datapart2" + "." * (self.data_bits - self.address_bits - len("datapart2")) + "_"
                h1 += "datprt1" + "." * (self.address_bits - len("datprt1")) + "  "
                h1 += "DW:"
                h1 += "p_hamm" + "." * (self.hamming_bits - len("p_hamm") + 2) + "_"
                h1 += "datapart2" + "." * (self.data_bits - self.address_bits - len("datapart2")) + "_"
                h1 += "datprt1" + "." * (self.address_bits - len("datprt1")) + "  "
                print(h1)
                # print("aaaaaaaaap p_hhhhhh_ddddddddddddddddddddddd_ddddddddd     p_hhhhhh_ddddddddddddddddddddddd_ddddddddd")
                h2 = "a" * self.address_bits + "p "
                h2 += "p_" + "h" * self.hamming_bits + "_"
                h2 += "d" * (self.data_bits - self.address_bits) + "_"
                h2 += "d" * self.address_bits + "  "
                h2 += "DW:"
                h2 += "p_" + "h" * self.hamming_bits + "_"
                h2 += "d" * (self.data_bits - self.address_bits) + "_"
                h2 += "d" * self.address_bits + "  "
                print(h2)
                # print("aaaaaaaaaa p_310000_33222222222211111111110_000000000     p_310000_33222222222211111111110_000000000")
                h3 = "a" * self.address_bits + "p "
                h3 = ''.join("{:02d}".format(i)[0] for i in range(self.address_bits-1, -1, -1)) + "p "
                h3 += "p_" + ''.join("{:02d}".format(2**i)[0] for i in range(self.hamming_bits-1, -1, -1)) + "_"
                h3 += ''.join("{:02d}".format(i)[0] for i in range(self.data_bits-1, self.address_bits, -1)) + "_"
                h3 += ''.join("{:02d}".format(i)[0] for i in range(self.address_bits, -1, -1)) + "  "
                h3 += "DW:"
                h3 += "p_" + "0" * self.hamming_bits + "_"
                h3 += "1" * (self.data_bits - self.address_bits) + "_"
                h3 += "0" * self.address_bits + "  "
                print(h3)
                # print("123456789p p_268421_10987654321098765432109_876543210     p_268421_10987654321098765432109_876543210 ones")
                h4 = ''.join("{:02d}".format(i)[1] for i in range(self.address_bits-1, -1, -1)) + "p "
                h4 += "p_" + ''.join("{:02d}".format(2**i)[1] for i in range(self.hamming_bits-1, -1, -1)) + "_"
                h4 += ''.join("{:02d}".format(i)[1] for i in range(self.data_bits-1, self.address_bits, -1)) + "_"
                h4 += ''.join("{:02d}".format(i)[1] for i in range(self.address_bits, -1, -1)) + "  "
                h4 += "DW:"
                h4 += "p_" + ''.join("{:02d}".format(2**i)[1] for i in range(self.hamming_bits-1, -1, -1)) + "_"
                h4 += ''.join("{:02d}".format(i)[1] for i in range(self.data_bits-1, self.address_bits, -1)) + "_"
                h4 += ''.join("{:02d}".format(i)[1] for i in range(self.address_bits, -1, -1)) + "  "
                print(h4)

        num_str = "{:0{width}b}".format(self.address, width=self.address_bits) + "{:01b}".format(self.address_parity) + " "
        num_str += "{:01b}".format(self.parity)
        num_str += "_"
        num_str += "{:0{width}b}".format(self.ecc, width=self.hamming_bits)
        num_str += "_"
        data_str = "{:0{width}b}".format(self.in_value, width=self.data_bits)
        split_at = self.data_bits - self.address_bits - 1
        num_str +=  data_str[0:split_at] + "_" + data_str[split_at:32] 
        num_str += "  DW:"
        num_str += "{:01b}".format(self.parity)
        num_str += "_"
        num_str += "{:06b}".format(self.ecc)
        num_str += "_"
        data_str = "{:032b}".format(self.dw)
        num_str +=  data_str[0:23] + "_" + data_str[23:32] 
        num_str += " " + str(self.num_ones)
        if monia_order:
            num_str = reverse(num_str)
        print(num_str)



def test_print():
    print("hello world")

    data = numberWithEcc(0)
    data.print()

    data.set_data(1)
    data.print(True, True)

    data.set_data(2)
    data.print(True, True)

    data.set_data(0)
    data.print(True)

    for i in range(0, 32):
        data.write(2**i)
        data.print(False,False)

    data.write(0)
    data.print(True)

    for i in range(0, 256):
        data.write(i)
        data.print(False,False)

    print("\nmonia's order:")

    data.print_monia_order()


    n = 0

def test_hamming():
    print("Walking 1s:")
    data = numberWithEcc(0)
    data.print()
    for i in range(0, 32):
        data.write(2**i)
        data.print(header=False)

    print("Count:")
    data = numberWithEcc(0)
    data.print()
    for i in range(0, 256):
        data.write(i)
        data.print(header=False)

def test_hashing():
    print("Walking 1s vs 0:")
    data = numberWithEcc(0)
    data.print()
    for i in range(0, data.address_bits):
        data.write(0, 2**i)
        data.print(header=False)

    print("Walking 1s vs 1:")
    data = numberWithEcc(2**(data.address_bits+1)-1, 0)
    data.print()
    for i in range(0, data.address_bits):
        data.write(2**(data.address_bits+1)-1, 2**i)
        data.print(header=False)

def test_injection():
    print("Walking 1s vs 0:")
    data = numberWithEcc(0)
    data.print()
    for i in range(0, 39):
        data.write(0)
        data.inject_sb_error(i)
        data.print(header=False)

def count_all_single_ones():
    ones_cases = []
    data_bits = 32
    data = numberWithEcc(value=0, address=0)
    j=0
    for i in range(0, 2**data_bits):
        for a in range(0, 2**data.address_bits):
            data = numberWithEcc(value=i, address=a)
            # data.print(header=False)
            if data.num_ones == 1:
                print(f"found one case: address={a} data={i}")
                data.print(header=True, print_hex=True)
                ones_cases.append({"data":i, "address":a})
            j += 1
            if j % 100000 == 0:
                print(f"i={i} / {2**data_bits} a="+ "{:4d}".format(a)  + " %.6f"%(100*i/(2**data_bits)) + f"% found "+str(len(ones_cases))+" cases" + "(0x{:08x})".format(i) + " " + str(int.bit_length(i)) + " bits" )  

    if True:
        unique_addresses = []
        print("all cases:")
        for case in ones_cases:
            print(case)

        first_flag = True
        for case in ones_cases:
            data = numberWithEcc(case["data"], case["address"])
            if first_flag:
                data.print(header=True, print_hex=True)
                first_flag = False
            else:
                data.print(header=False, print_hex=False)
            if case["address"] not in unique_addresses:
                unique_addresses.append(case["address"])
        print( f"total cases: {len(ones_cases)} out of {2**data.address_bits} addresses and {2**data.address_bits * 2**data_bits} total values")
        print( f"unique addresses: {len(unique_addresses)}")

    


def main():
    # test_print()

    # test_hamming()

    # test_hashing()

    count_all_single_ones()

if __name__ == "__main__":
    main()
