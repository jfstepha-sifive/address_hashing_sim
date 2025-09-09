class ArbCodes:
    def __init__(self, dataWidth, totalWidth):
        self.dataWidth = dataWidth
        self.totalWidth = totalWidth
        self.total_data_words = 2**self.dataWidth
        self.total_code_words = 2**totalWidth
        self.encoding = [None] * self.total_code_words 
        self.encoding_list = []

        # SECDED:
        self.correctable_hamming_distance = 1
        self.uncorrectable_hamming_distance = 2

        # parity:
        #self.correctable_hamming_distance = 0
        #self.uncorrectable_hamming_distance = 1

    def print(self):

        i = 1
        for encoding in self.encoding_list:
            print(f"-- encoding {i}--")
            for cw in range(0, self.total_code_words):
                e = encoding[cw]
                if e is None:
                    print(f"  {cw:0{self.totalWidth}b}: -")
                else:
                    print(f"  {cw:0{self.totalWidth}b}: {e}")
                    #print(f"  {cw:0{self.totalWidth}b}: {e['data']:0{self.totalWidth}b} ({e['type']})")
            i += 1

    def calcHamming(self, d1, d2):
        s1 = f"{d1:0{self.totalWidth}b}"
        s2 = f"{d2:0{self.totalWidth}b}"
        hamming = 0
        for i in range(0, self.totalWidth):
            if s1[i] != s2[i]:
                hamming += 1
        return hamming
    
        
        
    def checkduplicates(self, data_encoding):
        for i in range(0, self.total_data_words):
            for j in range(i+1, self.total_data_words):
                if data_encoding[i] is not None and data_encoding[j] is not None:
                    if data_encoding[i] == data_encoding[j]:
                        # print(f"  duplicate data {i} and {j}")
                        return True
        return False

    def assignAdjacents(self, encoding):
        for i in range(0, self.total_code_words):
            for j in range(0, self.total_code_words):
                if encoding[i] is not None and encoding[i]['type'] == 'data' and i != j:

                    # check for uncorrectable encoding
                    if self.calcHamming(i, j) <= self.uncorrectable_hamming_distance and self.calcHamming(i, j) > self.correctable_hamming_distance:
                        # j should be an uncorrectable
                        if encoding[j] is None:
                            encoding[j] = {'data': None, 'type': 'uncorrectable'}
                            # print(f"  assigned {j} as uncorrectable")
                        else:
                            if encoding[j]['type'] != 'uncorrectable':
                                # print(f"  {j} is already assigned: {encoding[j]}")
                                return None
                            #else: 
                            #    print(f"  {j} was already uncorrectable")
                    
                    # check for correctable encoding
                    elif self.calcHamming(i, j) <= self.correctable_hamming_distance:
                        if encoding[j] is None:
                            encoding[j] = {'data': encoding[i]['data'], 'type': 'correctable'}
                            # print(f"  assigned {j} as correctable")
                        else:
                            if encoding[j]['type'] == 'correctable':
                                if encoding[j]['data'] != encoding[i]['data']:
                                    # print(f"  {j} is already correctable! {encoding[j]}")
                                    return None
                                #else:
                                #     print(f"  {j} is already correctable to {encoding[i]['data']}, assigned: {encoding[j]}")
                            else: 
                                print(f"  {j} is already assigned: {encoding[j]}")
                                return None
        return encoding

    def incrementEncoding(self, data_encodings):
        for i in range(0, self.total_data_words):
            data_encodings[i] += 1
            if data_encodings[i] >= self.total_code_words:
                data_encodings[i] = 0
            else:
                return data_encodings

        return None
    
    def checkEncodingHammingDistance(self, encoding):
        for i in range(0, self.total_code_words):
            for j in range(i+1, self.total_code_words):
                if encoding[i] is not None and encoding[j] is not None:
                    if self.calcHamming(i, j) <= (self.uncorrectable_hamming_distance + self.correctable_hamming_distance):
                        # print(f"  code-to-code hamming distance failed between {i} and {j}")
                        return True
        return False
       
    def findEncodings(self):
        data_encodings = [0] * self.total_data_words
        done = False 
        i = 0
        while not done:
            encoding = [None] * self.total_code_words
            
            # set up initial encoding
            for dataWord in range(0, self.total_data_words):
                cw = data_encodings[dataWord]
                encoding[cw] = {'data': dataWord, 'type': 'data'}
            
            
            # first pass - check for duplicates
            if self.checkduplicates(data_encodings):
                # print(f"  duplicate data, trying again")
                encoding = None
            # second pass - check for code-to-code hamming distance
            elif self.checkEncodingHammingDistance(encoding):
                # print(f"  code-to-code hamming distance failed, trying again")
                encoding = None
            else:
                encoding = self.assignAdjacents(encoding)
                # if encoding is None:
                #     print(f"  adjacent constraints failed, trying again")
            if encoding is not None:
                # print(f"  found an encoding: {encoding}")
                self.encoding_list.append(encoding)

            data_encodings = self.incrementEncoding(data_encodings)
            if data_encodings is None:
                done = True
 
            if i % 100000 == 0 or done:
 
                print(f"tried {i} encodings, found {len(self.encoding_list)}")
            i += 1

 

    def createCode(self):
        print(f"Attempting to create a code with {self.dataWidth} data bits and {self.totalWidth} total bits")
        all_constraints_pass = True

        print(f"total codewords needed: {self.total_data_words}")
        self.findEncodings()

        if len(self.encoding_list) > 0:
            print(f"found {len(self.encoding_list)} encodings:")
            self.print()
            print(f"created {len(self.encoding_list)} encodings")
        else:
            print("failed to create code")


        

if __name__ == "__main__":
    code=ArbCodes(3,4)
    code.createCode()
