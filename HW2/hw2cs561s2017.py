# encoding=utf-8
import random
from copy import deepcopy

def openfile(filename):
    fr=open(filename,"r")
    linenum = 0
    M = 0
    N = 0
    for line in fr :
        s = line.split()
        if linenum==0:
            M = int(s[0])
            N = int(s[1])
            matrix = [[0]*M for i in range(M)]
        else:
            if s[2]=='F':
                xtemp=int(s[0])-1
                ytemp=int(s[1])-1
                matrix[xtemp][ytemp]=1
                matrix[ytemp][xtemp]=1
            if s[2]=='E':
                xtemp=int(s[0])-1
                ytemp=int(s[1])-1
                matrix[xtemp][ytemp]=-1
                matrix[ytemp][xtemp]=-1
        linenum+=1
    fr.close()
    return matrix,M,N

# [[A,D],[B],[C]]
# (A V D)Λ B Λ C
#
#  V Xai  -->  [[Xa0,Xa1,...,XaN-1]]
#  Λ [~(Xai Λ Xaj)]  -->  Λ (~Xai V ~Xaj)     0<i<j<N-1
#                    -->  [[~Xa0,~Xa1],[~Xa0,~Xa2],...,[~XaN-2,~XaN-1]]
def each_guest(num,N):
    sentence =[]
    clause = []
    for i in range(N):
        li0 = "X%d#%d"%(num,i)
        clause.append(li0)
        for j in range(i+1,N):
            li1 = "~X%d#%d" % (num,i)
            li2 = "~X%d#%d" % (num,j)
            sentence.append([li1,li2])
    sentence.append(clause)
    return sentence

# Λ [~(Xai Λ Xbj)] -->  Λ( ~Xai V ~Xbj)        i!=j
#                  -->  [[~Xa0,~Xb1],[~Xa0,~Xb2],...,[~XaN-1,~XaN-2]]
def each_friend(num1,num2,N):
    sentence =[]
    for i in range(N):
        for j in range(N):
            if i==j:
                continue
            li1 = "~X%d#%d" % (num1,i)
            li2 = "~X%d#%d" % (num2,j)
            sentence.append([li1,li2])

    return sentence

# def each_friend(num1,num2,N):
    # sentence =[]
    # for i in range(N):
        # li1 = "~X%d#%d" % (num1,i)
        # li2 = "X%d#%d" % (num2,i)
        # li3 = "X%d#%d" % (num1,i)
        # li4 = "~X%d#%d" % (num2,i)
        # sentence.append([li1,li2])
        # sentence.append([li3,li4])
    # # print sentence
    # return sentence

# Λ [~(Xai Λ Xbi)] -->  Λ( ~Xai V ~Xbi)
#                  -->  [[~Xa0,~Xb0],[~Xa1,~Xb1],...,[~XaN-1,~XaN-1]]
def each_enemy(num1,num2,N):
    sentence =[]
    for i in range(N):
        li1 = "~X%d#%d" % (num1,i)
        li2 = "~X%d#%d" % (num2,i)
        sentence.append([li1,li2])
    return sentence

def generate_cnf(matrix,M,N):
    cnf = []
    for i in range(M):
        cnf.extend(each_guest(i,N))
        for j in range(i+1,M):
            if i==j:
                continue
            if matrix[i][j]==1:
                cnf.extend(each_friend(i,j,N))
            else:
                if matrix[i][j]==-1:
                    cnf.extend(each_enemy(i,j,N))
    return cnf



def value_of_literal(li,matrix):
    i=0
    j=0
    value = 0
    if li.startswith('~'):
        arr = li[2:].split('#')
        i=int(arr[0])
        j=int(arr[1])
        value = 1 - matrix[i][j]
    else:
        arr = li[1:].split('#')
        i=int(arr[0])
        j=int(arr[1])
        value = matrix[i][j]
    return value

def sovle_sentence(c,matrix):
    mul = 1
    for x in c:
        if value_of_literal(x,matrix)==1:
            return True
    return False


def everyClauseTrue(clauses, model):
    length = len(clauses)
    if length==0:
        return True
    return False
    # for i in range(length):
        # if sovle_sentence(clauses[i],model)==False:
            # return False
    # return True

def someClauseFalse(clauses, model):
    length = len(clauses)
    for c in clauses:
        if c==[]:
            return True
    return False

def find_pure_symbol(symbols, clauses, model):
    for sym in symbols:
        sum1=0
        sum2=0
        for c in clauses:
            if sym in c:
                sum1+=1
            if '~'+sym in c:
                sum2+=1
        if sum1+sum2 == 0:
            symbols.remove(sym)
            continue
        if sum1==0:#only ~sym
            return sym,False,symbols
        if sum2==0:#only sym
            return sym,True,symbols
    return None,True ,symbols

def setmodel(model,P,value):
    arr = P[1:].split('#')
    i=int(arr[0])
    j=int(arr[1])
    if value==True:
        model[i][j] = 1
    else :
        model[i][j] = 0

def find_unit_clause(clauses, model):
    for c in clauses:
        if len(c)==1:
            if c[0].startswith('~'):
                return c[0][1:],False
            else:
                return c[0],True
    return None,True

def remove_clause_with_symbol(clauses,sym):
    c = deepcopy(clauses)
    for c1 in clauses:
        if sym in c1:
            # print sym,c1
            c.remove(c1)
    # print "--->",sym,c
    return c

def remove_p_from_clauses(clauses,sym):
    for c1 in clauses:
        if sym in c1:
            c1.remove(sym)
    return clauses

def apply_value(clauses,p,value):
    c = []
    if value == True:
        c = remove_clause_with_symbol(clauses,p)# remove clause contains p
        c = remove_p_from_clauses(c,'~'+p)# remove ~p from clauses
    else:
        c = remove_clause_with_symbol(clauses,'~'+p)
        c = remove_p_from_clauses(c,p)
    return c

def DPLL(clauses,symbols,model):
    if symbols==[]:
        return True
    if everyClauseTrue(clauses, model):
        return True
    if someClauseFalse(clauses, model):
        return False

    #P, value <- FIND-PURE-SYMBOL(symbols, clauses, model)
    P,value,symbols = find_pure_symbol(symbols, clauses, model)
    #if P is non-null then
    if P !=None:
        #return DPLL(clauses, symbols - P, model U {P = value})
        if value == True:
            clauses = remove_clause_with_symbol(clauses,P)
        else :
            clauses = remove_clause_with_symbol(clauses,'~'+P)
        # symbols.remove(P)
        setmodel(model,P,value)
        return DPLL(clauses,symbols,model)


    #P, value <- FIND-UNIT-CLAUSE(clauses, model)
    P,value = find_unit_clause(clauses, model)
    #if P is non-null then
    if P !=None:
        #return DPLL(clauses, symbols - P, model U {P = value})
        if value == True:
            clauses = remove_clause_with_symbol(clauses,P)
            clauses = remove_p_from_clauses(clauses,'~'+P)
        else :
            clauses = remove_clause_with_symbol(clauses,'~'+P)
            clauses = remove_p_from_clauses(clauses,P)
        # symbols.remove(P)
        setmodel(model,P,value)
        return DPLL(clauses,symbols,model)

    # P <- FIRST(symbols); rest <- REST(symbols)
    p = symbols[0]
    rest = symbols[1:]
    # return DPLL(clauses, rest, model U {P = true})
        # or DPLL(clauses, rest, model U {P = false})
    model1 = deepcopy(model)
    clauses1 = deepcopy(clauses)
    rest1 = deepcopy(rest)
    clauses1= apply_value(clauses1,p,True)
    setmodel(model1,p,True)

    model2 = deepcopy(model)
    clauses2 = deepcopy(clauses)
    rest2 = deepcopy(rest)
    setmodel(model2,p,False)
    clauses2 = apply_value(clauses2,p,False)
    return DPLL(clauses1,rest1,model1) or DPLL(clauses2,rest2,model2)

def dpllSatisfiable(cnf,M,N):

    model = []
    model = [[0]*N for i in range(M)]

    symbols=[]
    for i in range(M):
        for j in range(N):
            li = "X%d#%d" % (i,j)
            symbols.append(li)

    return DPLL(cnf,symbols,model)

def walksat_sovle(c,matrix):
    mul = 1
    for x in c:
        if value_of_literal(x,matrix)==1:
            return True
    return False

def walksat_resolve(cnf,matrix):
    length = len(cnf)
    for i in range(length):
        if walksat_sovle(cnf[i],matrix)==False:
            return False
    return True

def random_flip(matrix,p):
    for i in range(len(matrix)):
        if(random.random()>p):
            matrix[i]=[0]*len(matrix[i])
            num = int(random.random()*len(matrix[i]))
            matrix[i][num]=1
    return matrix

def WalkSAT(cnf,p,max_flips,M,N):
    matrix = []
    state = [0]*M
    matrix = [[0]*N for i in range(M)]
    for i in range(M):
        num = int(random.random()*N)
        matrix[i][num]=1
    for iter in range(max_flips):
        # print 'iter: %d'%iter,matrix

        if walksat_resolve(cnf,matrix)==True:
            return matrix
        else :
            matrix = random_flip(matrix,p)
    return matrix


def main():
    # matrix,M,N = openfile('data/input5.txt')


    matrix,M,N = openfile('input/input%d.txt'%(5))
    fw=open("output/output%d.txt"%(5),"w")
        # print matrix
    cnf = generate_cnf(matrix,M,N)
        # print cnf
    r = dpllSatisfiable(cnf,M,N)

    if r==False:
        fw.write('no')
        print 'no'
        fw.close()
        #return
    else:
        resolvent = WalkSAT(cnf,0.5,100000,M,N)
        fw.write('yes\n')
        for i in range(len(resolvent)):
            fw.write("%d %d\n" %(i+1,resolvent[i].index(1)+1))
        fw.close()


if __name__ == "__main__":
    main()
