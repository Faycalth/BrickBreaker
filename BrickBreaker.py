from tkinter import *
from random import randrange
from math import cos,pi,sin
#from sense_hat  import SenseHat
#import pyautogui
import sys
import os

#sense = SenseHat()
stop = 0
speed = 3
score = 1

class Principale(Tk):
    
    def __init__(self,parent,vie=3):
        
        Tk.__init__(self,parent)
        
        #Initialisation des paramètres                                                                                                                                               
        
        self.parent = parent    
        self.flag = 0 #Variable permettant d'empêcher/autoriser, le lancement de la balle
        self.vie = [] 
        self.score = 0

        #On crée une liste contenant autant d'élement que de vie
        
        for i in range(0,vie):
            self.vie.append('')

        #On crée un canevas
            
        can = self.can = Canvas(width=490, height = 500,bg='black')
        can.focus()
        
        #Initialisation des commandes
        can.bind_all('<Key>', self.move)
        can.bind_all('<Return>', self.starter)
        can.bind_all('p',self.pause)
        can.bind_all('<Left>', self.clickButton3)
        can.bind_all('<Up>', self.clickButton2)
        can.bind_all('<Down>', self.clickButton2)
        can.bind_all('<Right>', self.clickButton1)

    
        can.create_rectangle(0,470,492,502,fill='light grey') #Pour les vies et le score

        can.create_text(415,480,text='Score: ')
        self.tscore =  can.create_text(460,480,text='0')
        
        self.tag = can.create_text(250,250,text='Press the joystick to start',fill='white')
        
        self.speedtag = can.create_text(250,300, text='Choose the speed of the ball', fill='white')
        self.speedtag1 = can.create_text(150,325, text='Joystick : Left', fill='white')
        self.speedtag2 = can.create_text(250,325, text='Joystick : Up', fill='white')
        self.speedtag3 = can.create_text(350,325, text='Joystick : Right', fill='white')
        self.speed1 = Button(self, text="Low", command=self.clickButton1);
        self.speed1.place(x=150,y=350);
        self.speed2 = Button(self, text="Medium", command=self.clickButton2);
        self.speed2.place(x=215,y=350);
        self.speed3 = Button(self, text="High", command=self.clickButton3);
        self.speed3.place(x=305,y=350);

        #On crée les balles représentatives des vies
        for i in range(0,vie):
            self.vie[i] = can.create_oval((25*vie)-(25*i),493,(25*vie)-10-(25*i),483,fill='red')

        #On initialise d'autres paramètres
        self.pose = 0 #Pause On/Off
        self.angle = pi/3 #Angle de rebond de la balle
        self.sens = -1 #Sens Haut/Bas de la balle
        self.horizon = 1 #Sens Gauche/Droite de la balle
        
        a = self.lbrique=[] #Liste comportant les briques (pour les supprimers)
        self.l = [] #Coordonnées (tuple) des briques
        b = self.mtextbrique=[]
        self.m = []
        self.c = [] #Colors of all bricks

        coul=['green','yellow','light blue','red','orange'] #Différentes couleurs des briques
        i = 1 #Permet de définir: Résistance des briques/Couleur des briques
        x = 12 #Coordonnées en Abscisses
        y = 40 #Coordonnées en Ordonnées
        
        #On crée les 110 briques du jeu
        
        while x<470:
            a.append([can.create_rectangle(x,y,x+40,y+10,fill=coul[i]),(i%4)+1])
            self.l.append((x,y))
            if coul[i]=='green':
                self.c.append(x)
            y+=12
            i+=1
            b.append([can.create_text(x+20,y-7,text=i, fill='grey')])
            self.m.append((x+20,y-7))
            i = (i%4)
            # i est la résistance de la brique. Si ((i%4)+1) = 3, il faudra taper 3fois la brique
            if y==160:
                x+=43
                y = 40
                
        #Creation de la balle
        self.boule = self.can.create_oval(250,450,260,460,fill='red')                            
        self.coord = [250,450]

        #Creation de la barre(pour les rebonds)
        self.barre = can.create_rectangle(235,470,275,465,fill='light green')
        self.bar = 235

        can.pack()

    def starter(self,event): #Fonction qui démarre les balles
        global stop
        stop = 0
        self.can.delete(self.tag)
        self.disparitionButton()
        if self.flag == 0 and len(self.vie)!=0:
            self.go()
            move = event.keysym = pyautogui.keyDown('space')
            self.flag = 1

    def pause(self,event): #Fonction qui met en pause le jeu
        self.pose+=1
        self.pose = self.pose%2
        if self.pose==0:
            self.go()
            self.can.delete(self.text)
            move = event.keysym = pyautogui.keyDown('space')
        else:
            self.text = self.can.create_text(250,250,text='PAUSE',fill='white')
            move = event.keysym = pyautogui.keyUp('space')
    
    def move(self,event): #Permet de déplacer la barre avec le sense hat
        
        global stop
        
        acceleration = sense.get_accelerometer_raw()
        a= -acceleration['x']*100
        #print (a)
        
        x = event.keysym
        if a < -10:
            x = 'Left'
        if -10 <= a < 10:
            x = 'Middle'
        if a > 10 :
            x = 'Right'
            
        if x == 'Left':                                         
            self.direction = -7
        if x == 'Middle':
            self.direction = 0
        if x == 'Right':
            self.direction = 7

        if x!='Return' and x!='':
            x = self.bar = self.bar+self.direction
            if 5 < x < 455 and self.pose == 0:
                self.can.coords(self.barre,x,470,x+40,465)
            else:
                self.bar-=self.direction

        if stop == 1 :
           pyautogui.keyUp('space')
                
        
    def clickButton1(self,event):
        global speed, score
        speed = 4
        score = 1
        self.disparitionButton()
        
    def clickButton2(self,event):
        global speed, score
        speed = 3
        score = 2
        self.disparitionButton()
        
    def clickButton3(self,event):
        global speed, score
        speed = 2
        score = 3
        self.disparitionButton()
        
    def disparitionButton(self):
        self.can.delete(self.speedtag)
        self.can.delete(self.speedtag1)
        self.can.delete(self.speedtag2)
        self.can.delete(self.speedtag3)
        self.speed1.destroy()
        self.speed2.destroy()
        self.speed3.destroy()
        
        
    def go(self): #Fonction principale, déplace la balle

        global stop, speed, score

        #On modifie les coordonnées de la balle en fonction des précedentes
        x = self.coord[0]
        y = self.coord[1]
        y += (sin(self.angle)*self.sens*5/speed)
        x += ((cos(self.angle))*self.horizon/speed)
        
        self.coord[1]=y
        self.coord[0]=x
        self.can.coords(self.boule,x,y,x+10,y+10)                         
        
        i = 0
        while i<len(self.l):  #Pour chaque brique
            self.textbrique = self.mtextbrique[i][0]
            if self.textbrique:
                self.can.delete(self.textbrique)
            #On vérifie si elles sont en contact avec la balle
            if self.l[i][1]-2 <= y <= self.l[i][1]+12 and self.l[i][0]-2 <= x <= self.l[i][0]+42:
                #Si oui on change de direction
                self.sens = (-1)*self.sens
                self.lbrique[i][1] += -1
                if self.lbrique[i][1] == 0: #Si la brique ne peut plus tenir                          
                    #if self.c[i]:
                        #self.can.create_text(250,250,text='Bonus',fill='white')
                    
                    #On la détruit et on augmente le score
                    self.can.delete(self.lbrique[i][0])
                    self.score+= 20*(len(self.vie))*score
                    
                    texte = str(self.score)
                    self.can.delete(self.tscore)
                    self.tscore = self.can.create_text(460,480,text=texte)
                    
                    del self.lbrique[i]
                    del self.l[i]
                    if len(self.l)==0:
                    #Si il n'y a plus de brique on arrête la balle
                        stop = 1
                break
            i+=1

        #Si la balle tape la barre
        if 460 <= y <= 465 and self.bar-10 < x < self.bar+47:
            #Si c'est sur le coin gauche, un angle plus grand
            if self.bar-10 <= x <= self.bar-5:
                self.angle = 2*pi/3
                self.horizon = 5

            #Si c'est sur le coin droit, un angle plus petit
            if self.bar+37 <= x <= self.bar+47:
                self.angle = pi/5
                self.horizon = 5

            #Sinon l'angle sera dans l'autre sens
            if self.bar+5 < x < self.bar+40:
                self.angle = pi/3

            self.sens = (-1)*self.sens

                
        if x<10 or x>478:  #Si on tape sur le bord gauche/droit
            self.horizon = (-1)*self.horizon
            
        if y<10: #Si on tape le plafond
            self.sens = (-1)*self.sens

        if y>466 and x>self.bar+47 or y>466 and x<self.bar-10:
            #Si on tombe à coté de la barre, on perd une vie
            self.can.delete(self.vie[0])
            del self.vie[0]
            stop = 1
            
        if stop == 1: #Si on a perdu une balle,ou gagné, on remet la balle à sa place
            self.flag=0
            self.sens = (-1)*self.sens
            self.can.coords(self.boule,250,440,260,430)
            self.can.coords(self.barre,235,470,275,465)
            self.bar = 235
            self.coord=[250,440]

        if len(self.vie)==0: #Si on a plus de vie, on écrit 'perdu'#
            self.can.create_text(250,250,text='GAME OVER',fill='white')
            self.restart = Button(self, text='Restart', command=self.restart)
            self.restart.place(x=215,y=350)
            
        if len(self.l)==0:
            self.can.create_text(250,250,text='YOU WIN',fill='white')
            
        if stop ==0 and self.pose==0: #Si on a pas perdu la balle, on recommence
            self.can.after(2,self.go)
            
            
    def restart(self):
        python = sys.executable
        os.execl(python, python, * sys.argv)
            
        
            

            

app = Principale(None) ###We start the app

w = 492 # width for the Tk root
h = 502 # height for the Tk root

# get screen width and height
ws = app.winfo_screenwidth() # width of the screen
hs = app.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

# set the dimensions of the screen
# and where it is placed
app.geometry('%dx%d+%d+%d' % (w, h, x, y))
app.mainloop()
