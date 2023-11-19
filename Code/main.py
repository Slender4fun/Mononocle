import touch
import device
import display
import time
import uos
import gc
import screens.logo as logo
import screens.arrows as arrows
import projects.battery_status.battery_status as battery_status


powerBarVisible = False
onDisplay = {}
activeElement = 0
current_dir = "/projects"
lines = {}

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
    
        
    
left_button_pressed_time = None

def navigate_up():
    global onDisplay, current_dir, activeElement
    if "/projects" in current_dir:                  # Don't navigate above the root directory
        parts = current_dir.split('/')              # Split the current_dir path to move up one level
        if len(parts) > 2:
            parts.pop()
            current_dir = '/'.join(parts)
        else:
            display.show(display.Text("Already at root", display.WIDTH/2, display.HEIGHT/2, display.RED, justify=display.MIDDLE_CENTER))
            time.sleep(1)
            current_dir = "/projects"
        activeElement = 0                           # Reset the activeElement to the top
        list_the_directorys()
        
def left_button_function(button):
    global left_button_pressed_time
    print("left_button_function")
    if left_button_pressed_time is None:
        left_button_pressed_time = time.time()
    
    print("# Left Button pressed")
    selectNext()
    time.sleep(0.5)
    
    if True == touch.state("B"):
        print("# Long pressed")
        navigate_up()
    else:
        print("# Short pressed")
    
    left_button_pressed_time = None
    
def selectNext():
    global onDisplay, activeElement, lines
    
    # Set the 'active' property for the previous activeElement to False
    if activeElement in lines:
        lines[activeElement]['active'] = False
    activeElement += 1
    print(f'activeElement: {activeElement}')
    print(f'len(lines): {len(lines)}')
    if activeElement >= len(lines):
        print(f'set back active element to 0')
        activeElement = 0
    else:
        print(f'select next as active: {activeElement}')
    
    # If the active element is "Keine Datei im Verzeichnis", navigate up
    if lines[activeElement]['name'] == "No file in directory":
        navigate_up()
    else:
        list_the_directorys()
    



        
def right_button_function(button):
    global onDisplay, activeElement, current_dir
    # from lines the activeElement is used to get the name of the directory then if the directory ends with .py it will run the file
    for i, item in enumerate(lines):
        if i == activeElement:
            active_element_path = current_dir + "/" + lines[i]['name']  # Construct the full file path
            stat_info = uos.stat(active_element_path)
            if (stat_info[0] & 0x4000):                                 # Check if the item is a directory
                current_dir += f"/{lines[i]['name']}"
                activeElement = 0                                       # Reset the activeElement to the top
                list_the_directorys()
                return
            elif lines[i]['name'].endswith(".py"):
                file_name = lines[i]['name']                            # Get the name of the Python file
                file_path = current_dir + "/" + file_name               # Construct the full file path
                with open(file_path, "r") as file:
                    file_contents = file.read()                         # Read the file contents
                try:
                    exec(file_contents, {})                             # Execute the file contents
                except Exception as e:
                    print(f"Error executing {file_name}: {e}")
                return
            else:
                print("Not a Python file")
                display.show(display.Text("Not a Python file", 0, 0, display.RED))
                time.sleep(1)
                list_the_directorys()
                return
    

    
    
    

def battery():
    global onDisplay
    stash = []
    stash.append(onDisplay)
    # stash.append(battery_status.battery_icon())
    stash.append(battery_status.battery_line_vertical())
    onDisplay = stash
    return
      
      
      
def list_the_directorys():
    global onDisplay, activeElement, current_dir, lines
    fileTree = []
    formatted_lines = []
    directory_text = []
    lines = {}
    
    
    for item in uos.ilistdir(current_dir):
        # if (item[1] & 0x4000) == 0x4000:                  # Check if the item is a directory
            fileTree.append(item[0])                        # Append the directory name to the fileTree list.
    

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
    printDisplay()

def printDisplay():
    global onDisplay
    battery()
    display.show(onDisplay)

def logoDisplay():
    print("### \t Logo Display ###")
    speed = 5
    display.brightness(1)
    display.show(logo.logo.screen)
    time.sleep(speed)

def init():
    # This function gives the user time to take the mononocle out of the case and put it on
    print("### \t Init ###")
    touch.callback(touch.EITHER, wait)
    logoDisplay()
    s = 5
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