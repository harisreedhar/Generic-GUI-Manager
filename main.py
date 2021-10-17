import subprocess
import tkinter as tk
from config import projects
from tkinter import filedialog

def createInput(frame, index=0, name="STRING", type=None, value=None):
    fieldText = tk.StringVar()
    field = tk.Entry(frame, textvariable=fieldText, width=60)
    field.grid(row=index, column=1, padx=(0,5), pady=(5,5))
    if value is not None: fieldText.set(value)

    if type == "FILE":
        button = tk.Button(frame, width=15)
        button["text"] = name
        button["command"] = lambda: fieldText.set(filedialog.askopenfilename(initialdir=value, title="Select file"))
        button.grid(row=index, column=0, padx=(5,5), pady=(5,5))
    elif type == "DIRECTORY":
        button = tk.Button(frame, width=15)
        button["text"] = name
        button["command"] = lambda: fieldText.set(filedialog.askdirectory(initialdir=value, title="Select directory"))
        button.grid(row=index, column=0, padx=(5,5), pady=(5,5))
    elif type == "STRING":
        label = tk.Label(frame, text=name, width=15)
        label.grid(row=index, column=0, padx=(5,5), pady=(5,5))
    return field

class App:
    def __init__(self, root):
        root.title("GUI Manager")
        self.fields = []

        frame = tk.Frame(root, relief="groove")
        label = tk.Label(frame, text="Select Project")
        label.grid(row=0, column=0)
        self.currentProjectName = tk.StringVar(frame)
        self.currentProjectName.set(list(projects.keys())[0])
        self.currentProjectName.trace("w", self.setCurrentProject)
        optionMenu = tk.OptionMenu(frame, self.currentProjectName, *projects.keys())
        optionMenu.grid(row=0, column=1)
        runButton = tk.Button(frame, bg="#424949", fg="#fff", activebackground="#cd6155", activeforeground="#fff", width=20)
        runButton["text"] = 'RUN'
        runButton["command"] = self.runCommand
        runButton.grid(row=0, column=2, padx=5)
        frame.pack(padx=10,pady=(20,0))

        fileFrame = tk.LabelFrame(root, text=" Path ", relief="groove")
        self.envPath= tk.StringVar()
        envField = tk.Entry(fileFrame, textvariable=self.envPath, width=60)
        envField.grid(row=0, column=1, padx=(0,5), pady=(5,5))
        button = tk.Button(fileFrame, width=15, text="Python Environment")
        button["command"] = lambda: self.envPath.set(filedialog.askopenfilename(initialdir=self.currentProject['python path'], title="Select file"))
        button.grid(row=0, column=0, padx=(5,5), pady=(5,5))
        self.filePath= tk.StringVar()
        fileField = tk.Entry(fileFrame, textvariable=self.filePath, width=60)
        fileField.grid(row=1, column=1, padx=(0,5), pady=(5,5))
        button = tk.Button(fileFrame, width=15, text="File to Execute")
        button["command"] = lambda: self.filePath.set(filedialog.askopenfilename(initialdir=self.currentProject['file path'], title="Select file"))
        button.grid(row=1, column=0, padx=(5,5), pady=(5,5))
        fileFrame.pack(fill="both", expand="yes", padx=10, pady=10)

        self.setCurrentProject()

    def setCurrentProject(self, *args):
        self.removeFrame()
        self.currentProject = projects[self.currentProjectName.get()]
        self.createInputs()
        self.envPath.set(self.currentProject['python path'])
        self.filePath.set(self.currentProject['file path'])

    def createInputs(self):
        self.argFrame = tk.LabelFrame(root, text=" Arguments ", relief="groove")
        for item in self.currentProject['inputs']:
            self.fields.append(createInput(self.argFrame, **item))
        self.argFrame.pack(fill="both", expand="yes", padx=10, pady=10)

    def generateCommand(self):
        fullCommand = self.envPath.get()
        fullCommand += " " + self.filePath.get()
        for i, command in enumerate(self.currentProject['splitted command']):
            fullCommand += " " + command + " " + self.fields[i].get() + " "
        return fullCommand

    def removeFrame(self):
        if hasattr(self, 'argFrame'):
            self.argFrame.pack_forget()
            self.argFrame.destroy()
        self.fields.clear()

    def runCommand(self):
        command = self.generateCommand()
        path = self.currentProject['project directory']
        subprocess.run(f"cd {path} && {command}", shell=True, stdout=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
