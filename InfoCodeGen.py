from pynput import keyboard
from pynput.keyboard import Key, Controller
from ctypes import windll, create_unicode_buffer
from typing import Optional
from PIL import ImageGrab
import time

GAME_NAME = 'UFO 50'

fileName = ""

#Max Number of Combinations is 38^4 - 1 (reason -1 is because we start at 0) which is 2085135

StartNumber = 10000
EndNumber = 10000

keyBoardController = Controller()

UP = [0, 1]
DOWN = [0, 1]
LEFT = [0, 1]
RIGHT = [0, 1]

currX = 0
currY = 0

InputDirections = {
    'A' : [0, 0],
    'B' : [1, 0],
    'C' : [2, 0],
    'D' : [3, 0],
    'E' : [4, 0],
    'F' : [5, 0],
    'G' : [6, 0],
    'H' : [7, 0],
    'I' : [0, 1],
    'J' : [1, 1],
    'K' : [2, 1],
    'L' : [3, 1],
    'M' : [4, 1],
    'N' : [5, 1],
    'O' : [6, 1],
    'P' : [7, 1],
    'Q' : [0, 2],
    'R' : [1, 2],
    'S' : [2, 2],
    'T' : [3, 2],
    'U' : [4, 2],
    'V' : [5, 2],
    'W' : [6, 2],
    'X' : [7, 2],
    'Y' : [0, 3],
    'Z' : [1, 3],
    '0' : [2, 3],
    '1' : [3, 3],
    '2' : [4, 3],
    '3' : [5, 3],
    '4' : [6, 3],
    '5' : [7, 3],
    '6' : [0, 4],
    '7' : [1, 4],
    '8' : [2, 4],
    '9' : [3, 4],
    '?' : [4, 4],
    '!' : [5, 4],
}

digit = "{number:04d}"

def getForegroundWindowTitle() -> Optional[str]:
    hWnd = windll.user32.GetForegroundWindow()
    length = windll.user32.GetWindowTextLengthW(hWnd)
    buf = create_unicode_buffer(length + 1)
    windll.user32.GetWindowTextW(hWnd, buf, length + 1)
    

    # 1-liner alternative: return buf.value if buf.value else None
    if buf.value:
        return buf.value
    else:
        return None

def doNextEntry(value):
    title = getForegroundWindowTitle()

    if (title != GAME_NAME):
        print("Focused window not correct name!")
        exit(1)

    global currX 
    currX = 0
    global currY 
    currY= 0

    directionList = splitIntoBase38(value)

    for directions in directionList:
        setGoal(directions[0], directions[1])
        
        keyBoardController.press('z')
        keyBoardController.release('z')

        time.sleep(0.1)

        setGoal(0, 0)
    
    time.sleep(3.0)

    print(digit.format(number = StartNumber) + " - " + fileName)
    newImage = ImageGrab.grab()
    newImage.save("./screenshots/" + fileName + ".png")
    
def setGoal(endX, endY):
    global currX 
    global currY

    while currX != endX:
        if (currX < endX):
            keyBoardController.press(Key.right)
            keyBoardController.release(Key.right)
            currX += 1
        else:
            keyBoardController.press(Key.left)
            keyBoardController.release(Key.left)
            currX -= 1
        
        time.sleep(0.1)

    time.sleep(0.1)

    while currY != endY:
        if (currY < endY):
            keyBoardController.press(Key.down)
            keyBoardController.release(Key.down)
            currY += 1
        else:
            keyBoardController.press(Key.up)
            keyBoardController.release(Key.up)
            currY -= 1
        
        time.sleep(0.1)

    time.sleep(0.1)

def splitIntoBase38(value):
    InputDirectionsList = list(InputDirections.items())
    numberList = []
    result = []

    nonResult = []

    while value > 0:
        numberList.insert(0, value % 38)
        value //= 38
    
    while len(numberList) < 4:
        numberList.insert(0, 0)

    for i in range(3, -1, -1):
        nonResult.append(InputDirectionsList[numberList[i]][0])
        result.append(InputDirectionsList[numberList[i]][1])


    nonResult.insert(0, InputDirectionsList[14][0])
    nonResult.insert(0, InputDirectionsList[5][0])
    nonResult.insert(0, InputDirectionsList[13][0])
    nonResult.insert(0, InputDirectionsList[8][0])

    result.insert(0, InputDirectionsList[14][1])
    result.insert(0, InputDirectionsList[5][1])
    result.insert(0, InputDirectionsList[13][1])
    result.insert(0, InputDirectionsList[8][1])

    global fileName
    fileName = ''.join(nonResult)
    fileName = fileName[4:8]
    fileName = fileName.replace('?', 'x')

    return result

def startDoingStuff():
    for i in range(StartNumber, EndNumber + 1):
        doNextEntry(i)
    
    print("Finished displaying games between: " + digit.format(number = StartNumber) + " and " + digit.format(number = EndNumber))
    exit(0)

with keyboard.GlobalHotKeys({'<ctrl>+<alt>+j': startDoingStuff}) as h:
    h.join()
