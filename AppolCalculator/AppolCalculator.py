import tkinter as tk
from tkinter import font

class AppolCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Appol Calculator")
        self.root.configure(bg='#000000')
        self.root.resizable(False, False)
        
        # Initialize variables
        self.current_input = ""
        self.expression = ""
        self.result_var = tk.StringVar()
        self.expression_var = tk.StringVar()
        self.result_var.set("0")
        self.expression_var.set("")
        self.operator = None
        self.previous_value = 0
        self.new_input = True
        
        # Create custom fonts
        self.display_font = font.Font(family="Helvetica", size=32, weight="normal")
        self.expression_font = font.Font(family="Helvetica", size=16, weight="normal")
        self.button_font = font.Font(family="Helvetica", size=20, weight="normal")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Display frame
        display_frame = tk.Frame(self.root, bg='#000000')
        display_frame.pack(pady=(30, 20), padx=20, fill='x')
        
        # Expression display (shows the full calculation)
        expression_label = tk.Label(
            display_frame, 
            textvariable=self.expression_var, 
            font=self.expression_font,
            bg='#000000', 
            fg='#8E8E93',
            anchor='e'
        )
        expression_label.pack(fill='x')
        
        # Result display
        result_label = tk.Label(
            display_frame, 
            textvariable=self.result_var, 
            font=self.display_font,
            bg='#000000', 
            fg='#FFFFFF',
            anchor='e'
        )
        result_label.pack(fill='x')
        
        # Buttons frame
        buttons_frame = tk.Frame(self.root, bg='#000000')
        buttons_frame.pack(pady=10, padx=10)
        
        # Button layout - note the empty space after 0
        buttons = [
            ['C', '±', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '−'],
            ['1', '2', '3', '+'],
            ['0', '', '.', '=']  # Empty space after 0
        ]
        
        # Button colors
        button_colors = {
            'number': {'bg': '#333333', 'fg': '#FFFFFF', 'active': '#505050'},
            'operator': {'bg': '#FF9500', 'fg': '#FFFFFF', 'active': '#FFB143'},
            'function': {'bg': '#A5A5A5', 'fg': '#000000', 'active': '#C0C0C0'}
        }
        
        # Create buttons
        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                if text == '':
                    # Create empty space
                    empty = tk.Frame(buttons_frame, width=70, height=70, bg='#000000')
                    empty.grid(row=i, column=j, padx=3, pady=3)
                    empty.grid_propagate(False)
                    continue
                    
                # Determine button type and colors
                if text in ['÷', '×', '−', '+', '=']:
                    colors = button_colors['operator']
                elif text in ['C', '±', '%']:
                    colors = button_colors['function']
                else:
                    colors = button_colors['number']
                
                # Create circular button
                btn = CircularButton(
                    buttons_frame, 
                    text=text,
                    font=self.button_font,
                    bg=colors['bg'],
                    fg=colors['fg'],
                    active_bg=colors['active'],
                    command=lambda t=text: self.button_click(t),
                    diameter=70
                )
                btn.grid(row=i, column=j, padx=3, pady=3)
        
        # Configure grid weights for equal spacing
        for i in range(5):
            buttons_frame.grid_rowconfigure(i, weight=1, minsize=70)
        for j in range(4):
            buttons_frame.grid_columnconfigure(j, weight=1, minsize=70)
    
    def button_click(self, value):
        if value.isdigit() or value == '.':
            self.input_number(value)
        elif value in ['÷', '×', '−', '+']:
            self.input_operator(value)
        elif value == '=':
            self.calculate()
        elif value == 'C':
            self.clear()
        elif value == '±':
            self.negate()
        elif value == '%':
            self.percentage()
    
    def input_number(self, num):
        if self.new_input:
            self.current_input = num
            self.new_input = False
        else:
            # Prevent multiple decimal points
            if num == '.' and '.' in self.current_input:
                return
            self.current_input += num
        
        self.result_var.set(self.current_input)
        
        # Update expression display
        if self.operator:
            self.expression_var.set(f"{self.previous_value} {self.operator} {self.current_input}")
        else:
            self.expression_var.set("")
    
    def input_operator(self, op):
        if self.current_input:
            if self.operator and not self.new_input:
                self.calculate()
            
            self.previous_value = float(self.current_input)
            self.operator = op
            self.new_input = True
            
            # Update expression display
            self.expression_var.set(f"{self.previous_value} {self.operator}")
    
    def calculate(self):
        if self.operator and self.current_input:
            current_value = float(self.current_input)
            
            try:
                if self.operator == '+':
                    result = self.previous_value + current_value
                elif self.operator == '−':
                    result = self.previous_value - current_value
                elif self.operator == '×':
                    result = self.previous_value * current_value
                elif self.operator == '÷':
                    if current_value == 0:
                        self.result_var.set("Error")
                        self.current_input = ""
                        self.operator = None
                        self.new_input = True
                        self.expression_var.set("")
                        return
                    result = self.previous_value / current_value
                
                # Format result to avoid unnecessary decimal places
                if result.is_integer():
                    display_result = str(int(result))
                    self.result_var.set(display_result)
                else:
                    display_result = str(result)
                    self.result_var.set(display_result)
                
                # Update expression to show the full calculation
                self.expression_var.set(f"{self.previous_value} {self.operator} {self.current_input} = {display_result}")
                
                self.current_input = display_result
                self.operator = None
                self.new_input = True
                
            except Exception:
                self.result_var.set("Error")
                self.current_input = ""
                self.operator = None
                self.new_input = True
                self.expression_var.set("")
    
    def clear(self):
        self.current_input = ""
        self.result_var.set("0")
        self.operator = None
        self.previous_value = 0
        self.new_input = True
        self.expression_var.set("")
    
    def negate(self):
        if self.current_input:
            value = float(self.current_input)
            value = -value
            self.current_input = str(value)
            self.result_var.set(self.current_input)
            
            # Update expression display
            if self.operator:
                self.expression_var.set(f"{self.previous_value} {self.operator} {self.current_input}")
    
    def percentage(self):
        if self.current_input:
            value = float(self.current_input)
            value = value / 100
            self.current_input = str(value)
            self.result_var.set(self.current_input)
            
            # Update expression display
            if self.operator:
                self.expression_var.set(f"{self.previous_value} {self.operator} {self.current_input}")


class CircularButton(tk.Canvas):
    def __init__(self, parent, text, font, bg, fg, active_bg, command, diameter=70, **kwargs):
        self.diameter = diameter
        super().__init__(
            parent, 
            width=diameter, 
            height=diameter, 
            highlightthickness=0, 
            borderwidth=0,
            bg='#000000'
        )
        
        self.text = text
        self.font = font
        self.bg = bg
        self.fg = fg
        self.active_bg = active_bg
        self.command = command
        self.is_pressed = False
        
        # Create the circle and text
        self.circle_id = self.create_oval(
            2, 2, 
            diameter-2, diameter-2, 
            fill=bg, 
            outline=bg,
            width=0
        )
        
        self.text_id = self.create_text(
            diameter/2, 
            diameter/2, 
            text=text, 
            font=font, 
            fill=fg
        )
        
        # Bind events
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
    def on_press(self, event):
        self.is_pressed = True
        self.itemconfig(self.circle_id, fill=self.active_bg, outline=self.active_bg)
        
    def on_release(self, event):
        self.is_pressed = False
        self.itemconfig(self.circle_id, fill=self.bg, outline=self.bg)
        self.command()
        
    def on_enter(self, event):
        if not self.is_pressed:
            # Slight highlight on hover
            pass
            
    def on_leave(self, event):
        if not self.is_pressed:
            self.itemconfig(self.circle_id, fill=self.bg, outline=self.bg)


if __name__ == "__main__":
    root = tk.Tk()
    calculator = AppolCalculator(root)
    root.mainloop()
