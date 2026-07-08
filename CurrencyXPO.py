import customtkinter as ctk
import tkinter as tk
import requests
import random
import time
import threading

# System Styling Config
ctk.set_appearance_mode("dark")
BG_COLOR = "#0A0A0A"        # Deep Black Terminal
TEXT_WHITE = "#FFFFFF"      # White Labels
NEON_GREEN = "#00FF66"      # Up / Profits
NEON_RED = "#FF3333"        # Down / Expenses
PANEL_DARK = "#121212"      # Off-black panel division

class CurrencyXPO(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("CurrencyXPO - Global Matrix Terminal")
        self.geometry("1300x800")
        self.configure(fg_color=BG_COLOR)
        
        # Comprehensive Master List of Global Currencies (African, European, Asian, etc.)
        self.currencies = [
            "USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF", "CNY", "HKD", "NZD",
            # African Currencies
            "ZAR", "EGP", "NGN", "KES", "GHS", "MAD", "DZD", "TND", "UGX", "TZS", 
            "ETB", "ZMW", "MUR", "BWP", "XOF", "XAF", "RWF", "AOA", "MZN", "SCR",
            # European (Non-EUR)
            "CHF", "SEK", "NOK", "DKK", "PLN", "CZK", "HUF", "RON", "BGN", "TRY", 
            # Middle East & Asia
            "AED", "SAR", "INR", "KRW", "SGD", "MYR", "THB", "IDR", "PHP", "VND", 
            "ILS", "KWD", "QAR", "OMR", "BHD", "PKR", "BDT", "LKR", "TWD",
            # Americas & Others
            "MXN", "BRL", "ARS", "CLP", "COP", "PEN", "UYU", "CRC", "DOP", "ISK"
        ]
        
        # Fallback local data setup in case API is unreachable initially
        self.rates = {c: round(random.uniform(0.5, 150.0), 2) for c in self.currencies}
        self.rates["USD"] = 1.00
        
        self.purchase_history = []
        self.wishlist = []

        # Top Header Bar
        self.header_frame = ctk.CTkFrame(self, fg_color=PANEL_DARK, height=50, corner_radius=0)
        self.header_frame.pack(side="top", fill="x")
        
        self.logo_label = ctk.CTkLabel(self.header_frame, text="CurrencyXPO // ALL-WORLD QUANT TERMINAL", font=("Courier New", 20, "bold"), text_color=NEON_GREEN)
        self.logo_label.pack(side="left", padx=20, pady=10)
        
        self.api_status_label = ctk.CTkLabel(self.header_frame, text="[API: CONNECTING...]", font=("Courier New", 12), text_color="#888888")
        self.api_status_label.pack(side="right", padx=20, pady=10)
        
        # Main Layout Grid
        self.dashboard_grid = ctk.CTkFrame(self, fg_color=BG_COLOR, corner_radius=0)
        self.dashboard_grid.pack(side="top", fill="both", expand=True, padx=15, pady=15)
        
        self.dashboard_grid.grid_columnconfigure(0, weight=45)
        self.dashboard_grid.grid_columnconfigure(1, weight=55)
        self.dashboard_grid.grid_rowconfigure(0, weight=1)

        # Left Column Frame
        self.left_column = ctk.CTkFrame(self.dashboard_grid, fg_color=BG_COLOR)
        self.left_column.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self.left_column.grid_columnconfigure(0, weight=1)
        self.left_column.grid_rowconfigure(0, weight=45) 
        self.left_column.grid_rowconfigure(1, weight=55) 

        # Sub-Modules
        self.setup_calc_module()
        self.setup_vault_module()
        self.setup_log_module()
        self.setup_marquee_bar()
        
        # Async Network Fetch so UI doesn't freeze on launch
        threading.Thread(target=self.fetch_live_rates, daemon=True).start()
        
        # Live Interface Engine loops
        self.update_live_market_log()
        self.animate_marquee()

    def fetch_live_rates(self):
        try:
            # Fetching live feeds via an open real-time API exchange
            response = requests.get("https://open.er-api.com/v6/latest/USD", timeout=5)
            if response.status_code == 200:
                data = response.json()
                fetched_rates = data.get("rates", {})
                
                # Dynamic Sync: Add any real-world currency missing from our local master arrays
                for currency, rate in fetched_rates.items():
                    self.rates[currency] = rate
                    if currency not in self.currencies:
                        self.currencies.append(currency)
                
                self.currencies.sort()
                self.from_curr.configure(values=self.currencies) # Push newly discovered symbols to calculator list
                self.api_status_label.configure(text="[API: LIVE SECURE SYNCED]", text_color=NEON_GREEN)
        except Exception:
            self.api_status_label.configure(text="[API: OFFLINE MOCK MODE]", text_color=NEON_RED)

    # ---------------- MODULE: MULTI-CALCULATOR ----------------
    def setup_calc_module(self):
        calc_frame = ctk.CTkFrame(self.left_column, fg_color=PANEL_DARK, border_color="#222222", border_width=1)
        calc_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        
        lbl = ctk.CTkLabel(calc_frame, text="[ GLOBAL CONVERSION MATRIX ]", font=("Courier New", 14, "bold"), text_color=TEXT_WHITE)
        lbl.pack(anchor="w", padx=15, pady=(10, 5))
        
        input_row = ctk.CTkFrame(calc_frame, fg_color="transparent")
        input_row.pack(fill="x", padx=15, pady=5)
        
        self.amount_entry = ctk.CTkEntry(input_row, placeholder_text="Enter Amount", fg_color=BG_COLOR, text_color=TEXT_WHITE, font=("Courier New", 12), height=28)
        self.amount_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        self.from_curr = ctk.CTkOptionMenu(input_row, values=self.currencies, fg_color=BG_COLOR, button_color="#222222", font=("Courier New", 12), width=95, height=28)
        self.from_curr.pack(side="left", padx=5)
        self.from_curr.set("USD")
        
        calc_btn = ctk.CTkButton(input_row, text="COMPUTE ALL", fg_color=NEON_GREEN, text_color=BG_COLOR, font=("Courier New", 12, "bold"), width=100, height=28, command=self.perform_calculation)
        calc_btn.pack(side="left", padx=(5, 0))
        
        self.calc_output = ctk.CTkTextbox(calc_frame, fg_color=BG_COLOR, font=("Courier New", 12), text_color=TEXT_WHITE, border_color="#1A1A1A", border_width=1)
        self.calc_output.pack(fill="both", expand=True, padx=15, pady=(5, 15))
        self.calc_output.insert("end", "Enter data profile metrics to execute matrix cross-conversion...")

    def perform_calculation(self):
        try:
            amt = float(self.amount_entry.get())
            base = self.from_curr.get()
            base_rate = self.rates[base]
            usd_amt = amt / base_rate
            
            self.calc_output.delete("1.0", "end")
            self.calc_output.insert("end", f"--- ALL WORLD OUT-OUTPUT MATRIX FOR {amt:,} {base} ---\n\n")
            
            # Print calculated output grouped neatly into rows
            count = 0
            row_str = ""
            for target in sorted(self.rates.keys()):
                converted = usd_amt * self.rates[target]
                row_str += f"{target}: {converted:<13,.2f}  "
                count += 1
                if count == 3:  # Arrange nicely in 3 clean horizontal data columns
                    self.calc_output.insert("end", row_str + "\n")
                    row_str = ""
                    count = 0
            if row_str:
                self.calc_output.insert("end", row_str + "\n")
        except ValueError:
            self.calc_output.delete("1.0", "end")
            self.calc_output.insert("end", "ERROR: INVALID LOGICAL VALUE ENTERED.")

    # ---------------- MODULE: PURCHASES & SAVINGS VAULT ----------------
    def setup_vault_module(self):
        vault_frame = ctk.CTkFrame(self.left_column, fg_color=PANEL_DARK, border_color="#222222", border_width=1)
        vault_frame.grid(row=1, column=0, sticky="nsew")
        
        vault_frame.grid_columnconfigure(0, weight=1)
        vault_frame.grid_columnconfigure(1, weight=1)
        vault_frame.grid_rowconfigure(0, weight=1)

        # Expenses Ledger
        p_frame = ctk.CTkFrame(vault_frame, fg_color="transparent")
        p_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        ctk.CTkLabel(p_frame, text="[ TRACKED PURCHASES ]", font=("Courier New", 13, "bold"), text_color=NEON_RED).pack(anchor="w")
        self.item_entry = ctk.CTkEntry(p_frame, placeholder_text="Item / Metric", fg_color=BG_COLOR, height=25, font=("Courier New", 11))
        self.item_entry.pack(fill="x", pady=2)
        self.cost_entry = ctk.CTkEntry(p_frame, placeholder_text="Cost & Denomination", fg_color=BG_COLOR, height=25, font=("Courier New", 11))
        self.cost_entry.pack(fill="x", pady=2)
        
        ctk.CTkButton(p_frame, text="+ Append Expense", fg_color=NEON_RED, text_color=TEXT_WHITE, font=("Courier New", 11, "bold"), height=25, command=self.add_purchase).pack(fill="x", pady=4)
        self.purchase_box = ctk.CTkTextbox(p_frame, fg_color=BG_COLOR, font=("Courier New", 11))
        self.purchase_box.pack(fill="both", expand=True)

        # Savings Vault Target 
        s_frame = ctk.CTkFrame(vault_frame, fg_color="transparent")
        s_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        ctk.CTkLabel(s_frame, text="[ RESERVED TARGETS ]", font=("Courier New", 13, "bold"), text_color=NEON_GREEN).pack(anchor="w")
        self.save_entry = ctk.CTkEntry(s_frame, placeholder_text="Reserve Profile Name", fg_color=BG_COLOR, height=25, font=("Courier New", 11))
        self.save_entry.pack(fill="x", pady=2)
        self.target_entry = ctk.CTkEntry(s_frame, placeholder_text="Target Allocation", fg_color=BG_COLOR, height=25, font=("Courier New", 11))
        self.target_entry.pack(fill="x", pady=2)
        
        ctk.CTkButton(s_frame, text="+ Append Target Plan", fg_color=NEON_GREEN, text_color=BG_COLOR, font=("Courier New", 11, "bold"), height=25, command=self.add_wishlist).pack(fill="x", pady=4)
        self.wishlist_box = ctk.CTkTextbox(s_frame, fg_color=BG_COLOR, font=("Courier New", 11))
        self.wishlist_box.pack(fill="both", expand=True)

    def add_purchase(self):
        if self.item_entry.get() and self.cost_entry.get():
            self.purchase_history.append(f"- {self.item_entry.get()}: {self.cost_entry.get()}")
            self.purchase_box.delete("1.0", "end")
            self.purchase_box.insert("end", "\n".join(self.purchase_history))
            self.item_entry.delete(0, 'end'); self.cost_entry.delete(0, 'end')

    def add_wishlist(self):
        if self.save_entry.get() and self.target_entry.get():
            self.wishlist.append(f"> [VAULTED] {self.save_entry.get()} -> Target: {self.target_entry.get()}")
            self.wishlist_box.delete("1.0", "end")
            self.wishlist_box.insert("end", "\n".join(self.wishlist))
            self.save_entry.delete(0, 'end'); self.target_entry.delete(0, 'end')

    # ---------------- MODULE: LIVE UPDATE MONITOR LOG ----------------
    def setup_log_module(self):
        log_frame = ctk.CTkFrame(self.dashboard_grid, fg_color=PANEL_DARK, border_color="#222222", border_width=1)
        log_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        lbl = ctk.CTkLabel(log_frame, text="--- LIVE GLOBAL QUANT MONITOR FEED ---", font=("Courier New", 14, "bold"), text_color=TEXT_WHITE)
        lbl.pack(anchor="w", padx=15, pady=(10, 5))
        
        self.log_container = tk.Frame(log_frame, bg=PANEL_DARK)
        self.log_container.pack(fill="both", expand=True, padx=15, pady=(5, 15))
        
        self.log_text = tk.Text(self.log_container, bg=BG_COLOR, fg=TEXT_WHITE, font=("Courier New", 11), bd=1, relief="solid", highlightthickness=0)
        self.log_text.pack(side="left", fill="both", expand=True)
        
        self.log_text.tag_config("UP_TAG", foreground=NEON_GREEN)
        self.log_text.tag_config("DOWN_TAG", foreground=NEON_RED)
        self.log_text.tag_config("SYSTEM_TAG", foreground="#555555")
        
        self.log_text.insert("end", "[SYSTEM TERMINAL HOOKED COMPLETE] Stream Live Global Array Loaded.\n", "SYSTEM_TAG")
        self.log_text.configure(state="disabled")

    def update_live_market_log(self):
        if self.currencies:
            curr = random.choice(self.currencies)
            if curr != "USD":
                # Simulated flux shifting calculations 
                change = random.uniform(-0.02, 0.02)
                self.rates[curr] = max(0.0001, round(self.rates[curr] * (1 + change), 5))
                
                timestamp = time.strftime("%H:%M:%S")
                self.log_text.configure(state="normal")
                
                self.log_text.insert("end", f"[{timestamp}] FLUX UPDATE: {curr}/USD at {self.rates[curr]:,.5f} (")
                if change >= 0:
                    self.log_text.insert("end", f"▲ UP {change*100:+.3f}%", "UP_TAG")
                else:
                    self.log_text.insert("end", f"▼ DOWN {change*100:+.3f}%", "DOWN_TAG")
                self.log_text.insert("end", ")\n")
                
                self.log_text.see("end")
                self.log_text.configure(state="disabled")
            
        self.after(800, self.update_live_market_log)

    # ---------------- FOOTER MARQUEE EFFECT ----------------
    def setup_marquee_bar(self):
        self.marquee_frame = ctk.CTkFrame(self, fg_color=PANEL_DARK, height=30, corner_radius=0)
        self.marquee_frame.pack(side="bottom", fill="x")
        
        self.canvas = tk.Canvas(self.marquee_frame, bg=PANEL_DARK, highlightthickness=0, height=25)
        self.canvas.pack(fill="both", expand=True)
        
        # Build marquee using 15 random items for density
        marquee_items = random.sample(self.currencies, min(15, len(self.currencies)))
        self.marquee_text = " || ".join([f"{c}/USD: {self.rates[c]:.2f}" for c in marquee_items])
        self.text_item = self.canvas.create_text(1300, 12, text=self.marquee_text, font=("Courier New", 11), fill=NEON_GREEN, anchor="w")

    def animate_marquee(self):
        self.canvas.move(self.text_item, -2, 0)
        try:
            x1 = self.canvas.bbox(self.text_item)[2]
            if x1 < 0:
                # Cycle display items dynamically
                marquee_items = random.sample(self.currencies, min(15, len(self.currencies)))
                self.marquee_text = " || ".join([f"{c}/USD: {self.rates[c]:,.2f}" for c in marquee_items])
                self.canvas.itemconfig(self.text_item, text=self.marquee_text)
                self.canvas.coords(self.text_item, self.winfo_width(), 12)
        except (TypeError, tk.TclError):
            pass 
            
        self.after(25, self.animate_marquee)

if __name__ == "__main__":
    app = CurrencyXPO()
    app.mainloop()