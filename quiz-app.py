###
#   quiz-app.py
#   Written on stream with twitch.tv/CodeNameTribbs
#
#   Entire quiz based on Dungeons and Dragon 5e, because I like it.

# Need to figure out how to generate the questions
# Would like dynamically generated questions based on my own mongodb dataset
import platform
import os
import json

#       UTILITY
def clearTerminal():
    if platform.system() == "Windows": os.system('cls')    
    if platform.system() == "Linux": os.system('clear')
    if platform.system() == "Darwin": os.system('clear')

def sleepTerminal(show:bool=False):
    if show:
        input("Press Any Key To Continue...")
    else:
        input("")

def errorHandler(msg:str, e:Exception=None, sleep:bool=True):
    print(msg)
    if e: print(e)
    if sleep:
        sleepTerminal()

def loadSettings(filename:str) -> dict:
    try:
        with open(filename, "r") as infile:
            data = json.load(infile)    
        return data
    except Exception as e:
        pass
        errorHandler("Error Loading File.", e)

def createSettings(filename:str) -> dict:
    userObj = {
        "name": "",
        "score": 0,
        "time": "00:00:000"
    }
    data = {
        "settings": {
            "name": "",
            "difficulty": 1,
            "quiz-length": 10,
            "timer": False
        },
        "highscores":
            [userObj, userObj, userObj, userObj, userObj],
    }
    try:
        with open(filename, "w") as outfile:
            json.dump(data, outfile, indent=4)
        return data
    except Exception as e:
        errorHandler("Error Creating Setting File.", e)

def saveSettings(filename:str, settings:dict):
    try:
        with open(filename, "w") as savefile:
            json.dump(settings, savefile, indent=4)
    except Exception as e:
        errorHandler(f"Save file failed for {filename}", e)

def updateHighScores(scores:list) -> list:
    return sorted(scores, key=lambda item: item['score'], reverse=True)

#       DISPLAYS
def displayMainMenu():
    text = ""
    text+=f"{'Quiz App Main Menu':_^40}\n"
    text+= "  1.) New Quiz \n"
    text+= "  2.) Highscores \n"
    text+= "  3.) Settings \n"
    text+= " -1.) Exit App \n"
    print(text)

def displaySettings():
    text = ""
    text+=f"{'Settings Menu':_^40}\n"
    text+= "  1.) Set Username \n"
    text+= "  2.) Change difficulty \n"
    text+= "  3.) Toggle Timer \n"
    text+= "  4.) Set Quiz Length \n"
    text+= "  5.) View Settings \n"
    text+= " -1.) Back To Main Menu\n"
    print(text)

def displayHighscores(scores:dict):
    print(f"{'Highscores':_^40}")
    
    for i, item in enumerate(scores):
        if item['name']:
            print(f"{i+1:>3}. {item['name']:<15} {item['score']:<4} {item['time']:<11}")
        else:
            print(f"{i+1:>3}. {'-----':<15} {'---':<4} {'--:--:---':<11}")
        
def displayCurrentSettings(settings:dict):
    print(f"{'Current Settings':_^40}")
    text =f"Set Username: {settings['name']}\n"
    text+=f"Difficult: {settings['difficulty']}\n"
    text+=f"Quiz Length: {settings['quiz-length']}\n"
    text+=f"Timer: {'On' if settings['timer'] else 'Off'}\n"
    print(text)
    
#       MENUS
def menuSettings(settings:dict):
    while True:
        clearTerminal()
        displaySettings()
        inp = input(">> ")
        match inp:
            case "-1": # Back To Main Menu
                break
            case "1": # Set User Name
                clearTerminal()
                print(f"Current name is {settings['name']}")
                inp = input("Enter new username (-1 to go back) :")
                if inp != "-1":
                    settings["name"] = inp
            case "2": # Change Difficulty
                while True:
                    clearTerminal()
                    print(f"Current difficulty is {settings['difficulty']}")
                    inp = input("Enter difficulty (1, 2, 3) -1 to go back: ")
                    if inp in ["1", "2", "3"]:
                        settings["difficulty"] = int(inp)
                        break
                    if inp == "-1":
                        break
                    errorHandler("Please choose valid option.")
            case "3": # Toggle Timer
                while True:
                    clearTerminal()
                    print(f"Currently Timer is {'On' if settings['timer'] else 'Off'}")
                    inp = input("Turn quiz timer (on/off) -1 to go back: ")
                    if inp.lower() == "on":
                        settings['timer'] = True
                    if inp.lower() == "off":
                        settings['timer'] = False
                    if inp in ['off', 'on', '-1']:
                        break
                    errorHandler("Please choose valid option")
            case "4": # set quiz length
                while True:
                    clearTerminal()
                    print(f"Current Quiz Length: {settings['quiz-length']}")
                    inp = input("Enter number of quiz questions. Min 5, Max 100. -1 to go back: ")
                    if inp == "-1":
                        break
                    if inp.isdigit():
                        if int(inp) >= 5 and int(inp) <= 100:
                            settings['quiz-length'] = int(inp)
                            break
                    errorHandler("Enter a valid number or -1 to go back.")
            case "5": # View Settings
                clearTerminal()
                displayCurrentSettings(settings)
                sleepTerminal(show=True)    
            case _:   # Handle invalid cases
                errorHandler("Please choose valid option.")
    return settings

#       QUIZ TIME
def startQuiz(settings:dict) -> dict:
    pass  
    # quiz = [question * settings['quiz-length']]
    # question = {
    #     "msg": "foo?",
    #     "answer": "bar",
    #     "a": "bar",
    #     "b": "car",
    #     "c": "foo",
    #     "d": "hoo"
    # }
    # for question in quiz:
    #   display question['msg']
    #   display choices (question[a-d]) in random order
    #   prompt user for choice
    #   if user choice == question[answer]
    #       log correct answer
    #   else
    #       log incorrect answer
    #   tell user
    #  
    # tally score, show user stats
    # create userObj
    # return userObj

#       APP
def app():
    settings_file = "settings.json"
    settings = None
    if os.path.exists(settings_file):
        settings = loadSettings(settings_file)
    else:
        settings = createSettings(settings_file)
    
    while True:
        clearTerminal()
        displayMainMenu()
        inp = input(">> ")
        match inp:
            case "-1": # Exit Application
                break
            case "1": # Start New Quiz
                pass
            case "2": # View Highscores
                clearTerminal()
                settings['highscores'] = updateHighScores(settings['highscores'])
                displayHighscores(settings['highscores'])
                sleepTerminal(show=True)       
            case "3": # Settings Menu
                settings['settings'] = menuSettings(settings['settings'])                        
                saveSettings(settings_file, settings)
            case _:
                errorHandler("Please choose valid option.")
                
    print("Exit Quiz App")
    sleepTerminal(True)
    clearTerminal()
        
if __name__ == "__main__":
    app()
