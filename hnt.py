import pygame
import random

plate = 0
while plate < 1 or plate > 10:
    plate = int(input("Nhập số đĩa từ 1 đến 10: "))

fps = 90 * plate

dis_width = 120 * plate + 100
dis_height = 100 * plate + 100

towerColor = (0, 0, 0)
plateColor = (74, 187, 35)

pygame.init()
window = pygame.display.set_mode((dis_width, dis_height))
backgroundImage = pygame.image.load('bg.jpg')
pygame.display.flip()

towerTop = []
towerList = []
towerPlate = []
plateLocation = []

clock = pygame.time.Clock()

def setup():
    for i in range(3):
        towerList.append([])
        towerTop.append([])
        towerPlate.append([])
    for i in range(plate):
        plateLocation.append([])

def setupTower():
    bottomLength = 5 + ((plate - 1) * 2)
    for i in range(3):
        towerX = dis_width * (1 / 4) + (i * dis_width * (1 / 4))
        towerY = dis_height * (3 / 4)
        towerList[i] = [towerX, towerY]
        for j in range(plate + 1):
            x = towerX
            y = towerY - ((j + 1) * 10)
            pygame.draw.rect(window, towerColor, [x, y, 10, 10])

        towerTop[i] = [towerX, towerY - ((plate + 3) * 10)]

        for j in range(bottomLength):
            x = towerX - (10 + plate * 10) + (j * 10)
            y = towerY
            pygame.draw.rect(window, towerColor, [x, y, 10, 10])

def getTowerLocation(tower):
    if tower > 3:
        tower = 3
    if tower < 1:
        tower = 1
    return towerList[tower - 1]

def getTowerPlateSize(tower):
    if tower > 3:
        tower = 3
    if tower < 1:
        tower = 1
    return len(towerPlate[tower - 1])

def getPlateIndex(tower, plate):
    if tower > 3:
        tower = 3
    if tower < 1:
        tower = 1
    if towerPlate[tower - 1].count(plate) == 0:
        return -1
    else:
        return towerPlate[tower - 1].index(plate)

def displayTower(tower, plateSize):
    plateIndex = getPlateIndex(tower, plateSize)
    if plateIndex == -1:
        return
    towerLocation = getTowerLocation(tower)
    towerPlateSize = getTowerPlateSize(tower)
    plateLength = 3 + ((plateSize - 1) * 2)
    plateX = towerLocation[0]
    plateY = towerLocation[1]
    for j in range(plateLength):
        x = plateX - (10 + plate * 10) + (j * 10) + (((plate - plateSize) + 1) * 10)
        y = plateY - (plateIndex + 1) * 10
        pygame.draw.rect(window, plateColor, [x, y, 10, 10])  

def predictLocation(tower, plateSize):
    plateIndex = getPlateIndex(tower, plateSize)
    towerLocation = getTowerLocation(tower)
    towerPlateSize = getTowerPlateSize(tower)
    plateLength = 3 + ((plateSize - 1) * 2)
    plateX = towerLocation[0]
    plateY = towerLocation[1] - (plateIndex + 1) * 10
    return [plateX, plateY]

def putLocation(tower, plateSize):
    plateIndex = getPlateIndex(tower, plateSize)
    towerLocation = getTowerLocation(tower)
    towerPlateSize = getTowerPlateSize(tower)
    plateLength = 3 + ((plateSize - 1) * 2)
    plateX = towerLocation[0]
    plateY = towerLocation[1] - (plateIndex + 1) * 10
    plateLocation[plateSize - 1] = [plateX, plateY]

def putPlateToTower(tower, plateSize):
    if towerPlate[tower - 1].count(plateSize) == 0:
        towerPlate[tower - 1].append(plateSize)
        putLocation(tower, plateSize)

def plateToTower(plateSize):
    for i in range(plate):
        plateList = towerPlate[i]
        for p in plateList:
            if p == plateSize:
                return i + 1
    return -1

def rotateLocationPlate(plate, dir):
    if dir != None:
        for i in range(plate):
            if plate == i + 1:
                curLoc = plateLocation[i]
                plateLocation[i][0] += dir[0]
                plateLocation[i][1] += dir[1]

def movePlate(plate, towerTo):
    towerFrom = plateToTower(plate)
    towerPlate[towerFrom - 1].remove(plate)
    towerPlate[towerTo - 1].append(plate)

def reloadPlate():
    plateSize = 1
    for loc in plateLocation:
        plateX = loc[0]
        plateY = loc[1]
        plateLength = 3 + ((plateSize - 1) * 2)
        for j in range(plateLength):
            x = plateX - (10 + plate * 10) + (j * 10) + (((plate - plateSize) + 1) * 10)
            y = plateY
            pygame.draw.rect(window, plateColor, [x, y, 10, 10])

        plateSize += 1

def rotatePlate(plateSize, plateFrom, plateTo):
    rotating = True
    rotatePlate = plateSize
    rotateTowerTo = plateTo
    rotateTo = towerTop[plateToTower(rotatePlate) - 1]
    rotateState = "up"
    while True:
        for event in pygame.event.get():
            pass

        if not rotating:
            break

        loc = plateLocation[rotatePlate - 1]
        plateX = loc[0]
        plateY = loc[1]
        toX = rotateTo[0]
        toY = rotateTo[1]
        dir = None

        if plateX == toX and plateY != toY:
            if plateY < toY:
                dir = [0, 1]
            elif plateY > toY:
                dir = [0, -1]
        elif plateY == toY and plateX != toX:
            if plateX < toX:
                dir = [1, 0]
            elif plateX > toX:
                dir = [-1, 0]
        else:
            if rotateState == "up":
                rotateState = "top"
                rotateTo = towerTop[rotateTowerTo - 1]
            elif rotateState == "top":
                rotateState = "tower"
                movePlate(rotatePlate, rotateTowerTo)
                rotateTo = predictLocation(rotateTowerTo, rotatePlate)
            else:
                rotating = False
                rotatePlate = 0
                rotateTowerTo = 0
                rotateTo = []
                rotateState = ""
        rotateLocationPlate(rotatePlate, dir)

        window.blit(pygame.transform.scale(backgroundImage, (dis_width, dis_height)), (0, 0))
        setupTower()
        reloadPlate()

        pygame.display.update()
        clock.tick(fps)
        print(f"{plateLocation}")

def hnt(plateSize, plateFrom, plateTo, plateAux):
    if plateSize == 0:
        return
    else:
        hnt(plateSize - 1, plateFrom, plateAux, plateTo)
        rotatePlate(plateSize, plateFrom, plateTo)
        hnt(plateSize - 1, plateAux, plateTo, plateFrom)

def run():
    setup()
    setupTower()
    for i in range(plate, 0, -1):
        putPlateToTower(1, i)

    hnt(plate, 1, 3, 2)

run()
print("done lmaooooooooooooooo")
while True:
    for event in pygame.event.get():
        pass
