StackLL1 = ['EOF','pgm']
AlphaSet = {chr(a) for a in range(ord('A'), ord('Z')+1)}
TerminalSet = {"+", "-", "IF", "<", "=", "PRINT", "GOTO", "STOP", "EOF"}
Ops=["+","-","<","="]
LowerTerminal=["IF","PRINT","STOP"]
BCodeType ={
    "#line" : 10,
    "#id" : 11,
    "#const" : 12,
    "#if" : 13,
    "#goto" : 14,
    "#print" : 15,
    "#stop" : 16,
    "#op" : 17,
}

NextSet ={
    1 : ["line", "pgm"],
    2 : ["EOF"],
    3 : ["line_num", "stmt"],
    4 : ["asgmnt"],
    5 : ["if"],
    6 : ["print"],
    7 : ["goto"],
    8 : ["stop"],
    9 : ["id", "=", "exp"],
    10 : ["term", "split1"],
    11 : ["+", "term"],
    12 : ["-", "term"],
    13 : None,
    14 : ["id"],
    15 : ["const"],
    16 : ["IF", "cond", "line_num"],
    17 : ["term", "split2"],
    18 : ["<", "term"],
    19 : ["=", "term"],
    20 : ["PRINT", "id"],
    21 : ["GOTO", "line_num"],
    22 : ["STOP"]
}

ParsingTable = {
    "pgm" : {"line_num" : 1, "EOF" : 2},
    "line" : {"line_num" : 3},
    "asgmnt" : {"id" : 9},
    "split1" : {"line_num" : 13, "+" : 11, "-" : 12, "EOF" : 13},
    "term" : {"id" : 14, "const" : 15},
    "if" : {"IF" : 16},
    "split2" : {"<" : 18, "=" : 19},
    "print" : {"PRINT" : 20},
    "goto" : {"GOTO" : 21},
    "stop" : {"STOP" : 22},
    "stmt" : {"id" : 4, "IF" : 5, "PRINT" : 6, "GOTO" : 7, "STOP" : 8},
    "exp" : {"id" : 10, "const" : 10},
    "cond" : {"id" : 17, "const" : 17}
}

def GetTerminalType(Token):
    if Token.isdigit():
        return "num"
    if Token in AlphaSet:
        return "id"
    if Token in TerminalSet:
        return Token 
    raise Exception('Symbol ' +Token +' is not in terminal set')

def GetRule(Top, Token):
    TerminalType = GetTerminalType(Token)
    if(TerminalType != "num" and TerminalType in ParsingTable[Top]):
        return ParsingTable[Top][TerminalType]
    if("line_num" in ParsingTable[Top]):
        return ParsingTable[Top]["line_num"]
    if("const" in ParsingTable[Top]):
        return ParsingTable[Top]["const"]
    raise Exception('Rule is not defined')

def GetBCode(TerminalSym, Value):
    if(TerminalSym == "line_num"): 
        return ("#line", int(Value))
    if(TerminalSym == "id"): 
        return ("#id", ord(Value) - ord('A') + 1)
    if(TerminalSym == "const"):
        return ("#const", int(Value))
    if(TerminalSym in LowerTerminal):
        return ('#'+TerminalSym.lower(),0)
    if(TerminalSym == "GOTO"):
        return ("#goto", int(Value))
    if TerminalSym in Ops: 
        return ("#op", Ops.index(TerminalSym)+1)

def IsSameTerminal(Token, Top):       
    TerminalType = GetTerminalType(Token)
    if(TerminalType != "num"):
        return TerminalType == Top
    else:
        return Top == "line_num" or Top == "const"
    
def GenerateBCode(ParsedList):
    BCodeList = []
    for i in range(len(ParsedList)):
        if(ParsedList[i][0] not in ["GOTO","line_num"] or not i):
            BCodeList.append(GetBCode(ParsedList[i][0], ParsedList[i][1]))
        else:
            if(ParsedList[i][0] == 'line_num' and i):
                BCodeList.append(GetBCode("GOTO", ParsedList[i][1]))
    return BCodeList

def parse(Token):
    while(not IsSameTerminal(Token, StackLL1[-1])):
        Top = StackLL1.pop()
        if not Top in ParsingTable:
            raise Exception("Symbol '"+ Token + "' is unexpected (mismatch terminal symbol to parsing table)") 
        Rule = GetRule(Top, Token)
        if(NextSet[Rule] != None):
            StackLL1.extend(NextSet[Rule][::-1])
    if(StackLL1[-1] == 'line_num' and not 1 <=int(Token) <= 1000):
        raise Exception("Value of line_num is not in appropriate range")
    if(StackLL1[-1] == 'const' and not 0 <=int(Token) <= 100):
        raise Exception("Value of const is not in appropriate range") 
    return StackLL1.pop()

def ConvertToBCode(Line):
    ParsedList = []
    for Token in Line:
        ParsedList.append((parse(Token), Token))
    BCodeList = GenerateBCode(ParsedList)
    print('Generated bcode :',*BCodeList)
    BCodeString = ''
    for Types, Value in BCodeList:
        BCodeString = BCodeString + str(BCodeType[Types])+ ' ' + str(Value) + ' '
    print('bcode :',BCodeString)
    return BCodeString

f = open("input.txt", "r")
Raw=[Line.replace('\n','') for Line in f.readlines()]
f.close()
BCodeString=''
for Line in Raw:
    print(Line)
    BCodeString += ConvertToBCode(Line.split(' '))+'\n'
o = open("output.bout", "w")
o.write(BCodeString)
o.close()
print('Finished! look the result in output.bout')
