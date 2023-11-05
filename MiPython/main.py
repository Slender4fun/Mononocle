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
current_dir = "/"
lines = {}


# this would be used to set the time zone and time
#     time.zone("1:00")
#     time.time(1698971886)

def display_countdown(value):
    countdown_text = display.Text(f"{value}", display.WIDTH/2, display.HEIGHT/2, display.GREEN)
    display.show(countdown_text)

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
    pass
    
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
    
    
    
    
    
# def right_button_function(button):
#     global powerBarVisible, onDisplay
    # if powerBarVisible == False:
    #     stash = onDisplay
    #     battery()
    #     powerBarVisible = True
    # elif powerBarVisible == True:
    #     onDisplay = stash
    #     display.show(onDisplay)
    #     powerBarVisible = False
    
    
    
    
# def battery():
#     global onDisplay
#     battery_level = device.battery_level()
#     if battery_level >= 40:
#         display.show(display.Text(f"{device.battery_level()}%", 0, 0, display.GREEN))
#         return
#     elif battery_level < 40:
#         display.show(display.Text(f"{device.battery_level()}%", 0, 0, display.RED))
#         return

def battery():
    global onDisplay
    stash = []
    stash.append(onDisplay)
    # stash.append(battery_status.battery_icon())
    stash.append(battery_status.battery_line())
    onDisplay = stash
    display.show(onDisplay)
      
      
      
def list_the_directorys():
    global onDisplay, activeElement, current_dir, lines
    fileTree = []
    formatted_lines = []
    directory_text = []
    
   
    display.CLEAR
    
    for item in uos.ilistdir(current_dir):
        if (item[1] & 0x4000) == 0x4000:                # Check if the item is a directory
            fileTree.append(item[0])                    # Append the directory name to the fileTree list.
    
    # if there is no directorys in the current directory show all files
    if len(fileTree) == 0:
        fileTree = []
        lines = {}
        activeElement = 0
        for item in uos.ilistdir(current_dir):
            fileTree.append(item[0])
    

    directory_text.append(display.Text("List of Directories:", 0, 0, display.BLUE))
    
    # Display directory names
    for i, item in enumerate(fileTree):
        lines[i] = {'name': item, 'active': False}
        
    for i, item in enumerate(lines):
        if i == activeElement:
            lines[i]['active'] = True
            formatted_lines.append(display.Text(f"> {lines[i]['name']}", 0, (50*i)+50, display.GREEN))
        else:
            lines[i]['active'] = False
            formatted_lines.append(display.Text(f"  {lines[i]['name']}", 0, (50*i)+50, display.BLUE))
    
    directory_text.append(formatted_lines)
    directory_text.append(arrows.arrows.screen)
        
    onDisplay = directory_text
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

def init():
    # This function gives the user time to take the mononocle out of the case and put it on
    print("### \t Init ###")
    touch.callback(touch.EITHER, wait)
    logoDisplay()
    s = 10
    while s>=1 :
        display_countdown(s)
        s -= 1
        time.sleep(0.1)
    display.show(display.Text("Welcome, User", display.WIDTH/2, display.HEIGHT/2, display.BLUE))
    time.sleep(1)
    main()
    return
    
    
    
def main():
    touch.callback(touch.EITHER, buttons)
    print(f"### \t Battery: {device.battery_level()}% ###")
    list_the_directorys()
    

init()