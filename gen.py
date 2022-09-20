import pandas as pd
import numpy as np
import random
from PIL import Image


def show(Table):
    for i in range(0,8):
        print(Table[i])

def InitTable(StrChromosome,Table):
    Chromosome = StrToList(StrChromosome)
    i = 0
    while i<8:
            j = Chromosome[i]
            Table[j][i][0]=[j,i]
            i = i+1
    return(Table)

def buildTable(Table1 = None):
        Table1 = [[],[],[],[],[],[],[],[]]
        for i in range(0,8):
            for j in range(0,8):
                Table1[i].append(['    '])
        return(Table1)

def StrToList(Str):
    L = [0,1,2,3,4,5,6,7]
    Str = int(Str)
    for i in range(0,8):
        num = Str%10
        L[7-i]=num
        Str = int(Str/10)
    return(L)

def ListToStr(List):
    Str = str()
    for i in range(0,8):
        Str = Str + str(List[i])
    return(Str)

def chess_board_show(ArrayList, df):
    img1 = Image.open(r"E:\programming\python\genetic\image\Chess_Board.png")
    img2 = Image.open(r"E:\programming\python\genetic\image\q12.png")
    for i in range(0,8):
        if i==7 or i==6 :
            img1.paste(img2, (-96 + 59*i + 3 , -93 + 59*ArrayList[i]), mask = img2)
        else:
            img1.paste(img2, (-96 + 60*i , -93 + 59*ArrayList[i]), mask = img2)
    img1.show()
    img1.save("E:\\programming\\python\\genetic\\Answer-Image\\"f"{len(df)}.jpg")
#_______________________________________________________________________________________________________________________________________________

class genetic :
    def __init__(self, Chromosome1=None, Chromosome2=None) :
        self.Chromosome1 = Chromosome1
        self.Chromosome2 = Chromosome2
        self.ChromosomeBank = pd.DataFrame(data=None, columns=['Chromosome','score','chance'])
        self.indexNumber = -1
        self.Score = 1
        self.strChromosome = str()
        self.std = list()
        self.ToF = True
        self.True_Answer_DB = pd.DataFrame(data=None, columns=['Chromosome'])

    def Scoring(self,strChromosome,Table) :

        Chromosome = StrToList(strChromosome)
        Score = 0
        ChromosomeScore = [0,0,0,0,0,0,0,0]

        for i in range(0,8):
            for j in range(i+1,8):
                if Chromosome[i]==Chromosome[j]:
                    ChromosomeScore[i] = ChromosomeScore[i]+1
            for k in range(0,i):
                if Chromosome[i]==Chromosome[k]:
                    ChromosomeScore[i] = ChromosomeScore[i]+1


        for m in range(0,8):
            for n in range(1,8):
                if (Chromosome[m]+n >= 0)and(Chromosome[m]+n <= 7)and(m+n >= 0)and(m+n <= 7):
                    if type(Table[Chromosome[m]+n][m+n][0])==list:
                        ChromosomeScore[m]=ChromosomeScore[m]+1

        for m in range(0,8):
            for n in range(1,8):
                if (Chromosome[m]-n >= 0)and(Chromosome[m]-n <= 7)and(m-n >= 0)and(m-n <= 7):
                    if type(Table[Chromosome[m]-n][m-n][0])==list:
                        ChromosomeScore[m]=ChromosomeScore[m]+1

        for m in range(0,8):
            for n in range(1,8):
                if (Chromosome[m]-n >= 0)and(Chromosome[m]-n <= 7)and(m+n >= 0)and(m+n <= 7):
                    if type(Table[Chromosome[m]-n][m+n][0])==list:
                        ChromosomeScore[m]=ChromosomeScore[m]+1

        for m in range(0,8):
            for n in range(1,8):
                if (Chromosome[m]+n >= 0)and(Chromosome[m]+n <= 7)and(m-n >= 0)and(m-n <= 7):
                    if type(Table[Chromosome[m]+n][m-n][0])==list:
                        ChromosomeScore[m]=ChromosomeScore[m]+1
        
        self.indexNumber = self.indexNumber + 1
        for i in range(0,8): 
            Score = Score + ChromosomeScore[i]
        Score = 56 - Score
        self.Score = Score

        
        self.ChromosomeBank.at[self.indexNumber,:] = [strChromosome, Score,Score] 
        sumS = self.ChromosomeBank['score'].sum()
        if sumS==0: 
            sumS = 1 
            self.ChromosomeBank['score'] = 1
        self.ChromosomeBank['chance'] = self.ChromosomeBank['score']
        self.ChromosomeBank['chance'] = self.ChromosomeBank['chance'].divide(sumS)
        self.strChromosome =  strChromosome

    def ChoiceAndMerge(self):

        newChromosome1 = [0,1,2,3,4,5,6,7]
        newChromosome2 = [0,1,2,3,4,5,6,7]
        chosenChromosomes = np.random.choice(self.ChromosomeBank['Chromosome'],p=self.ChromosomeBank['chance'],size=2)
        chosenList = StrToList(chosenChromosomes[0]), StrToList(chosenChromosomes[1])
        hashList = [0,1,2,3,4,5,6,7]

        for i in range(0,8):
            hashList[i]=random.randint(0,1)
            newChromosome1[i]=chosenList[hashList[i]][i]
            newChromosome2[i]=chosenList[np.absolute(hashList[i]-1)][i]
        newChromosome1[random.randint(0,7)] = random.randint(0,7)
        newChromosome2[random.randint(0,7)] = random.randint(0,7)

        return(ListToStr(newChromosome1),ListToStr(newChromosome2))

    def end(self):
        if self.Score == 56 :
            
            # print(self.ChromosomeBank)
            # print('The operation ended')
            print('one solution is : ' + self.strChromosome)
            # show(InitTable(self.strChromosome, buildTable()))
            chess_board_show(StrToList(self.strChromosome), self.True_Answer_DB)
            self.ToF = False

            temp_list = []
            temp_list.append(self.strChromosome)
            length_df = len(self.True_Answer_DB)
            self.True_Answer_DB.loc[length_df] = temp_list
            self.True_Answer_DB = self.True_Answer_DB.drop_duplicates()
            self.True_Answer_DB.to_csv('Answers.csv', index=False, header=['Answers'])
            
    def heuristic(self):

        if self.indexNumber%5 == 0:
            self.ChromosomeBank = self.ChromosomeBank.drop_duplicates(subset='Chromosome')
            mean = self.ChromosomeBank['score'].mean()
            stdNow = self.ChromosomeBank['score'].std()
            self.ChromosomeBank = self.ChromosomeBank.drop(self.ChromosomeBank[self.ChromosomeBank['score'] < (mean + stdNow/2)].index)
            print(self.ChromosomeBank)

            print('mean : ' + str(mean))
            self.std.append(stdNow)
            print('standard deviation : ' + str(stdNow))

        else:
            pass
        
#_______________________________________________________________________________________________________________________________________________
def init():
    t1 = buildTable()
    T1 = InitTable('00000000',t1)
    t2 = buildTable()
    T2 = InitTable('00000000',t2)
    g1 = genetic()
    g1.Scoring('00000000',T1)
    g1.Scoring('00000000',T2)
    print('-----------------------------')
    return(g1)
    

def make_solution(g1):
    while g1.ToF:
        nd1 , nd2 = g1.ChoiceAndMerge()
        g1.heuristic()
        t3 = buildTable()
        t4 = buildTable()
        g1.Scoring(nd1,InitTable(nd1,t3))
        g1.Scoring(nd2,InitTable(nd2,t4))
        g1.end()

def all_solution(g, number=1):
    while len(g.True_Answer_DB)<int(number) :
        
        g.ChromosomeBank = pd.DataFrame(data=None, columns=['Chromosome','score','chance'])
        t1 = buildTable()
        t2 = buildTable()
        T1 = InitTable('00000000',t1)
        T2 = InitTable('00000000',t2)
        g.Scoring('00000000',T1)
        g.Scoring('00000000',T2)
        g.indexNumber = -1
        g.Score = 1
        g.ToF = True
        make_solution(g)
        
g1 = init()
all_solution(g1,input("how many solutions do you want ? : "))






