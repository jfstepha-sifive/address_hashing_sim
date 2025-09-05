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

    print("\n\n******************* Directed tests that prove points *********************")
    print("***** test ACSECDED 9 2 - E E *****")
    code = ACSECDEDCodes(dWidth=9, aWidth=2, codeType=ACSECDEDType.CODE_EVEN_EVEN)
    code.printInfo()
    test = tests.ZerosAndOnesTest.ZerosAndOnesTest(code)
    test.runOneTestAC(data=0, address=0, print_all = True, print_errors = True, print_header = True )
    print("**(fails zero check on all 0s because even-even. Also does not meet constraints)**")

    print("***** test ACSECDED 9 2 - E O *****")
    code = ACSECDEDCodes(dWidth=9, aWidth=2, codeType=ACSECDEDType.CODE_EVEN_ODD)
    code.printInfo()
    test = tests.ZerosAndOnesTest.ZerosAndOnesTest(code)
    #test.runTestAllSingleBitInjectionsAC(print_all = False, print_errors = True, random_order = True )
    test.runOneBitInjectionAC(data=0, address=0, bit=15, bit2=None, print_all = True, print_errors = True, print_header = True )
    print("**(fails zero check on all 0s on injection. Also does not meet constraints)**")

    print("***** test ACSECDED 26 20 - E E *****")
    code = ACSECDEDCodes(dWidth=16, aWidth=4, codeType=ACSECDEDType.CODE_EVEN_EVEN)
    code.printInfo()
    test = tests.ZerosAndOnesTest.ZerosAndOnesTest(code)
    test.runOneTestAC(data=0, address=0, print_all = True, print_errors = True, print_header = True )
    print("**(fails zero check on all 0s because even-even.)**")


    print("***** test ACSECDED 26 20 - E O *****")
    code = ACSECDEDCodes(dWidth=16, aWidth=4, codeType=ACSECDEDType.CODE_EVEN_ODD)
    code.printInfo()
    test = tests.ZerosAndOnesTest.ZerosAndOnesTest(code)
    #test.runTestAllRandAC(print_all = False, print_errors = True )
    test.runOneTestAC(data=0, address=0b0111, print_all = True, print_errors = True, print_header = True )
    test.runOneTestAC(data=0b1111111111111111, address=0b0100, print_all = True, print_errors = True, print_header = True )
    print("**(fails all zeros and all ones check on some data patters)**")


    print("********* ACSECDED 26 20 Odd Odd ************")
    code = ACSECDEDCodes(dWidth=16, aWidth=4, codeType=ACSECDEDType.CODE_ODD_ODD)
    code.printInfo()
    test = tests.ZerosAndOnesTest.ZerosAndOnesTest(code)
    #test.runTestAllRandAC(print_all = False, print_errors = True )
    #test.runTestAllSingleBitInjectionsAC(print_all = False, print_errors = True, random_order = True )
    test.runOneBitInjectionAC(data=0b1000000000000000, address=0b0011, bit=19, bit2=None, print_all = True, print_errors = True, print_header = True )
    print("**(fails all zeros check after single bit injection where should have been corrected.)**")


    print("\n\n******************* Complete tests that prove points *********************")

    if False:
        print("***** test ACSECDED 9 2 - E E *****")
        code = ACSECDEDCodes(dWidth=9, aWidth=2, codeType=ACSECDEDType.CODE_EVEN_EVEN)
        code.printInfo()
        test = tests.ZerosAndOnesTest.ZerosAndOnesTest(code)
        test.runTestAllRandAC(print_all = False, print_errors = True )
        print("**(fails all 0s because even-even. Also does not meet constraints)**")

    if False:
        print("***** test ACSECDED 9 2 - E O *****")
        code = ACSECDEDCodes(dWidth=9, aWidth=2, codeType=ACSECDEDType.CODE_EVEN_ODD)
        code.printInfo()
        test = tests.ZerosAndOnesTest.ZerosAndOnesTest(code)
        test.runTestAllRandAC(print_all = False, print_errors = True )
        test.runTestAllSingleBitInjectionsAC(print_all = False, print_errors = True, random_order = True )
        print("**(fails all 0s on injection because even-even. Also does not meet constraints)**")

    if False:
        print("***** test ACSECDED 9 2 - O E *****")
        code = ACSECDEDCodes(dWidth=9, aWidth=2, codeType=ACSECDEDType.CODE_ODD_EVEN)
        code.printInfo()
        test = tests.ZerosAndOnesTest.ZerosAndOnesTest(code)
        test.runTestAllRandAC(print_all = False, print_errors = True )
        test.runTestAllSingleBitInjectionsAC(print_all = False, print_errors = True, random_order = True )
        print("**(Passes, but does not meet constraints)**")
        print("**This only proves that ACSECDED 9 2 O E works.  But other combos of Address and Data widths fail.**")


    if False:
        print("***** test ACSECDED 26 20 - E E *****")
        code = ACSECDEDCodes(dWidth=16, aWidth=4, codeType=ACSECDEDType.CODE_EVEN_EVEN)
        code.printInfo()
        test = tests.ZerosAndOnesTest.ZerosAndOnesTest(code)
        test.runTestAllRandAC(print_all = False, print_errors = True )
        print("**(fails all 0s because even-even.)**")


    if False:
        print("***** test ACSECDED 26 20 - E O *****")
        code = ACSECDEDCodes(dWidth=16, aWidth=4, codeType=ACSECDEDType.CODE_EVEN_ODD)
        code.printInfo()
        test = tests.ZerosAndOnesTest.ZerosAndOnesTest(code)
        test.runTestAllRandAC(print_all = False, print_errors = True )
        print("**(fails all 0s because even-even.)**")

    if False:
        print("***** test ACSECDED 26 20 - O E *****")
        code = ACSECDEDCodes(dWidth=16, aWidth=4, codeType=ACSECDEDType.CODE_ODD_EVEN)
        code.printInfo()
        test = tests.ZerosAndOnesTest.ZerosAndOnesTest(code)
        test.runTestAllRandAC(print_all = False, print_errors = True )
        test.runTestAllSingleBitInjectionsAC(print_all = False, print_errors = True, random_order = True )
        print("**(fails all 0s because even-even.)**")

    if True:
        print("***** test ACSECDEDd 26 20 - O O *****")
        code = ACSECDEDCodes(dWidth=16, aWidth=4, codeType=ACSECDEDType.CODE_ODD_EVENd)
        code.printInfo()
        test = tests.ZerosAndOnesTest.ZerosAndOnesTest(code)

        print("Specific failing case from before:")
        test.runOneBitInjectionAC(data=0b1000000000000001, address=0b0011, bit=19, bit2=None, print_all = True, print_errors = True, print_header = True )
        test.runOneBitInjectionAC(data=0b1000000000000000, address=0b0011, bit=19, bit2=None, print_all = True, print_errors = True, print_header = True )

        # Case of address injection failing (only 1/2 coverage):
        #  data             ad   -> enc                        (eDat             eA   syn   ) -> injected                   -> decoded                    (dDat             dA   syn   ) | cor/uncor  zeros ones testpass
        #  1110011101100011 1100 -> 11111111100111011000111100 (1110011101100011 1100 111111) -> 11111111100111011000101100 -> 11111111100111011000101100 (1110011101100010 1100 111111) | False/True          FAIL     
        #                           11111111100111011000110100 
        test.runOneBitInjectionAC(data=0b1110011101100011, address=0b1100, bit=3, bit2=None, print_all = True, print_errors = True, print_header = True, count_addr_as_fail=False )

        # Another address injection case that failed due to a bug:
        #  0100010101101111 0001 -> 00011101000101011011110001 (0100010101101111 0001 000111) -> 00011101000101011011110000 -> 00011101000101011011110000 (0100010101101111 0000 000111) | False/True          FAIL  
        #                           00011101000101011011110000
        #                           00011101000101011011110000
        test.runOneBitInjectionAC(data=0b0100010101101111, address=0b0001, bit=0, bit2=None, print_all = True, print_errors = True, print_header = True, count_addr_as_fail=False )

        #print("all single bit injections:")
        #test.runTestAllRandAC(print_all = False, print_errors = True )
        #test.runTestAllSingleBitInjectionsAC(print_all = False, print_errors = True, random_order = True, count_addr_as_fail=False )

        #print("press enter to continue...")
        #input()

        print("Specific double bit failing case from before (parity bit injection):")
        # failing because of another bug where we weren't shifting the parity bit back to zero again:
        #  data             ad   -> enc                        (eDat             eA   syn   ) -> injected                   -> decoded                    (dDat             dA   syn   ) | cor/uncor  zeros ones testpass
        #  0010111110110101 0000 -> 01100000101111101101010000 (0010111110110101 0000 011000) -> 11100000101111101101000000 -> 11100000101111101101010000 (0010111110110101 0000 111000) | True/False          FAIL  
        test.runOneBitInjectionAC(data=0b0010111110110101, address=0b0000, bit=6, bit2=25, print_all = True, print_errors = True, print_header = True, count_addr_as_fail=False )


        #  data             ad   -> enc                        (eDat             eA   syn   ) -> injected                   -> decoded                    (dDat             dA   syn   ) | cor/uncor  zeros ones testpass
        #  0000001000100000 1101 -> 00000000000010001000001101 (0000001000100000 1101 000000) -> 00000000000000000000001101 -> 00000000000000000000001101 (0000000000000000 1101 000000) | False/True ZERO
        #                           00000000000000000000001101
        test.runOneBitInjectionAC(data=0b0000001000100000, address=0b1101, bit=10, bit2=14, print_all = True, print_errors = True, print_header = True, count_addr_as_fail=False )
        print("all double bit injections:")
        test.runTestAllDoubleBitInjectionsAC(print_all = False, print_errors = True, random_order = True, count_addr_as_fail=False )
