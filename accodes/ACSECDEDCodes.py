from enum import Enum
import sys
from .ACSECCodes import ACSECCodes
from JulianBaileyUseful.py.protections.ecc.codes.ParityCodes import ParityCode, Decoder
from JulianBaileyUseful.py.protections.ecc.codes.SECDEDCodes import SECDEDCode, SECDEDType
from .PartialParityCode import PartialParityCode

class ACSECDEDType(Enum):
    CODE_EVEN_EVEN = 1 # Even SEC, Even Parity
    CODE_ODD_ODD   = 2 # Odd SEC, Odd Parity
    CODE_EVEN_ODD  = 3 # Even SEC, Odd Parity
    CODE_ODD_EVEN  = 4 # Odd SEC, Even Parity
    CODE_EVEN_EVENd = 5 # Even SEC, Even Parity (data only)
    CODE_ODD_ODDd   = 6 # Odd SEC, Odd Parity (data only)
    CODE_EVEN_ODDd  = 7 # Even SEC, Odd Parity (data only)
    CODE_ODD_EVENd  = 8 # Odd SEC, Even Parity (data only)

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
    def __init__(self, dWidth : int, aWidth : int, codeType : ACSECDEDType):
        self.dWidth = dWidth
        self.aWidth = aWidth
        self.totalWidth = dWidth + aWidth
        self.dataWidth = dWidth + aWidth
        self.codeACType = codeType
        self.partialParity = ((codeType == ACSECDEDType.CODE_EVEN_EVENd) or (codeType == ACSECDEDType.CODE_ODD_ODDd) or (codeType == ACSECDEDType.CODE_EVEN_ODDd) or (codeType == ACSECDEDType.CODE_ODD_EVENd))
        if codeType == ACSECDEDType.CODE_EVEN_EVEN or codeType == ACSECDEDType.CODE_EVEN_EVENd:
            self.codeType = SECDEDType.CODE_EVEN_EVEN
        elif codeType == ACSECDEDType.CODE_ODD_ODD or codeType == ACSECDEDType.CODE_ODD_ODDd:
            self.codeType = SECDEDType.CODE_ODD_ODD
        elif codeType == ACSECDEDType.CODE_EVEN_ODD or codeType == ACSECDEDType.CODE_EVEN_ODDd:
            self.codeType = SECDEDType.CODE_EVEN_ODD
        elif codeType == ACSECDEDType.CODE_ODD_EVEN or codeType == ACSECDEDType.CODE_ODD_EVENd:
            self.codeType = SECDEDType.CODE_ODD_EVEN
        self.secOdd       = ((codeType == ACSECDEDType.CODE_ODD_ODD) or (codeType == ACSECDEDType.CODE_ODD_EVEN) or (codeType == ACSECDEDType.CODE_ODD_ODDd) or (codeType == ACSECDEDType.CODE_ODD_EVENd))
        self.parOdd       = ((codeType == ACSECDEDType.CODE_ODD_ODD) or (codeType == ACSECDEDType.CODE_EVEN_ODD) or (codeType == ACSECDEDType.CODE_ODD_ODDd) or (codeType == ACSECDEDType.CODE_EVEN_ODDd))
        self.alwaysCorrect = False
        # print(f"ACSECDEDCodes::init dWidth={dWidth} aWidth={aWidth} codeType={codeType} partialParity={self.partialParity} secOdd={self.secOdd} parOdd={self.parOdd}")
        self.sec = ACSECCodes(dWidth, aWidth, self.secOdd)
        super().__init__(self.totalWidth, self.codeType)        
        if (codeType == ACSECDEDType.CODE_EVEN_EVENd) or (codeType == ACSECDEDType.CODE_ODD_ODDd) or (codeType == ACSECDEDType.CODE_EVEN_ODDd) or (codeType == ACSECDEDType.CODE_ODD_EVENd):
            self.par  = PartialParityCode(self.sec.encodedWidth(), self.aWidth, self.parOdd)
        else:
            self.par  = ParityCode(self.sec.encodedWidth(), self.parOdd) 
        #print(f"ACSECDEDCodes::init superEncodedWidth={super().encodedWidth()} encodedWidth={self.par.encodedWidth()}")
        self.syndromeWidth = self.encodedWidth() - self.totalWidth
        # for secded the syndrome includes the additional parity bit
        if self.encodedWidth() == (2**(self.syndromeWidth-1)):
            self.perfectCode=True
        else:
            self.perfectCode=False

    def checkConstraints(self):
        # Constraints:
        # 1) Odd.even -> will be odd.odd
        # 2) Addr are in LSB -> by construction
        # 3) At least 2 hamming bits depend only on data
        # 4) At least 2 hamming bits depending on data have an odd number of inputs

        print("Checking constraints:")

        # check constraint #3
        print(f"code mask = {self.sec.codeMasks}")
        print("Checking constriant 3: (At least 2 hamming bits depend only on data)")
        n_data_only = 0
        for cm in self.sec.codeMasks:
            cm_addr = cm & ((1<<self.aWidth)-1)
            cm_data = (cm >> self.aWidth) & ((1<<self.dWidth)-1)
            if cm_addr == 0:
                n_data_only += 1
            print(f"  codemask: {cm:0{self.encodedWidth()}b} addr={cm_addr:0{self.aWidth}b} data={cm_data:0{self.dWidth}b} data_only={cm_addr!=0} ")

        if n_data_only < 2:
            print(f"Error: {n_data_only} hamming bits depend only on data (need at least 2)")

        # check constraint #4
        print("Checking constriant 4: (At least 2 hamming bits depending on data have an odd number of inputs)")
        n_odd_inputs = 0
        for cm in self.sec.codeMasks:
            cm_addr = cm & ((1<<self.aWidth)-1)
            cm_data = (cm >> self.aWidth) & ((1<<self.dWidth)-1)
            num_inputs = bin(cm_data).count("1")
            if cm_addr == 0 and num_inputs % 2 != 0:
                n_odd_inputs += 1

            print(f"  codemask: {cm:0{self.encodedWidth()}b} addr={cm_addr:0{self.aWidth}b} data={cm_data:0{self.dWidth}b} num_inputs={num_inputs} odd_inputs={num_inputs % 2 != 0} ")
                    







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
        print("--------------------------------------------")
        self.checkConstraints()
        print("--------------------------------------------")


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
