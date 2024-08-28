#!/usr/bin/env python
# coding: utf-8

# In[13]:


import cv2
from cvzone.HandTrackingModule import HandDetector
import time

class Button:
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self, img):
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), 
                      (225, 225, 225), cv2.FILLED)
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), 
                      (50, 50, 50), 3)
        cv2.putText(img, self.value, (self.pos[0] + 40, self.pos[1] + 60), cv2.FONT_HERSHEY_PLAIN,
                    2, (50, 50, 50), 2)

    def click(self, x, y):
        if self.pos[0] < x < self.pos[0] + self.width and self.pos[1] < y < self.pos[1] + self.height:
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), 
                          (255, 255, 255), cv2.FILLED)
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), 
                          (50, 50, 50), 3)
            cv2.putText(img, self.value, (self.pos[0] + 20, self.pos[1] + 70), cv2.FONT_HERSHEY_PLAIN,
                        2, (0, 0, 0), 5)
            return True
        else: 
            return False

cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Width
cap.set(4, 720)   # Height
detector = HandDetector(detectionCon=0.8, maxHands=1)

buttonListValues = [['7','8','9','*'],
                    ['4','5','6','-'],
                    ['1','2','3','+'],                 
                    ['0','/','.','=']]

# Creating buttons
buttonList = []
for x in range(4):
    for y in range(4):
        xpos = x * 100 + 800
        ypos = y * 100 + 150
        buttonList.append(Button((xpos, ypos), 100, 100, buttonListValues[y][x]))

# Variables        
myEquation = ''
delayCounter = 0

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    
    # Detect hands
    hands, img = detector.findHands(img, flipType=False)
    
    # Draw the buttons
    for button in buttonList:
        button.draw(img)
    
    # If hands are detected
    if hands:
        lmList = hands[0]['lmList']
        
        # Extract only the (x, y) coordinates
        x1, y1 = lmList[8][:2]
        x2, y2 = lmList[12][:2]
        
        length, _, img = detector.findDistance((x1, y1), (x2, y2), img)
        print(length)
        
        # Extract the x and y coordinates of the 8th landmark
        x, y = lmList[8][:2]  # Only take x and y
        
        if length < 50:
            for i, button in enumerate(buttonList):
                if button.click(x, y) and delayCounter == 0:
                    myValue = buttonListValues[int(i % 4)][int(i // 4)]
                    if myValue == "=":
                        try:
                            myEquation = str(eval(myEquation))
                        except:
                            myEquation = "Error"
                    else:
                        myEquation += myValue
                    delayCounter = 1
                    
    if delayCounter != 0:  
        delayCounter += 1
        if delayCounter > 10:
            delayCounter = 0
    
    # Display the Equation
    cv2.putText(img, myEquation, (810, 120), cv2.FONT_HERSHEY_PLAIN,
                3, (50, 50, 50), 3)
    
    cv2.imshow("Image", img)
    cv2.waitKey(1)


# In[ ]:




