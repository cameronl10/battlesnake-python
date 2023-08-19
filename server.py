import os
import random
import math
import cherrypy
from datetime import datetime
import numpy as np



"""
SBEEVESNAKE IS SWAG
WIPING OUT TOMATO TOWN ONE STEP AT A TIME
COPYRIGHT TO YO MAMA CORP. ALL RIGHTS RESERVED
"""

class Battlesnake(object):
    nextMove = 0
    @cherrypy.expose
    @cherrypy.tools.json_out()

    def index(self):
        # This function is called when you register your Battlesnake on play.battlesnake.com
        # It controls your Battlesnake appearance and author permissions.
        # TIP: If you open your Battlesnake URL in browser you should see this data
        return {
            "apiversion": "1",
            "author": "cameron",  # TODO: Your Battlesnake Username
            "color": "#EAD3F0",  # TODO: Personalize
            "head": "pixel",  # TODO: Personalize
            "tail": "sharp",  # TODO: Personalize
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    
    def start(self):
        # This function is called everytime your snake is entered into a game.
        # cherrypy.request.json contains information about the game that's about to be played.
        data = cherrypy.request.json
        boardheight = data['board']['height']
        boardwidth = data['board']['width']

        print("\n")
        print(
            "!#!#!#!#!#!#!#!!#!#!#!#!#!#!#!START!#!#!#!#!#!#!#!!#!#!#!#!#!#!#!"
        )
        print("Board Height")
        print(boardheight)
        print("Board Width")
        print(boardwidth)
        now = datetime.now()

        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)
        return "ok"


    def getBoardHeight(self):
        data = cherrypy.request.json
        return data['board']['height']


    def getBoardWidth(self):
        data = cherrypy.request.json
        return data['board']['width']


    ##########################################
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()

    def move(self):
        # Valid moves are "up", "down", "left", or "right".
        global nextMove

        data = cherrypy.request.json
        food = data['board']['food']
        headPosX = data['you']['head']['x']
        headPosY = data['you']['head']['y']
        status = ""
        sortedFood = self.sortFoodArray(food)
        ping = data['you']['latency']
        
        prevDir = self.nextMove
        ableToMove = True
        finalMove = 0

        ##Illegal moves array

        illegalMoves = self.illegalMove(prevDir)

        ##Sets up the board 2d array
     
        boardArray = []

        for r in range(self.getBoardHeight()):
            row = []
            for c in range(self.getBoardWidth()):
                row.append(0)
            boardArray.append(row)

        ##Sets up snakes position array

        allSnakes = data['board']['snakes']
        snakeBodiesArray = [[0, 0], [0, 0]]
        snakeBodiesArray.pop(0)
        snakeBodiesArray.pop(0)
        snakeHeadSpaceArray = [[0, 0], [0, 0]]
        snakeHeadSpaceArray.pop(0)
        snakeHeadSpaceArray.pop(0)
        
        for i in range(len(allSnakes)):
            for j in range(len(allSnakes[i]['body']) - 1):
                snakeBodiesArray.append([allSnakes[i]['body'][j]['x'],allSnakes[i]['body'][j]['y']])
                if allSnakes[i]['id'] != data['you']['id'] and allSnakes[i]['length'] >= data['you']['length']:
                    snakeHeadSpaceArray.append([allSnakes[i]['head']['x'] + 1, allSnakes[i]['head']['y']])

                    snakeHeadSpaceArray.append([allSnakes[i]['head']['x'] - 1, allSnakes[i]['head']['y']])

                    snakeHeadSpaceArray.append([allSnakes[i]['head']['x'], allSnakes[i]['head']['y'] + 1])

                    snakeHeadSpaceArray.append([allSnakes[i]['head']['x'], allSnakes[i]['head']['y'] - 1])

        for i in range(len(snakeBodiesArray)):
            boardArray[self.getBoardHeight() - snakeBodiesArray[i][1] - 1][snakeBodiesArray[i][0]] = 1

        ##for i in range(len(snakeHeadSpaceArray)):
        ##    if boardArray[self.getBoardHeight() - snakeHeadSpaceArray[i][1] - 1][snakeHeadSpaceArray[i][0]] != 1:
        ##        boardArray[self.getBoardHeight() - snakeHeadSpaceArray[i][1] - 1][snakeHeadSpaceArray[i][0]] = 2

        ##DECIDING WHERE TO MOVE || Currently going to closest food, after we will take into account of other snake positions
        
        threshold = 100
        curHealth = data['you']['health']




        if curHealth < threshold:

            ##HUNT
            status = "Hunting"

            if sortedFood[0]['x'] < headPosX and sortedFood[0]['y'] > headPosY:
                if self.ableToMoveCheck(3,illegalMoves):
                    self.nextMove = 3
                elif self.ableToMoveCheck(0,illegalMoves):
                        self.nextMove = 0
                elif self.ableToMoveCheck(2,illegalMoves):
                        self.nextMove = 2 
                elif self.ableToMoveCheck(1,illegalMoves):
                        self.nextMove = 1 
            elif sortedFood[0]['x'] == headPosX and sortedFood[0]['y'] > headPosY:
                if self.ableToMoveCheck(0,illegalMoves):
                    self.nextMove = 0
                elif self.ableToMoveCheck(1,illegalMoves):
                        self.nextMove = 1
                elif self.ableToMoveCheck(3,illegalMoves):
                        self.nextMove = 3 
                elif self.ableToMoveCheck(2,illegalMoves):
                        self.nextMove = 2
            elif sortedFood[0]['x'] > headPosX and sortedFood[0]['y'] > headPosY:
                if self.ableToMoveCheck(1,illegalMoves):
                    self.nextMove = 1
                elif self.ableToMoveCheck(0,illegalMoves):
                        self.nextMove = 0
                elif self.ableToMoveCheck(3,illegalMoves):
                        self.nextMove = 3 
                elif self.ableToMoveCheck(2,illegalMoves):
                        self.nextMove = 2
            elif sortedFood[0]['x'] < headPosX and sortedFood[0]['y'] == headPosY:
                if self.ableToMoveCheck(3,illegalMoves):
                    self.nextMove = 3
                elif self.ableToMoveCheck(2,illegalMoves):
                        self.nextMove = 2
                elif self.ableToMoveCheck(0,illegalMoves):
                        self.nextMove = 0 
                elif self.ableToMoveCheck(1,illegalMoves):
                        self.nextMove = 1
            elif sortedFood[0]['x'] > headPosX and sortedFood[0]['y'] == headPosY:
                if self.ableToMoveCheck(1,illegalMoves):
                    self.nextMove = 1
                elif self.ableToMoveCheck(0,illegalMoves):
                        self.nextMove = 0
                elif self.ableToMoveCheck(2,illegalMoves):
                        self.nextMove = 2 
                elif self.ableToMoveCheck(3,illegalMoves):
                        self.nextMove = 3 
            elif sortedFood[0]['x'] < headPosX and sortedFood[0]['y'] < headPosY:
                if self.ableToMoveCheck(3,illegalMoves):
                    self.nextMove = 3
                elif self.ableToMoveCheck(2,illegalMoves):
                        self.nextMove = 2
                elif self.ableToMoveCheck(1,illegalMoves):
                        self.nextMove = 1 
                elif self.ableToMoveCheck(0,illegalMoves):
                        self.nextMove = 0
            elif sortedFood[0]['x'] == headPosX and sortedFood[0]['y'] < headPosY:
                if self.ableToMoveCheck(2,illegalMoves):
                    self.nextMove = 2
                elif self.ableToMoveCheck(1,illegalMoves):
                        self.nextMove = 1
                elif self.ableToMoveCheck(3,illegalMoves):
                        self.nextMove = 3 
                elif self.ableToMoveCheck(0,illegalMoves):
                        self.nextMove = 0
            elif sortedFood[0]['x'] > headPosX and sortedFood[0]['y'] < headPosY:
                if self.ableToMoveCheck(2,illegalMoves):
                    self.nextMove = 2
                elif self.ableToMoveCheck(1,illegalMoves):
                        self.nextMove = 1
                elif self.ableToMoveCheck(3,illegalMoves):
                        self.nextMove = 3 
                elif self.ableToMoveCheck(0,illegalMoves):
                        self.nextMove = 0      
            
        ##IDLEING kinda trash ngl
        else:
            status = "Idling"
            counter = 0
            for i in range(4):
                self.nextMove = i
                for j in range(len(illegalMoves)):
                    if illegalMoves[j] == self.nextMove:
                        ableToMove = False
                if ableToMove:
                    break
                else:
                    ableToMove = True
                    counter+=1

            if counter == 4:
                self.nextMove = prevDir
        
        ##PRINTING

        print("")
        print("")
        print("!#!#!#!#!#!#!#!!#!#!#!#!#!#!#!PRINTING!#!#!#!#!#!#!#!!#!#!#!#!#!#!#!")

        print(f"Turn Number: {data['turn']}")

        print(f"Status: {status}")
        
        print(f"Ping: {ping}ms")

        print(f"Health: {curHealth}")

        print("Closest Food:")
        print(sortedFood[0])
    
        print("Current Head Position:")
        print(data['you']['head'])

        print("Illegal Moves:")
        print(illegalMoves)

        print("Board Array:")
        print(np.array(boardArray))


        #TRANSLATOR
        if self.nextMove == 0:
            finalMove = "up"
        elif self.nextMove == 1:
            finalMove = "right"
        elif self.nextMove == 2:
            finalMove = "down"
        else:
            finalMove = "left"
        print(f"Final Move: {finalMove}")

        print("!#!#!#!#!#!#!#!!#!#!#!#!#!#!END_OF_PRINT!#!#!#!#!#!#!!#!#!#!#!#!#!#!")
        print("")
        print("")

        return {"move": finalMove}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    ##########################################

    def ableToMoveCheck(self, move, illegalMoves):
        
        for j in range(len(illegalMoves)):
            if illegalMoves[j] == move:
                return False
        return True


    def sortFoodArray(self, food):
        ##print("check sFA 1")
        data = cherrypy.request.json
        
        sortedFood = food.copy()
        finalSortedFood = food.copy()
        
        headPosX = data['you']['head']['x']
        headPosY = data['you']['head']['y']
        distance = 0

        foodDistances = [[0, 0], [0, 0]]
        ##print("check sFA 2")
        for i in range(len(sortedFood)):
            ####print("check sFA 3")
            distance = abs(headPosX - data['board']['food'][i]['x']) + abs(headPosY - data['board']['food'][i]['y'])

            ##print('distance')
            ##print(distance) 
            
            foodDistances.append([distance, i])
            
            ##print('foodDistances')
            ##print(foodDistances)

        foodDistances.pop(0)
        foodDistances.pop(0)
                
        foodDistances.sort()

        ##print('check sFA 4')

        for i in range(len(foodDistances)):
            finalSortedFood.insert(i, data['board']['food'][foodDistances[i][1]])
            finalSortedFood.pop(i+1) 

        ##print('final')
        ##print(finalSortedFood)

        return finalSortedFood   


    def illegalMove(self,prevDir):
        data = cherrypy.request.json
        illegalMoveset = []
        bodyArray = data['you']['body'].copy()
        snakes = data['board']['snakes'].copy()
        transBodyArray = [[0, 0], [0, 0]]
        transBodyArray.pop(0)
        transBodyArray.pop(0)
        
        for i in range(len(snakes)):
            if snakes[i]['id'] != data['you']['id']:
                for j in range(len(snakes[i]['body']) - 1):
                    transBodyArray.append([snakes[i]['body'][j]['x'],snakes[i]['body'][j]['y']])

                if snakes[i]['length'] >= data['you']['length']:

                    transBodyArray.append([snakes[i]['head']['x'] + 1, snakes[i]['head']['y']])

                    transBodyArray.append([snakes[i]['head']['x'] - 1, snakes[i]['head']['y']])

                    transBodyArray.append([snakes[i]['head']['x'], snakes[i]['head']['y'] + 1])

                    transBodyArray.append([snakes[i]['head']['x'], snakes[i]['head']['y'] - 1])
        
        for i in range(len(bodyArray) - 1):
            transBodyArray.append([bodyArray[i]['x'], bodyArray[i]['y']])
        
        directionsNextMove = [[data['you']['head']['x'] + 1, data['you']['head']['y']], [data['you']['head']['x'] - 1, data['you']['head']['y']], [data['you']['head']['x'], data['you']['head']['y'] + 1], [data['you']['head']['x'], data['you']['head']['y'] - 1]]

        ##print("Next moves array")
        ##print(directionsNextMove)
        
        ##print("All snake locations")
        ##print(transBodyArray)
        
        ##CHECKING WALLS
        if data['you']['head']['x'] == self.getBoardWidth() - 1 or directionsNextMove[0] in transBodyArray: 
            illegalMoveset.append(1)
        if data['you']['head']['x'] == 0 or directionsNextMove[1] in transBodyArray:
            illegalMoveset.append(3)
        ##CHECKING CEILING AND FLOOR
        if data['you']['head']['y'] == self.getBoardHeight() - 1 or directionsNextMove[2] in transBodyArray:
            illegalMoveset.append(0)
        if data['you']['head']['y'] == 0 or directionsNextMove[3] in transBodyArray:
            illegalMoveset.append(2)
        

        if (prevDir + 2) % 4 not in illegalMoveset:
            illegalMoveset.append((prevDir + 2) % 4)
        
        #returns list of illegal moves

        return illegalMoveset


    ##def tBoneCheck(self,prevDir):


    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.
        data = cherrypy.request.json

        print(
            "!#!#!#!#!#!#!#!!#!#!#!#!#!#!#!END!#!#!#!#!#!#!#!!#!#!#!#!#!#!#!")

        print("\n")
        return "ok"


if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update({
        "server.socket_port":
        int(os.environ.get("PORT", "8080")),
    })
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
