import tkinter as tk
import ttkbootstrap
from ttkbootstrap.dialogs import Messagebox
from PIL import Image, ImageTk
from tkinter import PhotoImage
import requests

#Globals variables.
counter = 0
counter_1 = 0
player_cards = []
crupier_cards = []
player_cards_label = []
crupier_hand = 0
player_hand = 0

#Functions.
def get_deck():
    global counter, counter_1
    
    response = requests.get('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1')
    data = response.json()
    deck_id = data['deck_id']
    counter = 100  #starts the game with counter = 100.
    counter_1 = 100
    return deck_id

def set_value(card):
    value_card = card['value']
    if value_card.isdigit():
        return int(value_card)
    elif value_card in ['KING', 'QUEEN', 'JACK']:
        return 10
    elif value_card == 'ACE':
        return 1

def start_game():
    global player_hand, player_cards, crupier_hand, crupier_cards, label_x, counter, counter_1, player_cards_label, card_2
    counter = 100 #starts the new game with counter = 100. 
    counter_1 = 100
    crupier_hand = 0 #restars the crupier hand
    crupier_cards = []
    
    for i in player_cards_label:
        i.destroy()
    player_cards_label = []
    
    player_cards = [] #begins the new game with 0 player cards value.
    response = requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=4')
    data = response.json() #data is a dictionary.
    cards = data['cards'] 
    
    card_hidden = Image.open('/home/bruce/Escritorio/Python/BLACK_JACK/card_hidden.png')
    card_hidden = card_hidden.resize((175, 225), Image.ANTIALIAS)
    photo_hidden = ImageTk.PhotoImage(card_hidden)
    
    if len(cards) >= 4:
        card_1 = cards[0]
        card_2 = cards[1]
        card_3 = cards[2]
        card_4 = cards[3]
        value_card_1 = set_value(card_1)
        value_card_2 = set_value(card_2)
        value_card_3 = set_value(card_3)
        value_card_4 = set_value(card_4)
        
        img_url_1 = card_1['image']
        image_1 = Image.open(requests.get(img_url_1, stream=True).raw)
        image_1 = image_1.resize((175, 225), Image.ANTIALIAS)
        photo_1 = ImageTk.PhotoImage(image_1)
        label_1.config(image=photo_1)
        label_1.image = photo_1
        
        img_url_2 = card_2['image']
        image_2 = Image.open(requests.get(img_url_2, stream=True).raw)
        image_2 = image_2.resize((175, 225), Image.ANTIALIAS)
        #photo_2 = ImageTk.PhotoImage(image_2)
        label_2.config(image=photo_hidden)
        label_2.image = photo_hidden
        
        img_url_3 = card_3['image']
        image_3 = Image.open(requests.get(img_url_3, stream=True).raw)
        image_3 = image_3.resize((175, 225), Image.ANTIALIAS)
        photo_3 = ImageTk.PhotoImage(image_3)
        label_3.config(image=photo_3)
        label_3.image = photo_3
        
        img_url_4 = card_4['image']
        image_4 = Image.open(requests.get(img_url_4, stream=True).raw)
        image_4 = image_4.resize((175, 225), Image.ANTIALIAS)
        photo_4 = ImageTk.PhotoImage(image_4)
        label_4.config(image=photo_4)
        label_4.image = photo_4
        
        player_cards.extend([value_card_3, value_card_4])
        crupier_cards.extend([value_card_1, value_card_2])
        
    else:
        print("No quedan suficientes cartas en el mazo.")
    
    player_hand = sum(player_cards)
    crupier_hand = sum(crupier_cards)
    
    if player_hand == 21:
        end_game('Blackjack, has ganado!', 'Sorprendente')
    else:
        button_hit.config(state='active')
        button_stay.config(state='active')
    
    center_window(700, 675)  
    label_title.pack(anchor='center', expand=False, pady=25)
    button_start_game.place(x=145, y=625)
    button_start_game.config(text='Nuevo')
    button_hit.place(x=318, y=625)
    button_hit.config(bootstyle='info')
    button_stay.place(x=500, y=625)
    button_stay.config(bootstyle='warning')
    
    print(f'Player hand: {player_hand}')
    print(f'Crupier hand: {crupier_hand}')

def create_card_player():    
    global counter, label_x
    counter += 100
    
    response = requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=1')
    data = response.json()
    cards = data['cards']
    
    if len(cards) >= 1:
        card_x = cards[0]
        value_card_x = set_value(card_x)
        img_url_x = card_x['image']
        image_x = Image.open(requests.get(img_url_x, stream=True).raw)
        image_x = image_x.resize((175, 225), Image.ANTIALIAS)
        photo_x = ImageTk.PhotoImage(image_x)
        label_x = ttkbootstrap.Label(window, image=photo_x)
        label_x.place(x=counter, y=350)
        label_x.image = photo_x
        player_cards_label.append(label_x)
    
    return label_x, value_card_x

def create_card_crupier():    
    global counter_1, label_x
    counter_1 += 100
    
    response = requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=1')
    data = response.json()
    cards = data['cards']
    
    if len(cards) >= 1:
        card_x = cards[0]
        value_card_x = set_value(card_x)
        img_url_x = card_x['image']
        image_x = Image.open(requests.get(img_url_x, stream=True).raw)
        image_x = image_x.resize((175, 225), Image.ANTIALIAS)
        photo_x = ImageTk.PhotoImage(image_x)
        label_x = ttkbootstrap.Label(window, image=photo_x)
        label_x.place(x=counter_1, y=100)
        label_x.image = photo_x
        player_cards_label.append(label_x)
    
    return label_x, value_card_x

def hit_me():
    global player_hand
    
    card_hit_me = create_card_player()
    value_card_hit_me = [card_hit_me[1]]
    player_cards.extend(value_card_hit_me)
    player_hand = sum(player_cards)
    
    if player_hand > 21:
        end_game('Crupier gana!', 'Intentalo nuevamente.')
        img_url_2 = card_2['image']
        image_2 = Image.open(requests.get(img_url_2, stream=True).raw)
        image_2 = image_2.resize((175, 225), Image.ANTIALIAS)
        photo_2 = ImageTk.PhotoImage(image_2)
        label_2.config(image=photo_2)
        label_2.image = photo_2

    print(f'Player hand: {player_hand}')
    print(f'Crupier hand: {crupier_hand}')
    
def end_game(mensaje, titulo):
    Messagebox.show_info(message=mensaje, title=titulo)
    button_hit.config(state='disable')
    button_stay.config(state='disable')
    
def stay():
    global crupier_hand
    
    while crupier_hand < 17:
        crupier_card_stay = create_card_crupier()
        value_crupier_card_stay = [crupier_card_stay[1]]
        crupier_cards.extend(value_crupier_card_stay)
        crupier_hand = sum(crupier_cards)
    
    if crupier_hand > 21:
        end_game('Usted gana!', 'Felicitaciones.')
    elif (crupier_hand <= 21) and (crupier_hand > player_hand):
        end_game('Crupier gana!', 'Vuelve a intentarlo.')
    elif (crupier_hand < 21) and (crupier_hand < player_hand):
        end_game('Usted gana!', 'Felicitaciones.')
    elif crupier_hand == player_hand:
        end_game('Nada para nadie!', 'Empate.')
        
    img_url_2 = card_2['image']
    image_2 = Image.open(requests.get(img_url_2, stream=True).raw)
    image_2 = image_2.resize((175, 225), Image.ANTIALIAS)
    photo_2 = ImageTk.PhotoImage(image_2)
    label_2.config(image=photo_2)
    label_2.image = photo_2
        
    print(f'Crupier hand: {crupier_hand}')
    print(f'Player hand: {player_hand}')
    print('-------------------------------------------------')
    
def center_window(w, h):
    window_w = w
    window_h = h
    window.geometry(f'{window_w}x{window_h}')
    screen_w = window.winfo_screenwidth()
    screen_h =  window.winfo_screenheight()
    x = (screen_w - window_w) // 2
    y = (screen_h - window_h) // 2
    window.geometry(f'+{x}+{y}')
        
#Main window config.
window = ttkbootstrap.Window(themename='darkly')
window.resizable(width=False, height=False)
center_window(300,200)
window.title("Blackjack")
label_x = ttkbootstrap.Label(window)
deck_id = get_deck()

#Labels config.
label_title = ttkbootstrap.Label(window, text='BJ♠', font=('Helvetica', 30))
label_title.pack(anchor='center', expand=True)

label_1 = tk.Label(window)
label_1.place(x=20, y=100)
label_2 = tk.Label(window)
label_2.place(x=100, y=100)

label_3 = tk.Label(window)
label_3.place(x=20, y=350)
label_4 = tk.Label(window)
label_4.place(x=100, y=350)

#Buttons config.
button_start_game = ttkbootstrap.Button(window, text="Iniciar", command=start_game, bootstyle='success')
button_start_game.pack(anchor='center', expand=True)
button_hit = ttkbootstrap.Button(window, text="Hit me", state='disabled', command=hit_me)
button_stay = ttkbootstrap.Button(window, text="Stay", state='disabled', command=stay)

window.mainloop()