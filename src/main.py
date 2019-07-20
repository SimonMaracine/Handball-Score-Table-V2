import tkinter as tk
from src.timer import Timer
# from src.second_window import second_window


def say_hello():
    print("Hello")


def main():
    root.mainloop()


root = tk.Tk()

# Configure the root and add a menu
###########################################################################################
root.geometry("1024x768")
root.option_add("*tearOff", False)
root.minsize(width=1024, height=768)
menu_bar = tk.Menu()
root.config(menu=menu_bar)
content = tk.Frame(root)

content.pack(side="top", fill="both", expand=True, padx=10, pady=10)

# File menu
###########################################################################################
file_menu = tk.Menu(menu_bar)
file_menu.add_command(label="New", state="disabled")
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

# Edit menu
###########################################################################################
edit_menu = tk.Menu(menu_bar)
edit_menu.add_command(label="Preferences", state="disabled")
menu_bar.add_cascade(label="Edit", menu=edit_menu)

# Help menu
###########################################################################################
help_menu = tk.Menu(menu_bar)
help_menu.add_command(label="About", command=say_hello)
menu_bar.add_cascade(label="Help", menu=help_menu)

# A context menu
###########################################################################################
context = tk.Menu(root)
for i in ('One', 'Two', 'Three'):
    context.add_command(label=i)
root.bind('<3>', lambda e: context.post(e.x_root, e.y_root))

# Team 1
###########################################################################################
team1_name = tk.Frame(content, borderwidth=5, relief="sunken", width=400, height=100)
tk.Label(team1_name, text="Home", font="Times, 40").pack(padx=70, pady=20)

team1_score = tk.Frame(content, borderwidth=3, relief="sunken")
score_team1 = tk.IntVar(content, value=0)
tk.Label(team1_score, text="{}".format(score_team1.get()), font="Times, 35").pack(padx=30, pady=10)

team1_players = tk.Frame(content, borderwidth=3, relief="sunken")
players1 = tk.Listbox(team1_players, font="Times, 15", height=17)
for i in range(5):
    players1.insert(i, "Player {}".format(i + 1))

team1_suspended = tk.Frame(content, borderwidth=5, relief="sunken")
players_suspended1 = tk.Listbox(team1_suspended, font="Times, 14", width=14, height=17)
for i in range(2):
    players_suspended1.insert(i, "I'm suspended")

players1.pack(padx=2, pady=2)
players_suspended1.pack(padx=2, pady=2)

team1_name.grid(column=0, row=0)
team1_score.grid(column=0, row=1)
team1_players.grid(column=0, row=3)
team1_suspended.grid(column=1, row=3)

# Team 2
###########################################################################################
team2_name = tk.Frame(content, borderwidth=5, relief="sunken", width=400, height=100)
tk.Label(team2_name, text="Guest", font="Times, 40").pack(padx=70, pady=20)

team2_score = tk.Frame(content, borderwidth=3, relief="sunken")
score_team2 = tk.IntVar(content, value=0)
tk.Label(team2_score, text="{}".format(score_team2.get()), font="Times, 35").pack(padx=30, pady=10)

team2_players = tk.Frame(content, borderwidth=3, relief="sunken")
players2 = tk.Listbox(team2_players, font="Times, 15", height=17)
for i in range(5):
    players2.insert(i, "Player {}".format(i + 1))

team2_suspended = tk.Frame(content, borderwidth=5, relief="sunken")
players_suspended2 = tk.Listbox(team2_suspended, font="Times, 14", width=14, height=17)
for i in range(3):
    players_suspended2.insert(i, "I'm suspended")

players2.pack(padx=2, pady=2)
players_suspended2.pack(padx=2, pady=2)

team2_name.grid(column=3, row=0)
team2_score.grid(column=3, row=1)
team2_players.grid(column=3, row=3)
team2_suspended.grid(column=2, row=3)

# Main timer
###########################################################################################
time_var = tk.StringVar(content, value="0")  # time in seconds
timer = Timer(time_var, 3600)
time_var.set(timer.get_time())

main_timer = tk.Frame(content, borderwidth=5, relief="sunken")
tk.Label(main_timer, textvariable=time_var, font="Times, 75").pack(padx=40, pady=10)

main_timer.grid(column=1, row=0, columnspan=2)

# Match round
###########################################################################################
match_round = tk.Frame(content, borderwidth=5, relief="sunken")
round_num = tk.IntVar(content, value=1)
tk.Label(match_round, text="{}".format(round_num.get()), font="Times, 55").pack(padx=30, pady=10)

match_round.grid(column=1, row=1, columnspan=2)

# Temp button
###########################################################################################
tk.Button(content, text="Start timer", command=timer.start).grid(column=0, row=4)
tk.Button(content, text="Stop timer", command=timer.stop).grid(column=1, row=4)
tk.Button(content, text="Pause timer", command=timer.pause).grid(column=2, row=4)

# Second window
###########################################################################################
second_window = tk.Toplevel()
content2 = tk.Frame(second_window)

content2.pack(side="top", fill="both", expand=True, padx=10, pady=10)


team1_name = tk.Frame(content2, borderwidth=5, relief="sunken", width=400, height=100)
tk.Label(team1_name, text="Home", font="Times, 40").pack(padx=70, pady=20)

team1_score = tk.Frame(content2, borderwidth=3, relief="sunken")
score_team1 = tk.IntVar(content2, value=0)
tk.Label(team1_score, text="{}".format(score_team1.get()), font="Times, 35").pack(padx=30, pady=10)

team1_players = tk.Frame(content2, borderwidth=3, relief="sunken")
players1 = tk.Listbox(team1_players, font="Times, 15", height=17)
for i in range(5):
    players1.insert(i, "Player {}".format(i + 1))

team1_suspended = tk.Frame(content2, borderwidth=5, relief="sunken")
players_suspended1 = tk.Listbox(team1_suspended, font="Times, 14", width=14, height=17)
for i in range(2):
    players_suspended1.insert(i, "I'm suspended")

players1.pack(padx=2, pady=2)
players_suspended1.pack(padx=2, pady=2)

team1_name.grid(column=0, row=0)
team1_score.grid(column=0, row=1)
team1_players.grid(column=0, row=3)
team1_suspended.grid(column=1, row=3)


team2_name = tk.Frame(content2, borderwidth=5, relief="sunken", width=400, height=100)
tk.Label(team2_name, text="Guest", font="Times, 40").pack(padx=70, pady=20)

team2_score = tk.Frame(content2, borderwidth=3, relief="sunken")
score_team2 = tk.IntVar(content2, value=0)
tk.Label(team2_score, text="{}".format(score_team2.get()), font="Times, 35").pack(padx=30, pady=10)

team2_players = tk.Frame(content2, borderwidth=3, relief="sunken")
players2 = tk.Listbox(team2_players, font="Times, 15", height=17)
for i in range(5):
    players2.insert(i, "Player {}".format(i + 1))

team2_suspended = tk.Frame(content2, borderwidth=5, relief="sunken")
players_suspended2 = tk.Listbox(team2_suspended, font="Times, 14", width=14, height=17)
for i in range(3):
    players_suspended2.insert(i, "I'm suspended")

players2.pack(padx=2, pady=2)
players_suspended2.pack(padx=2, pady=2)

team2_name.grid(column=3, row=0)
team2_score.grid(column=3, row=1)
team2_players.grid(column=3, row=3)
team2_suspended.grid(column=2, row=3)


main_timer = tk.Frame(content2, borderwidth=5, relief="sunken")
tk.Label(main_timer, textvariable=time_var, font="Times, 75").pack(padx=40, pady=10)

main_timer.grid(column=1, row=0, columnspan=2)


match_round = tk.Frame(content2, borderwidth=5, relief="sunken")
tk.Label(match_round, text="{}".format(round_num.get()), font="Times, 55").pack(padx=30, pady=10)

match_round.grid(column=1, row=1, columnspan=2)
