import customtkinter as ctk
import tkinter as tk
import requests
import random
import time
import threading

# System Styling Config
ctk.set_appearance_mode("dark")
BG_COLOR = "#0A0A0A"        # Deep Terminal Black
TEXT_WHITE = "#FFFFFF"      # Pure White Labels
NEON_GREEN = "#00FF66"      # Profit / Value Up
NEON_RED = "#FF3333"        # Expense / Value Down
PANEL_DARK = "#121212"      # High-Contrast Component Gray

# Currency to Flag Emoji Mapping Matrix
FLAGS = {
    "USD": "🇺🇸", "EUR": "🇪🇺", "GBP": "🇬🇧", "JPY": "🇯🇵", "CAD": "🇨🇦", "AUD": "🇦🇺", "CHF": "🇨🇭", "CNY": "🇨🇳", "HKD": "🇭🇰", "NZD": "🇳🇿",
    "ZAR": "🇿🇦", "EGP": "🇪🇬", "NGN": "🇳🇬", "KES": "🇰🇪", "GHS": "🇬🇭", "MAD": "🇲🇦", "DZD": "🇩🇿", "TND": "🇹🇳", "UGX": "🇺🇬", "TZS": "🇹🇿",
    "ETB": "🇪🇹", "ZMW": "🇿🇲", "MUR": "🇲🇺", "BWP": "🇧🇼", "XOF": "🇨🇮", "XAF": "🇨🇲", "RWF": "🇷🇼", "AOA": "🇦🇴", "MZN": "🇲🇿", "SCR": "🇸🇨",
    "SEK": "🇸🇪", "NOK": "🇳🇴", "DKK": "🇩🇰", "PLN": "🇵🇱", "CZK": "🇨🇿", "HUF": "🇭🇺", "RON": "🇷🇴", "BGN": "🇧🇬", "TRY": "🇹🇷", "AED": "🇦🇪",
    "SAR": "🇸🇦", "INR": "🇮🇳", "KRW": "🇰🇷", "SGD": "🇸🇬", "MYR": "🇲🇾", "THB": "🇹🇭", "IDR": "🇮🇩", "PHP": "🇵🇭", "VND": "🇻🇳", "ILS": "🇮🇱",
    "KWD": "🇰🇼", "QAR": "🇶🇦", "OMR": "🇴🇲", "BHD": "🇧🇭", "PKR": "🇵🇰", "BDT": "🇧🇩", "LKR": "🇱🇰", "TWD": "🇹🇼", "MXN": "🇲🇽", "BRL": "🇧🇷",
    "ARS": "🇦🇷", "CLP": "🇨🇱", "COP": "🇨🇴", "PEN": "🇵🇪", "UYU": "🇺🇾", "CRC": "🇨🇷", "DOP": "🇩🇴", "ISK": "🇮🇸"
}

class CurrencyXPO(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("CurrencyXPO - Quantum Array Terminal")
        self.geometry("1350x850")
        self.configure(fg_color=BG_COLOR)
        
        # Base Master Currencies Profile List
        self.currencies = sorted(list(FLAGS.keys()))
        self.rates = {c: round(random.uniform(0.5, 150.0), 2) for c in self.currencies}
        self.rates["USD"] = 1.00
        
        self.purchase_history = []
        self.wishlist = []

        # Top Header Bar
        self.header_frame = ctk.CTkFrame(self, fg_color=PANEL_DARK, height=55, corner_radius=0)
        self.header_frame.pack(side="top", fill="x")
        
        self.logo_label = ctk.CTkLabel(self.header_frame, text="⚙️ CurrencyXPO // GLOBAL MONITOR MATRIX", font=("Courier New", 20, "bold"), text_color=NEON_GREEN)
        self.logo_label.pack(side="left", padx=20, pady=12)
        
        # Right Side Cool Dashboard Metrics Panel
        self.stats_label = ctk.CTkLabel(self.header_frame, text="[VOLATILITY: NORMAL]  [ACTIVE CORES: 8]  [SYNC: CONNECTING]", font=("Courier New", 12, "bold"), text_color="#666666")
        self.stats_label.pack(side="right", padx=20, pady=12)
        
        # Main Layout Dashboard Grid splitting Left Panels vs Right Log Terminal
        self.dashboard_grid = ctk.CTkFrame(self, fg_color=BG_COLOR, corner_radius=0)
        self.dashboard_grid.pack(side="top", fill="both", expand=True, padx=15, pady=10)
        
        self.dashboard_grid.grid_columnconfigure(0, weight=48)
        self.dashboard_grid.grid_columnconfigure(1, weight=52)
        self.dashboard_grid.grid_rowconfigure(0, weight=1)

        # Left Stack Container
        self.left_column = ctk.CTkFrame(self.dashboard_grid, fg_color=BG_COLOR)
        self.left_column.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self.left_column.grid_columnconfigure(0, weight=1)
        self.left_column.grid_rowconfigure(0, weight=45) 
        self.left_column.grid_rowconfigure(1, weight=55) 

        # Sub-Module Initializations
        self.setup_calc_module()
        self.setup_vault_module()
        self.setup_log_module()
        self.setup_marquee_bar()
        
        # Multi-Thread Engine Booting (Ensures UI doesn't stutter while fetching API)
        threading.Thread(target=self.fetch_live_rates, daemon=True).start()
        
        self.update_live_market_log()
        self.animate_marquee()

    def fetch_live_rates(self):
        try:
            response = requests.get("https://open.er-api.com/v6/latest/USD", timeout=5)
            if response.status_code == 200:
                fetched_rates = response.json().get("rates", {})
                for currency, rate in fetched_rates.items():
                    self.rates[currency] = rate
                    if currency not in self.currencies and currency not in FLAGS:
                        FLAGS[currency] = "🏳️"  # Default fallback flag for unknown discovered pairs
                        self.currencies.append(currency)
                
                self.currencies.sort()
                # Dynamic update of display lists
                self.from_curr.configure(values=[f"{FLAGS.get(c, '🏳️')} {c}" for c in self.currencies])
                self.stats_label.configure(text="[VOLATILITY: REALTIME]  [ACTIVE CORES: 8]  [SYNC: SECURE]", text_color=NEON_GREEN)
        except Exception:
            self.stats_label.configure(text="[VOLATILITY: SIMULATED]  [ACTIVE CORES: 4]  [SYNC: LOCAL]", text_color=NEON_RED)

    # ---------------- CALCULATOR MODULE (TOP LEFT) ----------------
    def setup_calc_module(self):
        calc_frame = ctk.CTkFrame(self.left_column, fg_color=PANEL_DARK, border_color="#222222", border_width=1)
        calc_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        
        lbl = ctk.CTkLabel(calc_frame, text="[ GLOBAL CROSS-EXCHANGE GRAPH ]", font=("Courier New", 14, "bold"), text_color=TEXT_WHITE)
        lbl.pack(anchor="w", padx=15, pady=(10, 5))
        
        input_row = ctk.CTkFrame(calc_frame, fg_color="transparent")
        input_row.pack(fill="x", padx=15, pady=5)
        
        self.amount_entry = ctk.CTkEntry(input_row, placeholder_text="Enter Numerical Quant...", fg_color=BG_COLOR, text_color=TEXT_WHITE, font=("Courier New", 12), height=28)
        self.amount_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        # Display formatted currencies with Flag Icons inside the Selection list
        display_options = [f"{FLAGS.get(c, '🏳️')} {c}" for c in self.currencies]
        self.from_curr = ctk.CTkOptionMenu(input_row, values=display_options, fg_color=BG_COLOR, button_color="#222222", font=("Courier New", 12), width=110, height=28)
        self.from_curr.pack(side="left", padx=5)
        self.from_curr.set("🇺🇸 USD")
        
        calc_btn = ctk.CTkButton(input_row, text="COMPUTE MATRIX", fg_color=NEON_GREEN, text_color=BG_COLOR, font=("Courier New", 12, "bold"), width=120, height=28, command=self.perform_calculation)
        calc_btn.pack(side="left", padx=(5, 0))
        
        self.calc_output = ctk.CTkTextbox(calc_frame, fg_color=BG_COLOR, font=("Courier New", 12), text_color=TEXT_WHITE, border_color="#1A1A1A", border_width=1)
        self.calc_output.pack(fill="both", expand=True, padx=15, pady=(5, 15))
        self.calc_output.insert("end", "System operational. Input quantitative base variables to resolve equations.")

    def perform_calculation(self):
        try:
            amt = float(self.amount_entry.get())
            raw_selection = self.from_curr.get()
            base = raw_selection.split()[-1] # Pull out currency code part only
            base_rate = self.rates[base]
            usd_amt = amt / base_rate
            
            self.calc_output.delete("1.0", "end")
            self.calc_output.insert("end", f"--- COMPLETE TRANS-CONVERSION SYSTEM FOR {amt:,} {base} ---\n\n")
            
            count = 0
            row_str = ""
            for target in sorted(self.rates.keys()):
                converted = usd_amt * self.rates[target]
                flag = FLAGS.get(target, "🏳️")
                
                # Format with neat column gaps
                item_entry = f"{flag} {target}: {converted:<12,.2f} "
                row_str += f"{item_entry:<24}"
                count += 1
                if count == 3:  # Perfect spacing constraint parameters 
                    self.calc_output.insert("end", row_str + "\n")
                    row_str = ""
                    count = 0
            if row_str:
                self.calc_output.insert("end", row_str + "\n")
        except ValueError:
            self.calc_output.delete("1.0", "end")
            self.calc_output.insert("end", "SYNTAX ERROR: CRITICAL NON-NUMERIC CHARACTER DETECTED.")

    # ---------------- VAULT & LEDGER MODULE (BOTTOM LEFT) ----------------
    def setup_vault_module(self):
        vault_frame = ctk.CTkFrame(self.left_column, fg_color=PANEL_DARK, border_color="#222222", border_width=1)
        vault_frame.grid(row=1, column=0, sticky="nsew")
        
        vault_frame.grid_columnconfigure(0, weight=1)
        vault_frame.grid_columnconfigure(1, weight=1)
        vault_frame.grid_rowconfigure(0, weight=1)

        # Expense Tracking Segment
        p_frame = ctk.CTkFrame(vault_frame, fg_color="transparent")
        p_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        ctk.CTkLabel(p_frame, text="🟥 [ TRANSACTION LOGS ]", font=("Courier New", 13, "bold"), text_color=NEON_RED).pack(anchor="w")
        self.item_entry = ctk.CTkEntry(p_frame, placeholder_text="Item Description", fg_color=BG_COLOR, height=25, font=("Courier New", 11))
        self.item_entry.pack(fill="x", pady=2)
        self.cost_entry = ctk.CTkEntry(p_frame, placeholder_text="Amount (e.g. 50 EUR)", fg_color=BG_COLOR, height=25, font=("Courier New", 11))
        self.cost_entry.pack(fill="x", pady=2)
        
        ctk.CTkButton(p_frame, text="APPEND OUTFLOW", fg_color=NEON_RED, text_color=TEXT_WHITE, font=("Courier New", 11, "bold"), height=25, command=self.add_purchase).pack(fill="x", pady=4)
        self.purchase_box = ctk.CTkTextbox(p_frame, fg_color=BG_COLOR, font=("Courier New", 11))
        self.purchase_box.pack(fill="both", expand=True)

        # Savings Asset Allocator Segment
        s_frame = ctk.CTkFrame(vault_frame, fg_color="transparent")
        s_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        ctk.CTkLabel(s_frame, text="🟩 [ ASSET TARGET VAULT ]", font=("Courier New", 13, "bold"), text_color=NEON_GREEN).pack(anchor="w")
        self.save_entry = ctk.CTkEntry(s_frame, placeholder_text="Target Allocation Target", fg_color=BG_COLOR, height=25, font=("Courier New", 11))
        self.save_entry.pack(fill="x", pady=2)
        self.target_entry = ctk.CTkEntry(s_frame, placeholder_text="Total Capital Needed", fg_color=BG_COLOR, height=25, font=("Courier New", 11))
        self.target_entry.pack(fill="x", pady=2)
        
        ctk.CTkButton(s_frame, text="COMMIT TARGET", fg_color=NEON_GREEN, text_color=BG_COLOR, font=("Courier New", 11, "bold"), height=25, command=self.add_wishlist).pack(fill="x", pady=4)
        self.wishlist_box = ctk.CTkTextbox(s_frame, fg_color=BG_COLOR, font=("Courier New", 11))
        self.wishlist_box.pack(fill="both", expand=True)

    def add_purchase(self):
        if self.item_entry.get() and self.cost_entry.get():
            self.purchase_history.append(f"[-] DEBIT // {self.item_entry.get()}: {self.cost_entry.get()}")
            self.purchase_box.delete("1.0", "end")
            self.purchase_box.insert("end", "\n".join(self.purchase_history))
            self.item_entry.delete(0, 'end'); self.cost_entry.delete(0, 'end')

    def add_wishlist(self):
        if self.save_entry.get() and self.target_entry.get():
            self.wishlist.append(f"[+] HELD // {self.save_entry.get()} -> Target: {self.target_entry.get()}")
            self.wishlist_box.delete("1.0", "end")
            self.wishlist_box.insert("end", "\n".join(self.wishlist))
            self.save_entry.delete(0, 'end'); self.target_entry.delete(0, 'end')

    # ---------------- LIVE CONSOLE STREAM LOG MODULE (RIGHT COLUMN) ----------------
    def setup_log_module(self):
        log_frame = ctk.CTkFrame(self.dashboard_grid, fg_color=PANEL_DARK, border_color="#222222", border_width=1)
        log_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        lbl = ctk.CTkLabel(log_frame, text="--- LIVE MACRO QUANTUM DATASTREAM ---", font=("Courier New", 14, "bold"), text_color=TEXT_WHITE)
        lbl.pack(anchor="w", padx=15, pady=(10, 5))
        
        self.log_container = tk.Frame(log_frame, bg=PANEL_DARK)
        self.log_container.pack(fill="both", expand=True, padx=15, pady=(5, 15))
        
        self.log_text = tk.Text(self.log_container, bg=BG_COLOR, fg=TEXT_WHITE, font=("Courier New", 11), bd=1, relief="solid", highlightthickness=0)
        self.log_text.pack(side="left", fill="both", expand=True)
        
        self.log_text.tag_config("UP_TAG", foreground=NEON_GREEN)
        self.log_text.tag_config("DOWN_TAG", foreground=NEON_RED)
        self.log_text.tag_config("SYSTEM_TAG", foreground="#444444")
        
        self.log_text.insert("end", "[SYSTEM BOOT COMPLETION SUCCESS] Matrix Stream Online.\n", "SYSTEM_TAG")
        self.log_text.configure(state="disabled")

    def update_live_market_log(self):
        if self.currencies:
            curr = random.choice(self.currencies)
            if curr != "USD":
                change = random.uniform(-0.015, 0.015)
                self.rates[curr] = max(0.0001, round(self.rates[curr] * (1 + change), 5))
                
                timestamp = time.strftime("%H:%M:%S")
                flag = FLAGS.get(curr, "🏳️")
                
                self.log_text.configure(state="normal")
                self.log_text.insert("end", f"[{timestamp}] VOLATILITY DETECTED: {flag} {curr}/USD -> {self.rates[curr]:,.5f} (")
                if change >= 0:
                    self.log_text.insert("end", f"▲ HIGH {change*100:+.3f}%", "UP_TAG")
                else:
                    self.log_text.insert("end", f"▼ LOSS {change*100:+.3f}%", "DOWN_TAG")
                self.log_text.insert("end", ")\n")
                
                self.log_text.see("end")
                self.log_text.configure(state="disabled")
            
        self.after(600, self.update_live_market_log)

    # ---------------- EXPANDED FOOTER TICKER MARQUEE ----------------
    def setup_marquee_bar(self):
        self.marquee_frame = ctk.CTkFrame(self, fg_color=PANEL_DARK, height=35, corner_radius=0)
        self.marquee_frame.pack(side="bottom", fill="x")
        
        self.canvas = tk.Canvas(self.marquee_frame, bg=PANEL_DARK, highlightthickness=0, height=30)
        self.canvas.pack(fill="both", expand=True)
        
        # Build ultra-dense ticker text strings
        self.build_marquee_content()

    def build_marquee_content(self):
        self.canvas.delete("all")
        # Pull 25 items for a high-intensity ticker feed
        sampled_currencies = random.sample(self.currencies, min(25, len(self.currencies)))
        
        current_x = 1350
        for currency in sampled_currencies:
            flag = FLAGS.get(currency, "🏳️")
            rate_val = self.rates[currency]
            text_string = f" {flag} {currency}: {rate_val:,.2f} || "
            
            # Alternate item colors randomly to emulate flashing terminal feeds
            text_color = random.choice([NEON_GREEN, TEXT_WHITE, NEON_RED])
            
            item = self.canvas.create_text(current_x, 15, text=text_string, font=("Courier New", 11, "bold"), fill=text_color, anchor="w")
            # Shift spacing coordinate based on string pixel width bounds
            bounds = self.canvas.bbox(item)
            text_width = bounds[2] - bounds[0]
            current_x += text_width

    def animate_marquee(self):
        # Move all items leftwards
        all_items = self.canvas.find_all()
        for item in all_items:
            self.canvas.move(item, -2, 0)
            
        # Re-verify layout text structures if items scroll out of sight lines
        if all_items:
            last_item_bounds = self.canvas.bbox(all_items[-1])
            if last_item_bounds and last_item_bounds[2] < 0:
                self.build_marquee_content()
                
        self.after(20, self.animate_marquee)

if __name__ == "__main__":
    app = CurrencyXPO()
    app.mainloop()