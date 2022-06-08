from tkinter import *
import tkinter.messagebox
import requests

# ***** Common global variables
blue = "#437BEC"
white = "#FFFFFF"
l_font = ("PT Sans Bold", 25)
m_font = ("PT Sans", 15)
s_font = ("PT Sans", 10)
btn_font = ("PT Sans", 12)
head_font = ("PT Sans", 18)

# ***** API Key and URL variables
api_key = "9e1a3e4359429e810034fswf165c08728"
url_weather = "http://api.openweathermap.org/data/2.5/weather?q="


# ***** Class: contains GUI
class MainWindow(Tk):
    def __init__(self):
        super().__init__()

        # ***** Method: weather search request
        def search_request():
            weather_results.delete(0, END)
            temp_results.delete(0, END)
            response = requests.get(f"{url_weather}{search_entry.get()}&appid={api_key}")
            if response.status_code == 200:
                data = response.json()
                weather_data = data["weather"][0]["description"]
                temp = data["main"]["temp"] - 273.15
                weather = weather_data.capitalize()
                temp_c = round(temp), "celsius"
                weather_results.insert(0, weather.title())
                temp_results.insert(0, temp_c)
            else:
                search_entry.delete(0, END)
                tkinter.messagebox.showerror(title="Error", message="Unsuccessful, please try again.")

        # ***** Main window attributes
        self.title("Simple Weather Search")
        self.geometry("500x250")
        self.resizable(False, False)

        # ***** Main window geometry
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # ***** Frame: top frame containing application title
        t_frame = Frame(self, bg=blue)
        t_frame.grid(row=0, column=0, sticky="nesw")

        # ***** Label: title of the application
        title_string: str = "Simple Weather Search"
        title = Label(t_frame, bg=blue, font=l_font, fg=white, text=title_string)
        title.place(anchor=CENTER, relx=0.5, rely=0.3)

        # ***** Label: enter city
        city_string: str = "Enter City:"
        city_label = Label(t_frame, bg=blue, font=m_font, fg=white, text=city_string)
        city_label.place(anchor=CENTER, relx=0.25, rely=0.7)

        # ***** Entry: user enters city
        search_entry = Entry(t_frame, highlightthickness=0, width=14, bg=white, font=m_font, fg=blue,
                             insertbackground=blue, justify=CENTER)
        search_entry.place(anchor=CENTER, relx=0.5, rely=0.7)

        # ***** Button: search button once user enters a valid city
        search_button = Button(t_frame, text="Search", highlightbackground=blue, font=btn_font, fg=blue,
                               command=search_request)
        search_button.place(anchor=CENTER, relx=0.75, rely=0.69)

        # ***** Frame: bottom frame containing weather results
        b_frame = Frame(self, bg=white)
        b_frame.grid(row=1, column=0, sticky="nesw")

        # ***** Label: enter city
        city_string: str = "Enter City:"
        city_label = Label(t_frame, bg=blue, font=m_font, fg=white, text=city_string)
        city_label.place(anchor=CENTER, relx=0.25, rely=0.7)

        # ***** Label: weather results
        weather_string: str = "Weather"
        weather_label = Label(b_frame, bg=white, font=head_font, fg=blue, text=weather_string)
        weather_label.place(anchor=CENTER, relx=0.33, rely=0.3)

        # ***** Label: temperature results
        temp_string: str = "Temperature"
        temp_label = Label(b_frame, bg=white, font=head_font, fg=blue, text=temp_string)
        temp_label.place(anchor=CENTER, relx=0.66, rely=0.3)

        # ***** Entry: inserting roll results in to entry box
        weather_results = Entry(b_frame, highlightthickness=0, width=15, bg=white, font=m_font, fg=blue,
                                justify=CENTER)
        weather_results.place(anchor=CENTER, relx=0.33, rely=0.55)

        # ***** Entry: inserting roll results in to entry box
        temp_results = Entry(b_frame, highlightthickness=0, width=15, bg=white, font=m_font, fg=blue,
                             justify=CENTER)
        temp_results.place(anchor=CENTER, relx=0.66, rely=0.55)

        # ***** Label: developer of application
        dev_string: str = "Developed by AporoSoft / 2022"
        developer = Label(b_frame, bg=white, font=s_font, fg=blue, text=dev_string)
        developer.place(anchor=CENTER, relx=0.5, rely=0.9)


main = MainWindow()
main.mainloop()
