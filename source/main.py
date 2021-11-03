import re
import json
import platform
import subprocess
import tkinter as tk
from tkinter import filedialog, font as tkFont


class Theme:
    def __init__(self):
        self.a1 = "#282c34"
        self.a2 = "#333842"
        self.a3 = "#3b4048"
        self.a4 = "#e79d28"
        self.b1 = "#e06c70"
        self.b2 = "#abb2bf"
        self.b3 = "#469aef"
        self.b4 = "#98c379"
        self.fieldWidth = 60
        self.labelWidth = 16
        self.runButtonWidth = 8
        self.fontA = tkFont.Font(family='helvetica', size=13)
        self.fontB = tkFont.Font(family='helvetica', size=14, weight=tkFont.BOLD)
        self.fontC = tkFont.Font(family='helvetica', size=12, slant='italic')
        self.settings = {
            'root':{'bg':self.a1},
            'frame':{'bg':self.a1},
            'label':{'bg':self.a1, 'fg':self.b2},
            'label_frame':{'bg':self.a1, 'fg':self.b1},
            'menu':{'bg':self.a2, 'fg':self.b2, 'activebackground':self.b3},
            'text_field':{'highlightthickness':0, 'bg':self.a3, 'fg':self.b4},
            'button_1':{'highlightthickness':0, 'bg':self.a2, 'fg':self.b2, 'activebackground':self.b3},
            'run_button':{'highlightthickness':0, 'bg':self.a2, 'fg':self.b2, 'activebackground':self.b1},
            'check_button':{'highlightthickness':0, 'bg':self.a1, 'fg':self.b2, 'activebackground':self.a1, 'activeforeground':self.b3, 'selectcolor':self.a2}
        }


class App:
    def __init__(self, root, theme):
        self.root = root
        self.theme = theme
        self.projects = self.getProjects('config.json')
        self.projectName = tk.StringVar()
        self.projectName.set(list(self.projects.keys())[0])
        self.projectName.trace("w", self.setCurrentProject)
        self.runInProjectPath = tk.BooleanVar(value=True)
        self.fields = []
        self.frameA()
        self.frameB()
        self.dynamicFrame = tk.LabelFrame(self.root, text=" Arguments ", relief="groove")
        self.setCurrentProject()
        self.frameD()

    def frameA(self):
        frame =  tk.Frame(self.root, relief="groove")
        frame.config(**self.theme.settings.get('frame'))

        optionMenu = tk.OptionMenu(frame, self.projectName, *self.projects.keys())
        optionMenu.config(**self.theme.settings.get('menu'))
        optionMenu.config(width=30)
        optionMenu["menu"].config(**self.theme.settings.get('menu'))
        optionMenu.config(highlightthickness=0)
        optionMenu["font"] = self.theme.fontB
        optionMenu.grid(row=0, column=0)

        self.description = tk.Label(frame, text="Face swaping project")
        self.description.config(**self.theme.settings.get('label'))
        self.description["font"] = self.theme.fontC
        self.description.grid(row=1, column=0, padx=2, pady=2)

        frame.pack(padx=6, pady=(12,0))

    def frameB(self):
        frame = tk.LabelFrame(self.root, text=" Settings ", relief="groove")
        frame.config(**self.theme.settings.get('label_frame'))
        self.projectPath = self.createInput(frame, index=0, name="Project path", type="DIRECTORY")
        self.filePath = self.createInput(frame, index=1, name="File path", type="FILE")
        self.pythonPath = self.createInput(frame, index=2, name="Python path", type="FILE")
        frame.pack(fill="y", expand="yes", padx=6, pady=(0,6))

    def frameC(self):
        self.dynamicFrame.config(**self.theme.settings.get('label_frame'))
        for i, item in enumerate(self.currentProject['inputs']):
            self.fields.append(self.createInput(self.dynamicFrame, index=i, **item))
        self.dynamicFrame.pack(fill="y", expand="yes", padx=6, pady=6)

    def frameD(self):
        frame =  tk.Frame(self.root, relief="groove")
        frame.config(**self.theme.settings.get('frame'))

        checkButton = tk.Checkbutton(frame, variable=self.runInProjectPath)
        checkButton["text"] = "Run in project directory"
        checkButton.config(**self.theme.settings.get('check_button'))
        checkButton.grid(row=0, column=0, sticky='E')

        runButton = tk.Button(frame, width=self.theme.runButtonWidth)
        runButton.config(**self.theme.settings.get('run_button'))
        runButton["text"] = 'RUN'
        runButton["command"] = self.runCommand
        runButton["font"] = self.theme.fontB
        runButton.grid(row=0, column=1, padx=6, sticky='E')

        frame.pack(padx=24, pady=(6,12), side=tk.RIGHT)

    def removeFrame(self):
        for widget in self.dynamicFrame.winfo_children():
            widget.destroy()
        self.fields.clear()

    def setCurrentProject(self, *args):
        self.removeFrame()
        self.currentProject = self.projects[self.projectName.get()]
        self.frameC()
        self.projectPath.set(self.currentProject['project path'])
        self.filePath.set(self.currentProject['file path'])
        self.pythonPath.set(self.currentProject['python path'])
        description = self.currentProject.get('description')
        description = re.sub("(.{100})", "\\1\n", description, 0, re.DOTALL)
        self.description.configure(text="( " + description + " )")

    def getProjects(self, configPath):
        with open(configPath) as json_file:
            return json.load(json_file)

    def generateCommand(self):
        env = self.pythonPath.get()
        command = env + " " + self.filePath.get()
        for i, arg in enumerate(self.currentProject['arguments']):
            value = self.fields[i].get()
            command = " ".join([command, arg, value])
        cdCommand = f"cd {self.projectPath.get() if self.runInProjectPath.get() else '.'}"
        preCommands = self.currentProject.get("pre_commands")
        if isinstance(preCommands, list):
            preCommands = " && ".join(preCommands)
        postCommands = self.currentProject.get("post_commands")
        if isinstance(postCommands, list):
            postCommands = " && ".join(postCommands)
        subprocess.run(f" echo {preCommands}", shell=True, stdout=True)
        commands = [cdCommand, preCommands, command, postCommands]
        commands = filter(None, commands)
        finalCommand = " && ".join(commands)
        return finalCommand

    def runCommand(self):
        command = self.generateCommand()
        print("---------------------- Command --------------------------------")
        print(command)
        print("---------------------- Execution started ----------------------")
        subprocess.run(command, shell=platform.system() != 'Windows', stdout=True)
        print("---------------------- Execution ended ------------------------")

    # https://stackoverflow.com/questions/4266566/stardand-context-menu-in-python-tkinter-text-widget-when-mouse-right-button-is-p
    def rClickMenu(self, e):
        try:
            def rCopy(e, apnd=0):
                e.widget.event_generate('<Control-c>')
            def rCut(e):
                e.widget.event_generate('<Control-x>')
            def rPaste(e):
                e.widget.event_generate('<Control-v>')
            e.widget.focus()
            nclst = [
                (' Cut', lambda e=e: rCut(e)),
                (' Copy', lambda e=e: rCopy(e)),
                (' Paste', lambda e=e: rPaste(e)),]
            rMenu = tk.Menu(None, tearoff=0, takefocus=0)
            rMenu.config(**self.theme.settings.get('menu'))
            for (txt, cmd) in nclst:
                rMenu.add_command(label=txt, command=cmd)
            rMenu.tk_popup(e.x_root + 40, e.y_root + 10, entry="0")
        except tk.TclError:
            pass
        return "break"

    def rClickBinder(self, r):
        try:
            for b in [ 'Text', 'Entry', 'Listbox', 'Label']:
                r.bind_class(b, sequence='<Button-3>', func=self.rClickMenu, add='')
        except tk.TclError:
            pass

    def createInput(self, frame, index=0, name="", type="STRING", value=None):
        text = tk.StringVar()
        if isinstance(value, (str, int, float)):
            text.set(value)
        label = tk.Label(frame, text=name, width=self.theme.labelWidth, anchor="e")
        label.config(**self.theme.settings.get('label'))
        label.grid(row=index, column=0, padx=2, pady=2, sticky="E")
        if type == "FILE":
            button = tk.Button(frame, anchor="w")
            button["text"] = "..."
            button["command"] = lambda: text.set(filedialog.askopenfilename(title="Select file"))
            button.config(**self.theme.settings.get('button_1'))
            button.grid(row=index, column=2, padx=2, pady=2)
        elif type == "DIRECTORY":
            button = tk.Button(frame, anchor="w")
            button["text"] = "..."
            button["command"] = lambda: text.set(filedialog.askdirectory(title="Select directory"))
            button.config(**self.theme.settings.get('button_1'))
            button.grid(row=index, column=2, padx=2, pady=2)
        elif type == "LIST":
            menu = tk.OptionMenu(frame, text, *value)
            menu.config(**self.theme.settings.get('menu'))
            menu["menu"].config(**self.theme.settings.get('menu'))
            menu.config(highlightthickness=0)
            menu.grid(row=index, column=1, padx=(0,2), pady=2, sticky="W")
            text.set(value[0])
        elif type == "STRING":
            pass
        if type != "LIST":
            field = tk.Entry(frame, textvariable=text, width=self.theme.fieldWidth)
            field.config(**self.theme.settings.get('text_field'))
            field.bind('<Button-3>', self.rClickMenu, add='')
            field.grid(row=index, column=1, padx=(0,1), pady=2)
        return text


if __name__ == "__main__":
    root = tk.Tk()
    theme = Theme()
    root.title("Py-Cli2Gui")
    root.config(**theme.settings.get('root'))
    root.option_add("*font", theme.fontA)
    root.resizable(width=False, height=False)
    #root.rowconfigure(0, weight=1)
    #root.columnconfigure(0, weight=1)
    app = App(root, theme)
    root.mainloop()
