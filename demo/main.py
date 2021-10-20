import json
import subprocess
import tkinter as tk
from tkinter import filedialog, font as tkFont

class Theme:
    colorA_1 = "#282c34"
    colorA_2 = "#333842"
    colorA_3 = "#3b4048"
    colorA_4 = "#e79d28"
    colorB_1 = "#e06c70"
    colorB_2 = "#abb2bf"
    colorB_3 = "#469aef"
    colorB_4 = "#98c379"
    buttonWidth = 18
    fieldWidth = 60

# https://stackoverflow.com/questions/4266566/stardand-context-menu-in-python-tkinter-text-widget-when-mouse-right-button-is-p
def rClicker(e):
    try:
        def rClick_Copy(e, apnd=0):
            e.widget.event_generate('<Control-c>')
        def rClick_Cut(e):
            e.widget.event_generate('<Control-x>')
        def rClick_Paste(e):
            e.widget.event_generate('<Control-v>')
        e.widget.focus()
        nclst=[
               (' Cut', lambda e=e: rClick_Cut(e)),
               (' Copy', lambda e=e: rClick_Copy(e)),
               (' Paste', lambda e=e: rClick_Paste(e)),
               ]
        rmenu = tk.Menu(None, tearoff=0, takefocus=0)
        rmenu.config(bg=Theme.colorA_2, fg=Theme.colorB_2, activebackground=Theme.colorB_3)
        for (txt, cmd) in nclst:
            rmenu.add_command(label=txt, command=cmd)
        rmenu.tk_popup(e.x_root+40, e.y_root+10,entry="0")
    except tk.TclError:
        pass
    return "break"

def rClickbinder(r):
    try:
        for b in [ 'Text', 'Entry', 'Listbox', 'Label']: #
            r.bind_class(b, sequence='<Button-3>',
                         func=rClicker, add='')
    except tk.TclError:
        pass

def createInput(frame, index=0, name="STRING", type=None, value=None):
    fieldText = tk.StringVar()
    field = tk.Entry(frame, textvariable=fieldText, width=Theme.fieldWidth)
    field.config(highlightthickness=0, bg=Theme.colorA_3, fg=Theme.colorB_4)
    field.bind('<Button-3>',rClicker, add='')
    field.grid(row=index, column=1, padx=(0,5), pady=(5,5))
    if value is not None: fieldText.set(value)

    if type == "FILE":
        button = tk.Button(frame, width=Theme.buttonWidth)
        button["text"] = name
        button["command"] = lambda: fieldText.set(filedialog.askopenfilename(initialdir=value, title="Select file"))
        button.config(highlightthickness=0, bg=Theme.colorA_2, fg=Theme.colorB_2, activebackground=Theme.colorB_3)
        button.grid(row=index, column=0, padx=(5,5), pady=(5,5))
    elif type == "DIRECTORY":
        button = tk.Button(frame, width=Theme.buttonWidth)
        button["text"] = name
        button["command"] = lambda: fieldText.set(filedialog.askdirectory(initialdir=value, title="Select directory"))
        button.config(highlightthickness=0, bg=Theme.colorA_2, fg=Theme.colorB_2, activebackground=Theme.colorB_3)
        button.grid(row=index, column=0, padx=(5,5), pady=(5,5))
    elif type == "STRING":
        label = tk.Label(frame, text=name, width=Theme.buttonWidth)
        label.config(bg=Theme.colorA_1, fg=Theme.colorB_2)
        label.grid(row=index, column=0, padx=(5,5), pady=(5,5))
    return fieldText

class App:
    def __init__(self, root):
        root.title("Py-cli2gui")

        with open('config.json') as json_file:
            self.projects = json.load(json_file)

        self.fields = []

        frame = tk.Frame(root, relief="groove", bg=Theme.colorA_1)
        _font = tkFont.Font(family='helvetica', size=14, weight=tkFont.BOLD)

        self.currentProjectName = tk.StringVar(frame)
        self.currentProjectName.set(list(self.projects.keys())[0])
        self.currentProjectName.trace("w", self.setCurrentProject)
        optionMenu = tk.OptionMenu(frame, self.currentProjectName, *self.projects.keys())
        optionMenu.config(bg=Theme.colorA_2, fg=Theme.colorB_2, highlightthickness=0, activebackground=Theme.colorB_3)
        optionMenu["menu"].config(bg=Theme.colorA_2, fg=Theme.colorB_2, activebackground=Theme.colorB_3)
        optionMenu["font"] = _font
        optionMenu.grid(row=0, column=0)

        runButton = tk.Button(frame, fg=Theme.colorB_2, bg=Theme.colorA_2, activebackground=Theme.colorB_1, width=Theme.buttonWidth)
        runButton["text"] = 'RUN'
        runButton["command"] = self.runCommand
        runButton["font"] = _font
        runButton.config(highlightthickness=0)
        runButton.grid(row=0, column=1, padx=5)

        self.inProjectDir = tk.BooleanVar(value=True)
        inProjectDirButton = tk.Checkbutton(frame, variable=self.inProjectDir, bg=Theme.colorA_1, fg=Theme.colorB_2)
        inProjectDirButton["text"] = "Run in project directory"
        inProjectDirButton.config(highlightthickness=0, activebackground=Theme.colorA_1, activeforeground=Theme.colorB_3, selectcolor=Theme.colorA_2)
        inProjectDirButton.grid(row=1, column=1, padx=2)

        frame.pack(padx=10,pady=(10,0))

        fileFrame = tk.LabelFrame(root, text=" Path settings ", relief="groove", bg=Theme.colorA_1, fg=Theme.colorB_1)

        self.projectDirectory = createInput(fileFrame, index=0, name="Project directory", type="DIRECTORY")
        self.filePath = createInput(fileFrame, index=1, name="File path", type="FILE")
        self.pythonPath = createInput(fileFrame, index=2, name="Python path", type="FILE")
        fileFrame.pack(fill="both", expand="yes", padx=10, pady=0)

        self.setCurrentProject()

    def setCurrentProject(self, *args):
        self.removeFrame()
        self.currentProject = self.projects[self.currentProjectName.get()]
        self.createInputs()
        self.projectDirectory.set(self.currentProject['project path'])
        self.filePath.set(self.currentProject['file path'])
        self.pythonPath.set(self.currentProject['python path'])

    def createInputs(self):
        self.argFrame = tk.LabelFrame(root, text=" Arguments ", relief="groove", bg=Theme.colorA_1, fg=Theme.colorB_1)
        for i, item in enumerate(self.currentProject['inputs']):
            self.fields.append(createInput(self.argFrame, index=i, **item))
        self.argFrame.pack(fill="both", expand="yes", padx=10, pady=10)

    def generateCommand(self):
        env = self.pythonPath.get()
        command = env + " " + self.filePath.get()
        for i, arg in enumerate(self.currentProject['arguments']):
            value = self.fields[i].get()
            command = " ".join([command, arg, value])
        return command

    def removeFrame(self):
        if hasattr(self, 'argFrame'):
            self.argFrame.pack_forget()
            self.argFrame.destroy()
        self.fields.clear()

    def runCommand(self):
        command = self.generateCommand()
        path = self.projectDirectory.get() if self.inProjectDir.get() else "."
        subprocess.run(f"cd {path} && {command}", shell=True, stdout=True)

if __name__ == "__main__":
    root = tk.Tk()
    root["bg"] = Theme.colorA_1
    _font = tkFont.Font(family='helvetica', size=13)
    root.option_add("*font", _font)
    root.resizable(width=False, height=False)
    app = App(root)
    root.mainloop()
