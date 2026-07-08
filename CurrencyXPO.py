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

# 3-Letter Clean ISO Country Identifiers & Full Names Matrix
ALPHA3 = {
    "USD": ("USA", "United States Dollar"), "EUR": ("EUR", "Euro Zone"), "GBP": ("GBR", "Great Britain Pound"), 
    "JPY": ("JPN", "Japan Yen"), "CAD": ("CAN", "Canada Dollar"), "AUD": ("AUS", "Australia Dollar"), 
    "CHF": ("CHE", "Switzerland Franc"), "CNY": ("CHN", "China Yuan"), "HKD": ("HKG", "Hong Kong Dollar"), 
    "NZD": ("NZL", "New Zealand Dollar"), "ZAR": ("ZAF", "South Africa Rand"), "EGP": ("EGY", "Egypt Pound"), 
    "NGN": ("NGA", "Nigeria Naira"), "KES": ("KEN", "Kenya Shilling"), "GHS": ("GHA", "Ghana Cedi"), 
    "MAD": ("MAR", "Morocco Dirham"), "DZD": ("DZA", "Algeria Dinars"), "TND": ("TUN", "Tunisia Dinar"), 
    "UGX": ("UGA", "Uganda Shilling"), "TZS": ("TZA", "Tanzania Shilling"), "ETB": ("ETH", "Ethiopia Birr"), 
    "ZMW": ("ZMB", "Zambia Kwacha"), "MUR": ("MUS", "Mauritius Rupee"), "BWP": ("BWA", "Botswana Pula"), 
    "XOF": ("WAF", "West African CFA Franc"), "XAF": ("CAF", "Central African CFA Franc"), "RWF": ("RWA", "Rwanda Franc"), 
    "AOA": ("AGO", "Angola Kwanza"), "MZN": ("MOZ", "Mozambique Metical"), "SCR": ("SYC", "Seychelles Rupee"),
    "SEK": ("SWE", "Sweden Krona"), "NOK": ("NOR", "Norway Krone"), "DKK": ("DNK", "Denmark Krone"), 
    "PLN": ("POL", "Poland Zloty"), "CZK": ("CZE", "Czech Koruna"), "HUF": ("HUN", "Hungary Forint"), 
    "RON": ("ROU", "Romania Leu"), "BGN": ("BGR", "Bulgaria Lev"), "TRY": ("TUR", "Turkey Lira"), 
    "AED": ("ARE", "United Arab Emirates Dirham"), "SAR": ("SAU", "Saudi Arabia Riyal"), "INR": ("IND", "India Rupee"), 
    "KRW": ("KOR", "South Korea Won"), "SGD": ("SGP", "Singapore Dollar"), "MYR": ("MYS", "Malaysia Ringgit"), 
    "THB": ("THA", "Thailand Baht"), "IDR": ("IDN", "Indonesia Rupiah"), "PHP": ("PHL", "Philippines Peso"), 
    "VND": ("VNM", "Vietnam Dong"), "ILS": ("ISR", "Israel Shekel"), "KWD": ("KWT", "Kuwaiti Dinar"), 
    "QAR": ("QAT", "Qatar Riyal"), "OMR": ("OMN", "Oman Rial"), "BHD": ("BHR", "Bahrain Dinar"), 
    "PKR": ("PAK", "Pakistan Rupee"), "BDT": ("BGD", "Bangladesh Taka"), "LKR": ("LKA", "Sri Lanka Rupee"), 
    "TWD": ("TWN", "Taiwan New Dollar"), "MXN": ("MEX", "Mexico Peso"), "BRL": ("BRA", "Brazil Real"),
    "ARS": ("ARG", "Argentina Peso"), "CLP": ("CHL", "Chile Peso"), "COP": ("COL", "Colombia Peso"), 
    "PEN": ("PER", "Peru Sol"), "UYU": ("URY", "Uruguay Peso"), "CRC": ("CRI", "Costa Rica Colon"), 
    "DOP": ("DOM", "Dominican Republic Peso"), "ISK": ("ISL", "Iceland Krona")
}

class CurrencyXPO(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("CurrencyXPO - Quantum Array Terminal")
        self.geometry("1400x850")
        self.configure(fg_color=BG_COLOR)
        
        # Base Master Currencies Profile List
        self.currencies = sorted(list(ALPHA3.keys()))
        self.rates = {c: round(random.uniform(0.5, 150.0), 2) for c in self.currencies}
        self.rates["USD"] = 1.00
        
        self.purchase_history = []
        self.wishlist = []

        # Top Header Bar
        self.header_frame = ctk.CTkFrame(self, fg_color=PANEL_DARK, height=55, corner_radius=0)
        self.header_frame.pack(side="top", fill="x")
        
        self.logo_label = ctk.CTkLabel(self.header_frame, text="⚙️ CurrencyXPO // GLOBAL MONITOR MATRIX", font=("Courier New", 20, "bold"), text_color=NEON_GREEN)
        self.logo_label.pack(side="left", padx=20, pady=12)
        
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
        self.left_column.grid_rowconfigure(0, weight=48) 
        self.left_column.grid_rowconfigure(1, weight=52) 

        # Sub-Module Initializations
        self.setup_calc_module()
        self.setup_vault_module()
        self.setup_log_module()
        self.setup_marquee_bar()
        
        # Async Network Engine Booting
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
                    if currency not in self.currencies and currency not in ALPHA3:
                        ALPHA3[currency] = (currency, f"{currency} Alternative Market")
                        self.currencies.append(currency)
                
                self.currencies.sort()
                self.filter_options()  # Sync menu layout list variables safely
                self.stats_label.configure(text="[VOLATILITY: REALTIME]  [ACTIVE CORES: 8]  [SYNC: SECURE]", text_color=NEON_GREEN)
        except Exception:
            self.stats_label.configure(text="[VOLATILITY: SIMULATED]  [ACTIVE CORES: 4]  [SYNC: LOCAL]", text_color=NEON_RED)

    # ---------------- CALCULATOR MODULE (TOP LEFT) ----------------
    def setup_calc_module(self):
        calc_frame = ctk.CTkFrame(self.left_column, fg_color=PANEL_DARK, border_color="#222222", border_width=1)
        calc_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        
        lbl = ctk.CTkLabel(calc_frame, text="[ GLOBAL CROSS-EXCHANGE GRAPH ]", font=("Courier New", 14, "bold"), text_color=TEXT_WHITE)
        lbl.pack(anchor="w", padx=15, pady=(10, 5))
        
        # Interactive Layout Filter Matrix Row
        filter_row = ctk.CTkFrame(calc_frame, fg_color="transparent")
        filter_row.pack(fill="x", padx=15, pady=2)
        
        # Live Entry Search Field Box
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.filter_options())
        
        self.search_field = ctk.CTkEntry(filter_row, textvariable=self.search_var, placeholder_text="🔍 Search Country, Code, Name...", fg_color=BG_COLOR, text_color=TEXT_WHITE, font=("Courier New", 11), height=28)
        self.search_field.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        # Option Selection Menu Dropdown
        self.from_curr = ctk.CTkOptionMenu(filter_row, values=[], fg_color=BG_COLOR, button_color="#222222", font=("Courier New", 11), width=140, height=28)
        self.from_curr.pack(side="left")
        
        # Computation Trigger Output Entry Row
        input_row = ctk.CTkFrame(calc_frame, fg_color="transparent")
        input_row.pack(fill="x", padx=15, pady=5)
        
        self.amount_entry = ctk.CTkEntry(input_row, placeholder_text="Enter Numerical Quant...", fg_color=BG_COLOR, text_color=TEXT_WHITE, font=("Courier New", 12), height=28)
        self.amount_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        calc_btn = ctk.CTkButton(input_row, text="COMPUTE MATRIX", fg_color=NEON_GREEN, text_color=BG_COLOR, font=("Courier New", 12, "bold"), width=140, height=28, command=self.perform_calculation)
        calc_btn.pack(side="left")
        
        self.calc_output = ctk.CTkTextbox(calc_frame, fg_color=BG_COLOR, font=("Courier New", 12), text_color=TEXT_WHITE, border_color="#1A1A1A", border_width=1)
        self.calc_output.pack(fill="both", expand=True, padx=15, pady=(5, 15))
        self.calc_output.insert("end", "System operational. Input search patterns and baseline values to run equations.")
        
        self.filter_options() # Populate initially

    def filter_options(self):
        query = self.search_var.get().lower().strip()
        filtered_list = []
        
        for c in self.currencies:
            code3, fullname = ALPHA3.get(c, ("???", "Alternative Asset"))
            # Match against: Code name (USD), ISO Code (USA), or Full Title Name (United States)
            if not query or query in c.lower() or query in code3.lower() or query in fullname.lower():
                filtered_list.append(f"[{code3}] {c}")
                
        if not filtered_list:
            filtered_list = ["No Match Found"]
            
        self.from_curr.configure(values=filtered_list)
        
        # Set selection choice defaults cleanly matching active query changes safely
        if "[USA] USD" in filtered_list and not query:
            self.from_curr.set("[USA] USD")
        else:
            self.from_curr.set(filtered_list[0])

    def perform_calculation(self):
        try:
            amt = float(self.amount_entry.get())
            raw_selection = self.from_curr.get()
            if raw_selection == "No Match Found":
                raise ValueError
                
            base = raw_selection.split()[-1] # Extract symbol index token text segment
            base_rate = self.rates[base]
            usd_amt = amt / base_rate
            
            self.calc_output.delete("1.0", "end")
            self.calc_output.insert("end", f"--- COMPLETE TRANS-CONVERSION SYSTEM FOR {amt:,} {base} ---\n\n")
            
            count = 0
            row_str = ""
            for target in sorted(self.rates.keys()):
                converted = usd_amt * self.rates[target]
                code3, _ = ALPHA3.get(target, ("???", ""))
                
                item_entry = f"[{code3}] {target}: {converted:<12,.2f} "
                row_str += f"{item_entry:<26}"
                count += 1
                if count == 3:  
                    self.calc_output.insert("end", row_str + "\n")
                    row_str = ""
                    count = 0
            if row_str:
                self.calc_output.insert("end", row_str + "\n")
        except ValueError:
            self.calc_output.delete("1.0", "end")
            self.calc_output.insert("end", "SYNTAX ERROR: CRITICAL INVALID VARIABLE MATCH ENCOUNTERED.")

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
                code3, _ = ALPHA3.get(curr, ("???", ""))
                
                self.log_text.configure(state="normal")
                self.log_text.insert("end", f"[{timestamp}] VOLATILITY DETECTED: [{code3}] {curr}/USD -> {self.rates[curr]:,.5f} (")
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
        
        self.build_marquee_content()

    def build_marquee_content(self):
        self.canvas.delete("all")
        sampled_currencies = random.sample(self.currencies, min(25, len(self.currencies)))
        
        current_x = 1400
        for currency in sampled_currencies:
            code3, _ = ALPHA3.get(currency, ("???", ""))
            rate_val = self.rates[currency]
            text_string = f" [{code3}] {currency}: {rate_val:,.2f} || "
            
            text_color = random.choice([NEON_GREEN, TEXT_WHITE, NEON_RED])
            
            item = self.canvas.create_text(current_x, 15, text=text_string, font=("Courier New", 11, "bold"), fill=text_color, anchor="w")
            bounds = self.canvas.bbox(item)
            text_width = bounds[2] - bounds[0]
            current_x += text_width

    def animate_marquee(self):
        all_items = self.canvas.find_all()
        for item in all_items:
            self.canvas.move(item, -2, 0)
            
        if all_items:
            last_item_bounds = self.canvas.bbox(all_items[-1])
            if last_item_bounds and last_item_bounds[2] < 0:
                self.build_marquee_content()
                
        self.after(20, self.animate_marquee)

if __name__ == "__main__":
    app = CurrencyXPO()
    app.mainloop()