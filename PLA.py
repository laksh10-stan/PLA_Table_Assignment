# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 22:44:06 2019
Created on Spyder IDE (Version 3.0)
Written for Python 3.6
"""
#Task Required: Implement a method to print the Program Table for Programmable Logic Array(PLA) with n functions and m variables.
"""
Author Details:
Name: Lakshmendra Singh
Class: BTech (Computer Engineering) 2nd Year 
Class Sr. No.: 60
Faculty No: 18 COB 523 
Enrolment No: GI 7220
"""
'''
NOTE: This program is intended for Mid-Semester Assignment for the Autumn Semester of 2019-20 session.
Couse No.: COC 2070
Course Name: Digital Logic and System Design
Instructor: Prof. M.M. Sufyan Beg
'''
'''
This program uses the Quine-McCluskey algorithm with Petrick's method to find the minimum sum of products solutions.
'''
class Implicant:
    #Represents a single Implicant
    binrep = ""
    
    #Tells what "size" the prime implicant is.
    order = 0

    #Minterms that said implicants are made up of.
    terms = []

    def __init__(self, binrepsize, terms, implicant1 = None, implicant2 = None):
        '''
        An implicant of order n is made of 2 implicants of order n-1, except for order 0 implicants,
        which are simply just a single term. Terms may be an empty list if 2 implicants are provided.
        '''
        self.binrep = ""
        self.order = 0
        self.terms = []

        if implicant1 == None and implicant2 == None:
            self.binrep = bin(terms[0])[2:]
            if len(self.binrep) != binrepsize:
                while len(self.binrep) < binrepsize:
                    self.binrep = "0" + self.binrep
                
            self.terms = terms
        else:
            if implicant1 == None or implicant2 == None:
                print("Error: An implicant is uninitialized!")                       #Prints Error message
            else:
                if implicant1.order != implicant2.order:
                    print("Error: 2 implicants of varying order were provided!")     #Prints Error message
                else:
                    distance = 0
                    self.order = implicant1.order + 1
                    self.terms = list(implicant1.terms + implicant2.terms)
                    for i in range(0, binrepsize):
                        if implicant1.binrep[i] != implicant2.binrep[i]:
                            self.binrep = self.binrep + "-"
                            distance += 1
                        else:
                            self.binrep = self.binrep + implicant1.binrep[i]
                    if distance > 1:
                        print("Error: Implicants had distance greater than 1!")      #Prints Error message

    def getWeight(self):
        '''
        Basically, just gets the number of 1's in the binary representation of
        said term. 
        '''
        numOnes = 0
        for c in self.binrep:
            if c == '1':
                numOnes += 1
        return numOnes
    
    def getHyphenWeight(self):
        '''
        Returns the number of non-hyphen characters in the binary representation
        '''
        weight = 0
        for c in self.binrep:
            if c != "-":
                weight += 1
        return weight

    def getDistance(self, otherTerm):
        '''
        Gets the number of different places in the 2 terms.
        '''
        difference = 0
        for i in range(0, len(self.binrep)):
            if(self.binrep[i] != otherTerm.binrep[i]):
                difference += 1
        return difference
    
    def GetAsString(self, literalStrings):
        '''
        Gets the implicant as a string, using the list
        of strings literalStrings as the literals
        '''
        implicantString = ""
        for index, c in enumerate(self.binrep):
            if c == "0":
                implicantString += literalStrings[index] + "'"
            elif c == "1":
                implicantString += literalStrings[index]
        return implicantString
    
    def __eq__(self, other):
        if other == None:
            return False
        return self.binrep == other.binrep

    def __hash__(self):
        return self.binrep.__hash__()

class Product:
    
    def __init__(self):
        #Marks whether this is a product of sums or not.
        self.isPOS = True
        self.elements = set()
    
    def LiteralWeight(self):
        weight = 0
        for elem in self.elements:
            weight += elem.getHyphenWeight()
        return weight 

    def Distribute(self):
        if not self.isPOS:
            print("Can't distribute non product of sum term!")
            return
        if len(self.elements) <= 1:
            print("Can't distribute one term!")

        first = self.elements.pop()
        second = self.elements.pop()
        second.Multiply(first)
        self.elements.add(second)
        

    def CanDistribute(self):
        return len(self.elements) > 1 and self.isPOS

    def GetAsSum(self):
        while len(self.elements) > 1:
            self.Distribute()
        return self.elements.pop()
    
    def __hash__(self):
        hash = 0
        for elem in self.elements:
            hash ^= elem.__hash__()
        return hash
        
    def __eq__(self, other):
       return self.elements <= other.elements

class Sum:
    #marks whether this is a sum of products or not
    isSOP = True
    elements = set()

    def __init__(self):
        self.isSOP = True
        self.elements = set()

    def Multiply(self, other):
        self.TransformToSOP()
        other.TransformToSOP()
        
        newElems = set()
        while len(self.elements) > 0:
            myProd = self.elements.pop()
            for otherProduct in other.elements:
                newProd = Product()
                newProd.elements.update(myProd.elements)
                newProd.elements.update(otherProduct.elements)
                newElems.add(newProd)
        
        self.elements = newElems

    def TransformToSOP(self):
        if self.isSOP:
            return
        newElements = set()
        while len(self.elements) > 0:
            prod = Product()
            elem = self.elements.pop()
            prod.elements.add(elem)
            newElements.add(prod)
        self.elements = newElements
        self.isSOP = True

    def ApplyCovering(self):
        if self.isSOP:
            newSet = set()
            oldSet = self.elements.copy()
            '''
            Works because if there was a better (minimal) elem before it,
            It will already be removed, and therefore there is a contradiciton.
            '''
            while len(oldSet) > 0:
                elem = oldSet.pop()
                for prod in self.elements:
                    if elem.elements <= prod.elements:
                        if prod in oldSet:
                            oldSet.remove(prod)
                        if prod in newSet:
                            newSet.remove(prod)
                newSet.add(elem)
            self.elements = newSet 


    def __hash__(self):
        hash = 0
        for elem in self.elements:
            hash ^= elem.__hash__()
        return hash

    def __eq__(self, other):
       return self.elements <= other.elements

def GetPrimeImplicants(minterms):
    '''
    Takes in the minterms, which is a list of order 0 implicants, and returns a list of
    prime implicants of varying orders.
    '''
    primeImplicants = set()
    curImplicants = set()
    nextImplicants = set(minterms)
    combined = dict()

    while len(nextImplicants) > 0:
        curImplicants = nextImplicants
        nextImplicants = set()
        
        for implicant in curImplicants:
            combined[implicant] = False
        #Sort by weight, since 2 implicants can only be combined when the distance between them is 1 
        while len(curImplicants) > 0:
            currentImplicant = curImplicants.pop() 
            for implicant in curImplicants:
                if currentImplicant.getDistance(implicant) <= 1:
                    combined[implicant] = True
                    combined[currentImplicant] = True
                    nextImplicants.add(Implicant(len(currentImplicant.binrep), [], currentImplicant, implicant))
            
            if not combined[currentImplicant]:
                #The implicant couldn't be further combined, this it is a prime implicant, though maybe not essential
                primeImplicants.add(currentImplicant)

    return list(primeImplicants)

def PetricksMethod(columnDict):
    '''
        Takes in a dictionary with keys being variables not covered by essential prime implicants, 
        and values being the list of implicants which satisfy the midterm.
    '''
    # Create a sum for each column, and take the product.
    # We do this to generate a function that returns true if 
    # the implicants chosen cover the remainder of the function
    prod = Product()
    prod.isPOS = True
    
    for key, value in columnDict.items():
        sum = Sum()
        sum.isSOP = False
        sum.elements.update(set(value))
        prod.elements.add(sum)
    
    #We have a Product of sums, now we transform it into a sum of products
    sum = prod.GetAsSum()
    if not sum.isSOP:
        sum.TransformToSOP()
    sum.ApplyCovering()

    #Now we can sort by the number of terms
    possibilities = list(sum.elements)
    possibilities.sort(key = lambda x: len(x.elements))
    lowest = len(possibilities[0].elements)
    #and filter out elements larger than the smallest value
    possibilities = list(filter(lambda x: len(x.elements) <= lowest, possibilities))
    # Now, we need the possibilites with the lowest amount of literals.
    possibilities.sort(key = lambda x: x.LiteralWeight())
    minWeight = possibilities[0].LiteralWeight()
    possibilities = list(filter(lambda x: x.LiteralWeight() == minWeight, possibilities))

    possibilities = list(map(lambda x: x.elements, possibilities))

    return possibilities

def menu(var_num):
    class MenuState:
        POLLSTATE, MINTERMS, MAXTERMS, EQUATION = range(4)
    '''
    Runs a menu that asks the user for input.
    returns a 3-tuple, in the following order:
    A list of strings used to represent variables
    a list of minterms corresponding to function (F)
    a list of minterms corresponding to function inverse (F')
    '''
    state = MenuState.POLLSTATE
    
    #The Pollstate method facilitates more robust input.
    while True:
        if state == MenuState.POLLSTATE:
            print("Enter a method to input your logic function:")
            print("minterms: enter the number of each minterm (sigma shorthand notation)\nmaxterms: enter the number of each maxterm (pi shorthand notation)")
            value = input()
            if value.strip().lower() == "minterms":
                state = MenuState.MINTERMS
            elif value.strip().lower() == "maxterms":
                state = MenuState.MAXTERMS
    
        elif state == MenuState.MINTERMS:
            print("Enter your ",var_num ," variables as a space seperated list in the form of A B C D  and so on:")
            varInput = input()
            variables = list(map(lambda x: x.strip(), varInput.split(" ")))
            mintermsInput = input("Enter the numbers corresponding to each minterm as a space seperated list:")
            minterms = list(list(map(lambda x: int(x.strip()), mintermsInput.split(" "))))
            mintermsin = []
            for i in range(2**len(variables)):
                if i not in minterms:
                    mintermsin.append(i)
    
            return (variables, minterms, mintermsin)
                
        elif state == MenuState.MAXTERMS:
            print("Enter your ",var_num, " variables as a space seperated list in the form of A B C D  and so on:")
            varInput = input()
            variables = list(map(lambda x: x.strip(), varInput.split(" ")))
                
            mintermsInput = input("Enter the numbers corresponding to each maxterm as a space seperated list:")
            maxterms = list(list(map(lambda x: int(x.strip()), mintermsInput.split(" "))))
            mintermsin = list(list(map(lambda x: int(x.strip()), mintermsInput.split(" "))))
            minterms = []
            for i in range(2**len(variables)):
                if i not in maxterms:
                    minterms.append(i)
    
            return (variables, minterms, mintermsin)
        else:
            print("Unkown or bad state!")           #Prints Error message
            exit()
    def varname():
        obj1=MenuState()
        zy=obj1.zx
        return zy
    
def split_string(string): 
    # Split the string based on space delimiter 
    list_string = string.split('+')  
    return list_string 

def main():
    all_minimizations=[]
    all_minimizationsin=[]
    prod_term_str=[]
    prod_term_strin=[]
    set_prod_terms={}
    set_prod_termsin={}
    sl_curr=[]
    sl_currin=[]
    sl=[]
    varlist=[]
    functlist=[]
    ol=[]
    olin=[]
    olstrp=[]
    olstrpin=[]
    
    funct_num=int(input('Enter the no. of functions(n): '))   #Takes user input as the No. of functions (n)
    var_num=int(input('Enter the no. of variables(m): '))     #Takes user input as the No. of variables (m)
    
    for f in range(funct_num):
        tuple = menu(var_num)       #Returns a tuple from the menu method
        binrepsize = len(tuple[0])
        stringrep = tuple[0]
        minterms = tuple[1]
        mintermsin = tuple[2]
        implicants = []
        implicantsin = []
        for term in minterms:
            implicants.append(Implicant(binrepsize, [term]))
        for termin in mintermsin:
            implicantsin.append(Implicant(binrepsize, [termin]))
    
        primeImplicants = GetPrimeImplicants(implicants)
        primeImplicantsin = GetPrimeImplicants(implicantsin)
        #Here we build the chart, in a column major sort of fashion, using a dictionary, where the keys are the minterms
        chart = dict()
        for term in minterms:
            column = []
            for implicant in primeImplicants:
                if term in implicant.terms:
                    column.append(implicant)
            chart[term] = column
        chartin = dict()
        for termin in mintermsin:
            columnin = []
            for implicantin in primeImplicantsin:
                if termin in implicantin.terms:
                    columnin.append(implicantin)
            chartin[termin] = columnin
    
        #extracting essential prime implicants
        essentialPrimeImplicants = set()
        chart2 = dict()
        essentialPrimeImplicantsin = set()
        chart2in = dict()
    
        for term, column in chart.items():
            if len(column) == 1:
                essentialPrimeImplicants.add(column[0])
            else:
                chart2[term] = column
        chart = chart2

        for termin, columnin in chartin.items():
            if len(columnin) == 1:
                essentialPrimeImplicantsin.add(columnin[0])
            else:
                chart2in[termin] = columnin
        chartin = chart2in
    
        #remove all terms covered by prime implicants
        for implicant in essentialPrimeImplicants:
            for term in implicant.terms:
                if term in chart:
                    del chart[term]
        for implicantin in essentialPrimeImplicantsin:
            for termin in implicantin.terms:
                if termin in chartin:
                    del chartin[termin]
        #Now, we have our essential prime implicants.

        def MapImplicationsToString(x):
                total=''
                for implicant in x: 
                    total += implicant.GetAsString(stringrep) + " + "
                return total[0:-3]
        possibleAdditionStrings = [""]
        if len(chart) != 0:
            #essential implicants don't cover, Petrick's method must be used.
            possibleAdditions = PetricksMethod(chart)
            #Convert to strings
            possibleAdditionStrings = list(map(MapImplicationsToString, possibleAdditions))  
        possibleAdditionStringsin =[""]
        if len(chartin) != 0:
            #essential implicants don't cover, Petrick's method must be used.
            possibleAdditionsin = PetricksMethod(chartin)
            #Convert to strings
            possibleAdditionStringsin = list(map(MapImplicationsToString, possibleAdditionsin))
        '''
        print("Static hazard free implementation of function",f+1,':')
        print(MapImplicationsToString(primeImplicants))
        print("Static hazard free implementation of function'",f+1,':')
        print(MapImplicationsToString(primeImplicantsin))
        '''
        essentialPrimeImplicantsString = MapImplicationsToString(essentialPrimeImplicants)
        curr_minimization=[]
        essentialPrimeImplicantsStringin = MapImplicationsToString(essentialPrimeImplicantsin)
        curr_minimizationin=[]
        
        #This block prints a possible minimization of the function entered.
        print("------------------------------------")
        print("Possible Minimization of function",f+1,':')
        for string in possibleAdditionStrings:
            if string != "":
                if essentialPrimeImplicantsString != "":
                    print(essentialPrimeImplicantsString + " + " + string)
                    curr_minimization.append(essentialPrimeImplicantsString + " + " + string)
                    all_minimizations.append(essentialPrimeImplicantsString + " + " + string)
                    
                else:
                    print(string)
                    curr_minimization.append(string)
                    all_minimizations.append(string)
            else:
                print(essentialPrimeImplicantsString)
                curr_minimization.append(essentialPrimeImplicantsString)
                all_minimizations.append(essentialPrimeImplicantsString)
            break
        print("------------------------------------")
        print("Possible Minimization of inverse of function",f+1,':')
        for stringin in possibleAdditionStringsin:
            if stringin != "":
                if essentialPrimeImplicantsStringin != "":
                    print(essentialPrimeImplicantsStringin + " + " + stringin)
                    curr_minimizationin.append(essentialPrimeImplicantsStringin + " + " + stringin)
                    all_minimizationsin.append(essentialPrimeImplicantsStringin + " + " + stringin)
                    
                else:
                    print(stringin)
                    curr_minimizationin.append(stringin)
                    all_minimizationsin.append(stringin)
            else:
                print(essentialPrimeImplicantsStringin)
                curr_minimizationin.append(essentialPrimeImplicantsStringin)
                all_minimizationsin.append(essentialPrimeImplicantsStringin)
            break

        strspl2=curr_minimization[0]
        split_list=split_string(strspl2)  #Here we are splitting string using '+' as delimiter
        
        strspl2in=curr_minimizationin[0]
        split_listin=split_string(strspl2in)
        set_list=[]
        setcm=set(curr_minimization)     #Here we are making set of product terms
        
        set_listin=[]
        setcmin=set(curr_minimizationin)
        for setval in setcm:
            set_list.append(setval)
        for setvalin in setcmin:
            set_listin.append(setvalin) 
        strip_list=[]
        #This block removes the spaces by stripping the list items i.e. strings
        if f==funct_num-1:
            for val in range(len(all_minimizations)):
                sr=all_minimizations[val]
                listtemp=list(sr.split('+'))
                for value in range(len(listtemp)):
                    prod_term_str.append(listtemp[value])
            for vb in range(len(prod_term_str)):
                strip_list.append(str(prod_term_str[vb].strip()))
                
        set_prod_terms=set(strip_list)
        sl_curr.append('[%s]' % ', '.join(map(str, set_prod_terms)))
        ol.append(split_list)
        strip_listin=[]
        #This block removes the spaces by stripping the list items i.e. strings
        if f==funct_num-1:
            for valin in range(len(all_minimizationsin)):
                srin=all_minimizationsin[valin]
                listtempin=list(srin.split('+'))
                for valuein in range(len(listtempin)):
                    prod_term_strin.append(listtempin[valuein])
            for vbin in range(len(prod_term_strin)):
                strip_listin.append(str(prod_term_strin[vbin].strip()))
                
        set_prod_termsin=set(strip_listin)
        sl_currin.append('[%s]' % ', '.join(map(str, set_prod_termsin)))
        olin.append(split_listin)
        if f==funct_num-1:
            for val in range(len(ol)):
                srls=list(ol[val])
                sr=[]
                lcset={}
                for value in range(len(srls)):
                    sr.append(str(srls[value].strip()))
                lcset=set(sr)
                olstrp.append(lcset)
            for val2 in range(len(olin)):
                srls2=list(olin[val2])
                sr2=[]
                lcset2={}
                for value2 in range(len(srls2)):
                    sr2.append(str(srls2[value2].strip()))
                lcset2=set(sr2)
                olstrpin.append(lcset2)
    for setval in set_prod_terms:                 #This block appends the Product Terms Section of the PLA Program Table as list items
        sl.append(setval)
    
    zet=[]
    for z in range (len(olstrp)):
        zet.append([])
        zet[z]=[olstrp[z],olstrpin[z]]
    if funct_num==2:
        tempset=[]
        for za in range(len(zet)):
            for zb in range(2):
                tempset.append(set(zet[0][za].union(zet[1][zb])))
                
        ct=len(tempset[0])
        templist=[tempset[0]]
        for zc in range(1,len(tempset)):
            if ct>len(tempset[zc]):
                templist=list(tempset[zc])
                ct=len(tempset)
    if funct_num>=3:
        tempset=[]
        for za in range(2):
            for zb in range(2):
                for zc in range(2):
                    tempset.append(set(zet[0][za].union(zet[1][zb],zet[2][zc])))
                
        ct=len(tempset[0])
        templist=[tempset[0]]
        for zc in range(1,len(tempset)):
            if ct>len(tempset[zc]):
                templist=list(tempset[zc])
                ct=len(tempset)
        
    if(type(templist[0]) is set):
        templist=list(templist[0])
                
    fl=[]
    for p in templist:
        fl.append([])
        for q in range (len(olstrp)):
            if p in olstrp[q]:
                fl.append(list(olstrp[q]))
            if p in olstrpin[q]:
                fl.append(list(olstrpin[q]))
    ozlist = [x for x in fl if x]
    fsetl=[]
    for z in ozlist:
        fsetl.append([])
        if z in fsetl:
            pi=0
            pi+=1
        else:
            fsetl.append(z)
    ozls = [x for x in fsetl if x]
        
    varlist=list(map(chr, range(65, 65+var_num)))      #This list is used to print header of the table
    
    for qq in range (funct_num):
        functlist.append('F'+str(qq+1))               #This list is also used to print header of the table
        
    reg=[]
    for vb in range(len(ozls)):
        reg.append([])
        for fg in range(len(ozls[vb])):
            reg[vb].append(str(ozls[vb][fg].strip()))
            
    #This block appends the Outputs Section of the PLA Program Table as list items.
    ui=[]
    for qe in range(len(templist)):
        for qr in range(len(reg)):
            ui.append([])
            if templist[qe] in reg[qr]:
                ui[qe].append(1)
            else:
                ui[qe].append('-')            
    output_list = [x for x in ui if x]
    #print('templist',templist)
    #This block appends the Inputs Section of the PLA Program Table as list items.
    c=0
    input_list=[]
    for cc in range(len(templist)):
        input_list.append(['-']*(len(varlist)))
    for cc in range(len(templist)):
        j=0
        while(j<len(templist[cc])):
            for c in range(len(varlist)):
                if templist[cc][j]==varlist[c]:
                    if (j+1)<len(templist[cc]):
                        if(templist[cc][j+1]=="'"):
                            input_list[cc][c]=0
                            j+=1
                        else:
                            input_list[cc][c]=1
                    else:
                        input_list[cc][c]=1
            j+=1
    #print('input',input_list)
    print('---------------------------------------------------------------')
    print('The Program Table for implementing the given set of functions using PLA is:')
    print('---------------------------------------------------------------')
    print('Product Terms        Inputs          Outputs')                #Prints Heading of the table.
    print('                     ',*varlist,'         ',*functlist)
    for pterm in range(len(templist)):                                          #This block prints data corresponding to x product terms in PLA Program Table
        print(templist[pterm],' '*(20-len(templist[pterm])),*input_list[pterm],'          ',*output_list[pterm])         
             
if __name__ == '__main__':
    main()