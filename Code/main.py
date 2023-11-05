import touch
import device
import display
import time
import uos
import gc
import screens.logo as logo
import screens.arrows as arrows


powerBarVisible = False
onDisplay = {}
activeElement = 0
current_dir = "/projects"
lines = {}


def wait(arg):
    pass

def buttons(arg):
    gc.collect()
    if arg == touch.BOTH:
        battery()
    if arg == touch.A:
        right_button_function("A")
    if arg == touch.B:
        left_button_function("B")
    

def left_button_function(button):
    selectNext()
    
def selectNext():
    global onDisplay, activeElement
    activeElement += 1
    if activeElement >= len(onDisplay[1]):
        activeElement = 0
    list_the_directorys()

        
def right_button_function(button):
    global onDisplay, activeElement, current_dir
    # from lines the activeElement is used to get the name of the directory then if the directory ends with .py it will run the file
    for i, item in enumerate(lines):
        if i == activeElement:
            if lines[i]['name'].endswith(".py"):
                file_name = lines[i]['name']  # Get the name of the Python file
                file_path = current_dir + "/" + file_name  # Construct the full file path
                with open(file_path, "r") as file:
                    file_contents = file.read()  # Read the file contents
                try:
                    # exec(file_contents)  # Execute the file contents
                    exec(file_contents, {})
                except Exception as e:
                    print(f"Error executing {file_name}: {e}")
                return

    # from lines the activeElement is used to get the name of the directory then the current_dir is appended to the directory name
    for i, item in enumerate(lines):
        if i == activeElement:
            current_dir += f"/{lines[i]['name']}"
            list_the_directorys()
            return
      
      
def list_the_directorys():
    global onDisplay, activeElement, current_dir, lines
    fileTree = []
    formatted_lines = []
    directory_text = []
    
   
    display.CLEAR
    
    for item in uos.ilistdir(current_dir):                                                                  # 17. This gets the directorys in the current directory
        if (item[1] & 0x4000) == 0x4000:                                                                    # 18. Checks if the item is a directory (comes from chatGPT, detailed process unknown)
            fileTree.append(item[0])                                                                        # 19. IF the item is a Folder, it Appends the directory name to the fileTree list.
    
                    
    if len(fileTree) == 0:                                                                                  # 20. If there is no directory in the current directory, show all files instead
        fileTree = []
        lines = {}
        activeElement = 0
        for item in uos.ilistdir(current_dir):
            fileTree.append(item[0])
    

    #                                                                                                       # 21. display.show can work with a list [] of items, so we can add multiple items to the screen at once
    directory_text.append(display.Text("List of Directories:", 0, 0, display.BLUE))                         # 22. Starting here with a Title              
    
    for i, item in enumerate(fileTree):                                                                     # 23. This loops through the fileTree list and gives each item a number (i) and a name (item)
        lines[i] = {'name': item, 'active': False}                                                          # 24. This adds the item to the lines dictionary {} with the number (i) as the key and the name (item) as the value
        
    for i, item in enumerate(lines):                                                                        # 25. We can not realy print a dictionary, so we need to format the text to be able to print it
        if i == activeElement:                                                                              # 26. If the item is the activeElement, it will be formatted with a ">" in front of it and in green
            lines[i]['active'] = True                                                                       # 27. This sets the key "active" in the lines dictionary to True              
            formatted_lines.append(display.Text(f"> {lines[i]['name']}", 0, (50*i)+50, display.GREEN))      
        else:                                                                                               # 28. Else the item will be formatted with nothing in front of it and in blue
            lines[i]['active'] = False
            formatted_lines.append(display.Text(f"  {lines[i]['name']}", 0, (50*i)+50, display.BLUE))

    directory_text.append(formatted_lines)                                                                  # 29. This adds the formatted_lines to the directory_text list where until now only the title was in
    directory_text.append(arrows.arrows.screen)                                                             # 30. This adds the arrows to the directory_text list - the arrowsa are in a seperate file in the screens folder - screens can be simple created with the vscode mononocle plugin
        
    onDisplay = directory_text                                                                              # 31. Since i need to change the onDisplay variable elsewhere, it is global and gets reset here
    display.show(onDisplay)


def logoDisplay():
    print("### \t Logo Display ###")
    speed = 0.2
    display.brightness(1)
    display.show(logo.logo.screen)
    time.sleep(speed)
    display.brightness(2)
    display.show(logo.logo.screen)
    time.sleep(speed)
    display.brightness(3)
    display.show(logo.logo.screen)
    time.sleep(speed)
    display.brightness(4)
    display.show(logo.logo.screen)
    time.sleep(speed)
    display.brightness(3)



    
def main():
    touch.callback(touch.EITHER, buttons)                                                                   # 14. This gives the touch buttons a function to run when pressed            
    print(f"### \t Battery: {device.battery_level()}% ###")                                                 # 15. This logs the battery level
    list_the_directorys()                                                                                   # 16. This lists the directorys in the current directory           
    
def init():                                                                                                 # 2. This function gives the user time to take the mononocle out of the case and put it on and displays my Logo
    print("### \t Init ###")                                                                                # 3. This logs the start of the init function
    touch.callback(touch.EITHER, wait)                                                                      # 4. This gives the touch buttons a function that just does nothing
    logoDisplay()                                                                                           # 5. This displays my logo 
    
    s = 10                                                                                                  # 6. S is the number of seconds the user has to put the mononocle on
    while s>=1 :                                                                                            # 7. "While s is greater than or equal to 1, do the following:"
        countdown_text = display.Text(f"{s}", display.WIDTH/2, display.HEIGHT/2, display.GREEN)                 # 8. display.Text is the syntax for cresting text
        display.show(countdown_text)                                                                            # 9. To display anything (like text) you need to use display.show) - we could also: display.show(display.Text())                    
        s -= 1                                                                                                  # 10. This is the same as s = s - 1
        time.sleep(1)                                                                                           # 11. This Stops the program for 1 second
    
    display.show(display.Text("Welcome, User", display.WIDTH/2, display.HEIGHT/2, display.BLUE))            # 12. This displays the text "Welcome, User" in the middle of the screen
    time.sleep(1)
    main()                                                                                                  # 13. This runs the main function                 
    
# 1. Init - Starts the program
init()
