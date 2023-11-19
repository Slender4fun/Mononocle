import device
import display


# def draw_battery_status_text(x_offset=0, y_offset=0, color=0xffffff):
#     batt_level = device.battery_level()
#     display.show(display.Text("Battery: " + str(batt_level) + "%", x_offset + 0, y_offset + 0, color))

# draw_battery_status_text()

# def battery_icon():
#     batteryOutput = []
#     battery_level = device.battery_level()/100
#     bl_p = display.Polyline([565, 0, 640, 0, 640, 24, 565, 24, 565, 0], display.WHITE, thickness=1)
#     bl_l = display.Line(570, 12, 570 + int(battery_level * 2), 12, display.GREEN, thickness=12)
#     bl_m = display.Text(f'{int(battery_level * 67)}m', 640, 50, display.WHITE, justify=display.MIDDLE_RIGHT)

#     batteryOutput.append(bl_p)
#     batteryOutput.append(bl_l)
#     batteryOutput.append(bl_m)
#     display.show(batteryOutput)
#     return batteryOutput

# battery_icon()
    



def battery_line():
    batteryOutput = []
    battery_level = device.battery_level()/100
    field = display.Line(12, 12, 628, 12, display.GRAY1, thickness=12)
    bl_l = display.Line(12, 12, 12 + int(battery_level * 616), 12, display.GREEN, thickness=12)
    batteryOutput.append(bl_l)
    batteryOutput.append(field)
    display.show(batteryOutput)
    return batteryOutput

battery_line()
######## functional until here ########

def battery_line_vertical():
    batteryOutput = []
    battery_level = device.battery_level()/100
    field = display.Line(628, 1, 628, 339, display.GRAY1, thickness=12)
    bl_l = display.Line(628, 339- int(battery_level * 339), 628, 339, display.GREEN, thickness=12)    
    batteryOutput.append(bl_l)
    batteryOutput.append(field)
    display.show(batteryOutput)
    return batteryOutput