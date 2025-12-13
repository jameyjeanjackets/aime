import PySimpleGUI as sg

layout = [
    [sg.Text("Enter your name:"), sg.InputText(key='-NAME-')],
    [sg.Text("Your message:"), sg.Multiline(size=(40, 5), key='-MESSAGE-')],
    [sg.Button('Submit')]
]

window = sg.Window('PySimpleGUI Text Box Example', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Submit':
        break

window.close()