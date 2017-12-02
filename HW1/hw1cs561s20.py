from copy import deepcopy
import Queue
matrix = [[[]for i in range(8)]for i in range(8)]
matrixlist = list()


MatrixValue=[
[99,-8,8,6,6,8,-8,99],
[-8,-24,-4,-3,-3,-4,-24,-8],
[8,-4,7,4,4,7,-4,8],
[6,-3,4,0,0,4,-3,6],
[6,-3,4,0,0,4,-3,6],
[8,-4,7,4,4,7,-4,8],
[-8,-24,-4,-3,-3,-4,-24,-8],
[99,-8,8,6,6,8,-8,99]
]
fhand = open('input.txt')


#input the state
linenum=0
for line in fhand:
    line=line.rstrip()
    linenum += 1
    if linenum == 1:
        Turn = line
        #print Turn
    elif linenum ==2:
        depth = int(line)
        #print depth
    elif linenum > 2:
        t=list(line)

        matrix[linenum-3]=t

if Turn =='X':
    player =1
else:
    player=-1


for i in range(8):
    for j in range(8):
        if matrix[i][j]=='X':
            matrix[i][j]=1
        elif matrix[i][j]=='O':
            matrix[i][j]=-1
        elif matrix[i][j]=='*':
            matrix[i][j]=0



def isValid(matrix,mplay,x,y):
    valid=False


    if matrix[x][y]==0:

        for xoffset,yoffset in [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]:
            xpos,ypos = x,y

            xpos=xoffset+xpos
            ypos=yoffset+ypos
            if xpos>=0 and xpos<=7 and ypos>=0 and ypos<=7:        #print xpos,ypos
                while matrix[xpos][ypos]==-mplay:

                    xpos=xoffset+xpos
                    ypos=yoffset+ypos
                    if xpos<0 or xpos>7 or ypos<0 or ypos>7:
                        break
                    if matrix[xpos][ypos]==mplay:

                        valid=True
                        break


    return valid


def move((x,y),matrix1,mplay):

    matrixnew = [[[]for i in range(8)]for i in range(8)]
    for cc in range(8):
        for ll in range(8):
            matrixnew[cc][ll]=matrix1[cc][ll]

    for xoffset,yoffset in [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]:
        xpos,ypos = x,y
        xpos=xoffset+xpos
        ypos=yoffset+ypos
        #print xpos,ypos
        if xpos>=0 and xpos<=7 and ypos>=0 and ypos<=7:
            #print xpos,ypos
            while matrixnew[xpos][ypos]==-mplay:
                #print xpos,ypos
                xpos=xoffset+xpos
                ypos=yoffset+ypos
                #print xpos,ypos
                if xpos<0 or xpos>7 or y<0 or y>7:
                    break
                elif matrixnew[xpos][ypos]==mplay:
                    # print xpos,ypos
                    # print x,y
                    while xpos!=x or ypos!=y:
                        #print xpos,ypos
                        xpos=xpos-xoffset
                        ypos=ypos-yoffset
                        matrixnew[xpos][ypos]=mplay
                        #print matrix[xpos][ypos]

                #elif matrix[xpos][ypos]=='X':

    return matrixnew
printlist=list()
printlist.append(["Node","Depth","Value","Alpha","Beta"])
printlist.append(["root",0,"-Infinity","-Infinity","Infinity"])
passnum=0
def ABDecision(x, y, mState, mCell, mPlay , mLevel, mDepth, max, min):

    bmin = min
    bmax = max
    passgame=True
    global passnum
    int(passnum)
    choiceValue = []
    #print '?', y+1, x+1, mLevel, "alpha", bmax, "beta", bmin
    score_queue = Queue.Queue()
    for i in range(0, 8):
        for j in range(0, 8):
            if isValid(mState,mPlay,i,j):
                passgame=False
                passnum=0
                tmpState = deepcopy(mState)
                #tmpState[i][j] = mPlay
                tmpState=deepcopy(move((i,j),mState,mPlay))
                score_queue.put([-mCell[i][j], i, j, tmpState])
                #print j + 1, i + 1
    if passgame==True:
        tmpState=deepcopy(mState)
        score_queue.put([-mCell[i][j], -2, -2, tmpState])
        passnum=passnum+1


    fvalue = float("inf")
    if mLevel%2 == 0:
        fvalue = -fvalue
    while score_queue.empty() is False:
        tmp = score_queue.get()
        newState = deepcopy(tmp[3])


        if mLevel != mDepth:
            if (mLevel + 1)%2 == 0:
                if tmp[1]==-2 and tmp[2]==-2:
                    printlist.append([ "pass", mLevel + 1, -float("inf"), bmax, bmin])
                else:
                    printlist.append([chr(tmp[2]+97)+str(tmp[1]+1), mLevel + 1, bmax, bmax, bmin])

            if (mLevel + 1)%2 == 1:
                if tmp[1]==-2 and tmp[2]==-2:
                    printlist.append(["pass", mLevel + 1, float("inf"),  bmax, bmin])
                else:
                    printlist.append([chr(tmp[2]+97)+str(tmp[1]+1), mLevel + 1, bmin,  bmax,  bmin])

        if passnum>=2:
            score= ABcalculateScore(-3, -3, newState, mCell, mPlay, mLevel, mDepth, bmax, bmin)
            print score


        score = ABcalculateScore(tmp[1], tmp[2], newState, mCell, mPlay, mLevel, mDepth, bmax, bmin)
        print score

        if mLevel == mDepth:
            if tmp[1]==-2 and tmp[2]==-2:
                printlist.append(["pass", mLevel + 1, score, bmax, bmin])
            else:
                printlist.append([chr(tmp[2]+97)+str(tmp[1]+1), mLevel + 1,score,bmax, bmin])

        #print tmp[2]+1, tmp[1]+1, score;
        if (mLevel + 1)%2 == 0:
            if score < bmin and score > max:
                bmin = score
        if (mLevel + 1) % 2 == 1:
            if score > bmax and score < min:
                bmax = score


        if (mLevel) % 2 == 0:
            if score > fvalue:
                fvalue = score
            if x==-2 and y==-2:
                printlist.append(["pass", mLevel, fvalue,  bmax, bmin])
            else:
                printlist.append([chr(y+97)+str(x+1), mLevel, fvalue,  bmax, bmin])
        if (mLevel) % 2 == 1:
            if score < fvalue:
                fvalue = score
            if x==-2 and y==-2:
                printlist.append(["pass", mLevel, fvalue, bmax, bmin])
            else:
                printlist.append([chr(y+97)+str(x+1), mLevel, fvalue, bmax, bmin])

        choiceValue.append([score, newState, tmp[1], tmp[2]])
        if (mLevel + 1) % 2 == 0:

            if score <= max:
                return choiceValue
        else:
            if score >= min:
                return choiceValue

    if len(choiceValue) == 0:
        score = ABcalculateScore(mState, mCell, mPlay, mLevel, mDepth, bmax, bmin)
        choiceValue.append([score, mState, -1, -1])
    return choiceValue


def ABcalculateScore(tmp1, tmp2, cnewState, cmCell, cmPlay, cmLevel, cmDepth, max, min):


    if cmLevel == cmDepth:

        totalScore = 0
        for i in range(0, 8):
            for j in range(0, 8):
                totalScore = totalScore + cnewState[i][j]*cmCell[i][j]


                #print totalScore
        return totalScore
    else:

        choice = ABDecision(tmp1, tmp2, cnewState, cmCell, -cmPlay, cmLevel + 1, cmDepth, max, min)
        tmax = -float("inf")
        tmin = float("inf")
        for i in range(0, len(choice)):
            #print choice
            if choice[i][0] > tmax:
                tmax = choice[i][0]
            if choice[i][0] < tmin:
                tmin = choice[i][0]
        #print choice[0][0], max, min, cmLevel
        #print "!!!", tmp1, tmp1, cmLevel
        if (cmLevel + 1)%2 == 1:
            return tmin
        else:
            return tmax

#print ABDecision(matrix,MatrixValue,8,player,0,depth-2,-1000,1000)

ablist=list()
ablist=ABDecision(-1, -1, matrix,MatrixValue,player,0,depth-1,-float("inf"), float("inf"))
fout = open('output.txt', 'w')


maxm=ablist[0][0]
maxpos=0
for i in range(len(ablist)-1):
    if ablist[i+1][0]>maxm:
        maxm=ablist[i+1][0]
        maxpos=i+1


printmatrix=deepcopy(ablist[maxpos][1])

for i in range(8):
    for j in range(8):
        if printmatrix[i][j]==1:
            printmatrix[i][j]="X"
        elif printmatrix[i][j]==-1:
            printmatrix[i][j]="O"
        elif printmatrix[i][j]==0:
            printmatrix[i][j]="*"
for i in range(8):

    line=str(printmatrix[i][0]+printmatrix[i][1]+printmatrix[i][2]+printmatrix[i][3]+printmatrix[i][4]+printmatrix[i][5]+printmatrix[i][6]+printmatrix[i][7]+"\n")
    fout.write(line)

for a in range(0,len(printlist)):
    if printlist[a][0]=='`0':
        printlist[a][0]='root'
    for i in range(3):
        if printlist[a][i+2]==float("inf"):
            printlist[a][i+2]="Infinity"
        if printlist[a][i+2]==-float("inf"):
            printlist[a][i+2]="-Infinity"
    fout.write("%s,%s,%s,%s,%s\n"%(printlist[a][0],printlist[a][1],printlist[a][2],printlist[a][3],printlist[a][4]))


fout.close()

'''for aaa in range(len(printlist)):
    print printlist[aaa][0]
    for i in range(8):
        print printlist[aaa][1][i]
    print printlist[aaa][2]
    print printlist[aaa][3]
    print ''
'''
