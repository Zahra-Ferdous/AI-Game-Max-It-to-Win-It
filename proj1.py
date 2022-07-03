# -*- coding: utf-8 -*-
"""
Created on Sun Jul  3 00:16:41 2022

@author: root
"""

import tkinter as tk
from tkinter import*
import random
window = tk.Tk()
window.geometry("300x450")  # Size of the window 
window.title("max_it_to_win_it")  # Adding a title

import numpy as np
import matplotlib.pyplot as plt
import time
import sys
import os


vis = np.zeros((105,105), bool)
dp = np.zeros((105,105), int)
prefix = np.zeros((105,105), bool)
path = np.zeros((105,105), int)
test = []


totalH=""
numH=0
totalC=""
numC=0
isAI=True

numbers = [-23,56,1,-78,8,-9,11]
lastPressed = 0
lastSelected = -1

buttons = [] # to store button references

finalC= StringVar()
finalH= StringVar()
scoreH = Entry(window,textvariable=finalH).place(x=200,y=250)
scoreC = Entry(window,textvariable=finalC).place(x=-0,y=250)

hi = 0
lo = 0


#------------------ after a number is selected ---------------------

def show_press(press, lastPressed, valid):
    global numH,numC,totalH,totalC,isAI,lo,hi, lastSelected, test
    
    lo = valid[0]
    hi = valid[1]
    #lastSelected = -1
    
    # ---------------------------------- IF IT IS HUMAN ---------------------------------
    
    if isAI==False :
   
        for i in range(len(buttons)):
            if i==lastPressed:
                #print(lastPressed)
                
                if ( ( lastSelected == -1 and ( valid[0] == i or valid[1] == i ) ) or ( valid[0] == i and lastSelected == i-1 ) or ( valid[1] == i and lastSelected == i+1 ) ):
                    
                    if valid[0] == i :
                        lo = i+1
                        valid[0] = i+1
                    elif valid[1] == i :
                        hi = i-1
                        valid[1] = i-1
                    lastSelected = i
                    
                    numH=numH+int(test[i])
                    test[i]=0
                    buttons[i].pack_forget()
                    
            else:
                finalH.set("error")
            
    print("in show press: hi = {}, lo = {} ".format(hi, lo))
                    
                    
    #--------------------------------------- IF IT IS AI --------------------------------
    #else:
        
    
    
    
#----------------------- after pressing the pass buttton ----------------------   
    
def passval(btn, lo, hi):
    
    global numH,numC,totalH,totalC,isAI,lastSelected
    
    
    if( not(isAI) ):
        totalH=str(numH)
        finalH.set(totalH)
    else:
        totalC=str(numC)
        finalC.set(totalC)
    isAI = not(isAI)
    
    print("after pass: hi = {}, lo = {}".format(hi,lo))
    
    lastSelected = -1
    
    minmax(lo,hi)
    
    if(lo<hi):
    
        if (prefix[lo][hi]):
        
            for i in range(lo, lo+path[lo][hi]):
            
                #comp_val+=numbers[i]
                numC=numC+int(numbers[i])
                numbers[i]=0
                buttons[i].pack_forget()
            
            lo+=path[lo][hi]
              
        else:
     
            for i in range(hi, hi-path[lo][hi], -1):
            
                #comp_val+=numbers[i]
                numC=numC+int(numbers[i])
                numbers[i]=0
                buttons[i].pack_forget()
            
            hi-=path[lo][hi]
        
    #i = i+1  
    
    totalC=str(numC)
    finalC.set(totalC)
    isAI = not(isAI)
        
#--------------------------------------------minimax algo-----------------------------------------


def minmax(l,r):

    if l>r:
    
        return 0
    
    if vis[l][r]:
    
        return dp[l][r]
    
    x=-99999999
    a=0 
    
    for i in range(l,r+1):
    
        a += test[i]
        y = a - minmax(i+1,r)
        if y>x:
        
            x=y
            prefix[l][r]=True
            path[l][r]= (i-l)+1
        
        #x=max(x,a-call(i+1,r))
    
    
    a=0
    for i in range(r,l-1,-1):
    
        a+=test[i]
        y= a- minmax(l,i-1)
        if  y>x:
        
            x=y
            prefix[l][r] = False
            path[l][r] = (r-i)+1
        
        #x=max(x,a-call(l,i-1));
    
    vis[l][r] = True
    dp[l][r]=x
    
    return dp[l][r]


#---------------------------------------------delay----------------------------------------------------

def delay(sec):
    for i in range(sec):
        time.sleep(1)
        print(".")
        
#--------------------------------------------- GAME --------------------------------------------

def game():
    
    global lastPressed, window,lo,hi

    test.clear()
    
    #--------------------------------------- LEVEL -------------------------------------------

    while(1):
      level = int(input("Choose a level among 1 to 10: "))
      #delay(1)
      if level>=1 and level<=10:
        print("\n")
        break
      print("Chose a level within the limit!!!") 
      #delay(1)

    play = True
    
    
    #--------------------------------------------------
    
    #path = r'G:/4-1/AI/lab/test.text'
    #assert os.path.isfile(path)
    
    #---------------------------------------- TAKE INPUT FROM TEXT FILE ---------------------------------------

    #with open('/G:/fourone/AI/lab/test.txt', 'r') as file:
    with open('test.txt', 'r') as file:
        input_lines = [line.strip() for line in file]

    #sys.stdin = open('/content/sample_data/test.txt', 'r')

    line_num = 0
    t = int(input_lines[line_num])
    #print(t)
    line_num +=1
    for i in range(t):
        n = int(input_lines[line_num])
        #print(n)
        line_num +=1

        num_list = input_lines[line_num].split()
        line_num +=1

        if ( level == ( ( line_num ) // 2 ) ) :
          len_arr = n
          for j in range(n):
            test.append( int(num_list[j]) )
            #line_num +=1
            #print(num_list[j])
    
    delay(3)
    
    #----------------------------------------- START GAME ----------------------------------------------
    
    valid = [0, len(test)-1]
    #len_test = len(test)
    lo = 0
    hi = len_arr - 1
    
    while play:
        


      # make all the options unvisited intially
      for i in range(lo,hi+1):
        for j in range(lo,hi+1):
          vis[i][j]= False
          
      #------------------------------- CHOOSE FIRST PLAYER ------------------------------
      
      while (1):

        print ("Choose first player..\n1. Computer\n2. You\n")

        choice = int(input("Enter your choice: "))

        if (choice == 1 or choice == 2):
          break

        print("Wrong selection of player!!! Try again..\n\n")

      isAI = True
      if (choice == 2):
        isAI = False
        
      # set initial points to zero
      user_val = 0
      comp_val = 0
      turn = 0


#----------------------------------------SHOW ARRAY --------------------------------------------

      while (lo<=hi):
     
          
          print("available values:")
          for i in range(lo, hi+1):
          
            #print(test[i])
            btn = tk.Button(window, text=test[i], height=1, width=7, command=lambda lastPressed = lastPressed , press = i:show_press(press, lastPressed, valid))
            btn.pack()
            lastPressed += 1
            buttons.append(btn)
          
          print("\n\n")
          
          passBtn = Button(window, text=' PASS', fg='black', bg='red', height=1, width=7, command= lambda: passval(passBtn, lo, hi ))
          passBtn.pack()
        
          
          window.mainloop()


          '''
          curr_size = (hi-lo)+1
          if (not isAI):
              
            # ----------------------------------------- CHOOSE SUFFIX OR PREFIX ---------------------------------
            while (1):
            
                print("Do you want to chose from prefix or suffix\n")
                print("1. Prefix\n2. Suffix\n")
                type = int(input("Enter your choice: "))
                print("\n")
                if (type == 1 or type == 2):
                  break
               
                print("Wrong Selection!!! Try again..\n\n")
            
            #--------------------------------------- HOW MANY CONSECUTIVE VALUE --------------------------------
            
            while (1):

                print("How many consecutive values you want to pick: ")
                lenn = int(input())
                if (lenn<=curr_size and lenn>0):
                
                    print("\n")
                    break
                
                print("Chose within current size!!\n\n")
           
            # -------------------------------------- TAKE ALL USER INPUT ------------------------------------
            if (type == 1):
            
                for i in range(lo, lo+lenn):
                
                    user_val += test[i]
                
                lo+=lenn
            
            else:
            
                for i in range(hi, hi-lenn, -1):
                
                    user_val+=test[i]
                
                hi-=lenn
            

            
            print("After your turn\n")
          
            
          #------------------------------------ COMPUTER PLAYING WITH MINIMAX --------------------------------  
            
          else:
          
              minmax(lo,hi)
              #printf(lo,hi)
              
              print("Please Wait.. Computer is thinking")
              delay(3)
              print("\n\n")

              
              if (prefix[lo][hi]):
              
                  print("Computer has chosen {} values from prefix ".format(path[lo][hi]))
                  #print(path[lo][hi])

                  for i in range(lo, lo+path[lo][hi]):
                  
                      comp_val+=test[i]
                  
                  lo+=path[lo][hi]
              
              else:
              
                  print("Computer has chosen {} values from suffix ".format(path[lo][hi]))
                  #print(path[lo][hi])

                  for i in range(hi, hi-path[lo][hi], -1):
                  
                      comp_val+=test[i]
                  
                  hi-=path[lo][hi]
              

              
              print("\n\nAfter computer's turn\n")
        
          
          #----------------------------- SCORE ------------------------------
          
          print("Your current score: ")
          print(user_val)
          print("Computer's current score:")
          print(comp_val)
          print("\n\n")
          isAI = not isAI


      if (user_val>comp_val):
        
            print("Congratulations!!! You are the winner..\n")
        
      elif (user_val<comp_val):
        
            print("Computer Wins!!! Better luck next time..\n")
        
      else:
        
            print("The match drawn!!!\n")
        
      # ------------------------------- CONTINUATION ------------------------------------
      
      print("\nDo you want to continue?\n")
      print("1. Yes\n2. No\n")

      type = int(input("Enter Choice: "))
      
      if (type != 1):
      
          play=False
      
      print("\n\n")

#-------------------------------------------------------------------------------------------------------------

for i in numbers:
    btn = tk.Button(window, text=i, height=1, width=7, command=lambda lastPressed = lastPressed , press = i:show_press(press,lastPressed))
    btn.pack()
    lastPressed += 1
    buttons.append(btn)  # adding button reference
    
passBtn = Button(window, text=' PASS', fg='black', bg='red', height=1, width=7, command= lambda: passval(passBtn))
passBtn.pack()
    
finalC= StringVar()
finalH= StringVar()
scoreH = Entry(window,textvariable=finalH).place(x=200,y=250)
scoreC = Entry(window,textvariable=finalC).place(x=-0,y=250)
window.mainloop()

'''

game()
























