from Number import*

class Function:
    def __init__(self):
        self.information = "This is a function class"

    def transferToBinary(self, string, flag = 1):
        if len(string) % 8 != 0 and flag:
            string += (8-len(string)%8)*" "
        outputBinary = ""
        for i in range(len(string)):
            binary = bin(ord(string[i])).replace("0b", "")
            if len(binary) != 8:
                binary = (8-len(binary)) * "0" + binary
            outputBinary += binary
        return outputBinary

    def transferToASC(self, numberStr):
        # outputTemp stores 8 bites to help get word
        outputTemp = []
        outputString = ""
        for i in range(0, len(numberStr), 8):
            outputTemp.append(numberStr[i:i+8])
        for i in range(len(outputTemp)):
            outputString += chr(int(outputTemp[i], 2))
        return outputString

    def converteIP(self, text):
        outputIP = ""
        # IP do not have 0 so we need -1 to get 0 position
        for i in range(len(text)):
            outputIP += text[ip[i]-1]
        return outputIP

    def converteInvIP(self, text):
        outputInvIP = ""
        for i in range(len(text)):
            outputInvIP += text[invIp[i] - 1]
        return outputInvIP

    def keySet(self, key):
        leftKeyOut = [0 for i in range(17)]
        rightKeyOut = [0 for i in range(17)]
        midKey = [0 for i in range(17)]
        finalKey = [0 for i in range(17)]
        # step 0 converte key from str->binary
        if len(key) != 8:
            return "Please input right number for the key(8 words)!!"
        keyBinary = self.transferToBinary(key, 0)
        # step 1 initial permutation
        initialKey = ""
        for i in range(56):
            initialKey += keyBinary[compress1[i]-1]
        # step 2 separate key to 28:28
        leftKey = initialKey[0:28]
        rightKey = initialKey[28:56]
        # left move by using table d
        leftKeyOut[0] = leftKey
        rightKeyOut[0] = rightKey
        for i in range(len(d)):
            if d[i] == 1:
                leftKeyOut[i + 1], rightKeyOut[i + 1] = self.leftMove(leftKeyOut[i], rightKeyOut[i], 1)
            elif d[i] == 2:
                leftKeyOut[i + 1], rightKeyOut[i + 1] = self.leftMove(leftKeyOut[i], rightKeyOut[i], 2)
            midKey[i + 1] = leftKeyOut[i + 1] + rightKeyOut[i + 1]
        # step 3 second permutation
        for i in range(1, len(midKey)):
            temp = ""
            for j in range(48):
                 temp += midKey[i][compress2[j]-1]
            finalKey[i] = temp
        return finalKey

    def leftMove(self, leftKey, rightKey, move):
        if move == 1:
            leftKey1 = leftKey[1:28] + leftKey[0]
            rightKey1 = rightKey[1:28] + rightKey[0]
        elif move == 2:
            leftKey1 = leftKey[2:28] + leftKey[0] + leftKey[1]
            rightKey1 = rightKey[2:28] + rightKey[0] + rightKey[1]
        return leftKey1, rightKey1

    def F(self, leftPlaintext, rightPlaintext, key):
        rightPermutation = self.textPermutation(rightPlaintext)
        XOR = int(rightPermutation, 2) ^ int(key, 2)
        XOR = bin(XOR).replace("0b", "")
        XOR = self.verifyBinaryNumber(XOR, 48)
        afSBox = self.permutationSBox(XOR)
        afPBox = self.permutationPBox(afSBox)
        fintext = int(afPBox, 2) ^ int(leftPlaintext, 2)
        fintext = bin(fintext).replace("0b", "")
        fintext = self.verifyBinaryNumber(fintext, 32)
        return fintext

    def verifyBinaryNumber(self, number, flag):
        if len(number) != flag:
            binary = (flag - len(number)) * "0" + number
        else:
            binary = number
        return binary

    def textPermutation(self, text):
        fintext =""
        for i in range(48):
            fintext += text[extend[i]-1]
        return fintext

    def permutationSBox(self, text):
        midText = []
        fintext = ""
        textGroup = []
        # separate text into 8 groups, each group 6bits
        for i in range(0, len(text), 6):
            textGroup.append(text[i : i + 6])
        # 6 bits permutate to 4 bits
        for i in range(8):
            row = textGroup[i][0] + textGroup[i][5]
            column = textGroup[i][1:5]
            row = int(row, 2)
            column = int(column, 2)
            sbox = Sbox[i]
            midText.append(sbox[row][column])
        for i in range(len(midText)):
            binary = bin(midText[i]).replace("0b", "")
            if len(binary) != 4:
                binary = (4 - len(binary)) * "0" + binary
            fintext += binary
        return fintext

    def permutationPBox(self, text):
        fintext = ""
        for i in range(len(text)):
            fintext += text[p[i]-1]
        return fintext

    def verifyKey(self, key):
        if len(key) != 8:
            print("Wrong!!!!")
            key = input("Please input right key with 8 number")
        return key

class Des:
    function = Function()
    def __init__(self, choice, text, key):
        self.choice = choice
        self.text = text
        self.key = key

    def judge(self):
        finText = ""
        # step 1 asc-> binary
        binaryText = self.function.transferToBinary(self.text)
        if self.choice == 1:
            # return self.__desEncryption(self.text, self.key)
            for i in range(0, len(binaryText), 64):
                finText += self.desEncryption(binaryText[i:i+64], self.key)
            return finText
        elif self.choice == 2:
            for i in range(0, len(binaryText), 64):
                finText += self.desDecryption(binaryText[i:i+64], self.key)
            return finText
        else:
            print("Error choice. ")

    def desEncryption(self, plaintext, userKey):
        # encryption for each 64bit
        # step 1 using table ip
        plaintext = self.function.converteIP(plaintext)
        # step 2 separate plaintext
        leftPlaintext = plaintext[0:32]
        rightPlaintext = plaintext[32:64]
        # step 3 creating key
        key = self.function.keySet(userKey)
        # step 4 using function F and key 16 rounds
        for i in range(1, 17):
            temp = self.function.F(leftPlaintext, rightPlaintext, key[i])
            leftPlaintext = rightPlaintext
            rightPlaintext = temp
        # step 5 using inv IP
        combineText = leftPlaintext + rightPlaintext
        combineText = bin(int(combineText, 2)).replace("0b", "")
        combineText = self.function.verifyBinaryNumber(combineText, 64)
        fintext = self.function.converteInvIP(combineText)
        return fintext

    def desDecryption(self, ciphertext, userKey):
        # step 1 using table ip
        plaintext = ciphertext
        plaintext = self.function.converteIP(plaintext)
        # step 2 separate plaintext
        leftPlaintext = plaintext[0:32]
        rightPlaintext = plaintext[32:64]
        # step 3 creating keyciphertext
        key = self.function.keySet(userKey)
        # step 4 using function F and key 16 rounds
        for i in range(1, 17):
            # !!!!!! change position of rightPlaintext and leftPlaintext
            # !!!!!! using key 16->1
            temp = self.function.F(rightPlaintext, leftPlaintext, key[17 - i])
            rightPlaintext = leftPlaintext
            leftPlaintext = temp
        # step 5 using inv IP
        combineText = leftPlaintext + rightPlaintext
        combineText = bin(int(combineText, 2)).replace("0b", "")
        combineText = self.function.verifyBinaryNumber(combineText, 64)
        fintext = self.function.converteInvIP(combineText)
        return fintext

def main():
    function = Function()
    startSystem = 1
    while startSystem:
        print("This is a Des encryption and decrytion system!!")
        choice = input("What do you want? 1. Encryption 2. Decryption 3.Exit  ")
        if choice == "1":
            plaintext = input("Please input plaintext: ")
            userKey = input("Please input key: ")
            userKey = function.verifyKey(userKey)
            encryption = Des(1, plaintext, userKey)
            resultBinary = encryption.judge()
            print("The result is:", resultBinary)
            print("The result is:(word):", function.transferToASC(resultBinary))
        elif choice == "2":
            plaintext = input("Please input plaintext: ")
            userKey = input("Please input key: ")
            userKey = function.verifyKey(userKey)
            encryption = Des(2, plaintext, userKey)
            resultBinary = encryption.judge()
            print("The result is:", resultBinary)
            print("The result is:(word): ", function.transferToASC(resultBinary))
        elif choice == "3":
            startSystem = 0
        else:
            print("Please choose right number from 1 and 2")
