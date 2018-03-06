from DES import *
import random

def binaryIV():
    ranNumber = int(random.uniform(1, 100))
    i = 1
    while i:
        if ranNumber <= 10000000:
            ranNumber *= random.uniform(100,999)
        else:
            i = 0
    ranNumber = int(ranNumber)
    binText = bin(ranNumber).replace("0b", "")
    flag = 1
    while flag:
        if len(binText) < 64:
            binText += (64-len(binText))%8*binText + "0"
        elif len(binText) > 64:
            Fintext = binText[0:64]
            flag = 0
    return Fintext

def XORfunction(normalText, xorText):
    function = Function()
    XOR = int(normalText, 2) ^ int(xorText, 2)
    XOR = bin(XOR).replace("0b", "")
    XOR = function.verifyBinaryNumber(XOR, 64)
    return XOR

def encryption(plaintext, userKey):
    function = Function()
    userKey = function.verifyKey(userKey)
    encryption = Des(1, plaintext, userKey)
    resultBinary = encryption.judge()
    return resultBinary

class Chaining(Des):

    def judge(self):
        function = Function()
        finText = ""
        temp = ""
        IV = binaryIV()
        arrayPlaintext = []
        # step 1 asc-> binary
        binaryText = function.transferToBinary(self.text)
        if self.choice == 1:
            for i in range(0, len(binaryText), 64):
                arrayPlaintext.append(binaryText[i : i + 64])
            arrayPlaintext[0] = XORfunction(arrayPlaintext[0], IV)
            for i in range(len(arrayPlaintext)):
                midText = self.desEncryption(arrayPlaintext[i], self.key)
                finText += midText
                if len(arrayPlaintext) >= 2 and i+1 < len(arrayPlaintext):
                    arrayPlaintext[i+1] = XORfunction(midText, arrayPlaintext[i+1])
            print("IV is: ", IV)
            return finText

        elif self.choice == 2:
            IV = input("Please input IV: ")
            for i in range(0, len(binaryText), 64):
                midText = self.desDecryption(binaryText[i:i + 64], self.key)
                temp += midText
                if i >= 64:
                    finText += XORfunction(binaryText[i-64:i], midText)
            plaintextOne = XORfunction(temp[0:64], IV)
            finText = plaintextOne + finText
            return finText
        else:
            print("Error choice. ")

def mainChain():
    global test, IV, password
    print("This is a block chaining!!!")
    function = Function()
    startSystem = 1
    while startSystem:
        print("This is a Block chaning(DES) encryption and decrytion system!!")
        choice = input("What do you want? 1. Encryption 2. Decryption 3.Exit  ")
        if choice == "1":
            plaintext = input("Please input plaintext: ")
            userKey = input("Please input key: ")
            userKey = function.verifyKey(userKey)
            encryption = Chaining(1, plaintext, userKey)
            resultBinary = encryption.judge()
            print("The result is:", resultBinary)
            print("The result is:(word):", function.transferToASC(resultBinary))
        elif choice == "2":
            plaintext = input("Please input cipherText: ")
            # plaintext = test
            # print("Cipher text is: ", plaintext)
            userKey = input("Please input key: ")
            # userKey = password
            # print("The key is: ", userKey)
            1
            userKey = function.verifyKey(userKey)
            encryption = Chaining(2, plaintext, userKey)
            resultBinary = encryption.judge()
            print("The result is:", resultBinary)
            print("The result is:(word): ", function.transferToASC(resultBinary))
        elif choice == "3":
            startSystem = 0
        else:
            print("Please choose right number from 1 and 2")

mainChain()