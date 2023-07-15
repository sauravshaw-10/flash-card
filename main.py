import random
from tkinter import *
import pandas

BACKGROUND_COLOR = "#B1DDC6"
rand_word = {}
to_learn= {}

try:
    data = pandas.read_csv("./data/words_to_learn.csv")
    data_dict = data.to_dict(orient="records")
except FileNotFoundError:
    orig_data = pandas.read_csv("./data/french_words.csv")
    to_learn = orig_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

# ------------------------ Create New Flash Cards ---------------------- #
def new_card():
    global rand_word, flip_timer
    window.after_cancel(flip_timer)
    rand_word = random.choice(data_dict)
    canvas.itemconfig(text_lang, text="French", fill="black")
    canvas.itemconfig(text_word, text=rand_word["French"], fill="black")
    canvas.itemconfig(canvas_front, image= card_front_img)
    flip_timer = window.after(3000, flip_card)


# ------------------------- Flip Cards ---------------------------------- #
def flip_card():
    canvas.itemconfig(canvas_front, image=card_back_img)
    canvas.itemconfig(text_lang, text="English", fill="white")
    canvas.itemconfig(text_word, text=rand_word["English"], fill="white")

# ----------------------------Known Card ------------------------------- #

def is_known():
    data_dict.remove(rand_word)
    updated_data = pandas.DataFrame(data_dict)
    updated_data.to_csv("./data/words_to_learn.csv", index=False)
    print(len(data_dict))
    new_card()

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="./images/card_front.png")
canvas_front = canvas.create_image(400, 263, image=card_front_img)
card_back_img = PhotoImage(file="./images/card_back.png")
text_lang = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
text_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

cross_image = PhotoImage(file="./images/wrong.png")
unknown_button = Button(image=cross_image, highlightbackground=BACKGROUND_COLOR, command=new_card)
unknown_button.grid(column=0, row=1)

check_image = PhotoImage(file="./images/right.png")
known_button = Button(image=check_image, highlightbackground=BACKGROUND_COLOR, command=is_known)
known_button.grid(column= 1, row=1)

new_card()

window.mainloop()
