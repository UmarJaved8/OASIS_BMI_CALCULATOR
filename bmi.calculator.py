import tkinter as tk
from tkinter import messagebox
import csv
import os
from datetime import datetime

HISTORY_FILE = "bmi_history.csv"

class BMICalculator:
    def __init__(self, root):
        self.root = root
        root.title("Advanced BMI Calculator")
        root.geometry("500x600")
        root.configure(bg='#2c3e50')

        tk.Label(root, text="⚖️ BMI Calculator", font=("Arial", 20, "bold"), bg='#2c3e50', fg='white').pack(pady=10)

        frame = tk.Frame(root, bg='#34495e', padx=20, pady=20)
        frame.pack(pady=10, fill=tk.X)

        tk.Label(frame, text="Weight (kg):", font=("Arial", 12), bg='#34495e', fg='white').grid(row=0, column=0, sticky='w', pady=5)
        self.weight_entry = tk.Entry(frame, font=("Arial", 12))
        self.weight_entry.grid(row=0, column=1, pady=5)

        # --- CHANGED THIS LABEL ---
        tk.Label(frame, text="Height (feet):", font=("Arial", 12), bg='#34495e', fg='white').grid(row=1, column=0, sticky='w', pady=5)
        self.height_entry = tk.Entry(frame, font=("Arial", 12))
        self.height_entry.grid(row=1, column=1, pady=5)

        tk.Button(frame, text="Calculate BMI", command=self.calculate, bg="#1abc9c", fg="white", font=("Arial", 12)).grid(row=2, column=0, columnspan=2, pady=10)

        self.result_label = tk.Label(root, text="", font=("Arial", 14), bg='#2c3e50', fg='white')
        self.result_label.pack(pady=10)

        tk.Label(root, text="History (last 10)", font=("Arial", 14), bg='#2c3e50', fg='white').pack(pady=5)
        self.history_listbox = tk.Listbox(root, height=10, font=("Consolas", 10))
        self.history_listbox.pack(padx=20, fill=tk.BOTH, expand=True)

        self.load_history()
        self.display_history()

    def calculate(self):
        try:
            w = float(self.weight_entry.get())
            h_feet = float(self.height_entry.get())
            
            # --- NEW: Convert Feet to Meters ---
            h_meters = h_feet * 0.3048
            
            if h_meters <= 0 or w <= 0: 
                raise ValueError

            bmi = w / (h_meters ** 2)
            
            if bmi < 18.5: cat = "Underweight"
            elif bmi < 25: cat = "Normal"
            elif bmi < 30: cat = "Overweight"
            else: cat = "Obese"

            self.result_label.config(text=f"BMI: {bmi:.2f} - {cat}", fg='white')
            
            # Save the original feet value so history makes sense
            with open(HISTORY_FILE, 'a', newline='') as f:
                csv.writer(f).writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), 
                                        round(w,2), 
                                        round(h_feet,2),  # Saving feet in history
                                        round(bmi,2), 
                                        cat])
            self.display_history()
        except:
            messagebox.showerror("Error", "Enter valid positive numbers.")

    def load_history(self):
        self.history = []
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r') as f:
                self.history = list(csv.reader(f))

    def display_history(self):
        self.history_listbox.delete(0, tk.END)
        for entry in self.history[-10:][::-1]:
            # Entry format: [Date, Weight, Height(ft), BMI, Category]
            self.history_listbox.insert(tk.END, f"{entry[0]} | {entry[1]}kg, {entry[2]}ft | BMI {entry[3]} ({entry[4]})")

if __name__ == "__main__":
    root = tk.Tk()
    app = BMICalculator(root)
    root.mainloop()