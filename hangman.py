#########################################################
## File Name: hangman.py                               ##
## Description: Starter for Hangman project : CCE-UoA  ##
#########################################################
import pygame
import random
import pyttsx3

pygame.init()
winHeight = 600
winWidth = 900
win=pygame.display.set_mode((winWidth,winHeight))
pygame.display.set_caption("HANGMAN")
#---------------------------------------#
# initialize global variables/constants #
#---------------------------------------#
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)

#-------Colors--------------#
black = (0,0, 0)
white = (255,255,255)
red = (255,0, 0)
green = (0,255,128)
light_green = (40,255,70)
blue = (51,51,255)
light_blue = (102,255,255)

btn_font = pygame.font.SysFont("arial", 20)
guess_font = pygame.font.SysFont("monospace", 24)
lost_font = pygame.font.SysFont('arial', 40)
small_font = pygame.font.SysFont(None,25)
med_font = pygame.font.SysFont(None,50)
large_font = pygame.font.SysFont(None,80)
word = ''
str1 = ""
buttons = []
guessed = []
hangmanPics = [pygame.image.load('C:/Users/Lenovo pc/Desktop/Hangman/Hang_Images\\hangman0.png'), pygame.image.load('C:/Users/Lenovo pc/Desktop/Hangman/Hang_Images\\hangman1.png'), pygame.image.load('C:/Users/Lenovo pc/Desktop/Hangman/Hang_Images\\hangman2.png'), pygame.image.load('C:/Users/Lenovo pc/Desktop/Hangman/Hang_Images\\hangman3.png'), pygame.image.load('C:/Users/Lenovo pc/Desktop/Hangman/Hang_Images\\hangman4.png'), pygame.image.load('C:/Users/Lenovo pc/Desktop/Hangman/Hang_Images\\hangman5.png'), pygame.image.load('C:/Users/Lenovo pc/Desktop/Hangman/Hang_Images\\hangman6.png'), pygame.image.load('C:/Users/Lenovo pc/Desktop/Hangman/Hang_Images\\winner.gif').convert_alpha(), pygame.image.load('C:/Users/Lenovo pc/Desktop/Hangman/Hang_Images\\HighScore.png')]
star_overPics = [pygame.image.load('C:/Users/Lenovo pc/Desktop/Hangman/Hang_Images\\start.jpg')]
QuestionPics =[pygame.image.load('C:/Users/Lenovo pc/Desktop/Hangman/qtns_images\\img1.png'), pygame.image.load('C:/Users/Lenovo pc/Desktop/Hangman/qtns_images\\img2.jpg'), pygame.image.load('C:/Users/Lenovo pc/Desktop/Hangman/qtns_images\\img3.jpg'), pygame.image.load('C:/Users/Lenovo pc/Desktop/Hangman/qtns_images\\img4.jpg'), pygame.image.load('C:/Users/Lenovo pc/Desktop/Hangman/qtns_images\\img5.jpg'), pygame.image.load('C:/Users/Lenovo pc/Desktop/Hangman/qtns_images\\img6.jpg'), pygame.image.load('C:/Users/Lenovo pc/Desktop/Hangman/qtns_images\\img7.jpg'), pygame.image.load('C:/Users/Lenovo pc/Desktop/Hangman/qtns_images\\img8.jpg'), pygame.image.load('C:/Users/Lenovo pc/Desktop/Hangman/qtns_images\\img9.jpg'), pygame.image.load('C:/Users/Lenovo pc/Desktop/Hangman/qtns_images\\img10.jpg'), pygame.image.load('C:/Users/Lenovo pc/Desktop/Hangman/qtns_images\\img11.jpg'), pygame.image.load('C:/Users/Lenovo pc/Desktop/Hangman/qtns_images\\img12.jpg'), pygame.image.load('C:/Users/Lenovo pc/Desktop/Hangman/qtns_images\\img13.jpg'), pygame.image.load('C:/Users/Lenovo pc/Desktop/Hangman/qtns_images\\img14.jpg'), pygame.image.load('C:/Users/Lenovo pc/Desktop/Hangman/qtns_images\\img15.jpg'), pygame.image.load('C:/Users/Lenovo pc/Desktop/Hangman/qtns_images\\img16.jpg'), pygame.image.load('C:/Users/Lenovo pc/Desktop/Hangman/qtns_images\\img17.jpg'), pygame.image.load('C:/Users/Lenovo pc/Desktop/Hangman/qtns_images\\img18.jpg'), pygame.image.load('C:/Users/Lenovo pc/Desktop/Hangman/qtns_images\\img19.jpg'), pygame.image.load('C:/Users/Lenovo pc/Desktop/Hangman/qtns_images\\img20.jpg'), pygame.image.load('C:/Users/Lenovo pc/Desktop/Hangman/qtns_images\\img21.jpg'), pygame.image.load('C:/Users/Lenovo pc/Desktop/Hangman/qtns_images\\img22.jpg'), pygame.image.load('C:/Users/Lenovo pc/Desktop/Hangman/qtns_images\\img23.jpg'), pygame.image.load('C:/Users/Lenovo pc/Desktop/Hangman/qtns_images\\img24.jpg'),pygame.image.load('C:/Users/Lenovo pc/Desktop/Hangman/qtns_images\\img25.jpg')]
trialPics = [pygame.image.load('C:/Users/Lenovo pc/Desktop/Hangman/trialimage\\trial11.jpg'), pygame.image.load('C:/Users/Lenovo pc/Desktop/Hangman/trialimage\\trial13.jpg'), pygame.image.load('C:/Users/Lenovo pc/Desktop/Hangman/trialimage\\think.png')]
music = pygame.mixer.music.load('C:/Users/Lenovo pc/Desktop/Hangman/music\\destination.mp3')
pygame.mixer.music.play(-1)
btn_sound = pygame.mixer.Sound('C:/Users/Lenovo pc/Desktop/Hangman/music\\btn_eft.wav')
limbs = 0
score = 0
h_score = 0
hs_count = 0
Qtn_No = 0
msgcnt = 0
duplicate = []

def speak(audio):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice',voices[0].id)
    engine.say(audio,'Farhan')
    engine.runAndWait()

def redraw_game_window():
    global guessed
    global hangmanPics
    global limbs
    pic = trialPics[1] #"10","12"
    win.blit(pic,(0,0))
    # Buttons
    for i in range(len(buttons)):
        if buttons[i][4]:
            pygame.draw.circle(win, black, (buttons[i][1], buttons[i][2]), buttons[i][3])
            pygame.draw.circle(win, buttons[i][0], (buttons[i][1], buttons[i][2]), buttons[i][3] - 2)
            label = btn_font.render(chr(buttons[i][5]), 1, black)
            win.blit(label, (buttons[i][1] - (label.get_width() / 2), buttons[i][2] - (label.get_height() / 2)))

    spaced = spacedOut(word, guessed)
    label1 = guess_font.render(spaced, 1, black)
    win.blit(label1,(winWidth/6 , 440))
    file = open('C:/Users/Lenovo pc/Desktop/Hangman/text\Score.txt')
    global hs_count
    h_score = file.readlines()
    temp = h_score[0]
    if(score>int(temp)):
        h_score = score
        hs_count = hs_count+1
        if(hs_count==1):
            pic = hangmanPics[8]
            win.blit(pic, (0,0))
            pygame.display.update()
            pygame.time.delay(1000)
            pic = hangmanPics[7]
            win.blit(pic, (0,0))
            pygame.display.update()
            pygame.time.delay(1000)
        file = open("C:/Users/Lenovo pc/Desktop/Hangman/text\Score.txt",'w')
        file.write(str(h_score))
    lblh_s = lost_font.render('High Score : '+str(temp), 1, blue)
    lblscr = lost_font.render('Score : '+str(score), 1, red)
    win.blit(lblh_s, (winWidth-lblh_s.get_width()-10,0))
    win.blit(lblscr, (10, 0))
    pic = hangmanPics[limbs]
    win.blit(pic, (winWidth/2 - pic.get_width()/2 -350, 100))
    QPic = QuestionPics[Qtn_No]
    win.blit(QPic, (winWidth/2 - pic.get_width()/2+150,50))
    #stopWatch(timer)
    pygame.display.update()

def randomWord():
    global Qtn_No
    global str1
    file = open('C:/Users/Lenovo pc/Desktop/Hangman/text\Answer.txt')
    f = file.readlines()
    Qtn_No = random.randrange(0, len(f) - 1)
    global duplicate
    if Qtn_No not in duplicate:
        duplicate.append(Qtn_No)
        file = open('C:/Users/Lenovo pc/Desktop/Hangman/text\Question.txt')
        for i,strq in enumerate(file):
            if(i==Qtn_No):
                str1 = strq
    else:
        randomWord() 
    return f[Qtn_No][:-1]
    


def hang(guess):
    global word
    if guess.lower() not in word.lower():
        return True
    else: 
        return False

def spacedOut(word, guessed=[]):
    spacedWord = ''
    guessedLetters = guessed 
    for x in range(len(word)):
        if word[x] != ' ':
            spacedWord += '_ '
            for i in range(len(guessedLetters)):
                if guessedLetters[i]  == word[x].upper():
                    spacedWord = spacedWord[:-2]
                    spacedWord += word[x].upper() + ' '
        elif word[x] == ' ':
            spacedWord += ' '  
    return spacedWord
            
# Return Button Which Is Pressed
def buttonHit(x, y):
    for i in range(len(buttons)):
        if x < buttons[i][1] + 20 and x > buttons[i][1] - 20:
            if y < buttons[i][2] + 20 and y > buttons[i][2] - 20:
                btn_sound.play()
                return buttons[i][5]
    return None

def reset():
    global limbs
    global guessed
    global buttons
    global word
    for i in range(len(buttons)):
        buttons[i][4] = True
    limbs = 0
    guessed = []
    word = randomWord()

# Setup buttons
def set_button():
    increase = round(winWidth / 13)
    for i in range(26):
        if i < 13:
            y = 505
            x = 30 + (increase * i)
        else:
            x = 30 + (increase * (i - 13))
            y = 555
        buttons.append([light_blue, x, y, 22, True, 65 + i])
        # buttons.append([color, x_pos, y_pos, radius, visible, char])

def speak_qtn():
        pygame.mixer.music.stop()
        speak(str1)
        pygame.mixer.music.play(-1)
        return False

def end(winner=False):
    global limbs
    global score
    global speakqtn
    global msgcnt
    redraw_game_window()
    pygame.time.delay(1000)

    if winner == True:
        speakqtn = True
        pygame.display.update()
        score+=10
        msgcnt+=1

    else:
        speakqtn = True
        global hs_count
        score-=10
        msgcnt=0
        pygame.mixer.music.stop()
        speak('You Are Wrong...')
        message_to_screen("The Word Was : "+word.upper(),black,160,"medium")
        pygame.display.update()
        speak("The Word Was : "+word.upper())
        pygame.time.delay(1000)
    if(score<10 and msgcnt==0):
        score = 0
        win.fill(white)
        message_to_screen("You Lose The Game",red,50,"large")
        message_to_screen('Score : '+str(score),light_green,100,"medium")
        pic = hangmanPics[6]
        win.blit(pic, (winWidth/2-100, 100))
        pygame.display.update()
        speak('You Lose The Game')
        restartGame()
        pygame.time.delay(1000)
        #pygame.quit()
    elif(msgcnt==1):
        speak('Good..........')
    elif(msgcnt==2):
        speak('Awesome........')
    elif(msgcnt>=3):
        speak('Excellent.......')
    if(score==300):
        pic = hangmanPics[7]
        win.blit(pic, (0,0))
        pygame.display.update()
        pygame.time.delay(3000)
        pygame.quit()
    pygame.mixer.music.play(-1)
    pygame.display.update()
    reset()

def text_objects(text,color,size):
    if size == "small":
        textSurface = small_font.render(text,True,color)
    elif size == "medium":
        textSurface = med_font.render(text,True,color)
    elif size == "large":
        textSurface = large_font.render(text,True,color)
    return textSurface, textSurface.get_rect()

def message_to_screen(msg,color,y_displace=0,size = "small"):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = (winWidth/2), (winHeight/2) + y_displace
    win.blit(textSurf,textRect)

def text_to_button(msg,color,button_x,button_y,button_w,button_h,size="small"):
    textSurf,textRect = text_objects(msg,color,size)
    textRect.center = (button_x+button_w/2,button_y+button_h/2)
    win.blit(textSurf,textRect)

def stopWatch(timer):
    while timer > 0:
        lbltime = lost_font.render(str(timer), 1, red)
        win.blit(lbltime,(450,0))
        pygame.display.update()
        pygame.time.sleep(1)
        timer = timer - 1
        #redraw_game_window(timer)

def button(text,button_x,button_y,button_w,button_h,inactive_color,active_color,action = None):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if button_x + button_w > cur[0] > button_x and button_y + button_h > cur[1] > button_y:
        pygame.draw.rect(win,active_color,(button_x,button_y,button_w,button_h),5)
        if click[0] == 1:
            if action == "start":   
                startMenu()  
            if action == "easy":
                gameLoop()
            if action == "medi":
                gameLoop()
            if action == "hard":
                gameLoop()
        

    else:
        pygame.draw.rect(win,inactive_color,(button_x,button_y,button_w,button_h))
    text_to_button(text,black,button_x,button_y,button_w,button_h)

def gameLoop():
    global limbs
    global inPlay
    global speakqtn
    set_button()
    while inPlay:
        redraw_game_window()
        if(speakqtn):
            speakqtn = speak_qtn() 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                inPlay = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    inPlay = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clickPos = pygame.mouse.get_pos()
                letter = buttonHit(clickPos[0], clickPos[1])
                if letter != None:
                    guessed.append(chr(letter))
                    if hang(chr(letter)):
                        if limbs != 5:  
                            limbs += 1
                        else:
                            end()
                    else:
                        if spacedOut(word, guessed).count('_') == 0:
                            end(True)
    pygame.quit()
    quit()

def gameStart():
    start = True
    welcome = True
    while start:
        pic = star_overPics[0]  
        win.blit(pic,(0,0))
        button("Start",350,140,200,75,green,light_green,"start")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    start = False
        pygame.display.update()
        if(welcome):
            speak("Welcome      to      the     world       of      hangman ")
            welcome = False


def startMenu():
    strMenu = True
    while strMenu:
        pic = trialPics[0]
        win.blit(pic,(0,0))
        button("Easy",350,220,200,50,green,light_green,"easy")
        button("Medium",350,280,200,50,green,light_green,"medi")
        button("Hard",350,340,200,50,green,light_green,"hard")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                strMenu = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    strMenu = False
        pygame.display.update()

def restartGame():
    gameOver = True
    while gameOver == True:
        win.fill(white)
        message_to_screen("Game Over",red,-50,"large")
        message_to_screen("Press C to Play Again or Q to Quit",green,10,"medium")
        pygame.display.update()
        speak("Press C to Play Again or Q to Quit")
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    win.fill(white)
                    message_to_screen("I Hope You Enjoy The Game...",green,-100,"medium")
                    message_to_screen("Meet You Again.",green,-30,"medium")
                    message_to_screen("Thanks To Play",green,100,"large")
                    pygame.display.update()
                    speak("I Hope You Enjoy The Game...      Meet You Again.                Thanks To Play")
                    gameOver = False
                    pygame.time.delay(3000)
                    pygame.quit()
                if event.key == pygame.K_c:
                    reset()
                    gameLoop()
            if event.type == pygame.QUIT:
                pygame.quit()
#MAINLINE
word = randomWord()
inPlay = True
speakqtn = True
gameStart()

# always quit pygame when done!