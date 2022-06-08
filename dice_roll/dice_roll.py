from tkinter import *
from random import randint

# ***** Common global variables (font, colour)
blue_bg = "#437BEC"
white_bg = "#FFFFFF"
l_font = ("PT Sans", 18)
m_font = ("PT Sans", 13)
s_font = ("PT Sans", 10)


# ***** Class: contains GUI
class MainWindow(Tk):
    def __init__(self):
        super().__init__()

        # ***** Method: rolls virtual dice
        def roll_dice(dice_amount):
            roll_results.delete(0, END)
            for roll in range(dice_amount):
                roll_results.insert(0, str(randint(1, 6)).center(3))

        # ***** Main window attributes
        self.title("Virtual Dice Roll")
        self.geometry("650x350")
        self.resizable(False, False)

        # ***** Frame: left frame containing application description
        l_frame = Frame(self, bg=blue_bg)
        l_frame.pack(fill=BOTH, expand=TRUE, side=LEFT)

        # ***** Label: title of the application
        title_string: str = "Welcome to the Virtual Dice Roll\n▣ ▣ ▣ ▣ ▣ ▣"
        title = Label(l_frame, bg=blue_bg, font=l_font, fg=white_bg, text=title_string)
        title.place(anchor=CENTER, relx=0.5, rely=0.2)

        # ***** Message: description of the application
        desc_string: str = "This application rolls virtual dice producing random numbers between " \
                           "1 and 6. \nChoose how many to roll and the numbers will be randomly generated."
        description = Message(l_frame, bg=blue_bg, font=m_font, fg=white_bg, text=desc_string, width=250)
        description.place(anchor=CENTER, relx=0.5, rely=0.52)

        # ***** Label: developer of the application
        dev_string: str = "Developed by AporoSoft / 2022"
        developer = Label(l_frame, bg=blue_bg, font=s_font, fg=white_bg, text=dev_string)
        developer.place(anchor=CENTER, relx=0.5, rely=0.96)

        # ***** Frame: right frame containing dice roll UI
        r_frame = Frame(self, bg=white_bg)
        r_frame.pack(fill=BOTH, expand=TRUE, side=RIGHT)

        # ***** Label: heading of the application
        heading_string: str = "How many dice you want to roll:"
        heading = Label(r_frame, bg=white_bg, font=l_font, fg=blue_bg, text=heading_string)
        heading.place(anchor=CENTER, relx=0.5, rely=0.17)

        # ***** Buttons: how many dice the user wishes to roll between 1 and 6
        Button(r_frame, text="1", highlightbackground=white_bg, font=m_font, fg=blue_bg,
               command=lambda roll_1=1: roll_dice(roll_1)).place(anchor=CENTER, relx=0.143, rely=0.4)
        Button(r_frame, text="2", highlightbackground=white_bg, font=m_font, fg=blue_bg,
               command=lambda roll_1=2: roll_dice(roll_1)).place(anchor=CENTER, relx=0.286, rely=0.4)
        Button(r_frame, text="3", highlightbackground=white_bg, font=m_font, fg=blue_bg,
               command=lambda roll_1=3: roll_dice(roll_1)).place(anchor=CENTER, relx=0.429, rely=0.4)
        Button(r_frame, text="4", highlightbackground=white_bg, font=m_font, fg=blue_bg,
               command=lambda roll_1=4: roll_dice(roll_1)).place(anchor=CENTER, relx=0.571, rely=0.4)
        Button(r_frame, text="5", highlightbackground=white_bg, font=m_font, fg=blue_bg,
               command=lambda roll_1=5: roll_dice(roll_1)).place(anchor=CENTER, relx=0.714, rely=0.4)
        Button(r_frame, text="6", highlightbackground=white_bg, font=m_font, fg=blue_bg,
               command=lambda roll_1=6: roll_dice(roll_1)).place(anchor=CENTER, relx=0.857, rely=0.4)

        # ***** Label: roll results heading
        results_string: str = "Your roll results:"
        results = Label(r_frame, bg=white_bg, font=l_font, fg=blue_bg, text=results_string)
        results.place(anchor=CENTER, relx=0.5, rely=0.65)

        # ***** Entry: inserting roll results in to entry box
        roll_results = Entry(r_frame, highlightthickness=0, width=14, bg=white_bg, font=l_font, fg=blue_bg,
                             justify=CENTER)
        roll_results.place(anchor=CENTER, relx=0.5, rely=0.8)


main = MainWindow()
main.mainloop()
