'''
                    ASSIGNMENT : PROGRAM TO PRINT PLA TABLE
                                                                                    MD ATEEB SIDDIQUI
                                                                                    GK-9138
                                                                                    18-COB-110
                                                                                    COC2070
                                                                                    ROLL NO 36
'''
class POS:
    
    def __init__(self):
        
        self.isPOS = True
        self.elements = set()
    
    def LiteralWeight(self):
        w = 0
        for e in self.elements:
            w += e.count_nonhyphen()
        return w 

    def at_(self):
        if not self.isPOS:
            print("Can't distribute non product of sum term!")
            return
        if len(self.elements) <= 1:
            print("Can't distribute one term!")

        first = self.elements.pop()
        second = self.elements.pop()
        second._cross_(first)
        self.elements.add(second)
        

    def do_it(self):
        return len(self.elements) > 1 and self.isPOS

    def s__k(self):
        while len(self.elements) > 1:
            self.at_()
        return self.elements.pop()
    
    def t_e(self):
        ha = 0
        for m in self.elements:
            ha ^= m.f_c_()
        return ha
        
    def a_t(self, other):
       return self.elements <= other.elements

class SOP:
    isSOP = True
    elements = set()

    def __init__(self):
        self.isSOP = True
        self.elements = set()

    def _cross_(self, other):
        self._conv_()
        other._conv_()
        
        s = set()
        while len(self.elements) > 0:
            myProd = self.elements.pop()
            for otherProduct in other.elements:
                newProd = POS()
                newProd.elements.update(myProd.elements)
                newProd.elements.update(otherProduct.elements)
                s.add(newProd)
        
        self.elements = s

    def _conv_(self):
        if self.isSOP:
            return
        Element = set()
        while len(self.elements) > 0:
            p = POS()
            elem = self.elements.pop()
            p.elements.add(elem)
            Element.add(p)
        self.elements = Element
        self.isSOP = True

    def p__g(self):
        if self.isSOP:
            Set = set()
            old = self.elements.copy()
           
            while len(old) > 0:
                elem = old.pop()
                for pr in self.elements:
                    if elem.elements <= pr.elements:
                        if pr in old:
                            old.remove(pr)
                        if pr in Set:
                            Set.remove(pr)
                Set.add(elem)
            self.elements = Set 


    def t_e(self):
        ash = 0
        for l in self.elements:
            ash ^= l.t_e()
        return ash

    def a_t(self, other):
       return self.elements <= other.elements
class Implicant:
    
    brep = ""
    
    
    order = 0

    
    terms = []

    def __init__(self, bsize, terms, imp1 = None, imp2 = None):
      
        self.brep = ""
        self.order = 0
        self.terms = []

        if imp1 == None and imp2 == None:
            self.brep = bin(terms[0])[2:]
            if len(self.brep) != bsize:
                while len(self.brep) < bsize:
                    self.brep = "0" + self.brep
                
            self.terms = terms
        else:
            if imp1 == None or imp2 == None:
                print("Error: An implicant is uninitialized!")                       #Prints Error message
            else:
                if imp1.order != imp2.order:
                    print("Error: 2 implicants of varying order were provided!")     #Prints Error message
                else:
                    d = 0
                    self.order = imp1.order + 1
                    self.terms = list(imp1.terms + imp2.terms)
                    for i in range(0, bsize):
                        if imp1.brep[i] != imp2.brep[i]:
                            self.brep = self.brep + "-"
                            d += 1
                        else:
                            self.brep = self.brep + imp1.brep[i]
                    if d > 1:
                        print("Error: Implicants had distance greater than 1!")      #Prints Error message

    def count_dig(self):
        
        
         
        
        N = 0
        for c in self.brep:
            if c == '1':
                N += 1
        return N
    
    def count_nonhyphen(self):
        
        
        
        a = 0
        for c in self.brep:
            if c != "-":
                a += 1
        return a

    def count_d(self, nexterm):
        
        
        
        gb = 0
        for i in range(0, len(self.brep)):
            if(self.brep[i] != nexterm.brep[i]):
                gb += 1
        return gb
    
    def count_imp(self, lstr):
        
        
        istr = ""
        for index, c in enumerate(self.brep):
            if c == "0":
                istr += lstr[index] + "'"
            elif c == "1":
                istr += lstr[index]
        return istr
    
    def a_t(self, next):
        if next == None:
            return False
        return self.brep == next.brep

    def t_e(self):
        return self.brep()

def _Enter_(minterms):
    
    pimp = set()
    cimp = set()
    nextimp = set(minterms)
    combination = dict()

    while len(nextimp) > 0:
        cimp = nextimp
        nextimp = set()
        
        for i in cimp:
            combination[i] = False
        
        while len(cimp) > 0:
            currentImplicant = cimp.pop() 
            for implicant in cimp:
                if currentImplicant.count_d(implicant) <= 1:
                    combination[implicant] = True
                    combination[currentImplicant] = True
                    nextimp.add(Implicant(len(currentImplicant.brep), [], currentImplicant, implicant))
            
            if not combination[currentImplicant]:
                
                pimp.add(currentImplicant)

    return list(pimp)

def my_way(num):
   
    p = POS()
    p.isPOS = True
    
    for key, value in num.items():
        sum = SOP()
        sum.isSOP = False
        sum.elements.update(set(value))
        p.elements.add(sum)
    
    
    sum = p.s__k()
    if not sum.isSOP:
        sum._conv_()
    sum.p__g()

    
    pos = list(sum.elements)
    pos.sort(key = lambda x: len(x.elements))
    lowest = len(pos[0].elements)

    pos = list(filter(lambda x: len(x.elements) <= lowest, pos))
    
    pos.sort(key = lambda x: x.LiteralWeight())
    minWeight = pos[0].LiteralWeight()
    pos = list(filter(lambda x: x.LiteralWeight() == minWeight, pos))

    pos = list(map(lambda x: x.elements, pos))

    return pos

def _input_(var_num):
    class enter:
        POLLSTATE, MINTERMS, MAXTERMS, EQUATION = range(4)

    state = enter.POLLSTATE
    
    
    while True:
        if state == enter.POLLSTATE:
            print("Enter the way in which you want to give input :")
            print("Type'SIGMA' for SIGMA NOTATION  */*/*/*/*/*/* Type 'PI' for PI NOTATION ")
            value = input()
            if value.strip().lower() == "sigma":
                state = enter.MINTERMS
            elif value.strip().lower() == "pi":
                state = enter.MAXTERMS
    
        elif state == enter.MINTERMS:
            print("Enter",var_num ," variables as a space seperated list in the form of X Y Z and so on:")
            varInput = input()
            var = list(map(lambda x: x.strip(), varInput.split(" ")))
            mintermsInput = input("Enter MINTERMS in form of list of numbers i.e. space seperated list :")
            m = list(list(map(lambda x: int(x.strip()), mintermsInput.split(" "))))
            miin = []
            for i in range(2**len(var)):
                if i not in m:
                    miin.append(i)
    
            return (var, m, miin)
                
        elif state == enter.MAXTERMS:
            print("Enter",var_num ," variables as a space seperated list in the form of X Y Z and so on:")
            varInput = input()
            var = list(map(lambda x: x.strip(), varInput.split(" ")))
                
            mintermsInput = input("Enter MINTERMS in form of list of numbers i.e. space seperated list :")
            maxterms = list(list(map(lambda x: int(x.strip()), mintermsInput.split(" "))))
            miin = list(list(map(lambda x: int(x.strip()), mintermsInput.split(" "))))
            m = []
            for i in range(2**len(var)):
                if i not in maxterms:
                    m.append(i)
    
            return (var, m, miin)
        else:
            print("Unkown or bad state!")
            exit()
    def _VAR():
        obj1=enter()
        zy=obj1.zx
        return zy
    
def dist_str(strg): 
    
    l_string = strg.split('+')  
    return l_string 

def main():
    
    
    funct_num=int(input("Enter 'n' as number of functions you want to enter --:"))   
    var_num=int(input("Enter 'm' as number of variables you want to enter --:"))     
    
    l1,l2,l3,l4,l5,l6,l7,l8,l9,l10,l11,war_set,firedlist = [],[],[],[],[],[],[],[],[],[],[],[],[]
    s1={}
    s2={}
    
    for f in range(funct_num):
        tuple = _input_(var_num)       
        bsize = len(tuple[0])
        strep = tuple[0]
        m = tuple[1]
        miin = tuple[2]
        imp = []
        impin = []
        for t in m:
            imp.append(Implicant(bsize, [t]))
        for termin in miin:
            impin.append(Implicant(bsize, [termin]))
    
        primeImplicants = _Enter_(imp)
        primeImplicantsin = _Enter_(impin)
        
        ch = dict()
        for term in m:
            column = []
            for i in primeImplicants:
                if term in i.terms:
                    column.append(i)
            ch[term] = column
        chin = dict()
        for termin in miin:
            columnin = []
            for im in primeImplicantsin:
                if termin in im.terms:
                    columnin.append(im)
            chin[termin] = columnin
    
        
        epi = set()
        ch2 = dict()
        epin = set()
        ch2in = dict()
    
        for term, column in ch.items():
            if len(column) == 1:
                epi.add(column[0])
            else:
                ch2[term] = column
        ch = ch2

        for termin, columnin in chin.items():
            if len(columnin) == 1:
                epin.add(columnin[0])
            else:
                ch2in[termin] = columnin
        chin = ch2in
    
        
        for implicant in epi:
            for term in implicant.terms:
                if term in ch:
                    del ch[term]
        for implicantin in epin:
            for termin in implicantin.terms:
                if termin in chin:
                    del chin[termin]
            
        def _conversion_(x):
                t=''
                for imp in x: 
                    t += imp.count_imp(strep) + " + "
                return t[0:-3]
        possibleAdditionStrings = [""]
        if len(ch) != 0:
           
            possibleAdditions = my_way(ch)
            
            possibleAdditionStrings = list(map(_conversion_, possibleAdditions))  
        possibleAdditionStringsin =[""]
        if len(chin) != 0:
            
            possibleAdditionsin = my_way(chin)
            
            possibleAdditionStringsin = list(map(_conversion_, possibleAdditionsin))
     
        essentialPrimeImplicantsString = _conversion_(epi)
        curr_minimization=[]
        essentialPrimeImplicantsStringin = _conversion_(epin)
        curr_minimizationin=[]
        
        
        print("\n")
        print("F",f+1,':')
        for string in possibleAdditionStrings:
            if string != "":
                if essentialPrimeImplicantsString != "":
                    print(essentialPrimeImplicantsString + " + " + string)
                    curr_minimization.append(essentialPrimeImplicantsString + " + " + string)
                    l1.append(essentialPrimeImplicantsString + " + " + string)
                    
                else:
                    print(string)
                    curr_minimization.append(string)
                    l1.append(string)
            else:
                print(essentialPrimeImplicantsString)
                curr_minimization.append(essentialPrimeImplicantsString)
                l1.append(essentialPrimeImplicantsString)
            break
        print("\n\n")
        print("F",f+1,"'",':')
        for stringin in possibleAdditionStringsin:
            if stringin != "":
                if essentialPrimeImplicantsStringin != "":
                    print(essentialPrimeImplicantsStringin + " + " + stringin)
                    curr_minimizationin.append(essentialPrimeImplicantsStringin + " + " + stringin)
                    l2.append(essentialPrimeImplicantsStringin + " + " + stringin)
                    
                else:
                    print(stringin)
                    curr_minimizationin.append(stringin)
                    l2.append(stringin)
            else:
                print(essentialPrimeImplicantsStringin)
                curr_minimizationin.append(essentialPrimeImplicantsStringin)
                l2.append(essentialPrimeImplicantsStringin)
            break

        strspl2=curr_minimization[0]
        split_list=dist_str(strspl2)  
        
        strspl2in=curr_minimizationin[0]
        split_listin=dist_str(strspl2in)
        set_list=[]
        setcm=set(curr_minimization)     
        
        set_listin=[]
        setcmin=set(curr_minimizationin)
        for setval in setcm:
            set_list.append(setval)
        for setvalin in setcmin:
            set_listin.append(setvalin) 
        strip=[]
       
        if f==funct_num-1:
            for val in range(len(l1)):
                sr=l1[val]
                listtemp=list(sr.split('+'))
                for value in range(len(listtemp)):
                    l3.append(listtemp[value])
            for vb in range(len(l3)):
                strip.append(str(l3[vb].strip()))
                
        s1=set(strip)
        l5.append('[%s]' % ', '.join(map(str, s1)))
        l8.append(split_list)
        strip_listin=[]
        
        if f==funct_num-1:
            for valin in range(len(l2)):
                srin=l2[valin]
                listtempin=list(srin.split('+'))
                for valuein in range(len(listtempin)):
                    l4.append(listtempin[valuein])
            for vbin in range(len(l4)):
                strip_listin.append(str(l4[vbin].strip()))
                
        s2=set(strip_listin)
        l6.append('[%s]' % ', '.join(map(str, s2)))
        l9.append(split_listin)
        if f==funct_num-1:
            for val in range(len(l8)):
                srls=list(l8[val])
                sr=[]
                lcset={}
                for value in range(len(srls)):
                    sr.append(str(srls[value].strip()))
                lcset=set(sr)
                l10.append(lcset)
            for val2 in range(len(l9)):
                srls2=list(l9[val2])
                sr2=[]
                lcset2={}
                for value2 in range(len(srls2)):
                    sr2.append(str(srls2[value2].strip()))
                lcset2=set(sr2)
                l11.append(lcset2)
    for setval in s1:                 
        l7.append(setval)
    
    zit=[]
    for z in range (len(l10)):
        zit.append([])
        zit[z]=[l10[z],l11[z]]
    if funct_num==2:
        tlist=[]
        for a in range(len(zit)):
            for b in range(2):
                tlist.append(set(zit[0][a].union(zit[1][b])))
                
        ct=len(tlist[0])
        templist=[tlist[0]]
        for zc in range(1,len(tlist)):
            if ct>len(tlist[zc]):
                templist=list(tlist[zc])
                ct=len(tlist)
    if funct_num>=3:
        tlist=[]
        for a in range(2):
            for b in range(2):
                for c in range(2):
                    tlist.append(set(zit[0][a].union(zit[1][b],zit[2][c])))
                
        ct=len(tlist[0])
        templist=[tlist[0]]
        for zc in range(1,len(tlist)):
            if ct>len(tlist[zc]):
                templist=list(tlist[zc])
                ct=len(tlist)
        
    if(type(tlist[0]) is set):
        templist=list(templist[0])
                
    fl=[]
    for p in templist:
        fl.append([])
        for q in range (len(l10)):
            if p in l10[q]:
                fl.append(list(l10[q]))
            if p in l11[q]:
                fl.append(list(l11[q]))
    oz = [x for x in fl if x]
    fsetl=[]
    for z in oz:
        fsetl.append([])
        if z in fsetl:
            pi=0
            pi+=1
        else:
            fsetl.append(z)
    ozls = [x for x in fsetl if x]
        
    war_set=list(map(chr, range(65, 65+var_num)))      
    
    for qq in range (funct_num):
        firedlist.append('F'+str(qq+1))               
        
    reg=[]
    for vb in range(len(ozls)):
        reg.append([])
        for fg in range(len(ozls[vb])):
            reg[vb].append(str(ozls[vb][fg].strip()))
            
    
    ui=[]
    for qe in range(len(templist)):
        for qr in range(len(reg)):
            ui.append([])
            if templist[qe] in reg[qr]:
                ui[qe].append(1)
            else:
                ui[qe].append('-')            
    output_list = [x for x in ui if x]
    
    
    c=0
    input_list=[]
    for cc in range(len(templist)):
        input_list.append(['-']*(len(war_set)))
    for cc in range(len(templist)):
        j=0
        while(j<len(templist[cc])):
            for c in range(len(war_set)):
                if templist[cc][j]==war_set[c]:
                    if (j+1)<len(templist[cc]):
                        if(templist[cc][j+1]=="'"):
                            input_list[cc][c]=0
                            j+=1
                        else:
                            input_list[cc][c]=1
                    else:
                        input_list[cc][c]=1
            j+=1
       
    print('\n\n\n')
    print('FINALISED PLA TABLE --:')
    print('\n')
    print('Product Terms        Inputs          Outputs')                
    print('                     ',*war_set,'         ',*firedlist)
    for pterm in range(len(templist)):                                          
        print(templist[pterm],' '*(20-len(templist[pterm])),*input_list[pterm],'          ',*output_list[pterm])         
             
if __name__ == '__main__':
    main()