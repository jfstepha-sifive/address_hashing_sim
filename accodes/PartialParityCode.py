
from enum import Enum

from JulianBaileyUseful.py.protections.ecc.codes.ParityCodes import ParityCode
from JulianBaileyUseful.py.protections.ecc.codes.Utils import generateParityBit, Decoder

class PartialParityCode(ParityCode):
    def __init__(self, totalWidth, addressWidth, odd):
        print("PartialParityCode::init")
        self.aWidth = addressWidth  # just the address part
        self.totalWidth = totalWidth  # address + data + syndrome
        self.odd = odd
        super().__init__(totalWidth, odd)

    def encode(self, unencodedData):
        outputData = unencodedData

        bit = generateParityBit(unencodedData >> self.aWidth, self.totalWidth - self.aWidth, self.odd)
        if (bit):
            outputData = unencodedData + (1 << self.totalWidth)
        return(outputData)

    def encodedWidth(self):
        return (self.totalWidth + 1)
    
    def decode(self, encodedData):
        return (Decoder(
            encodedData >> self.aWidth, # uncorrected
            None,                   # corrected
            False,                  # correctable
            generateParityBit(encodedData >> self.aWidth, self.totalWidth - self.aWidth, self.odd) != (encodedData & (1 << self.totalWidth)) >> self.totalWidth,  # uncorrectable
            generateParityBit(encodedData >> self.aWidth, self.totalWidth - self.aWidth, self.odd)  # syndrome
        ))
