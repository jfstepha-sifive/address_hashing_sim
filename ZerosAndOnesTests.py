import sys
import tests.ZerosAndOnesTest
from accodes.ACSECCodes import ACSECCodes
from JulianBaileyUseful.py.protections.ecc.codes.SECDEDCodes import SECDEDType
from accodes.ACSECDEDCodes import ACSECDEDCodes
from accodes.ACSECDEDCodes import ACSECDEDType

from JulianBaileyUseful.py.protections.ecc import codes

### this is the top-level tests code that runs all the tests.  The tests are
### defined in tests/ZerosAndOnesTest.py

if __name__ == "__main__":

    print()

    print("Dummy test")
    code = codes.OddOddSECDEDCode(4)
    test = tests.ZerosAndOnesTest.ZerosAndOnesTest(code)
    result = test.testPass()
    print(f"  result: {result}")


    print()
    print("** Hamming 8 4 (SECDED) Code Test **")
    bits=4
    code = codes.EvenEvenSECDEDCode(bits)
    test = tests.ZerosAndOnesTest.ZerosAndOnesTest(code)
    result = test.runTestAllRandom(print_all = False, print_errors = True )

    print()
    bits=8
    print(f"** Hamming {bits} (SECDED) Code Test **")
    code = codes.EvenEvenSECDEDCode(bits)
    test = tests.ZerosAndOnesTest.ZerosAndOnesTest(code)
    result = test.runTestAllRandom(print_all = False, print_errors = True )

    print()
    bits = 4 
    print(f"** Hamming {bits} (SECDED) Injection Test **")
    code = codes.EvenEvenSECDEDCode(bits)
    test = tests.ZerosAndOnesTest.ZerosAndOnesTest(code)
    result = test.runOneSingleBitInjection(0, 0, print_all = True, print_errors = True )

    print()
    bits = 6 
    print(f"** Hamming {bits} (SECDED) All bits Injection Test **")
    code = codes.OddEvenSECDEDCode(bits)
    test = tests.ZerosAndOnesTest.ZerosAndOnesTest(code)
    result = test.runTestAllSingleBitInjections(print_all = True, print_errors = True )

    print()
    data_bits = 4
    address_bits = 4
    print(f"** ACSEC {data_bits} {address_bits} Code Test **")
    code = ACSECCodes(data_bits, address_bits,  False)
    code.printInfo()
    print(f"encoded example {code.encode(1,2):0{code.encodedWidth()}b}")
    test = tests.ZerosAndOnesTest.ZerosAndOnesTest(code)
    result = test.runOneTestAC(data=0, address=0, print_all = True, print_errors = True, print_header = True )
    # result = test.runTestAllBinAC(print_all = True, print_errors = True )

    print()
    data_bits = 4
    address_bits = 4
    print(f"** ACSECDED {data_bits} {address_bits} Code Test **")
    code = ACSECDEDCodes(data_bits, address_bits, ACSECDEDType.CODE_ODD_EVEN)
    code.printInfo()
    test = tests.ZerosAndOnesTest.ZerosAndOnesTest(code)
    print(f"encoded example {code.encode(1,2):0{code.encodedWidth()}b}")
    result = test.runOneTestAC(data=1, address=0, print_all = True, print_errors = True, print_header = True )
    result = test.runTestAllBinAC(print_all = True, print_errors = True )

    print()
    ### this is the problimatic code that fails the all 0's test
    data_bits = 6
    address_bits = 4
    print(f"** ACSECDED {data_bits} {address_bits} Code Test **")
    code = ACSECDEDCodes(data_bits, address_bits, ACSECDEDType.CODE_ODD_EVEN)
    code.printInfo()
    test = tests.ZerosAndOnesTest.ZerosAndOnesTest(code)
    # print(f"encoded example {code.encode(1,2):0{code.encodedWidth()}b}")
    #result = test.runOneTestAC(data=1, address=0, print_all = True, print_errors = True, print_header = True )
    #result = test.runOneTestAC(data=0, address=0, print_all = True, print_errors = True, print_header = True )
    result = test.runTestAllRandAC(print_all = False, print_errors = True )

    print()
    data_bits = 7
    address_bits = 4
    print(f"** ACSEC {data_bits} {address_bits} Code Test **")
    code = ACSECCodes(data_bits, address_bits,  False)
    code.printInfo()

    print()
    data_bits = 4
    address_bits = 2
    print(f"** ACSECDED {data_bits} {address_bits} Code Test **")
    code = ACSECDEDCodes(data_bits, address_bits, ACSECDEDType.CODE_EVEN_EVEN)
    code.printInfo()
    test = tests.ZerosAndOnesTest.ZerosAndOnesTest(code)
    # print(f"encoded example {code.encode(1,2):0{code.encodedWidth()}b}")
    #result = test.runTestAllBinAC(print_all = True, print_errors = True )
    # test.runOneTestAC(data=0, address=0, print_all = True, print_errors = True, print_header = True )
    test.runTestAllBinAC(print_all = True, print_errors = True )


    print()
    data_bits = 4
    address_bits = 2
    print(f"** ACSECDED Partial parity code {data_bits} {address_bits} Code Test **")
    code = ACSECDEDCodes(data_bits, address_bits, ACSECDEDType.CODE_ODD_EVENd)
    code.printInfo()
    test = tests.ZerosAndOnesTest.ZerosAndOnesTest(code)
    # print(f"encoded example {code.encode(1,2):0{code.encodedWidth()}b}")
    #result = test.runTestAllBinAC(print_all = True, print_errors = True )
    #test.runOneTestAC(data=0, address=0, print_all = True, print_errors = True, print_header = True )
    #test.runOneTestAC(data=0, address=1, print_all = True, print_errors = True, print_header = True )
    #test.runOneTestAC(data=1, address=0, print_all = True, print_errors = True, print_header = True )
    test.runTestAllBinAC(print_all = True, print_errors = True )
    


    print()
    data_bits = 7
    address_bits = 4
    print(f"** ACSECDED Partial parity code {data_bits} {address_bits} Code Test (perfect code) **")
    code = ACSECDEDCodes(data_bits, address_bits, ACSECDEDType.CODE_ODD_EVENd)
    code.printInfo()
    test = tests.ZerosAndOnesTest.ZerosAndOnesTest(code)
    # print(f"encoded example {code.encode(1,2):0{code.encodedWidth()}b}")
    #result = test.runTestAllBinAC(print_all = True, print_errors = True )
    #test.runOneTestAC(data=0, address=0, print_all = True, print_errors = True, print_header = True )
    #test.runOneTestAC(data=0, address=1, print_all = True, print_errors = True, print_header = True )
    #test.runOneTestAC(data=1, address=0, print_all = True, print_errors = True, print_header = True )
    test.runTestAllBinAC(print_all = False, print_errors = True )

    print()
    data_bits = 4
    address_bits = 2
    print(f"** ACSEC {data_bits} {address_bits} Single bit injection test **")
    code = ACSECCodes(data_bits, address_bits,False)
    code.printInfo()
    test = tests.ZerosAndOnesTest.ZerosAndOnesTest(code)
    # print(f"encoded example {code.encode(1,2):0{code.encodedWidth()}b}")
    #result = test.runTestAllBinAC(print_all = True, print_errors = True )
    #test.runOneTestAC(data=0, address=0, print_all = True, print_errors = True, print_header = True )
    #test.runOneTestAC(data=0, address=1, print_all = True, print_errors = True, print_header = True )
    #test.runOneTestAC(data=1, address=0, print_all = True, print_errors = True, print_header = True )
    result = test.runOneSingleBitInjectionAC(0, 0, 0, print_all = True, print_errors = True )

    print()
    data_bits = 4
    address_bits = 2
    print(f"** ACSEC {data_bits} {address_bits} Single bit injection test **")
    code = ACSECCodes(data_bits, address_bits,False)
    code.printInfo()
    test = tests.ZerosAndOnesTest.ZerosAndOnesTest(code)
    test.runTestAllSingleBitInjectionsAC(print_all = True, print_errors = True, random_order = False )
    # test.runOneSingleBitInjectionAC(0, 0, 8, print_all = True, print_errors = True )

    print()
    data_bits = 5
    address_bits = 4
    print(f"** ACSECDED {data_bits} {address_bits} Single bit injection test **")
    code = ACSECDEDCodes(data_bits, address_bits, ACSECDEDType.CODE_ODD_EVEN)
    code.printInfo()
    test = tests.ZerosAndOnesTest.ZerosAndOnesTest(code)
    #test.runOneSingleBitInjectionAC(0, 0, 1, print_all = True, print_errors = True )
    test.runTestAllSingleBitInjectionsAC(print_all = False, print_errors = True, random_order = False )
    exit(0)

    print()
    data_bits = 7
    address_bits = 4
    print(f"** ACSECDED {data_bits} {address_bits} Single bit injection test (perfect code) **")
    code = ACSECDEDCodes(data_bits, address_bits, ACSECDEDType.CODE_ODD_EVENd)
    code.printInfo()
    test = tests.ZerosAndOnesTest.ZerosAndOnesTest(code)
    #test.runOneSingleBitInjectionAC(0, 0, 1, print_all = True, print_errors = True )
    test.runTestAllSingleBitInjectionsAC(print_all = False, print_errors = True, random_order = False )

    print()
    data_bits = 7
    address_bits = 4
    print(f"** ACSECDED {data_bits} {address_bits} Double bit injection test (perfect code) **")
    code = ACSECDEDCodes(data_bits, address_bits, ACSECDEDType.CODE_ODD_EVENd)
    code.printInfo()
    test = tests.ZerosAndOnesTest.ZerosAndOnesTest(code)
    test.runOneBitInjectionAC(0, 0, 1, 4, print_all = True, print_errors = True)
    test.runOneBitInjectionAC(0, 0, 0, 1, print_all = True, print_errors = True)
    test.runOneBitInjectionAC(0, 0, 5, 6, print_all = True, print_errors = True)

    print()
    data_bits = 2
    address_bits = 2
    print(f"** ACSECDED {data_bits} {address_bits} Single bit injection test **")
    code = ACSECDEDCodes(data_bits, address_bits, ACSECDEDType.CODE_ODD_EVENd)
    code.printInfo()
    test = tests.ZerosAndOnesTest.ZerosAndOnesTest(code)
    #test.runOneSingleBitInjectionAC(0, 0, 1, print_all = True, print_errors = True )
    test.runTestAllDoubleBitInjectionsAC(print_all = True, print_errors = True, random_order = False )
