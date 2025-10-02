import math
from enum import Enum
from JulianBaileyUseful.py.protections.ecc import codes
from JulianBaileyUseful.py.protections.ecc.codes.SECCodes import SECCode
from JulianBaileyUseful.py.protections.ecc.codes.SECDEDCodes import SECDEDCode
from JulianBaileyUseful.py.protections import ecc


class ACSECCodes(ecc.codes.SECCodes.SECCode):
    def __init__(self, dWidth : int, aWidth : int, odd_parity : bool = False, bump_width=False):
        # dWidth and aWidth are the number of data and address bits as inputs
        # these are combined into dataWidth in Julian's library
        self.dWidth = dWidth
        self.aWidth = aWidth
        self.totalWidth = dWidth + aWidth
        self.odd_parity = odd_parity
        self.bump_width = bump_width
        super().__init__(dataWidth = self.totalWidth, odd=self.odd_parity, bump_width=self.bump_width)
        self.syndromeWidth = self.encodedWidth() - self.totalWidth
        if self.encodedWidth() == (2**self.syndromeWidth - 1):
            self.perfectCode=True
        else:
            self.perfectCode=False

    def __numCodeBits(self):
        m = int(math.log2(self.totalWidth)) + 1
        if (((1 << m) < m + self.totalWidth + 1)):
            m = m + 1
        if self.bump_width:
            m += 1
        return m


    def printInfo(self):
        print("--------------------------------------------")
        print("Code info:")
        print(f"  dWidth: {self.dWidth}")
        print(f"  aWidth: {self.aWidth}")
        print(f"  totalWidth: {self.totalWidth}")
        print(f"  odd_parity: {self.odd_parity}")
        print(f"  encodedWidth: {self.encodedWidth()}")
        print(f"  syndromeWidth: {self.syndromeWidth}")
        print(f"  perfectCode: {self.perfectCode}")
        print("--------------------------------------------")
        print("code constraints:")

    def encode(self, data, address):
        dataToEncode = address | data << self.aWidth
        # print(f"ACSECCodes::encode {data:0{self.dWidth}b} {address:0{self.aWidth}b} {dataToEncode:0{self.totalWidth}b}")
        returned = super().encode(dataToEncode)
        # print(f"ACSECCodes::encode returned {returned:0{self.encodedWidth()}b}")
        return super().encode(dataToEncode)

    def decode(self, data):
        decoded = super().decode(data)
        return decoded
    
    def encodedWidth(self):
        return (self.totalWidth + self.__numCodeBits())

    def isAllZerosUncorrectable(self):
        return(False)
