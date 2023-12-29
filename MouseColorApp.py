import pyautogui
from PIL import ImageGrab
import PySimpleGUI as sg

class MouseColorApp:
    def __init__(self):
        sg.theme('DefaultNoMoreNagging')

        left_column = [
            [sg.Text("Mouse Color Info", font=("Helvetica", 16), justification="center")],
            [sg.Canvas(size=(200, 200), background_color='#000000', key='-CANVAS-')],
            [sg.Checkbox("Lock Controls", default=False, font=("Helvetica", 12), key="-LOCK_CONTROLS-")]
        ]

        right_column = [
            [sg.Checkbox("Enable Mouse Color", default=False, font=("Helvetica", 12), key="-ENABLED-")],
            [sg.Text("", size=(30, 1), font=("Helvetica", 14), key="-INFO-", justification="center")],
            [sg.Text("RGB: 0, 0, 0", size=(20, 1), key='-RGB-'),
             sg.Text("Hex: #000000", size=(20, 1), key='-HEX-')],
            [sg.Text("Red", size=(5, 1)),
             sg.Slider(range=(0, 255), default_value=0, orientation='h', size=(30, 15), enable_events=True, key='-RED-')],
            [sg.Text("Green", size=(5, 1)),
             sg.Slider(range=(0, 255), default_value=0, orientation='h', size=(30, 15), enable_events=True, key='-GREEN-')],
            [sg.Text("Blue", size=(5, 1)),
             sg.Slider(range=(0, 255), default_value=0, orientation='h', size=(30, 15), enable_events=True, key='-BLUE-')],
            [sg.Button("Exit", size=(10, 1), font=("Helvetica", 12))]
        ]

        layout = [
            [sg.Column(left_column, justification="center"), sg.VSeparator(), sg.Column(right_column, justification="right")],
        ]

        self.window = sg.Window("Mouse Color Info", layout, finalize=True)
        self.canvas = self.window['-CANVAS-']

    def get_mouse_color(self):
        x, y = pyautogui.position()
        screenshot = ImageGrab.grab(bbox=(x, y, x + 1, y + 1))
        color = screenshot.getpixel((0, 0))
        return color, f"X: {x}, Y: {y} - Color: {color}"

    def update_color(self, values=None):
        if values is None:
            values = self.window.read()[1]

        r = int(values['-RED-'])
        g = int(values['-GREEN-'])
        b = int(values['-BLUE-'])

        rgb_text = f'RGB: {r}, {g}, {b}'
        hex_color = f'#{r:02x}{g:02x}{b:02x}'

        self.canvas.TKCanvas.create_rectangle((0, 0, 200, 200), outline="", fill=hex_color)
        self.window['-RGB-'].update(value=rgb_text)
        self.window['-HEX-'].update(value=f'Hex: {hex_color}')

    def run(self):
        while True:
            event, values = self.window.read(timeout=10)  # Cập nhật thông tin mỗi 10ms
            if event == sg.WINDOW_CLOSED or event == "Exit":
                break
            elif event in ['-RED-', '-GREEN-', '-BLUE-']:
                if not values['-LOCK_CONTROLS-']:
                    self.update_color(values)

            if values['-ENABLED-']:
                color, info = self.get_mouse_color()
                self.window["-INFO-"].update(info)
                if not values['-LOCK_CONTROLS-']:
                    self.update_color({'-RED-': color[0], '-GREEN-': color[1], '-BLUE-': color[2]})
            else:
                self.window["-INFO-"].update("Mouse Color Disabled")
        self.window.close()

if __name__ == "__main__":
    app = MouseColorApp()
    app.run()
