import tkinter as tk
from tkinter import simpledialog, messagebox
import random

MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

SYMBOL_COUNT = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}

SYMBOL_VALUE = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}


class SlotMachine:
    def __init__(self, root):
        self.root = root
        self.root.title("Machine à Sous")
        self.root.geometry("600x500")
        self.root.configure(bg="black")

        self.balance = 0

        self.create_widgets()

    def create_widgets(self):
        self.balance_label = tk.Label(self.root, text=f"Solde: $0", font=("Arial", 16), bg="black", fg="white")
        self.balance_label.pack(pady=10)

        self.deposit_button = tk.Button(self.root, text="Déposer de l'argent", font=("Arial", 14), command=self.deposit)
        self.deposit_button.pack(pady=5)

        self.deposit_entry = tk.Entry(self.root, font=("Arial", 14))
        self.deposit_entry.pack(pady=5)

        self.lines_label = tk.Label(self.root, text="Nombre de lignes: 1", font=("Arial", 14), bg="black", fg="white")
        self.lines_label.pack()
        self.lines_slider = tk.Scale(self.root, from_=1, to=MAX_LINES, orient="horizontal", command=self.update_lines,
                                     bg="black", fg="white")
        self.lines_slider.pack()

        self.bet_label = tk.Label(self.root, text=f"Mise par ligne: $1", font=("Arial", 14), bg="black", fg="white")
        self.bet_label.pack()
        self.bet_slider = tk.Scale(self.root, from_=MIN_BET, to=MAX_BET, orient="horizontal", command=self.update_bet,
                                   bg="black", fg="white")
        self.bet_slider.pack()

        self.spin_button = tk.Button(self.root, text="Tourner", font=("Arial", 16, "bold"), bg="gold",
                                     command=self.spin)
        self.spin_button.pack(pady=20)

        self.result_label = tk.Label(self.root, text="", font=("Arial", 14), bg="black", fg="white")
        self.result_label.pack()

        self.slot_display = tk.Label(self.root, text="[ ]  [ ]  [ ]\n[ ]  [ ]  [ ]\n[ ]  [ ]  [ ]",
                                     font=("Arial", 20, "bold"), bg="black", fg="white")
        self.slot_display.pack()

    def deposit(self):
        amount = self.deposit_entry.get()
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                self.balance += amount
                self.balance_label.config(text=f"Solde: ${self.balance}")
            else:
                messagebox.showerror("Erreur", "Veuillez entrer un montant valide.")
        else:
            messagebox.showerror("Erreur", "Veuillez entrer un montant numérique.")

    def update_lines(self, value):
        self.lines_label.config(text=f"Nombre de lignes: {value}")

    def update_bet(self, value):
        self.bet_label.config(text=f"Mise par ligne: ${value}")

    def get_slot_machine_spin(self):
        all_symbols = []
        for symbol, count in SYMBOL_COUNT.items():
            all_symbols.extend([symbol] * count)

        columns = []
        for _ in range(COLS):
            column = random.sample(all_symbols, ROWS)
            columns.append(column)

        return columns

    def check_winnings(self, columns, lines, bet):
        winnings = 0
        winning_lines = []
        for line in range(lines):
            symbol = columns[0][line]
            if all(column[line] == symbol for column in columns):
                winnings += SYMBOL_VALUE[symbol] * bet
                winning_lines.append(line + 1)
        return winnings, winning_lines

    def spin(self):
        lines = int(self.lines_slider.get())
        bet = int(self.bet_slider.get())
        total_bet = bet * lines

        if total_bet > self.balance:
            messagebox.showerror("Erreur", f"Solde insuffisant! Solde actuel: ${self.balance}")
            return

        self.balance -= total_bet
        self.balance_label.config(text=f"Solde: ${self.balance}")

        slots = self.get_slot_machine_spin()
        display_text = "\n".join(["  ".join(row) for row in zip(*slots)])
        self.slot_display.config(text=display_text)

        winnings, winning_lines = self.check_winnings(slots, lines, bet)
        self.balance += winnings
        self.balance_label.config(text=f"Solde: ${self.balance}")

        if winnings > 0:
            self.result_label.config(
                text=f"Bravo! Vous avez gagné ${winnings} sur les lignes {', '.join(map(str, winning_lines))}!",
                fg="green")
        else:
            self.result_label.config(text="Dommage, essayez encore!", fg="red")


if __name__ == "__main__":
    root = tk.Tk()
    app = SlotMachine(root)
    root.mainloop()
