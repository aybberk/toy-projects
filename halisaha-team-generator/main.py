from random import randint
import string
import random
import pandas as pd
class Player:
    
    def __init__(self,name):

        
        self.name = ''
        self.name = name
        self.attack = calculateAverage(puanlamalar[name])[0]
        self.defence = calculateAverage(puanlamalar[name])[1]
        self.physical = calculateAverage(puanlamalar[name])[2]
        self.overall = None;
        self.setOverall()
        
    def setAttack(self, attack):
        self.attack = attack
        self.setOverall()
        
    def setDefence(self, defence):
        self.defence = defence
        self.setOverall()
        
    def setPhysical(self, physical):
        self.physical = physical
        self.setOverall()
    def setName(self, name):
        self.name = name
    def isAllSet(self):
        attackSet = self.attack != None
        defenceSet = self.defence != None
        physicalSet = self.physical != None
        return (attackSet and defenceSet and physicalSet)
        
    def __str__(self):
        return "Name="+ str(self.name) +"\nOverall="+ str(self.overall)
    
        
    def setOverall(self):
        if self.isAllSet():
            self.overall = (self.attack + self.defence + self.physical) / 3.0

            
    def getOverall(self):
        return self.overall

    
class Team:
    def __init__(self):
        self.name = ''
        self.players = []
        self.attack = 0
        self.defence = 0
        self.physical = 0
        self.overall = 0
    def setName(self, name):
        self.name = name
    
    def addPlayer(self, player):
        self.players.append(player)
        self.attack += player.attack
        self.defence += player.defence
        self.physical += player.physical
        self.overall += player.overall
    
    def removePlayer(self, index):
        removedPlayer = self.players.pop(index)
        self.attack -= removedPlayer.attack
        self.defence -= removedPlayer.defence
        self.physical -= removedPlayer.physical
        self.overall -= removedPlayer.overall  
        return removedPlayer
        
    def printTeam(self):
        print '--------------------------------------\n'
        print "Name: " + self.name + "\nAttack: " + str(self.attack) + "\nDefence: " + str(self.defence) + "\nPhysical: "+str(self.physical)+"\nOverall: "+str(self.overall)+"\n"
        for player in self.players:
            print player.name
        print '--------------------------------------\n'
        

def calculateAverage(player):
    avg = [0, 0, 0]
    counter = 0
    for puanlar in player:
        puanlar = [float(puan) for puan in puanlar.split()]
        if len(puanlar) != 1:
            avg[0] += puanlar[0]
            avg[1] += puanlar[1]
            avg[2] += puanlar[2]
            counter += 1
    avg = [puan/counter for puan in avg]   
    return avg
    
teamBlue = Team()
teamBlue.setName('Team Blue')
teamRed = Team()
teamRed.setName('Team Red')


puanlamalar = pd.read_csv("puanlama.csv")
puanlamalar.set_index('adiniz soyadiniz', inplace = True)
puanlamalar.dropna(inplace = True)

playerList = []
playerList.append(Player('utku uzun'))
playerList.append(Player('ramazan doganay'))
playerList.append(Player('ayberk aydin'))
playerList.append(Player('koray eskiduman'))
playerList.append(Player('furkan gokmen'))
playerList.append(Player('emre bilir'))
playerList.append(Player('burak akyurek'))
playerList.append(Player('ozan bektas'))
playerList.append(Player('zafer taha ozdemir'))
playerList.append(Player('mert keles'))
playerList.append(Player('hasan ekin dogan'))
playerList.append(Player('hasan fatih koksal'))

teamSize = len(playerList)/2

limit = 1
while True:
    for n in range(teamSize):
        teamBlue.addPlayer(playerList.pop(randint(0,len(playerList)-1)))
        teamRed.addPlayer(playerList.pop(randint(0,len(playerList)-1)))
    if abs(teamRed.physical - teamBlue.physical)<limit and abs(teamRed.attack - teamBlue.attack)<limit\
    and abs(teamRed.defence - teamBlue.defence)<limit:
        break
    else:
        for n in range(teamSize):
            playerList.append(teamBlue.removePlayer(0))
            playerList.append(teamRed.removePlayer(0))
            
teamBlue.printTeam()
teamRed.printTeam()




            




