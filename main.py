from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

try:
    df = pandas.read_csv('data/words_to_learn.csv')
    word_dict = df.to_dict()
except FileNotFoundError:
    df = pandas.read_csv('data/french_words.csv')
    word_dict = df.to_dict()

index_list = list(word_dict['French'])
random_word = random.choice(index_list)


def flip_card():
    canvas.itemconfig(language, fill='white', text='English')
    canvas.itemconfig(word, fill='white', text=word_dict['English'][random_word])
    canvas.itemconfig(background, image=card_back)


def right():
    global random_word, word, timer, index_list
    window.after_cancel(timer)
    del word_dict['French'][random_word]
    del word_dict['English'][random_word]
    words_to_learn = pandas.DataFrame.from_dict(word_dict)
    words_to_learn.to_csv('data/words_to_learn.csv', index=False)
    index_list = list(word_dict['French'])
    random_word = random.choice(index_list)
    canvas.itemconfig(language, fill='black', text='French')
    canvas.itemconfig(word, fill='black', text=word_dict['French'][random_word])
    canvas.itemconfig(background, image=card_front)
    timer = window.after(5000, func=flip_card)


def wrong():
    global random_word, word, timer, index_list
    window.after_cancel(timer)
    random_word = random.choice(index_list)
    canvas.itemconfig(language, fill='black', text='French')
    canvas.itemconfig(word, fill='black', text=word_dict['French'][random_word])
    canvas.itemconfig(background, image=card_front)
    timer = window.after(5000, func=flip_card)


window = Tk()
window.title('Flash Card App')
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

timer = window.after(5000, func=flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file='images/card_front.png')
card_back = PhotoImage(file='images/card_back.png')
background = canvas.create_image(400, 263, image=card_front)
language = canvas.create_text(400, 150, text='French', font=('Arial', 40, 'italic'))
word = canvas.create_text(400, 263, text=word_dict['French'][random_word], font=('Arial', 60, 'bold'))
canvas.grid(column=0, row=0, columnspan=2)

wrong_image = PhotoImage(file='images/wrong.png')
wrong_button = Button(image=wrong_image, highlightthickness=0, command=wrong)
wrong_button.grid(column=0, row=1)

right_image = PhotoImage(file='images/right.png')
right_button = Button(image=right_image, highlightthickness=0, command=right)
right_button.grid(column=1, row=1)

window.mainloop()
