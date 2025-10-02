from enum import Enum
import math
import sys
from .ACSECCodes import ACSECCodes
from JulianBaileyUseful.py.protections.ecc.codes.ParityCodes import ParityCode, Decoder
from JulianBaileyUseful.py.protections.ecc.codes.SECDEDCodes import SECDEDCode, SECDEDType
from .PartialParityCode import PartialParityCode
from JulianBaileyUseful.py.protections.ecc.codes.Utils import isPow2, generateParityBit

class ACSECDEDType(Enum):
    CODE_EVEN_EVEN = 1 # Even SEC, Even Parity
    CODE_ODD_ODD   = 2 # Odd SEC, Odd Parity
    CODE_EVEN_ODD  = 3 # Even SEC, Odd Parity
    CODE_ODD_EVEN  = 4 # Odd SEC, Even Parity
    CODE_EVEN_EVENd = 5 # Even SEC, Even Parity (data only)
    CODE_ODD_ODDd   = 6 # Odd SEC, Odd Parity (data only)
    CODE_EVEN_ODDd  = 7 # Even SEC, Odd Parity (data only)
    CODE_ODD_EVENd  = 8 # Odd SEC, Even Parity (data only)
    CODE_EVEN_EVENdnoo = 9 # Even SEC, Even Parity (data only)
    CODE_ODD_ODDdnoo   = 10 # Odd SEC, Odd Parity (data only)
    CODE_EVEN_ODDdnoo  = 11 # Even SEC, Odd Parity (data only)
    CODE_ODD_EVENdnoo  = 12 # Odd SEC, Even Parity (data only)

class Decoder:
  def __init__(self, uncorrected = None, corrected = None, correctable = False, uncorrectable = False, syndrome = None, address_fault = False):
    self.uncorrected   = uncorrected
    self.corrected     = corrected
    self.correctable   = correctable
    self.uncorrectable = uncorrectable
    self.syndrome      = syndrome
    self.address_fault = False
  def __str__(self):
    s =  "uncorrected  : {0:0b}\n".format(self.uncorrected)
    s += "corrected    : {0:0b}\n".format(self.corrected)
    s += "correctable  : {0:0b}\n".format(self.correctable)
    s += "uncorrectable: {0:0b}\n".format(self.uncorrectable)
    s += "syndrome     : {0:0b}".format(self.syndrome)
    s += "address_fault: {0:0b}".format(self.address_fault)
    return(s)
  

class ACSECDEDCodes(SECDEDCode):
    def __init__(self, dWidth : int, aWidth : int, codeType : ACSECDEDType, bump_width=False, req_data_bits=2):
        self.dWidth = dWidth
        self.aWidth = aWidth
        self.totalWidth = dWidth + aWidth
        self.dataWidth = dWidth + aWidth
        self.codeACType = codeType
        self.bump_width = bump_width
        self.req_data_bits = req_data_bits   # number of hamming bits that are required to have only data inputs
        #self.bump_width = 0
        #if self.codeACType == ACSECDEDType.CODE_EVEN_EVENdnoo or self.codeACType == ACSECDEDType.CODE_ODD_ODDdnoo or self.codeACType == ACSECDEDType.CODE_EVEN_ODDdnoo or self.codeACType == ACSECDEDType.CODE_ODD_EVENdnoo: 
        #    self.bump_width = 1
        self.partialParity = ((codeType == ACSECDEDType.CODE_EVEN_EVENd) or (codeType == ACSECDEDType.CODE_ODD_ODDd) or (codeType == ACSECDEDType.CODE_EVEN_ODDd) or (codeType == ACSECDEDType.CODE_ODD_EVENd) or
                              (codeType == ACSECDEDType.CODE_EVEN_EVENdnoo) or (codeType == ACSECDEDType.CODE_ODD_ODDdnoo) or (codeType == ACSECDEDType.CODE_EVEN_ODDdnoo) or (codeType == ACSECDEDType.CODE_ODD_EVENdnoo))
        if codeType == ACSECDEDType.CODE_EVEN_EVEN or codeType == ACSECDEDType.CODE_EVEN_EVENd or codeType == ACSECDEDType.CODE_EVEN_EVENdnoo:
            self.codeType = SECDEDType.CODE_EVEN_EVEN
        elif codeType == ACSECDEDType.CODE_ODD_ODD or codeType == ACSECDEDType.CODE_ODD_ODDd or codeType == ACSECDEDType.CODE_ODD_ODDdnoo:
            self.codeType = SECDEDType.CODE_ODD_ODD
        elif codeType == ACSECDEDType.CODE_EVEN_ODD or codeType == ACSECDEDType.CODE_EVEN_ODDd or codeType == ACSECDEDType.CODE_EVEN_ODDdnoo:
            self.codeType = SECDEDType.CODE_EVEN_ODD
        elif codeType == ACSECDEDType.CODE_ODD_EVEN or codeType == ACSECDEDType.CODE_ODD_EVENd or codeType == ACSECDEDType.CODE_ODD_EVENdnoo:
            self.codeType = SECDEDType.CODE_ODD_EVEN
        self.secOdd       = ((codeType == ACSECDEDType.CODE_ODD_ODD) or (codeType == ACSECDEDType.CODE_ODD_EVEN) or (codeType == ACSECDEDType.CODE_ODD_ODDd) or (codeType == ACSECDEDType.CODE_ODD_EVENd) or (codeType == ACSECDEDType.CODE_ODD_ODDdnoo) or (codeType == ACSECDEDType.CODE_ODD_EVENdnoo))
        self.parOdd       = ((codeType == ACSECDEDType.CODE_ODD_ODD) or (codeType == ACSECDEDType.CODE_EVEN_ODD) or (codeType == ACSECDEDType.CODE_ODD_ODDd) or (codeType == ACSECDEDType.CODE_EVEN_ODDd) or (codeType == ACSECDEDType.CODE_ODD_ODDdnoo) or (codeType == ACSECDEDType.CODE_EVEN_ODDdnoo))
        self.alwaysCorrect = False
        # print(f"ACSECDEDCodes::init dWidth={dWidth} aWidth={aWidth} codeType={codeType} partialParity={self.partialParity} secOdd={self.secOdd} parOdd={self.parOdd}")
        self.sec = ACSECCodes(dWidth, aWidth, self.secOdd)
        super().__init__(self.totalWidth, self.codeType, bump_width=self.bump_width)

        
        if (codeType == ACSECDEDType.CODE_EVEN_EVENd) or (codeType == ACSECDEDType.CODE_ODD_ODDd) or (codeType == ACSECDEDType.CODE_EVEN_ODDd) or (codeType == ACSECDEDType.CODE_ODD_EVENd) or \
           (codeType == ACSECDEDType.CODE_EVEN_EVENdnoo) or (codeType == ACSECDEDType.CODE_ODD_ODDdnoo) or (codeType == ACSECDEDType.CODE_EVEN_ODDdnoo) or (codeType == ACSECDEDType.CODE_ODD_EVENdnoo):
            self.par  = PartialParityCode(self.sec.encodedWidth(), self.aWidth, self.parOdd)
        else:
            self.par  = ParityCode(self.sec.encodedWidth(), self.parOdd) 
        self.codeMaskCols = []
        self.sec.codeMasks = self.__generateMasks()  # overriding codes from Julian's library with my own
        self.sec.codeMaskCols = self.codeMaskCols
        self.sec.useCodeMaskCols = True
        
        #print(f"ACSECDEDCodes::init superEncodedWidth={super().encodedWidth()} encodedWidth={self.par.encodedWidth()}")
        self.syndromeWidth = self.encodedWidth() - self.totalWidth
        # for secded the syndrome includes the additional parity bit
        if self.encodedWidth() == (2**(self.syndromeWidth-1)):
            self.perfectCode=True
        else:
            self.perfectCode=False

    def __numCodeBits(self):
        m = int(math.log2(self.dataWidth)) + 1
        if (((1 << m) < m + self.dataWidth + 1)):
            m = m + 1
        if self.bump_width:
            m += 1
        return m

    def __dataMask(self):
        return ((1 << self.dataWidth) - 1)

    def __encodedMask(self):
        return ((1 << self.encodedWidth()) - 1)

    def encodedWidth(self): # this needs to be overridden because _numCodeBits() is overridden
        return (self.totalWidth + self.__numCodeBits())

    def correctionMask(self, synd):
        # Define the bit which must be flipped
        bit = 0

        if (synd != 0):
            # if the syndrome is a power of 2 then it is a parity bit
            # and affects the parity bits which are at the end of the 
            # codeword.
            if (isPow2(synd)):
                offset = (int(math.log(synd)/math.log(2))) 
                bit = 1 << (offset + self.dataWidth)
            # Otherwise, this is a data bit and we need to adjust for
            # fact the parity bits have been moved to the end.
            else:
                # The syndrome indicates which bit in the non-systematic
                # codeword has been flipped, we need to convert this to 
                # a value which has meaning for the systematic codeword.
                # Determine the offset in the non-systematic codeword
                offset = (int(math.log(synd)/math.log(2))) + 1
                bit = 1 << (synd - offset - 1)
                print(f"  synd: {synd} offset: {offset} bit: {bit}")


    def __generateMasks(self):
        print (f"ACSECDEDCodes::__generateMasks")
        numRows = self.__numCodeBits()
        numCols = self.encodedWidth() - 1 # Julian's code was called when encodedWidth did not include the parity bit.  Here it does.
        print (f"ACSECDEDCodes::__generateMasks numRows={numRows} numCols={numCols} encodedWidth={self.encodedWidth()}")

        matrix = []
        dont_use_mask = 1 << numRows
        if self.codeACType == ACSECDEDType.CODE_EVEN_EVENdnoo or self.codeACType == ACSECDEDType.CODE_ODD_ODDdnoo or self.codeACType == ACSECDEDType.CODE_EVEN_ODDdnoo or self.codeACType == ACSECDEDType.CODE_ODD_EVENdnoo: 
            print(f"ACSECDEDCodes::__generateMasks: calculating dont_use")
            print(f"ACSECDEDCodes::__generateMasks: numRows={numRows}")
            if self.bump_width:
                dont_use_mask = (1<<numRows-2) | (1<<(numRows-3))
            else:
                dont_use_mask = (1<<numRows-1) | (1<<(numRows-2))
            print(f"ACSECDEDCodes::__generateMasks: dont_use_mask={dont_use_mask:0{numRows}b}")

        for ii in range(numRows):
            dataBits   = []
            parityBits = []
            rowPow2    = (1 << ii)
            set_cols = 0
            jj = -1 # because we increment before using
            while set_cols < numCols:
                jj += 1
                if (dont_use_mask & (jj+1)) == dont_use_mask and isPow2(jj+1) == False: 
                    if ii == 0:
                        print(f"  skipping {jj+1} ({jj+1:0{numRows}b}) because it is in dont_use_mask")
                    continue
                set_cols += 1
                if ii == 0:
                    print(f"  using {jj+1} ({jj+1:0{numRows}b}) set_cols={set_cols}")
                value = ((jj + 1) & (1 << ii)) != 0
                if jj > 1 << numCols:
                    raise ValueError(f"More hamming bits needed than allocated: jj={jj} is greater than numCols={numCols}")
                if (isPow2(jj+1)):
                    parityBits.append(value)
                else:
                    dataBits.append(value)

            row = dataBits + parityBits
            matrix.append(row)

        codeMasks = []

        for row in matrix:
            value = 0
            for ii in range(numCols):
                value |= (row[ii] << ii)
            codeMasks.append(value)

        for i in range(self.encodedWidth()):
            col_val = 0
            j = 0
            for m in codeMasks:
                if (m & (1<<i)) != 0:
                    col_val += 1<<j
                j += 1
            print(f"  col {i}: {col_val:0{self.encodedWidth()}b} ({col_val})")
            self.codeMaskCols.append(col_val)

        print(f"  returning codeMasksCols: {self.codeMaskCols}")
        print(f"  returning codeMasks: {codeMasks}")

        return(codeMasks)


    def checkConstraints(self):
        # Constraints:
        # 0) Every hamming bit has at least one data input
        # 0a) Every column is unique
        # 1) Odd.even -> will be odd.odd
        # 2) Addr are in LSB -> by construction
        # 3) At least 2 hamming bits depend only on data
        # 4) At least 2 hamming bits depending on data have an odd number of inputs
        # 5) At least 2 hamming bits depending on data do not overlap (only for noo codes)

        print("Checking constraints:")
        test_pass = True

        # check constraint #0
        print("Checking constriant 0: (Every hamming bit has at least one data input)")
        n_zero_inputs = 0
        for cm in self.sec.codeMasks:
            cm_addr = cm & ((1<<self.aWidth)-1)
            cm_data = (cm >> self.aWidth) & ((1<<self.dWidth)-1)
            num_inputs = bin(cm_data).count("1")
            if num_inputs == 0:
                print(f"  ERROR:  Code mask {cm:0{self.encodedWidth()}b} has hamming bits with no data inputs.")
                print(f"                data={cm_data:0{self.dWidth}b} addr={cm_addr:0{self.aWidth}b} num_inputs={num_inputs}")
                n_zero_inputs += 1

            #print(f"  codemask: {cm:0{self.encodedWidth()}b} addr={cm_addr:0{self.aWidth}b} data={cm_data:0{self.dWidth}b} num_inputs={num_inputs} odd_inputs={num_inputs % 2 != 0} ")

        if n_zero_inputs > 0 :
            print(f"  ERROR:  {n_zero_inputs} hamming bits have no data inputs.")
            test_pass = False
        else:
            print("  ok")

        # check constraint #0a
        print("Checking constriant 0a: (Every column is unique)")
        unique_cols = []
        for ii in range(self.encodedWidth()):
            col = 0
            i = 0
            for cm in self.sec.codeMasks:
                this_bit = ((1 << ii) & cm) >> ii
                col |= this_bit << i
                i += 1
            if col in unique_cols:
                print(f"  ERROR:  Column {ii} is not unique.")
                print(f"           col={col:0{self.encodedWidth()}b}, ")
                print(f"           also at index={unique_cols.index(col)}")
                test_pass = False
            else:
                # print(f"  Column {ii} is unique. col={col:0{self.encodedWidth()}b}")
                unique_cols.append(col)



        # check constraint #3
        print(f"code mask = {self.sec.codeMasks}")
        # print("Checking constriant 3: (At least 2 hamming bits depend only on data)")
        print(f"Checking constriant 3: (At least {self.req_data_bits} hamming bits depend only on data)")
        n_data_only = 0
        for cm in self.sec.codeMasks:
            cm_addr = cm & ((1<<self.aWidth)-1)
            cm_data = (cm >> self.aWidth) & ((1<<self.dWidth)-1)
            if cm_addr == 0:
                n_data_only += 1
            #print(f"  codemask: {cm:0{self.encodedWidth()}b} addr={cm_addr:0{self.aWidth}b} data={cm_data:0{self.dWidth}b} data_only={cm_addr!=0} ")

        if n_data_only < self.req_data_bits:
            print(f"ERROR: {n_data_only} hamming bits depend only on data (need at least {self.req_data_bits})")
            test_pass = False
        else:
            print("  ok")

        # check constraint #4
        print(f"Checking constriant 4: (At least {self.req_data_bits} hamming bits depending on data have an odd number of inputs)")
        n_odd_inputs = 0
        for cm in self.sec.codeMasks:
            cm_addr = cm & ((1<<self.aWidth)-1)
            cm_data = (cm >> self.aWidth) & ((1<<self.dWidth)-1)
            num_inputs = bin(cm_data).count("1")
            if cm_addr == 0 and num_inputs % 2 != 0:
                n_odd_inputs += 1

            #print(f"  codemask: {cm:0{self.encodedWidth()}b} addr={cm_addr:0{self.aWidth}b} data={cm_data:0{self.dWidth}b} num_inputs={num_inputs} odd_inputs={num_inputs % 2 != 0} ")

        if n_odd_inputs < self.req_data_bits:
            print(f"  ERROR:  {n_odd_inputs} hamming bits have odd inputs.")
            test_pass = False
        else:
            print("  ok")


        if self.codeACType == ACSECDEDType.CODE_EVEN_EVENdnoo or self.codeACType == ACSECDEDType.CODE_ODD_ODDdnoo or self.codeACType == ACSECDEDType.CODE_EVEN_ODDdnoo or self.codeACType == ACSECDEDType.CODE_ODD_EVENdnoo: 
            # check constraint #5
            print("Checking constriant 5: (At least 2 hamming bits depending on data have do not overlap. Assume MSBs)")
            cm_len = len(self.sec.codeMasks)
            cm1 = self.sec.codeMasks[cm_len-1]
            cm2 = self.sec.codeMasks[cm_len-2]
            print(f"  cm1={cm1:0{self.encodedWidth()}b}")
            print(f"  cm2={cm2:0{self.encodedWidth()}b}")
            print(f"  1&2={cm1 & cm2:0{self.encodedWidth()}b}")
            if cm1 & cm2 != 0:
                print(f"  ERROR: Non-overlapping constraint failed")
                test_pass = False
            else:
                print("  ok")



    
        if test_pass:
            print("All constraints passed")
        else:
            print("ERROR: ######### Some constraints failed! ###########  ")
            raise ValueError("Some constraints failed")
        return test_pass
                    


    def printInfo(self):
        print("--------------------------------------------")
        print("Code info:")
        print(f"  dWidth: {self.dWidth}")
        print(f"  aWidth: {self.aWidth}")
        print(f"  totalWidth: {self.totalWidth}")
        print(f"  encodedWidth: {self.encodedWidth()}")
        print(f"  syndromeWidth: {self.syndromeWidth}")
        print(f"  perfectCode: {self.perfectCode}")        
        print(f"  secOdd: {self.secOdd}")
        print(f"  parOdd: {self.parOdd}")
        print(f"  parityWidth: {self.par.encodedWidth()}")
        print(f"  perfectCode: {self.perfectCode}")
        print(f"  bump_width: {self.bump_width}")
        print("--------------------------------------------")
        self.checkConstraints()
        print("--------------------------------------------")

    def printMask(self):
        print(f"SEC masks: {self.sec.codeMasks}")
        l = self.syndromeWidth
        ew = self.encodedWidth()
        print(f"  l={l} ew={ew}")

        print("my custom print:")
        for m in self.sec.codeMasks:
            bin_str = f"{m:0{ew}b}"
            unity_part = bin_str[:l]
            hamming_part = bin_str[l:]
            print(f"  {unity_part} {hamming_part}")

        print("regular print:")
        for m in self.sec.codeMasks:
            print(f"  {m:0{ew}b}")

        for i in range(self.encodedWidth()):
            col_val = 0
            j = 0
            for m in self.sec.codeMasks:
                if (m & (1<<i)) != 0:
                    col_val += 1<<j
                j += 1
            print(f"  col {i}: {col_val:0{ew}b} ({col_val})")


    def encodedWidth(self):
        #print(f"ACSECDEDCodes::encodedWidth {self.par.encodedWidth()}")
        return(self.par.encodedWidth())
    
        
    def encode(self, data, address):
        encodedSec = self.sec.encode(data << self.aWidth | address)
        encodedSecDed = self.par.encode(encodedSec)
        return(encodedSecDed)
    
    def decode(self, encodedData):

        parDecode = self.par.decode(encodedData)
        secDecode = self.sec.decode(encodedData)

        secdedDecode = Decoder(
            uncorrectable = not(parDecode.uncorrectable) and secDecode.correctable,
            correctable   = parDecode.uncorrectable,
            uncorrected   = encodedData,
            corrected     = encodedData,
            syndrome      = secDecode.syndrome
        )
        performCorrection = secdedDecode.correctable or (secdedDecode.uncorrectable and self.alwaysCorrect)

        # Data Correction
        if (performCorrection):
            # If the syndrome is zero then flip the parity bit...
            if (secdedDecode.syndrome == 0):
                secdedDecode.corrected = encodedData ^ (1 << (self.encodedWidth() - 1))
            # Take the corrected value from SEC code
            else:
                # if the corrected bit is in the address, then this is actually an uncorrected error
                correctedBits = secDecode.corrected ^ encodedData
                if (correctedBits & ((1<<self.aWidth)-1)) != 0:
                    secdedDecode.correctable = False
                    secdedDecode.uncorrectable = True
                    secdedDecode.address_fault = True
                else:
                    pmask = 1 << (self.par.encodedWidth() - 1)
                    smask = (1 << super().encodedWidth()) - 1
                    secdedDecode.corrected = (encodedData & pmask) | (secDecode.corrected & smask) 

        return(secdedDecode)

