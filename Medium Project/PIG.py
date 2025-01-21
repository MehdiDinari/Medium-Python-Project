import random
import tkinter as tk
from tkinter import messagebox, simpledialog

# Fonction pour lancer le dé
def roll():
    return random.randint(1, 6)

class DiceGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Jeu de Dés - Amélioré")
        self.master.geometry("600x400")  # Fenêtre plus grande
        self.master.configure(bg="#2C3E50")  # Couleur de fond modernisée

        self.high_score = 0
        self.max_score = 50
        self.player_scores = []
        self.current_player = 0

        self.setup_game()

    def setup_game(self):
        self.players = self.ask_number_of_players()
        self.player_scores = [0] * self.players

        self.title_label = tk.Label(self.master, text="Jeu de Dés", font=("Helvetica", 28, "bold"), bg="#2C3E50", fg="#ECF0F1")
        self.title_label.pack(pady=10)

        self.max_score_label = tk.Label(self.master, text=f"Score maximum: {self.max_score}", font=("Helvetica", 18), bg="#2C3E50", fg="#E74C3C")
        self.max_score_label.pack(pady=5)

        self.score_label = tk.Label(self.master, text=f"Scores: {self.player_scores}", font=("Helvetica", 16), bg="#2C3E50", fg="#ECF0F1")
        self.score_label.pack(pady=10)

        self.roll_button = tk.Button(self.master, text="🎲 Lancer le dé 🎲", command=self.roll_dice, font=("Helvetica", 16, "bold"), bg="#27AE60", fg="white", padx=10, pady=5)
        self.roll_button.pack(pady=10)

        self.end_turn_button = tk.Button(self.master, text="🔄 Terminer le tour", command=self.end_turn, font=("Helvetica", 16, "bold"), bg="#C0392B", fg="white", padx=10, pady=5)
        self.end_turn_button.pack(pady=10)

        self.message_label = tk.Label(self.master, text="", font=("Helvetica", 16), bg="#2C3E50", fg="#ECF0F1")
        self.message_label.pack(pady=10)

        self.update_message(f"C'est le tour du joueur {self.current_player + 1}!")

    def ask_number_of_players(self):
        while True:
            players = simpledialog.askinteger("Nombre de joueurs", "Entrez le nombre de joueurs (2 - 4):")
            if players in [2, 3, 4]:
                return players
            else:
                messagebox.showerror("Erreur", "Le nombre de joueurs doit être entre 2 et 4.")

    def roll_dice(self):
        value = roll()
        if value == 1:
            self.message_label.config(text="Oups! Vous avez lancé un 1! Votre score est perdu!", fg="#E74C3C")
            self.player_scores[self.current_player] = 0
            self.end_turn()
        else:
            self.player_scores[self.current_player] += value
            self.update_scores()
            self.update_message(f"Vous avez lancé: {value}. Votre score total est: {self.player_scores[self.current_player]}")
            if self.player_scores[self.current_player] >= self.max_score:
                self.end_game()

    def end_turn(self):
        self.current_player = (self.current_player + 1) % self.players
        self.update_message(f"C'est le tour du joueur {self.current_player + 1}!")

    def update_scores(self):
        self.score_label.config(text=f"Scores: {self.player_scores}")

    def update_message(self, message):
        self.message_label.config(text=message)

    def end_game(self):
        max_score = max(self.player_scores)
        winning_idx = self.player_scores.index(max_score)
        messagebox.showinfo("Fin du jeu", f"Le joueur {winning_idx + 1} est le gagnant avec un score de: {max_score}")

        if max_score > self.high_score:
            self.high_score = max_score
            messagebox.showinfo("Nouveau record", f"Nouveau record atteint par le joueur {winning_idx + 1} avec un score de: {self.high_score}")

        self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    game = DiceGame(root)
    root.mainloop()
