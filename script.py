import csv
import sys
from random import random

class RandomPassword:
    def __init__(self, wordList, generateMembernumber, memberNumber, chainLength, memberNumberLength):
        self.wordList = wordList
        self.memberNumberLength = memberNumberLength
        self.randomWordList = []
        self.chainLength = chainLength
        self.memberNumber = str(memberNumber)
        self.generateMembernumber = generateMembernumber
        self.password = self.generatePassword()

    def generatePassword(self):
        for i in range(1, self.chainLength):
            randomIndex = round(random() * len(self.wordList)) - 1
            word = self.wordList[randomIndex]
            while word in self.randomWordList:
                randomIndex = round(random() * len(self.wordList)) - 1
                word = self.wordList[randomIndex]
            self.randomWordList.append(word)
        if self.generateMembernumber:
            if len(self.memberNumber) < self.memberNumberLength:
                for i in range(0, self.memberNumberLength - len(self.memberNumber)):
                    self.memberNumber = '0' + self.memberNumber

            self.randomWordList.append(self.memberNumber)
        return '-'.join(self.randomWordList)



class PasswordGenerator:
    def __init__(self, setup):
        self.total = int(setup.get('total'))
        self.memberNumberLength = int(setup.get('memberNumberLength'))
        self.wordList = self.loadWordList()
        self.chainLength = int(setup.get('chainLength'))
        self.generateMembernumber = setup.get('generateMembernumber')
        self.memberNumber = 1
        self.passwords = []
        self.generatePasswords()

    def generatePasswords(self):
        while len(self.passwords) < self.total:
            newPassword = RandomPassword(self.wordList, self.generateMembernumber, self.memberNumber, self.chainLength, self.memberNumberLength)
            while newPassword.password in self.passwords:
                newPassword = RandomPassword(self.wordList, self.generateMembernumber, self.memberNumber, self.chainLength, self.memberNumberLength)
            print('new pw created: ' + newPassword.password)
            self.passwords.append(newPassword.password)
            self.updateMemberNumber()
        self.writeResultToFile()

    def updateMemberNumber(self):
        if self.generateMembernumber:
            self.memberNumber += 1

    def loadWordList(self):
        with open('input.csv', newline='') as f:
            reader = csv.reader(f)
            return [item[0] for item in list(reader)]

    def writeResultToFile(self):
        with open('output.csv', 'w') as f:
            writer = csv.writer(f)
            for password in self.passwords:
                writer.writerow({password})
        print('iserted into output.csv')
        print('job done')

args = {}
for arg in sys.argv:
    argSplit = arg.split('=')
    if len(argSplit) > 1:
        args.update({argSplit[0]: argSplit[1]})

PasswordGenerator({
    'total': args['total'] if 'total' in args else 20,
    'chainLength': args['chainLength'] if 'chainLength' in args else 4,
    'generateMembernumber': args['generateMembernumber'] if 'generateMembernumber' in args else True,
    'memberNumberLength': args['memberNumberLength'] if 'memberNumberLength' in args else 4,
})
