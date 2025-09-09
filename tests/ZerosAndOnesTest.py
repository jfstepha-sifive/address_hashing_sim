import numpy as np




class ZerosAndOnesTest:
    def __init__(self, code):
        self.code = code

    def myprint(self, encodedData,syndromeWidth):
        bits = self.code.dataWidth
        syndrome = encodedData >> bits
        encodedDataData = encodedData & ((1<<bits)-1)
        return f"{encodedDataData:0{bits}b} {syndrome:0{syndromeWidth}b}"
    
    def testPass(self):
        return True
    
    def runOneTest(self, data, print_all = True, print_errors = True):
        # no injections
        encodedData = self.code.encode(data)
        bits = self.code.dataWidth
        syndrome = encodedData >> bits
        encodedDataData = encodedData & ((1<<bits)-1)
        syndromeWidth = self.code.encodedWidth() - bits

        all_zero = (encodedData == 0)
        all_one =  (encodedData == (1<<self.code.encodedWidth())-1)
        zstring = "ZERO" if all_zero else "    "
        ostring = "ONE" if all_one else "   "
        if print_all or ((all_zero or all_one) and print_errors):
            print(f"  {data:0{bits}b} -> {encodedDataData:0{bits}b} {syndrome:0{syndromeWidth}b} {zstring} {ostring}")

        return (all_zero, all_one)

    def runOneTestAC(self, data, address, print_all = True, print_errors = True, print_header = False):
        # no injections
        encodedData = self.code.encode(data, address)
        dataBits = self.code.dWidth
        addressBits = self.code.aWidth
        syndrome = encodedData >> (dataBits + addressBits)
        encodedDataData = (encodedData >> addressBits) & ((1<<dataBits)-1)
        encodedDataAddress = encodedData & ((1<<addressBits)-1)
        syndromeWidth = self.code.encodedWidth() - (dataBits + addressBits)
        #print(f"runOneTestAC: data={data} address={address} encodedData={encodedData:0{self.code.encodedWidth()}b}")
        #print(f"runOneTestAC: dataBits={dataBits} addressBits={addressBits} syndromeWidth={syndromeWidth}")
        #print(f"runOneTestAC: encodedDataData={encodedDataData:0{dataBits}b} encodedDataAddress={encodedDataAddress:0{addressBits}b} syndrome={syndrome:0{syndromeWidth}b}")
        #print(f"runOneTestAC: syndromeWidth={syndromeWidth}")

        all_zero = (encodedDataData == 0 and syndrome == 0)
        all_one =  (encodedDataData == (1<<dataBits)-1) and (syndrome == (1<<syndromeWidth)-1)
        zstring = "ZERO" if all_zero else "    "
        ostring = "ONE" if all_one else "   "
        if print_header:
            print(f"  {'data':{dataBits}} {'ad':{addressBits}} -> {'enc':{self.code.encodedWidth()}} {'eDat':{dataBits}} {'eA':{addressBits}} {'syn':{syndromeWidth}} zeros ones")
        if print_all or ((all_zero or all_one) and print_errors):
            print(f"  {data:0{dataBits}b} {address:0{addressBits}b} -> {encodedData:0{self.code.encodedWidth()}b} {encodedDataData:0{dataBits}b} {encodedDataAddress:0{addressBits}b} {syndrome:0{syndromeWidth}b} {zstring} {ostring}")

        return (all_zero, all_one)
    
    def runTestAllAC(self, print_all = True, print_errors = True, random_order = False, print_skip=100000):
        all_zero_count = 0
        all_one_count = 0
        bits = self.code.totalWidth
        print_header = True
        tests = 1 << bits

        if random_order:
            rng = np.random.default_rng()
            bit_range = rng.permutation(1<<bits)
        else:
            bit_range = range(0, 1<<bits)

        i=0
        for d in bit_range :
            data = (d >> self.code.aWidth) & ((1<<self.code.dWidth)-1)
            address = d & ((1<<self.code.aWidth)-1)
            if i%print_skip==0:
                print(f" running test {i}/{tests} ({i/tests * 100:.2f}%)")            
            (all_zero, all_one) = self.runOneTestAC(data, address, print_all, print_errors, print_header)
            all_zero_count += all_zero
            all_one_count += all_one
            print_header = False
            i += 1

        if all_zero_count != 0 or all_one_count != 0:
            print(f"FAIL: Some encodings were all zero or all ones")
            print(f" all zeros: {all_zero_count}")
            print(f" all ones: {all_one_count}")
        else:
            print(f"PASS: No encodings were all zero or all ones")

    def runTestAllBinAC(self, print_all = True, print_errors = True):
        self.runTestAllAC(print_all, print_errors, random_order = False)

    def runTestAllRandAC(self, print_all = True, print_errors = True, print_skip=100000):
        print("running AllRandomAC test...")

        self.runTestAllAC(print_all, print_errors, random_order = True, print_skip=print_skip)



    def runTestAllBin(self, print_all = True, print_errors = True):
        all_zero_count = 0
        all_one_count = 0
        bits = self.code.dataWidth

        for i in range(0, 1<<bits):
            (all_zero, all_one) = self.runOneTest(i, print_all, print_errors)
            all_zero_count += all_zero
            all_one_count += all_one

        if all_zero_count != 0 or all_one_count != 0:
            print(f"FAIL: Some encodings were all zero or all ones")
            print(f" all zeros: {all_zero_count}")
            print(f" all ones: {all_one_count}")
        else:
            print(f"PASS: No encodings were all zero or all ones")

    def runTestAllRandom(self, print_all = True, print_errors = True, print_skip=100000):
        print("running AllRandom test...")
        all_zero_count = 0
        all_one_count = 0
        bits = self.code.dataWidth

        rng = np.random.default_rng()
        tests = 1 << bits
        i = 0

        for data in rng.permutation(1<<bits):
            if i%print_skip==0:
                print(f" running test {i}/{tests} ({i/tests * 100:.2f}%)")
            (all_zero, all_one) = self.runOneTest(data, print_all, print_errors)
            all_zero_count += all_zero
            all_one_count += all_one
            i += 1

        if all_zero_count != 0 or all_one_count != 0:
            print(f"FAIL: Some encodings were all zero or all ones")
            print(f" all zeros: {all_zero_count}")
            print(f" all ones: {all_one_count}")
        else:
            print(f"PASS: No encodings were all zero or all ones")

    def runOneSingleBitInjection(self, data, bit, print_all = True, print_errors = True):
        bits = self.code.dataWidth
        syndromeWidth = self.code.encodedWidth() - bits

        encodedData = self.code.encode(data)
        encodedDataData = encodedData & ((1<<bits)-1)
        syndrome = encodedData >> bits

        injected = encodedData ^ (1<<bit)
        decoded = self.code.decode(injected)
        all_zero = (injected == 0)
        all_one =  (injected == (1<<self.code.encodedWidth())-1)
        zstring = "ZERO" if all_zero else "    "
        ostring = "ONE" if all_one else "   "
        if print_all or ((all_zero or all_one) and print_errors):
            print(f"  {data:0{bits}b} -> {self.myprint(encodedData,syndromeWidth)} -> {self.myprint(injected,syndromeWidth)} -> {self.myprint(decoded.corrected,syndromeWidth)} {decoded.correctable}/{decoded.uncorrectable}  {zstring} {ostring}")

        return (all_zero, all_one)


    def runOneBitInjectionAC(self, data, address, bit, bit2, print_all = True, print_errors = True, print_header = True, count_addr_as_fail=True):
        dataBits = self.code.dWidth
        addressBits = self.code.aWidth        
        syndromeWidth = self.code.encodedWidth() - (dataBits + addressBits)

        encodedData = self.code.encode(data, address)
        encodedDataData = (encodedData >> self.code.aWidth) & ((1<<self.code.dWidth)-1)
        encodedDataAddress = encodedData & ((1<<self.code.aWidth)-1)
        syndrome = encodedData >> (self.code.dWidth + self.code.aWidth)

        injected = encodedData ^ (1<<bit) 
        if bit2 != None:
            injected = injected ^ (1<<bit2)
        decoded = self.code.decode(injected)
        decodedData = decoded.corrected

        decodedDataData = (decodedData >> self.code.aWidth) & ((1<<self.code.dWidth)-1)
        decodedDataAddress = decodedData & ((1<<self.code.aWidth)-1)
        decodedSyndrome = decodedData >> (self.code.dWidth + self.code.aWidth)

        all_zero = (injected >> self.code.aWidth) == 0
        all_one =  (injected >> self.code.aWidth) == (1<<self.code.encodedWidth())-1
        address_fault = decoded.uncorrectable and decoded.address_fault
        
        if bit2 == None:
            if bit < self.code.aWidth:
                if count_addr_as_fail:
                    test_fail = (address_fault == False)
                else:
                    test_fail = False
            else:
                test_fail = (decoded.corrected != encodedData)
        else:
            if bit < self.code.aWidth and bit2 < self.code.aWidth:
                test_fail = False  # double bit address faults are not detected
            elif bit >= self.code.aWidth and bit2 >= self.code.aWidth:
                test_fail = (decoded.uncorrectable == False)
            else:
                test_fail = False
                print("WARNING: combined address and data bit flips are not detectable")


        tstring = "FAIL" if test_fail else "    "
        zstring = "ZERO" if all_zero else "    "
        ostring = "ONE" if all_one else "   "
        astring = "ADFAIL" if address_fault else "      "

        if print_header:
            print(f"  {'data':{dataBits}} {'ad':{addressBits}} -> "+
                  f"{'enc':{self.code.encodedWidth()}} ({'eDat':{dataBits}} {'eA':{addressBits}} {'syn':{syndromeWidth}}) -> " +
                  f"{'injected':{self.code.encodedWidth()}} -> " +
                  f"{'decoded':{self.code.encodedWidth()}} ({'dDat':{dataBits}} {'dA':{addressBits}} {'syn':{syndromeWidth}}) | " +
                  f"{'cor/uncor':10} " +
                  f"zeros ones testpass")
        if print_all or ((all_zero or all_one or test_fail) and print_errors):
            print(f"  {data:0{dataBits}b} {address:0{addressBits}b} -> " +
                  f"{encodedData:0{self.code.encodedWidth()}b} ({encodedDataData:0{dataBits}b} {encodedDataAddress:0{addressBits}b} {syndrome:0{syndromeWidth}b}) -> "+
                  f"{injected:0{self.code.encodedWidth()}b} -> "+ 
                  f"{decodedData:0{self.code.encodedWidth()}b} ({decodedDataData:0{dataBits}b} {decodedDataAddress:0{addressBits}b} {decodedSyndrome:0{syndromeWidth}b}) | "+
                  f"{decoded.correctable}/{decoded.uncorrectable} " +
                  f"{zstring} {ostring} {tstring} {astring}")

        #if print_all or ((all_zero or all_one) and print_errors):
        #    print(f"  {data:0{bits}b} -> {self.myprint(encodedData,syndromeWidth)} -> {self.myprint(injected,syndromeWidth)} -> {self.myprint(decoded.corrected,syndromeWidth)} {decoded.correctable}/{decoded.uncorrectable}  {zstring} {ostring}")

        return (all_zero, all_one, test_fail)


    def runOneSingleBitInjectionAC(self, data, address, bit, print_all = True, print_errors = True, print_header = True, count_addr_as_fail=True):
        return self.runOneBitInjectionAC(data, address, bit, None, print_all, print_errors, print_header, count_addr_as_fail)

    def runTestAllSingleBitInjections(self, print_all = True, print_errors = True):
        print("running AllSingleBitInjections injection test...")
        all_zero_count = 0
        all_one_count = 0
        bits = self.code.dataWidth
        for data in range(0, 1<<bits):
            for bit in range(0, self.code.encodedWidth()):
                (all_zero, all_one) = self.runOneSingleBitInjection(data, bit, print_all, print_errors)
                all_zero_count += all_zero
                all_one_count += all_one

        if all_zero_count != 0 or all_one_count != 0:
            print(f"FAIL: Some encodings were all zero or all ones after injection")
            print(f" all zeros: {all_zero_count}")
            print(f" all ones: {all_one_count}")
        else:
            print(f"PASS: No encodings were all zero or all ones")

    def runTestAllSingleBitInjectionsAC(self, print_all = True, print_errors = True, random_order = False, print_skip=100000, count_addr_as_fail=True):
        print("running AllSingleBitInjectionsAC injection test...")
        all_zero_count = 0
        all_one_count = 0
        fail_count = 0
        dataBits = self.code.dWidth
        addressBits = self.code.aWidth
        bits = self.code.totalWidth
        print_header = True
        i=0
        tests = (1 << bits) * bits

        if random_order:
            rng = np.random.default_rng()
            dataRange = rng.permutation(1<<bits)
        else:
            dataRange = range(0, 1<<bits)
        for unencData in dataRange:
            for bit in range(0, self.code.encodedWidth()):
                if i%print_skip==0:
                    print(f" running test {i}/{tests} ({i/tests * 100:.2f}%)")
                address = (unencData >> dataBits) & ((1<<addressBits)-1)
                data = unencData & ((1<<dataBits)-1)
                (all_zero, all_one, test_fail) = self.runOneSingleBitInjectionAC(data, address, bit, print_all, print_errors, print_header, count_addr_as_fail)
                all_zero_count += all_zero
                all_one_count += all_one
                fail_count += test_fail
                print_header = False
                i += 1
                

        if all_zero_count != 0 or all_one_count != 0 or fail_count != 0:
            print(f"FAIL: Some encodings were all zero or all ones after injection or correction failed")
            print(f" all zeros: {all_zero_count}")
            print(f" all ones: {all_one_count}")
            print(f" failed: {fail_count}")
        else:
            print(f"PASS: all single bit injections passed, no encodings were all zero or all ones")

    def runTestAllDoubleBitInjectionsAC(self, print_all = True, print_errors = True, random_order = False, print_skip=100000, count_addr_as_fail=True):
        all_zero_count = 0
        all_one_count = 0
        fail_count = 0
        dataBits = self.code.dWidth
        addressBits = self.code.aWidth
        bits = self.code.totalWidth
        print_header = True
        i=0
        tests = (1 << bits) * (bits * (bits-1) )
        if random_order:
            rng = np.random.default_rng()
            dataRange = rng.permutation(1<<bits)
        else:
            dataRange = range(0, 1<<bits)
        for unencData in dataRange:
            # first do addresses
            for bit in range(0, self.code.aWidth):
                for bit2 in range(bit+1, self.code.aWidth):
                    if i%print_skip==0:
                        print(f" running test {i}/{tests} ({i/tests * 100:.2f}%)")
                    address = (unencData >> dataBits) & ((1<<addressBits)-1)
                    data = unencData & ((1<<dataBits)-1)
                    (all_zero, all_one, test_fail) = self.runOneBitInjectionAC(data, address, bit, bit2, print_all, print_errors, print_header, count_addr_as_fail)
                    all_zero_count += all_zero
                    all_one_count += all_one
                    fail_count += test_fail
                    print_header = False
                    i+=1
            # next do data/syndrome
            for bit in range(self.code.aWidth, self.code.encodedWidth()):
                for bit2 in range(bit+1, self.code.encodedWidth()):
                    if i%print_skip==0:
                        print(f" running test {i}/{tests} ({i/tests * 100:.2f}%) failures={fail_count}")
                    address = (unencData >> dataBits) & ((1<<addressBits)-1)
                    data = unencData & ((1<<dataBits)-1)
                    (all_zero, all_one, test_fail) = self.runOneBitInjectionAC(data, address, bit, bit2, print_all, print_errors, print_header, count_addr_as_fail)
                    all_zero_count += all_zero
                    all_one_count += all_one
                    fail_count += test_fail
                    print_header = False
                    i+=1
                

        if all_zero_count != 0 or all_one_count != 0 or fail_count != 0:
            print(f"FAIL: Some encodings failed")
            print(f" failed: {fail_count}")
        else:
            print(f"PASS: all double bit injections passed, no encodings were all zero or all ones")        