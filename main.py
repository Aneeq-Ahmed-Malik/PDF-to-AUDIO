import PyPDF2
import voicerss_tts
import customtkinter
from customtkinter import filedialog as fd
from CTkMessagebox import CTkMessagebox
import os

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")


WIDTH = 800
HEIGHT = 400


class MainWindow(customtkinter.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.maxsize(WIDTH, HEIGHT)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - WIDTH) // 2
        y = (screen_height - HEIGHT) // 2


        self.grid_columnconfigure(0, weight=1)


        self.title("PDF to Audio Book")
        self.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")

        self.filepath = customtkinter.StringVar

        self.heading = customtkinter.CTkLabel(self, text="PDF to Audio Converter",
                                              font=customtkinter.CTkFont(family="Helvetica", size=30, weight="bold"))
        self.heading.grid(row=0, column=0, sticky="ew", pady=50)

        self.entry = customtkinter.CTkEntry(self, placeholder_text="Filepath",
                                           font=customtkinter.CTkFont(family="calibiri", size=12, weight="bold"), width=250)
        self.entry.grid(row=1, column=0, sticky="s", pady=(20, 20))

        self.select = customtkinter.CTkButton(self, text="Select File",
                                            font=customtkinter.CTkFont(family="Trebuchet MS", size=20, weight="bold"),
                                            hover_color="DodgerBlue2", command=self.select_file)
        self.select.grid(row=2, column=0, sticky="n")

        self.confirm = customtkinter.CTkButton(self, text="Confirm",width=180,
                                              font=customtkinter.CTkFont(family="Trebuchet MS", size=20, weight="bold"),
                                              hover_color="DodgerBlue2", command=self.begin)

        self.entry.configure(state="disabled")

    def select_file(self):


        filetypes = (
            ('pdf files', '*.pdf'),
        )

        self.filepath = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)
        self.entry.configure(state="normal")
        self.entry.delete("0", "end")
        self.entry.insert("0", self.filepath)
        self.entry.configure(state="disabled")
        self.confirm.grid(row=3, column=0, sticky="s", pady=40)

    def begin(self):

        self.heading.grid_forget()
        self.entry.grid_forget()
        self.confirm.grid_forget()
        self.select.grid_forget()

        self.frame = Converter(self, self.filepath)
        self.frame.pack(side="top", fill="both", expand=True)
        self.frame.tkraise()



    def main_window(self):
        self.heading.grid(row=0, column=0, sticky="ew", pady=50)
        self.entry.grid(row=1, column=0, sticky="s", pady=(20, 20))
        self.select.grid(row=2, column=0, sticky="n")
        self.entry.configure(state="normal")
        self.entry.delete("0", "end")
        self.entry.configure(placeholder_text="Filepath")
        self.entry.configure(state="disabled")

class Converter(customtkinter.CTkFrame):
    def __init__(self, master: MainWindow, filepath, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.text = ""
        self.root = master

        self.lbl = customtkinter.CTkLabel(self, text="Convert your File", font=("Helvetica", 20, "bold"), text_color="orchid")
        self.lbl.grid(row=0, column=0, sticky="nsew", pady=50)

        self.format_option = customtkinter.StringVar(value="Select format")
        self.format = customtkinter.CTkOptionMenu(self, values=["mp3", "wav"], width=250,command=self.format_selected,
                                                 variable=self.format_option)

        self.format.grid(row=1, column=0, sticky="s")

        self.entry = customtkinter.CTkEntry(self, placeholder_text="Filepath",
                                            font=customtkinter.CTkFont(family="calibiri", size=12, weight="bold"),
                                            width=250)
        self.entry.grid(row=2, column=0, sticky="s", pady=(20, 20))

        self.select = customtkinter.CTkButton(self, text="Select Location", state="disabled",
                                              font=customtkinter.CTkFont(family="Trebuchet MS", size=15, weight="bold"),
                                              hover_color="DodgerBlue2", command=self.save)
        self.select.grid(row=3, column=0, sticky="n")

        self.convert = customtkinter.CTkButton(self, text="Convert",  width=180,
                                              font=customtkinter.CTkFont(family="Trebuchet MS", size=15, weight="bold"),
                                              hover_color="DodgerBlue2", command=self.convert_to_audio)
        self.read_pdf(filepath)

        self.entry.configure(state="disabled")
    def read_pdf(self, filepath):
        # creating a pdf file object
        pdfFileObj = open(filepath, 'rb')

        # creating a pdf reader object
        pdfReader = PyPDF2.PdfReader(pdfFileObj)

        for page in pdfReader.pages:
            self.text += page.extract_text()


    def format_selected(self, choice):
        self.select.configure(state="normal")
        self.entry.configure(state="normal", placeholder_text="Filepath")
        self.format_option = choice



    def save(self):
        files = [(f'{self.format_option} files', f'*.{self.format_option}'),]
        file = fd.asksaveasfile(filetypes=files, defaultextension=files)
        self.entry.configure(state="normal")
        self.entry.insert("0", file.name)
        self.select.configure(state="disabled")
        self.entry.configure(state="disabled")
        self.format.configure(state="disabled")
        self.convert.grid(row=4, column=0, sticky="n", pady=40)


    def convert_to_audio(self):

        self.convert.configure(state="disabled")

        voice = voicerss_tts.speech({
        "key": os.environ.get("API_KEY"),
            "hl": "en-us",
            "v": "Amy",
            "c":"mp3",
            "src": self.text
        })

        with open(self.entry.get(), 'wb') as f:
            f.write(voice['response'])

        msg = CTkMessagebox(message="Successfully converted to Audio file.",
                      icon="check", option_1="Thanks", title="Success", fade_in_duration=2)

        if msg.get() == "Thanks":
            self.destroy()
            self.root.main_window()


app = MainWindow()

app.mainloop()

