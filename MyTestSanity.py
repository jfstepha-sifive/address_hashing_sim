








### this is old.  Use ZerosAndOnesTest.py instead










import sys
sys.path.append('../JulianBaileyUseful/py/protections')
from ecc import codes

def myprint(encodedData,syndromeWidth):
    syndrome = encodedData >> bits
    encodedDataData = encodedData & ((1<<bits)-1)
    return f"{encodedDataData:0{bits}b} {syndrome:0{syndromeWidth}b}"


if __name__ == "__main__":

    print()
    print("** Hamming 8 4 (SECDED) Code Test **")
    bits=4
    code = codes.OddOddSECDEDCode(bits)
    syndromeWidth = code.encodedWidth() - bits
    print(f"  data bits {bits}")
    print(f"  code bits {code.encodedWidth()}")
    print(f"  Masks:")
    for m in code.sec.codeMasks:
        print(f"    {m:08b}")

    encoding_all_zero_count = 0
    encoding_all_one_count = 0
    for i in range(0, 1<<bits):
        encodedData = code.encode(i)
        syndrome = encodedData >> bits
        encodedDataData = encodedData & ((1<<bits)-1)
        all_zero = "    "
        all_one = "   "

        if encodedData == 0:
            all_zero = "ZERO"
            encoding_all_zero_count += 1
        if encodedData == (1<<code.encodedWidth())-1:
            all_one = "ONE"
            encoding_all_one_count += 1
        print(f"  {i:0{bits}b} -> {encodedDataData:0{bits}b} {syndrome:0{syndromeWidth}b} {all_zero} {all_one}")

    print()
    print(f" all zeros: {encoding_all_zero_count}")
    print(f" all ones: {encoding_all_one_count}")

    print()
    print(" *single bit injection:*")
    sb_all_zero_count = 0
    sb_all_one_count = 0
    for i in range(0, code.encodedWidth()):
        print(f"-- bit {i} --")
        print ( "  " + "data".ljust(bits) + " -> " + "encoded".ljust(code.encodedWidth()+1) + " -> " + "injected".ljust(code.encodedWidth()+1) + " -> " + "decoded".ljust(code.encodedWidth()+1) + " -> " + "cor/uncor")
        sb_this_zero_count = 0
        sb_this_one_count = 0

        for j in range(0, 1<<bits):
            encodedData = code.encode(j)
            injected = encodedData ^ (1<<i)
            decoded = code.decode(injected)
            all_zero = "    "
            all_one = "   "
            if encodedData == 0:
                sb_this_zero_count += 1
                all_zero = "ZERO"
            if encodedData == (1<<code.encodedWidth())-1:
                sb_this_one_count += 1
                all_one = "ONE"
            print(f"  {j:0{bits}b} -> {myprint(encodedData,syndromeWidth)} -> {myprint(injected,syndromeWidth)} -> {myprint(decoded.corrected,syndromeWidth)} -> {decoded.correctable}/{decoded.uncorrectable} {all_zero} {all_one}")

        sb_all_zero_count += sb_this_zero_count
        sb_all_one_count += sb_this_one_count

        print(f"  all zeros: {sb_this_zero_count}")
        print(f"  all ones: {sb_this_one_count}")
        sb_all_zero_count += sb_this_zero_count
        sb_all_one_count += sb_this_one_count

    print(f" single bit all zeros: {sb_all_zero_count}")
    print(f" single bit all ones: {sb_all_one_count}")
