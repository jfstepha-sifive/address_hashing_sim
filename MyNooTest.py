import sys
import tests.ZerosAndOnesTest
from accodes.ACSECCodes import ACSECCodes
from JulianBaileyUseful.py.protections.ecc.codes.SECDEDCodes import SECDEDType
from accodes.ACSECDEDCodes import ACSECDEDCodes
from accodes.ACSECDEDCodes import ACSECDEDType

from JulianBaileyUseful.py.protections.ecc import codes
from JulianBaileyUseful.py.protections.ecc.codes.SECDEDCodes import SECDEDType

if __name__ == "__main__":

    data_bits = int(sys.argv[1])
    address_bits = int(sys.argv[2])
    bump_width = int(sys.argv[3])
    #data_bits = 6
    #bump_width = 1
    # address_bits = 2
    
    code = codes.OddOddSECDEDCode(data_bits+address_bits)
    print("SECDED code masks:")
    print(f"  dataWidth: {code.dataWidth}")
    print(f"  encodedWidth: {code.encodedWidth()}")   # with the parity bit
    for m in code.sec.codeMasks:
            bin_str = f"{m:0{code.encodedWidth()}b}"   # top 0 is the parity bit
            print(f"  {bin_str}")


    #print("\n\n******************* EVEN_EVEN *********************")
    #code = ACSECDEDCodes(dWidth=data_bits, aWidth=address_bits, codeType=ACSECDEDType.CODE_EVEN_EVEN)
    #code.printInfo()
    #code.printMask()

    print("\n\n******************* EVEN_EVENdnoo *********************")
    code = ACSECDEDCodes(dWidth=data_bits, aWidth=address_bits, codeType=ACSECDEDType.CODE_ODD_EVENdnoo, bump_width=bump_width)
    code.printInfo()
    code.printMask()
    #user_input = input("Press enter to continue: ")
    test = tests.ZerosAndOnesTest.ZerosAndOnesTest(code)
    test.runOneTestAC(data=0, address=0, print_all = True, print_errors = True, print_header = True )
    user_input = input("Press enter to continue: ")
    #test.runOneBitInjectionAC(data=0, address=0, bit=4, bit2=None, print_all = True, print_errors = True, print_header = True )
    #test.runOneBitInjectionAC(data=0, address=0, bit=5, bit2=None, print_all = True, print_errors = True, print_header = True )
    #test.runOneBitInjectionAC(data=0, address=0, bit=6, bit2=None, print_all = True, print_errors = True, print_header = True )
    #test.runOneBitInjectionAC(data=0, address=0, bit=7, bit2=None, print_all = True, print_errors = True, print_header = True )
    #user_input = input("Press enter to continue: ")

    max_run_time = 60 * 10 # 10 minutes
    print("all binary tests:")
    test.runTestAllBinAC(print_all = False, print_errors = True, max_run_time=max_run_time )
    user_input = input("Press enter to continue: ")
    print("all single bit tests:")
    test.runTestAllSingleBitInjectionsAC(print_all = False, print_errors = True, random_order = True, count_addr_as_fail=False, max_run_time=max_run_time )
    user_input = input("Press enter to continue: ")
    print("all double bit tests:")
    test.runTestAllDoubleBitInjectionsAC(print_all = False, print_errors = True, random_order = True, count_addr_as_fail=False, max_run_time=max_run_time )
