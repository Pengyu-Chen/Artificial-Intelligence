import copy


class BayesNetwork:
    def __init__(self):
        self.node_name_list = []
        self.nodes_list = []
        self.utility_node = None

    def Addnode(self, node):
        self.nodes_list.append(node)
        self.node_name_list.append(node.m_name)

    def Getnode(self, node_name):
        index = self.node_name_list.index(node_name)
        return self.nodes_list[index]

class Query:
    def __init__(self):
        self.m_condition = []
        self.m_evidence = []
        self.m_type=""
        self.m_subtype=""

class BayesNode:
    def __init__(self):
        self.m_name =""
        self.m_parents = []
        self.m_probability = []
        self.m_type =""

    def get_p(self, symbol, current_events):
        if self.m_type == "decision": return 1.0
        for i in range(len(self.m_probability)):
            find = True
            for j in range(len(self.m_parents)):
                parent = self.m_parents[j]
                val = self.m_probability[i][j + 1]
                if current_events[parent] == val:
                    continue
                else:
                    find = False
                    break
            if find:
                if symbol == '+': return self.m_probability[i][0]
                else: return 1.0 - self.m_probability[i][0]

def ParseQuery(sentence):
    new_query=Query()
    if sentence.startswith('P') or sentence.startswith('E'):
        if sentence.startswith('P'):
            new_query.m_type='probability'
        elif sentence.startswith('E'):
            new_query.m_type='EU'
        tempsentence=sentence.split('(')[1].split(')')[0]
        if '|' in tempsentence:
            new_query.m_subtype='conditional'
            slist=tempsentence.split(' | ')[0]
            tlist=tempsentence.split(' | ')[1]
            slist1=slist.split(', ')
            tlist1=tlist.split(', ')

            for i in slist1:
                slist2=i.split(' ')


                new_query.m_condition.append((slist2[0],slist2[2]))

                # if len(slist2)>1:
                #     new_query.m_value[slist2[0]]=slist2[2]
                # else:
                #     new_query.m_value[slist2[0]]='+-'
            for i in tlist1:
                tlist2=i.split(' ')

                new_query.m_evidence.append((tlist2[0],tlist2[2]))
                # if len(tlist2)>1:
                #     new_query.m_value[tlist2[0]]=tlist2[2]
                # else:
                #     new_query.m_value[tlist2[0]]='+-'

        else:
            slist=tempsentence.split(', ')
            if len(slist)<=1:
                new_query.m_subtype='marginal'
            else:
                new_query.m_subtype='joint'
            for i in range(len(slist)):
                new_query.m_condition.append((slist[i].split(' = ')[0],slist[i].split(' = ')[1]))
                # new_query.m_value[slist[i].split(' = ')[0]]=slist[i].split(' = ')[1]



    if sentence.startswith('M'):
        new_query.m_type='MEU'
        tempsentence=sentence.split('(')[1].split(')')[0]
        if '|' in tempsentence:
            new_query.m_subtype='conditional'
        elif ',' in tempsentence:
            new_query.m_subtype='joint'
        else:
            new_query.m_subtype='marginal'
        slist=tempsentence.split(' | ')
        if len(slist)>1:
            slist1=slist[1].split(', ')
            for i in slist1:
                new_query.m_evidence.append((i.split(' = ')[0],i.split(' = ')[1]))
                # new_query.m_value[i.split(' = ')[0]]=i.split(' = ')[1]

        slist2=slist[0].split(', ')

        for i in slist2:
            new_query.m_condition.append(i)

    return new_query


def solution(query_sentence):
    new_query=ParseQuery(query_sentence)

    if new_query.m_type=='probability' and new_query.m_subtype=='conditional':

        variable = {}
        for tmp in new_query.m_condition:
            variable[tmp[0]] = tmp[1]
        evidence = {}
        for tmp in new_query.m_evidence:
            evidence[tmp[0]] = tmp[1]
        p = enumeration_ask(variable, evidence, my_bayes_net)
        return ("%.2f" % round((p + 1e-8), 2))

    elif new_query.m_type=='probability' and new_query.m_subtype!='conditional':

        variable = {}
        for tmp in new_query.m_condition:
            variable[tmp[0]] = tmp[1]
        p = enumerate_all(my_bayes_net.node_name_list, variable, my_bayes_net)
        return ("%.2f" % round((p + 1e-8), 2))

    elif new_query.m_type=='MEU':

        evi_dict = {}
        con_vars_arr = []
        if new_query.m_subtype!='marginal':
            for tmp in new_query.m_evidence:
                evi_dict[tmp[0]] = tmp[1]

        for tmp in new_query.m_condition:
            con_vars_arr.append(tmp)
        max_eu = -9999999
        max_eu_con_var_value = []
        con_var_length = len(con_vars_arr)
        for i in range(2 ** con_var_length):
            tmp_con_value_arr = []
            for p in range(con_var_length):
                if (i >> p) & 1 == 0:
                    tmp_con_value_arr.append('+')
                else:
                    tmp_con_value_arr.append('-')
            con_evi = copy.deepcopy(evi_dict)
            for j in range(con_var_length):
                con_evi[con_vars_arr[j]] = tmp_con_value_arr[j]
                utility_node = my_bayes_net.utility_node
                utility_node_parents = utility_node.m_parents
                sum_eu = 0.0
                for row in utility_node.m_probability:
                    con_dict = {}
                    for j in range(len(utility_node_parents)):
                        con_dict[utility_node_parents[j]] = row[j + 1]
                    sum_eu += enumeration_ask(con_dict, con_evi, my_bayes_net) * row[0]
                eu = sum_eu
                if (eu > max_eu):
                    max_eu = eu
                    max_eu_con_var_value = tmp_con_value_arr
        con_value, meu = max_eu_con_var_value, max_eu
        meu_line = ''
        for val in con_value:
            meu_line += val + ' '
        return(meu_line + str(int(round(meu))))


    elif new_query.m_type == 'EU':

        new_list=new_query.m_condition+new_query.m_evidence
        evidence = {}
        for content in new_list:

            evidence[content[0]] = content[1]
        utility_node = my_bayes_net.utility_node
        utility_node_parents = utility_node.m_parents
        sum_eu = 0.0
        for row in utility_node.m_probability:
            con_dict = {}
            length = len(utility_node_parents)
            for j in range(length):
                con_dict[utility_node_parents[j]] = row[j + 1]
            sum_eu += enumeration_ask(con_dict, evidence, my_bayes_net) * row[0]
        eu = sum_eu
        return(str(int(round(eu))))

def enumeration_ask(n_dict, d_dict, bn):
    for x in n_dict.keys():
        if d_dict.__contains__(x) and d_dict[x] != n_dict[x]:
                return 0.0
        elif d_dict.__contains__(x) and d_dict[x] == n_dict[x]:
                n_dict.__delitem__(x)
    index = 0
    for n in range(len(n_dict)):
        tmp = n_dict.keys()[n]
        if n_dict[tmp] == '+':
            index += 0
        else:
            index += 1 * (2 ** n);

    sum_p = 0
    for row in range(2 ** len(n_dict)):
        var_values = []
        for p in range(len(n_dict)):
            if (row >> p) & 1 == 0:
                var_values.append('+')
            else:
                var_values.append('-')
        nd_dict = copy.deepcopy(d_dict)
        for j in range(len(n_dict)):
            tmp = n_dict.keys()[j]
            nd_dict[tmp] = var_values[j]
        p1 = enumerate_all(my_bayes_net.node_name_list, nd_dict, my_bayes_net)
        if (row == index):
            n_p = p1
        sum_p = sum_p + p1

    p = n_p / sum_p
    return p


def enumerate_all(variables, e, bn):
    if not variables:
        return 1.0

    Y = variables[0]
    rest = variables[1:]
    node = bn.Getnode(Y)
    if Y not in e.keys():
        eY_ture = copy.deepcopy(e)
        eY_ture[Y] = '+'
        eY_false = copy.deepcopy(e)
        eY_false[Y] = '-'
        a = node.get_p('+', e)
        b = enumerate_all(rest, eY_ture, bn)
        c = node.get_p('-', e)
        d = enumerate_all(rest, eY_false, bn)
        ans = a * b + c * d
        return ans
    else:
        a = node.get_p(e[Y], e)
        b = enumerate_all(rest, e, bn)
        ans = a * b
        return  ans

query_list = []
def parseInput():
    fileName ="input.txt"
    fr = open(fileName,'r')


    while True:
        line=fr.readline().rstrip()
        if line == "******":
            break
        query_list.append(line)


    while True:
        line=fr.readline().rstrip()
        line_split=line.split(' ')

        parentlist= line_split[2:]
        new_node=BayesNode()
        new_node.m_name=line_split[0]

        is_decision = False

        num_parent=len(parentlist)
        if num_parent>0:
            for i in range(num_parent):
                new_node.m_parents.append(parentlist[i])


        for i in range(2 ** num_parent):
            line=fr.readline().rstrip()
            problist=line.split(' ')
            if problist[0] == 'decision':
                new_node.m_type='decision'

            elif new_node.m_name=='utility':
                problist[0] = float(problist[0])

                new_node.m_probability.append(problist)
                new_node.m_type='utility'

                my_bayes_net.utility_node = new_node

            else:
                problist[0] = float(problist[0])

                new_node.m_probability.append(problist)
                new_node.m_type="nondecision"



        line=fr.readline().rstrip()

        my_bayes_net.Addnode(new_node)
        if not line:
            break



    fr.close()



def main():
    parseInput()
    fout = open('output.txt', 'w')
    for i in query_list:
        result=solution(i)
        fout.write('%s\n'%result)
    fout.close


my_bayes_net = BayesNetwork()
if __name__ == '__main__':
    main()
