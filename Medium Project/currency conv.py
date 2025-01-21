import tkinter as tk
from tkinter import ttk, messagebox
from requests import get

BASE_URL = "https://free.currconv.com/"
API_KEY = "562ddaf40c95f5d58108"

def get_currencies():
    endpoint = f"api/v7/currencies?apiKey={API_KEY}"
    url = BASE_URL + endpoint
    try:
        data = get(url).json()['results']
        data = list(data.items())
        data.sort()
        return data
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch currencies: {e}")
        return []

def exchange_rate(currency1, currency2):
    endpoint = f"api/v7/convert?q={currency1}_{currency2}&compact=ultra&apiKey={API_KEY}"
    url = BASE_URL + endpoint
    try:
        data = get(url).json()
        if not data:
            return None
        return list(data.values())[0]
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch exchange rate: {e}")
        return None

def convert(currency1, currency2, amount):
    rate = exchange_rate(currency1, currency2)
    if rate is None:
        messagebox.showerror("Error", "Invalid currencies or unable to fetch rate.")
        return None
    try:
        amount = float(amount)
        return rate * amount
    except ValueError:
        messagebox.showerror("Error", "Invalid amount.")
        return None

class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")

        self.currencies = get_currencies()
        self.currency_names = [f"{curr[1]['id']} - {curr[1]['currencyName']}" for curr in self.currencies]
        self.currency_ids = [curr[1]['id'] for curr in self.currencies]

        self.setup_ui()

    def setup_ui(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky="NSEW")

        ttk.Label(frame, text="Base Currency:").grid(row=0, column=0, padx=5, pady=5, sticky="W")
        self.base_currency = ttk.Combobox(frame, values=self.currency_names, width=30)
        self.base_currency.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Amount:").grid(row=1, column=0, padx=5, pady=5, sticky="W")
        self.amount_entry = ttk.Entry(frame, width=20)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Target Currency:").grid(row=2, column=0, padx=5, pady=5, sticky="W")
        self.target_currency = ttk.Combobox(frame, values=self.currency_names, width=30)
        self.target_currency.grid(row=2, column=1, padx=5, pady=5)

        self.convert_button = ttk.Button(frame, text="Convert", command=self.convert_currency)
        self.convert_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.result_label = ttk.Label(frame, text="", font=("Arial", 14))
        self.result_label.grid(row=4, column=0, columnspan=2, pady=10)

    def convert_currency(self):
        base_currency = self.get_currency_code(self.base_currency.get())
        target_currency = self.get_currency_code(self.target_currency.get())
        amount = self.amount_entry.get()

        if not base_currency or not target_currency:
            messagebox.showerror("Error", "Please select valid currencies.")
            return

        result = convert(base_currency, target_currency, amount)
        if result is not None:
            self.result_label.config(
                text=f"{amount} {base_currency} = {result:.2f} {target_currency}")

    def get_currency_code(self, currency_text):
        if " - " in currency_text:
            return currency_text.split(" - ")[0]
        return None

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()
