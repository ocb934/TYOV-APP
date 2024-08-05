import sys
import random
import csv
import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QPushButton, QMessageBox, QCheckBox, QSpinBox

#########################################################################################################################################################################  
#makes sure that if the user starts immediately, that the states are defined
state1 = "Unchecked" #toggles single alternate prompts
state2 = "Unchecked" #toggles multiple alternate prompts
state3 = "Unchecked" #toggles multiple alt prompts all at once
state4 = "Unchecked" #toggles rolling two d10s
state5 = "Unchecked" #toggles alternate starting point
state6 = "Unchecked" #toggles ending starting point
singlePromptLiklihood = 0
multiplePromptLiklihood = 0

#Getting Compilier to actually work
if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

#This is the Prompts Window
class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent (which it doesn't), it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()

        #Window Customization
        self.setMinimumSize(800, 800)
        self.setStyleSheet("background-color: #8B0000;")
        self.setWindowTitle("TYOV-APP Prompts Window")

        #Setting up variables
        global j
        global k 
        global l
        global m
        j=0
        k=0
        l=0
        m=0
      
        #Opens the file with the prompts
        #___Hits is the array of the prompts and how we will keep history of it

        with open('prompts.csv', mode='r') as csvfile:
            global prompts
            global promptHits
            
            prompts = list(csv.reader(csvfile, delimiter='|'))
            promptHits = [0] * len(prompts)
            
        with open('altstartingpoints.csv', mode='r') as altstartingcsvfile: 
            global altstartingpoints
            global altstartingpromptHits

            altstartingpoints = list(csv.reader(altstartingcsvfile, delimiter='|'))
            altstartingpromptHits = [0] * len(altstartingpoints)
        
        with open('altendingpoints.csv', mode='r') as altendingcsvfile:
            global altendingpoints
            global altendingpromptHits

            altendingpoints = list(csv.reader(altendingcsvfile, delimiter='|'))
            altendingpromptHits = [0] * len(altendingpoints)

        with open('singleentry.csv', mode='r') as singleentrycsvfile:
            global singleentrylist
            global singleentryHits

            singleentrylist = list(csv.reader(singleentrycsvfile, delimiter='|'))
            singleentryHits = [0] * len(singleentrylist)
           
        with open('multipleentry.csv', mode='r') as multipleentrycsvfile: #individual multiple entries
            global multipleentrylist #list of the prompts
            global multipleentryHits #how many times prompt has been hit
            global listEntries #amount of entries in each prompt
            
            multipleentrylist = list(csv.reader(multipleentrycsvfile, delimiter='|'))
            multipleentryHits = [0] * len(multipleentrylist)
            listEntries = []
                       
            for l in range(len(multipleentrylist)): #figuring out how many entries in each prompt
                mlist = len(multipleentrylist[l])
                listEntries.append(mlist)

        with open('multipleentry.csv', mode='r') as aaomultipleentrycsvfile: #multiple entries all at once
            global aaomultipleentrylist
            global aaomultipleentryHits
            
            aaomultipleentrylist = list(csv.reader(aaomultipleentrycsvfile, delimiter='@'))
            aaomultipleentryHits = [0] * len(aaomultipleentrylist)
            
            
           
    #Prompt Page

        #Prompt Title and Text Determination
            global prompt1Title 
            global prompt1
            
        if state5 == "Checked": #Alternate Starting Point
            t=random.randint(0, 4)
            prompt1Title = QLabel("Alternate Starting Prompt " + str(t+1))
            prompt1 = QLabel(altstartingpoints[t][altstartingpromptHits[t]])

        else: #Normal Starting Point
            promptHits[0]=1 #This makes it where the first entry is already "seen"
            j=0
            roll=random.randint(0,8)
            j = max(j + roll, 0) #This determines if we have "seen" an entry
            while promptHits[j] > 2: #This will make it where if we have seen an entry 3 times, we move to the next one
                j += 1  #Increments j by 1 aka "move to the next prompt"

            prompt1Title = QLabel("Prompt " + str(j+1) + ", Entry 1")
            prompt1 = QLabel(prompts[j][promptHits[j]])
            
            promptHits[j] += 1 #increments the times we have seen an entry
        
       
        #Formatting of Prompt Title and Text
        font = prompt1Title.font()
        font.setPointSize(30)
        prompt1Title.setStyleSheet("""
            background-color: #262626;
            color: #FFFFFF;
            font-family: Garamond;                    
            """)
        prompt1Title.setFont(font)
        prompt1Title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font.setPointSize(12)
        prompt1Title.setFixedHeight(200)
        prompt1.setFont(font)
        prompt1.setStyleSheet("""
            background-color: #262626;
            color: #FFFFFF;
            """)
        prompt1.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        prompt1.setWordWrap(True)
        
        #Next Prompt Button
        global button1
        button1 = QPushButton("Next Prompt")
        button1.clicked.connect(self.button1_clicked)
        button1.setStyleSheet("""
        background-color: #262626;
        color: #FFFFFF;
                              
        """)
        #link to Tim Hutchings's website
        global link
        link = QLabel("<a href=\'https://thousandyearoldvampire.com/'>\nThousand Year Old Vampire by Tim Hutchings</a>" + " | " + "<a href=\'https://github.com/ocb934/'>Code created by ocb934</a>")
        link.setStyleSheet("""
            background-color: #262626;
            color: #551A8B;
            font: italic 12px;
            """)
        font = link.font()
        font.setPointSize(12)
        link.setFont(font)
        link.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        link.setWordWrap(True)
        link.setOpenExternalLinks(True)
        link.setFixedHeight(30)
        
        #Layout of the Prompt Window
        global layout
        layout = QVBoxLayout()
        layout.addWidget(prompt1Title)
        layout.addWidget(prompt1)
        layout.addWidget(button1)
        layout.addWidget(link)
        self.setLayout(layout)
     
    #Defining the function of clicking Next Prompt Button    
    def button1_clicked(self, s): 
        #dialog box
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Roll")
        dlg.setStyleSheet("""
            background-color: #262626;
            color: #FFFFFF;
            """)
        
        #global
        global state2
        global state1
        global j
        global k
        global l
        global m

        #Deciding whether to go with single or multiple entries. 
        # f-> Single = 0, multiple=1
        #state 2 is multiple, state 1 is single
        if state2 == "Checked" and state1 == "Checked":
            f=random.randint(0,1)
        elif state2== "Checked" and state1== "Unchecked":
            f=1
        elif state2== "Unchecked" and state1== "Checked:":
            f=0
        else:
            f=0
                
        #==============================
        #Rolling the Prompt Progression
        #==============================

        if f==0: #Single entry possibility
            if state1=="Checked": #Single Alternate Prompt
                percentage=random.randint(0,99)
                if percentage<singlePromptLiklihood: #Single Alt Prompt Chance Hit
                    roll=random.randint(0,66)
                    k = max(k + roll, 0) #This determines if we have "seen" an entry
                    if k>66: #resets k if we reach the end of the list
                        k=0 #this line is the only difference between this if and the else
                        if singleentryHits[k]==1: #can't reset if we hit the end
                            k=0
                            if singleentryHits==([1]*67): #if we hit all the prompts, reset to normal prompts
                                state1="Unchecked"
                                dlg.setText("You ran out of Alternate Single Entry Prompts")
                            else: #make sure we don't error out if they are the same
                                while singleentryHits[k] > 0: #This will make it where if we have seen an entry once, we move to the next one
                                    k += 1  #Increments k by 1 aka "move to the next prompt"
                                dlg.setText("You rolled for an Alternate Single Entry Prompt " + str(k+1))
                        else: #continue as normal
            
                            if singleentryHits==([1]*67): #if we hit all the prompts, reset to normal prompts
                                state1="Unchecked"
                                dlg.setText("You ran out of Alternate Single Entry Prompts")
                            else: #make sure we don't error out if they are the same
                                while singleentryHits[k] > 0: #This will make it where if we have seen an entry once, we move to the next one
                                    k += 1  #Increments k by 1 aka "move to the next prompt"
                                dlg.setText("You rolled for an Alternate Single Entry Prompt " + str(k+1))
                       
                                    
                    else:
                        if singleentryHits[k]==1: #can't reset if we hit the end
                            k=0
                            if singleentryHits==([1]*67): #if we hit all the prompts, reset to normal prompts
                                state1="Unchecked"
                                dlg.setText("You ran out of Alternate Single Entry Prompts")
                            else: #make sure we don't error out if they are the same
                                while singleentryHits[k] > 0: #This will make it where if we have seen an entry once, we move to the next one
                                    k += 1  #Increments k by 1 aka "move to the next prompt"
                                dlg.setText("You rolled for an Alternate Single Entry Prompt " + str(k+1))
                        else: #continue as normal
                            if singleentryHits==([1]*67): #if we hit all the prompts, reset to normal prompts
                                state1="Unchecked"
                                dlg.setText("You ran out of Alternate Single Entry Prompts")
                            else: #make sure we don't error out if they are the same
                                while singleentryHits[k] > 0: #This will make it where if we have seen an entry once, we move to the next one
                                    k += 1  #Increments k by 1 aka "move to the next prompt"
                                dlg.setText("You rolled for an Alternate Single Entry Prompt " + str(k+1))                                 
                
                else: #Single Alt Prompt Chance Miss   
                    global d10
                    global d6
                    d6 = random.randint(1, 6)
                    if state4=="Checked": #toggle for rolling two d10s
                        oned10 = random.randint(1, 10)
                        twod10 = random.randint(1, 10)
                        d10= oned10+twod10
                    else: #single d10
                        d10 = random.randint(1, 10)
                    roll = d10-d6
                    j = max(j + roll, 0) #This determines if we have "seen" an entry
                    while promptHits[j] > 2: #This will make it where if we have seen an entry 3 times, we move to the next one
                        j += 1  #Increments j by 1 aka "move to the next prompt"
                    
                    #Makes sure that when the ending prompts show up, you cannot roll anymore
                    if j>70:
                        button1.clicked.disconnect(self.button1_clicked)
                        button1.setText("")

                    #dialog box text
                    if j<71:
                        
                        dlg.setText("Your dice rolls were d10 = " + str(d10) + " and d6 = " + str(d6) + ", giving you " + str(roll)+ ". \nYou are now at Prompt " + str(j+1) + ", Entry " + str(promptHits[j]+1) + ".")
                    else:
                        
                        dlg.setText("Your dice rolls were d10 = " + str(d10) + " and d6 = " + str(d6) + ", giving you " + str(roll) + ". \nYou are now at Prompt " + str(j+1) + "." + "\n\nThe game is over after this prompt.")
                    #End
            else: #Normal Entry if Single Alt Prompt is not selected 
                d6 = random.randint(1, 6)
                if state4=="Checked":
                    oned10 = random.randint(1, 10)
                    twod10 = random.randint(1, 10)
                    d10= oned10+twod10
                else:
                    d10 = random.randint(1, 10)
                roll = d10-d6
                j = max(j + roll, 0) #This determines if we have "seen" an entry
                while promptHits[j] > 2: #This will make it where if we have seen an entry 3 times, we move to the next one
                    j += 1  #Increments j by 1 aka "move to the next prompt"
                
                #Makes sure that when the ending prompts show up, you cannot roll anymore
                if j>70:
                    button1.clicked.disconnect(self.button1_clicked)
                    button1.setText("")

                #dialog box text
                if j<71:
                    
                    dlg.setText("Your dice rolls were d10 = " + str(d10) + " and d6 = " + str(d6) + ", giving you " + str(roll)+ ". \nYou are now at Prompt " + str(j+1) + ", Entry " + str(promptHits[j]+1) + ".")
                else:
                    
                    dlg.setText("Your dice rolls were d10 = " + str(d10) + " and d6 = " + str(d6) + ", giving you " + str(roll) + ". \nYou are now at Prompt " + str(j+1) + "." + "\n\nThe game is over after this prompt.")
                #End
        else: #multiple entry possibility
            if state2=="Checked": #AltMultiple Prompt Entry
                percentage=random.randint(0,99)
                if percentage<multiplePromptLiklihood: #AltMultiple Prompt Hit                   
                    if state3=="Checked": #This means we see the prompts all at once
                        global m
                        md6 = random.randint(1, 6)
                        if state4=="Checked": #toggle rolling two d10s
                            oned10 = random.randint(1, 10)
                            twod10 = random.randint(1, 10)
                            md10= oned10+twod10
                        else: #single d10
                            md10 = random.randint(1, 10)
                        rollmultiple = md10-md6
                        m = max(m + rollmultiple, 0) #This determines if we have "seen" an entry
                        if m>68: #resets m if we reach the end of the multiple entry list
                            m=0 #this line is the only difference between this if and the else.
                            if aaomultipleentryHits[m]==1: #can't reset if we hit the end
                                m=0
                                if aaomultipleentryHits== ([1]*69): #if we hit all the prompts reset to normal prompts
                                    state2="Unchecked"
                                    dlg.setText("You ran out of Alternate Multiple Entry Prompts")
                                else: #make sure we don't error out if they are the same
                                    while aaomultipleentryHits[m]>0:
                                        m+=1
                                    dlg.setText("You rolled for an Alternate Multiple Entry Prompt " + str(m+1))
                            else:
                                if aaomultipleentryHits== ([1]*69): #if we hit all the prompts reset to normal prompts
                                        state2="Unchecked"
                                else: #make sure we don't error out if they are the same
                                    while aaomultipleentryHits[m]>0:
                                        m+=1
                                    dlg.setText("You rolled for an Alternate Multiple Entry Prompt " + str(m+1))
                        else: #continue as normal
                            if aaomultipleentryHits[m]==1: #can't reset if we hit the end
                                m=0
                                if aaomultipleentryHits== ([1]*69): #if we hit all the prompts reset to normal prompts
                                    state2="Unchecked"
                                    dlg.setText("You ran out of Alternate Multiple Entry Prompts")
                                else: #make sure we don't error out if they are the same
                                    while aaomultipleentryHits[m]>0:
                                        m+=1
                                    dlg.setText("You rolled for an Alternate Multiple Entry Prompt " + str(m+1))
                            else:
                                if aaomultipleentryHits== ([1]*69): #if we hit all the prompts reset to normal prompts
                                        state2="Unchecked"
                                        dlg.setText("You ran out of Alternate Multiple Entry Prompts")
                                else: #make sure we don't error out if they are the same
                                    while aaomultipleentryHits[m]>0:
                                        m+=1
                                    dlg.setText("You rolled for an Alternate Multiple Entry Prompt " + str(m+1))
                        
                        dlg.setText("You rolled for an Alternate Multiple Entry Prompt " + str(m+1))
                    
                    else: #Multiple Alt Prompts individually
                        global multipleentrylist
                        global multipleentryHits
                        global listEntries

                        fixedlistEntries = [q-1 for q in listEntries] #makes some of the code easier and offsets the starting at 0
                        md6 = random.randint(1, 6)
                        if state4=="Checked": #rolling 2 d10s
                            oned10 = random.randint(1, 10)
                            twod10 = random.randint(1, 10)
                            md10= oned10+twod10
                        else: #rolling singular d10
                            md10 = random.randint(1, 10)
                        rollmultiple = md10-md6               
                        l = max(l + rollmultiple, 0) #This determines if we have "seen" an entry
                        if l>68: #resets l if we reach the end of the multiple entry list
                            l=0 #only difference between the if and else statement
                            if listEntries[l]==multipleentryHits[l]: #can't reset if we hit the end so we gotta do it for the program
                                l=0
                                if multipleentryHits==listEntries: #If all multiple prompts are seen, switch to normal prompts
                                    state2="Unchecked"
                                    dlg.setText("You ran out of Alternate Multiple Entry Prompts")
                                else: #make sure we don't error out if they are the same
                                    while multipleentryHits[l] > (fixedlistEntries[l]):
                                        l += 1     
                                    dlg.setText("You rolled for an Alternate Multiple Entry Prompt " + str(l+1) + ", Entry " + str(multipleentryHits[l]+1) + ".") 
                            else:       
                                if multipleentryHits==listEntries: #If all multiple prompts are seen, switch to normal prompts
                                    state2="Unchecked"
                                    dlg.setText("You ran out of Alternate Multiple Entry Prompts")
                                else: #make sure we don't error out if they are the same
                                    while multipleentryHits[l] > (fixedlistEntries[l]):
                                        l += 1   
                                    dlg.setText("You rolled for an Alternate Multiple Entry Prompt " + str(l+1) + ", Entry " + str(multipleentryHits[l]+1) + ".")    
                        else:
                            
                            if listEntries[l]==multipleentryHits[l]: #can't reset if we hit the end so we gotta do it for the program
                                l=0
                                if multipleentryHits==listEntries: #If all multiple prompts are seen, switch to normal prompts
                                    state2="Unchecked"
                                    dlg.setText("You ran out of Alternate Multiple Entry Prompts")
                                else: #make sure we don't error out if they are the same
                                    while multipleentryHits[l] > (fixedlistEntries[l]):
                                        l += 1 
                                    dlg.setText("You rolled for an Alternate Multiple Entry Prompt " + str(l+1) + ", Entry " + str(multipleentryHits[l]+1) + ".")
                            else:       
                                if multipleentryHits==listEntries: #If all multiple prompts are seen, switch to normal prompts
                                    state2="Unchecked"
                                    dlg.setText("You ran out of Alternate Multiple Entry Prompts")
                                else: #make sure we don't error out if they are the same
                                    while multipleentryHits[l] > (fixedlistEntries[l]):
                                        l += 1
                                    dlg.setText("You rolled for an Alternate Multiple Entry Prompt " + str(l+1) + ", Entry " + str(multipleentryHits[l]+1) + ".")
                else: #AltMultiple Prompt Miss
                    d6 = random.randint(1, 6)
                    if state4=="Checked": #roll 2 d10s
                        oned10 = random.randint(1, 10)
                        twod10 = random.randint(1, 10)
                        d10= oned10+twod10
                    else: #single d10
                        d10 = random.randint(1, 10)
                    roll = d10-d6
                    j = max(j + roll, 0) #This determines if we have "seen" an entry
                    while promptHits[j] > 2: #This will make it where if we have seen an entry 3 times, we move to the next one
                        j += 1  #Increments j by 1 aka "move to the next prompt"
                    
                    #Makes sure that when the ending prompts show up, you cannot roll anymore
                    if j>70:
                        button1.clicked.disconnect(self.button1_clicked)
                        button1.setText("")

                    #dialog box text
                    if j<71:
                        dlg.setText("Your dice rolls were d10 = " + str(d10) + " and d6 = " + str(d6) + ", giving you " + str(roll)+ ". \nYou are now at Prompt " + str(j+1) + ", Entry " + str(promptHits[j]+1) + ".")
                    else:
                        dlg.setText("Your dice rolls were d10 = " + str(d10) + " and d6 = " + str(d6) + ", giving you " + str(roll) + ". \nYou are now at Prompt " + str(j+1) + "." + "\n\nThe game is over after this prompt.")
                    #End of Normal Entry
            else: #Normal Entry
                d6 = random.randint(1, 6)
                if state4=="Checked":
                    oned10 = random.randint(1, 10)
                    twod10 = random.randint(1, 10)
                    d10= oned10+twod10
                else:
                    d10 = random.randint(1, 10)
                roll = d10-d6
                j = max(j + roll, 0) #This determines if we have "seen" an entry
                while promptHits[j] > 2: #This will make it where if we have seen an entry 3 times, we move to the next one
                    j += 1  #Increments j by 1 aka "move to the next prompt"
                
                #Makes sure that when the ending prompts show up, you cannot roll anymore
                if j>70:
                    button1.clicked.disconnect(self.button1_clicked)
                    button1.setText("")

                #dialog box text
                if j<71:
                    
                    dlg.setText("Your dice rolls were d10 = " + str(d10) + " and d6 = " + str(d6) + ", giving you " + str(roll)+ ". \nYou are now at Prompt " + str(j+1) + ", Entry " + str(promptHits[j]+1) + ".")
                else:
                    
                    dlg.setText("Your dice rolls were d10 = " + str(d10) + " and d6 = " + str(d6) + ", giving you " + str(roll) + ". \nYou are now at Prompt " + str(j+1) + "." + "\n\nThe game is over after this prompt.")
                #End

        #Executes the dialog      
        dlg.exec()

        #==============================
        #Changes the information of the Prompt Window
        #==============================
        if f==0:
            if state1=="Checked": #Single Alt Prompt
                if percentage<singlePromptLiklihood: #Single Alt Prompt Hit
                    prompt1Title.setText("Alternate Single Entry Prompt " + str(k+1))
                    prompt1.setText(singleentrylist[k][singleentryHits[k]])
                else: #Single Alt Prompt Miss
                    if j<71: #Progression
                        prompt1Title.setText("Prompt " + str(j+1) + ", Entry " + str(promptHits[j]+1))  
                        prompt1.setText(prompts[j][promptHits[j]])    
                    elif state6=="Checked": #Alt Ending Prompt
                        r= random.randint(0,4)
                        prompt1Title.setText("Alternate Ending Prompt " + str(r+1))
                        prompt1.setText(altendingpoints[r][altendingpromptHits[r]])
                    else: #Normal Ending Prompt
                        prompt1Title.setText("Prompt " + str(j+1))
                        prompt1.setText(prompts[j][promptHits[j]])   
            else: #Normal Entry
                if j<71: #Progression
                    prompt1Title.setText("Prompt " + str(j+1) + ", Entry " + str(promptHits[j]+1))  
                    prompt1.setText(prompts[j][promptHits[j]])    
                elif state6=="Checked": #Alt Ending Prompt
                    r= random.randint(0,4)
                    prompt1Title.setText("Alternate Ending Prompt " + str(r+1))
                    prompt1.setText(altendingpoints[r][altendingpromptHits[r]])
                else: #Normal Ending Prompt
                    prompt1Title.setText("Prompt " + str(j+1))
                    prompt1.setText(prompts[j][promptHits[j]])   
        else:
            if state2=="Checked": #Multiple Prompts                
                if percentage<multiplePromptLiklihood: #Multiple Prompts Hit
                    if state3=="Checked": #All Entries at Once Multiple Prompts
                        prompt1Title.setText("Alternate Multiple Entry Prompt " + str(m+1))
                        prompt1.setText(str(aaomultipleentrylist[m]).replace('|', '\n\n').replace('[', '').replace(']', ''))
                    else: #Individual Entry Multiple Prompts
                        prompt1Title.setText("Alternate Multiple Entry Prompt " + str(l+1) + ", Entry " + str(multipleentryHits[l]+1))
                        prompt1.setText(multipleentrylist[l][multipleentryHits[l]])
                else: #Multiple Prompts Miss
                    if j<71: #Progression
                        prompt1Title.setText("Prompt " + str(j+1) + ", Entry " + str(promptHits[j]+1))  
                        prompt1.setText(prompts[j][promptHits[j]])    
                    elif state6=="Checked": #Alt Ending Prompt
                        r= random.randint(0,4)
                        prompt1Title.setText("Alternate Ending Prompt " + str(r+1))
                        prompt1.setText(altendingpoints[r][altendingpromptHits[r]])
                    else: #Normal Ending Prompt
                        prompt1Title.setText("Prompt " + str(j+1))
                        prompt1.setText(prompts[j][promptHits[j]])   
            else: #normal entry
                if j<71: #progression
                    prompt1Title.setText("Prompt " + str(j+1) + ", Entry " + str(promptHits[j]+1))  
                    prompt1.setText(prompts[j][promptHits[j]])    
                elif state6=="Checked": #alt ending prompt
                    r= random.randint(0,4)
                    prompt1Title.setText("Alternate Ending Prompt " + str(r+1))
                    prompt1.setText(altendingpoints[r][altendingpromptHits[r]])
                else: #normal ending prompt
                    prompt1Title.setText("Prompt " + str(j+1))
                    prompt1.setText(prompts[j][promptHits[j]])   

        #==============================
        #increments the times we have seen an entry
        #==============================
        if f==0: #Single
            if state1=="Checked": #Single Alt Prompt
                if percentage<singlePromptLiklihood: #Single Alt Prompt Hit
                    singleentryHits[k] += 1
                else: #Single Alt Prompt Miss
                    promptHits[j] += 1
            else: #Normal Entry
                promptHits[j] += 1
        else: #Multiple
            if state2=="Checked": #multiple promts
                if percentage<multiplePromptLiklihood: #Multiple Prompt Hit
                    if state3 =="Checked": #All Entries at Once
                        aaomultipleentryHits[m] += 1
                    else: #Individual Entries
                        multipleentryHits[l] += 1
                else: #Normal Entry
                    promptHits[j] += 1
            else: #Normal Entry
                promptHits[j] += 1


#########################################################################################################################################################################       

#This is the Main Starting Window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.w = None  # No external window yet.
    
    #Starting Page
        #Sheet Style
        self.setStyleSheet("background-color: #000000;")  
        self.setWindowTitle("TYOV-APP")

        #Title
        global title
        title = QLabel("Thousand Year Old Vampire\nAutomatic Prompt Progression")
        title.setStyleSheet("""
            background-color: #262626;
            color: #FFFFFF;
            font-family: Garamond;
            """)
        font = title.font()
        font.setPointSize(25)
        title.setWordWrap(True)
        title.setFont(font)
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        
        #Disclaimer Text
        global disclaimer
        disclaimer = QLabel ("\nThousand Year Old Vampire is a solo RPG created by Tim Hutchings.\nYou can find the book and PDF on www.thousandyearoldvampire.com\nPlease support the game developer.\n\nThis application is meant to automate the prompt progression of the game. \nNo rolling is required, and you do not have to keep track \nof which Prompts you have hit.\nJust click 'Next Prompt.' \n\nThis does not include:\nInstructions on how to play the game\nHow to create your Vampire\nContent Warnings\nYour Vampire's Traits\nYour Vampire's Diary\n\nPlease consult the original book on these aspects of the game.\n\nIf you want to lengthen your game or make it more interesting, \nadd additional prompts below.\n\nWARNING: THERE IS NO BACK BUTTON!\n")
        disclaimer.setStyleSheet("""
            background-color: #262626;
            color: #FFFFFF;
            """)
        font = disclaimer.font()
        font.setPointSize(12)
        disclaimer.setFont(font)
        disclaimer.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        disclaimer.setWordWrap(True)

        #link to Tim Hutchings's website
        global link
        link = QLabel("<a href=\'https://thousandyearoldvampire.com/'>\nThousand Year Old Vampire by Tim Hutchings</a>" + " | " + "<a href=\'https://github.com/ocb934/'>Code created by ocb934</a>")
        link.setStyleSheet("""
            background-color: #262626;
            color: #551A8B;
            font: italic 12px;
            """)
        font = link.font()
        font.setPointSize(12)
        link.setFont(font)
        link.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        link.setWordWrap(True)
        link.setOpenExternalLinks(True)
        

        #Additional Prompts Title
        global aptitle
        aptitle = QLabel("Additional Options")
        aptitle.setStyleSheet("""
            background-color: #262626;
            color: #FFFFFF;
            font-family: Garamond;
            font: 25px;
            """)
        aptitle.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        #Additional Prompts Checkbox
        self.singlealtprompts = QCheckBox ("Click here for Single Entry Alternate Prompts", self)
        self.singlealtprompts.stateChanged.connect(self.singlealtprompts_clicked)

        self.multiplealtprompts = QCheckBox ("Click here for Multiple Entries Alternate Prompts", self)
        self.multiplealtprompts.stateChanged.connect(self.multiplealtprompts_clicked)

        self.allatonce = QCheckBox ("Click here if you want to receive all the entries at once for each Multiple Entries Alternate Prompt", self)
        self.allatonce.stateChanged.connect(self.allatonce_clicked)

        self.altstartingpoint = QCheckBox ("Click here for an Alternate Starting Point",self)
        self.altstartingpoint.stateChanged.connect(self.altstartingpoint_clicked)

        self.altendingpoint = QCheckBox ("Click here for an Alternate Ending Point",self)
        self.altendingpoint.stateChanged.connect(self.altendingpoint_clicked)

        self.twod10s = QCheckBox ("Click here to roll two d10s instead of one (Suggested for Multiplayer/Super Quick Solo Game)",self)
        self.twod10s.stateChanged.connect(self.twod10s_clicked)

        #Additional Prompts Formatting
        self.singlealtprompts.setStyleSheet("""
            color: #FFFFFF;
            """)
        self.multiplealtprompts.setStyleSheet("""
           color: #FFFFFF;
            """)
        self.allatonce.setStyleSheet("""
           color: #FFFFFF;
            """)
        self.altstartingpoint.setStyleSheet("""
            color: #FFFFFF;
            """)
        self.altendingpoint.setStyleSheet("""
            color: #FFFFFF;
            """)
        self.twod10s.setStyleSheet("""
            color: #FFFFFF;
            """)
        
    #Sliders
        #Single Entry
        self.singleentry = QSpinBox()
        self.singleentry.setMinimum(5)
        self.singleentry.setMaximum(90)
        self.singleentry.setSingleStep(15)
        self.singleentry.setPrefix("Liklihood of seeing an Alternate single entry prompt: ")
        self.singleentry.setSuffix("%")
        self.singleentry.setStyleSheet("""
            color: #FFFFFF;
            background-color: #262626
            """)
        self.singleentry.valueChanged.connect(self.value_changed)

        #Multiple Entry
        self.multipleentry= QSpinBox()
        self.multipleentry.setMinimum(5)
        self.multipleentry.setMaximum(90)
        self.multipleentry.setSingleStep(15)
        self.multipleentry.setPrefix("Liklihood of seeing an Alternate multiple entry prompt: ")
        self.multipleentry.setSuffix("%")
        self.multipleentry.setStyleSheet("""
            color: #FFFFFF;
            background-color: #262626
            """)
        self.multipleentry.valueChanged.connect(self.value_changed2)

    #Button
        self.button = QPushButton("Click here for the first random prompt")
        self.button.clicked.connect(self.show_new_window)
        self.button.setStyleSheet("""
            background-color: #8B0000;
            color: #FFFFFF;
            """)
        
    #Layout of the Main Window
        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(disclaimer)
        layout.addWidget(aptitle)
        layout.addWidget(self.altstartingpoint)
        layout.addWidget(self.altendingpoint)
        layout.addWidget(self.singlealtprompts)
        layout.addWidget(self.singleentry)
        layout.addWidget(self.multiplealtprompts)
        layout.addWidget(self.allatonce)
        layout.addWidget(self.multipleentry)
        layout.addWidget(self.twod10s)
        layout.addWidget(self.button)
        layout.addWidget(link)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    #Determinng slider values
    def value_changed(self, i):
        global singlePromptLiklihood
        singlePromptLiklihood = i

    def value_changed2(self, i):
        global multiplePromptLiklihood
        multiplePromptLiklihood = i
        
    
    #Determining if the checkboxes has been clicked
    def singlealtprompts_clicked(self, value1):
        global state1
        state1 = Qt.CheckState(value1)
        if state1 == Qt.CheckState.Checked:
            state1 = "Checked"
        elif state1 == Qt.CheckState.Unchecked:
            state1 = "Unchecked"
        
    def multiplealtprompts_clicked(self, value2):
        global state2
        state2 = Qt.CheckState(value2)
        if state2 == Qt.CheckState.Checked:
            state2 = "Checked"
        elif state2 == Qt.CheckState.Unchecked:
            state2 = "Unchecked"
    def allatonce_clicked(self, value3):
        global state3
        state3 = Qt.CheckState(value3)
        if state3 == Qt.CheckState.Checked:
            state3 = "Checked"
        elif state3 == Qt.CheckState.Unchecked:
            state3 = "Unchecked"

    def twod10s_clicked(self, value4):
        global state4
        state4 = Qt.CheckState(value4)
        if state4 == Qt.CheckState.Checked:
            state4 = "Checked"
        elif state4 == Qt.CheckState.Unchecked:
            state4 = "Unchecked"

    def altstartingpoint_clicked(self, value5):
        global state5
        state5 = Qt.CheckState(value5)
        if state5 == Qt.CheckState.Checked:
            state5 = "Checked"
        elif state5 == Qt.CheckState.Unchecked:
            state5 = "Unchecked"
            
    def altendingpoint_clicked(self, value6):
        global state6
        state6 = Qt.CheckState(value6)
        if state6 == Qt.CheckState.Checked:
            state6 = "Checked"
        elif state6 == Qt.CheckState.Unchecked:
            state6 = "Unchecked"
    

    #Getting the Prompt Window to show up
    def show_new_window(self, checked):
        if self.w is None:
            self.w = AnotherWindow()
            self.w.show()
        else:
            self.w.close()  # Close window.
            self.w = None  # Discard reference.

#########################################################################################################################################################################  

app = QApplication(sys.argv)
window = MainWindow()
window.show()  # IMPORTANT!!!!! Windows are hidden by default.
app.exec()