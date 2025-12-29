import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from tkcalendar import DateEntry

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("✓ Task Manager")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f5f5")
        
        self.tasks = []
        self.create_widgets()
        self.update_date()
    
    def create_widgets(self):
        # Header with gradient effect (simulated with frames)
        header_frame = tk.Frame(self.root, bg="#6200ea", height=140)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Date display
        self.date_label = tk.Label(
            header_frame, 
            text="", 
            font=("Arial", 11),
            bg="#6200ea",
            fg="#ffffff"
        )
        self.date_label.pack(pady=(20, 5))
        
        # Title
        title = tk.Label(
            header_frame, 
            text="✓ My Tasks", 
            font=("Arial", 28, "bold"),
            bg="#6200ea",
            fg="#ffffff"
        )
        title.pack()
        
        # Task counter in header
        self.counter_label = tk.Label(
            header_frame,
            text="0 tasks today",
            font=("Arial", 10),
            bg="#6200ea",
            fg="#e1bee7"
        )
        self.counter_label.pack(pady=(5, 0))
        
        # Main container with shadow effect
        main_container = tk.Frame(self.root, bg="#f5f5f5")
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=20)
        
        # Input card
        input_card = tk.Frame(main_container, bg="white", relief=tk.RAISED, bd=0)
        input_card.pack(fill=tk.X, pady=(0, 20))
        
        # Add subtle shadow effect
        shadow = tk.Frame(main_container, bg="#e0e0e0", height=2)
        shadow.place(in_=input_card, relx=0, rely=1, relwidth=1)
        
        input_inner = tk.Frame(input_card, bg="white")
        input_inner.pack(padx=20, pady=20)
        
        # Task entry with icon
        task_frame = tk.Frame(input_inner, bg="white")
        task_frame.pack(fill=tk.X, pady=(0, 12))
        
        task_icon = tk.Label(task_frame, text="📝", font=("Arial", 14), bg="white")
        task_icon.pack(side=tk.LEFT, padx=(0, 8))
        
        self.task_entry = tk.Entry(
            task_frame,
            font=("Arial", 13),
            relief=tk.FLAT,
            bg="#f9f9f9",
            fg="#333",
            insertbackground="#6200ea"
        )
        self.task_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=10, padx=2)
        self.task_entry.bind('<Return>', lambda e: self.add_task())
        self.task_entry.bind('<FocusIn>', lambda e: self.task_entry.config(bg="#ffffff"))
        self.task_entry.bind('<FocusOut>', lambda e: self.task_entry.config(bg="#f9f9f9"))
        self.task_entry.insert(0, "Add a new task...")
        self.task_entry.bind('<FocusIn>', self.clear_placeholder)
        self.task_entry.config(fg="#999")
        
        # Due date with icon
        date_frame = tk.Frame(input_inner, bg="white")
        date_frame.pack(fill=tk.X)
        
        date_icon = tk.Label(date_frame, text="📅", font=("Arial", 14), bg="white")
        date_icon.pack(side=tk.LEFT, padx=(0, 8))
        
        self.date_entry = DateEntry(
            date_frame,
            font=("Arial", 11),
            width=18,
            background='#6200ea',
            foreground='white',
            borderwidth=0,
            date_pattern='mm/dd/yyyy',
            relief=tk.FLAT
        )
        self.date_entry.pack(side=tk.LEFT, ipady=8)
        
        # Add button with hover effect
        self.add_btn = tk.Button(
            date_frame,
            text="+ Add Task",
            font=("Arial", 11, "bold"),
            bg="#6200ea",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.add_task,
            padx=25,
            pady=10,
            activebackground="#7c4dff",
            activeforeground="white"
        )
        self.add_btn.pack(side=tk.RIGHT)
        self.add_btn.bind('<Enter>', lambda e: self.add_btn.config(bg="#7c4dff"))
        self.add_btn.bind('<Leave>', lambda e: self.add_btn.config(bg="#6200ea"))
        
        # Tasks container
        tasks_label = tk.Label(
            main_container,
            text="Tasks",
            font=("Arial", 12, "bold"),
            bg="#f5f5f5",
            fg="#333",
            anchor="w"
        )
        tasks_label.pack(fill=tk.X, pady=(0, 10))
        
        # Scrollable frame for tasks
        canvas_frame = tk.Frame(main_container, bg="#f5f5f5")
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, bg="#f5f5f5", highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview, 
                                bg="#f5f5f5", troughcolor="#f5f5f5", width=12)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f5f5f5")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bottom button
        bottom_frame = tk.Frame(self.root, bg="#f5f5f5")
        bottom_frame.pack(pady=(0, 15))
        
        self.clear_btn = tk.Button(
            bottom_frame,
            text="🗑️ Clear All Tasks",
            font=("Arial", 10),
            bg="white",
            fg="#666",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.clear_all,
            padx=20,
            pady=8,
            activebackground="#ffebee",
            activeforeground="#d32f2f"
        )
        self.clear_btn.pack()
        self.clear_btn.bind('<Enter>', lambda e: self.clear_btn.config(bg="#ffebee", fg="#d32f2f"))
        self.clear_btn.bind('<Leave>', lambda e: self.clear_btn.config(bg="white", fg="#666"))
    
    def clear_placeholder(self, event):
        if self.task_entry.get() == "Add a new task...":
            self.task_entry.delete(0, tk.END)
            self.task_entry.config(fg="#333")
    
    def update_date(self):
        now = datetime.now()
        date_str = now.strftime("%A, %B %d, %Y")
        self.date_label.config(text=date_str)
    
    def create_task_item(self, task, index):
        # Task card with rounded corners effect
        task_card = tk.Frame(
            self.scrollable_frame,
            bg="white",
            relief=tk.FLAT,
            bd=0
        )
        task_card.pack(fill=tk.X, pady=6, padx=5)
        
        # Inner frame for padding
        inner_frame = tk.Frame(task_card, bg="white")
        inner_frame.pack(fill=tk.BOTH, padx=15, pady=12)
        
        # Checkbox variable
        var = tk.BooleanVar(value=task["completed"])
        
        # Custom checkbox
        check = tk.Checkbutton(
            inner_frame,
            variable=var,
            bg="white",
            activebackground="white",
            command=lambda: self.toggle_task(index, var, task_label, due_label),
            font=("Arial", 12)
        )
        check.pack(side=tk.LEFT, padx=(0, 10))
        
        # Task info frame
        info_frame = tk.Frame(inner_frame, bg="white")
        info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Task text
        font_style = ("Arial", 12, "overstrike") if task["completed"] else ("Arial", 12)
        text_color = "#999" if task["completed"] else "#333"
        
        task_label = tk.Label(
            info_frame,
            text=task['text'],
            font=font_style,
            bg="white",
            fg=text_color,
            anchor="w"
        )
        task_label.pack(anchor="w")
        
        # Due date with color coding
        due_date = datetime.strptime(task['due_date'], "%m/%d/%Y")
        today = datetime.now().date()
        days_until = (due_date.date() - today).days
        
        if task["completed"]:
            due_color = "#999"
            due_text = f"✓ Completed • Due: {task['due_date']}"
        elif days_until < 0:
            due_color = "#d32f2f"
            due_text = f"⚠️ Overdue by {abs(days_until)} days • {task['due_date']}"
        elif days_until == 0:
            due_color = "#f57c00"
            due_text = f"🔔 Due Today • {task['due_date']}"
        elif days_until <= 2:
            due_color = "#f57c00"
            due_text = f"⏰ Due in {days_until} days • {task['due_date']}"
        else:
            due_color = "#666"
            due_text = f"📅 Due: {task['due_date']}"
        
        due_label = tk.Label(
            info_frame,
            text=due_text,
            font=("Arial", 9),
            bg="white",
            fg=due_color,
            anchor="w"
        )
        due_label.pack(anchor="w", pady=(3, 0))
        
        # Delete button with hover
        delete_btn = tk.Button(
            inner_frame,
            text="×",
            font=("Arial", 18),
            bg="white",
            fg="#ccc",
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            command=lambda: self.delete_task(index),
            padx=10,
            activebackground="white",
            activeforeground="#d32f2f"
        )
        delete_btn.pack(side=tk.RIGHT)
        delete_btn.bind('<Enter>', lambda e: delete_btn.config(fg="#d32f2f"))
        delete_btn.bind('<Leave>', lambda e: delete_btn.config(fg="#ccc"))
        
        return {"frame": task_card, "var": var, "label": task_label, "due_label": due_label}
    
    def add_task(self):
        task_text = self.task_entry.get().strip()
        
        if task_text == "Add a new task..." or not task_text:
            messagebox.showwarning("Warning", "Please enter a task")
            return
            
        due_date = self.date_entry.get_date().strftime("%m/%d/%Y")
        
        task = {
            "text": task_text,
            "due_date": due_date,
            "completed": False,
            "created": datetime.now().strftime("%m/%d/%Y %I:%M %p")
        }
        self.tasks.append(task)
        self.task_entry.delete(0, tk.END)
        self.task_entry.insert(0, "Add a new task...")
        self.task_entry.config(fg="#999")
        self.refresh_tasks()
        self.update_counter()
    
    def toggle_task(self, index, var, task_label, due_label):
        if index < len(self.tasks):
            self.tasks[index]["completed"] = var.get()
            if var.get():
                task_label.config(fg="#999", font=("Arial", 12, "overstrike"))
                due_label.config(text=f"✓ Completed • Due: {self.tasks[index]['due_date']}", fg="#999")
            else:
                self.refresh_tasks()
    
    def delete_task(self, index):
        if index < len(self.tasks):
            self.tasks.pop(index)
            self.refresh_tasks()
            self.update_counter()
    
    def clear_all(self):
        if self.tasks:
            confirm = messagebox.askyesno("Confirm", "Delete all tasks?")
            if confirm:
                self.tasks.clear()
                self.refresh_tasks()
                self.update_counter()
        else:
            messagebox.showinfo("Info", "No tasks to clear")
    
    def refresh_tasks(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        for i, task in enumerate(self.tasks):
            self.create_task_item(task, i)
    
    def update_counter(self):
        count = len(self.tasks)
        completed = sum(1 for task in self.tasks if task["completed"])
        
        if count == 0:
            text = "No tasks yet"
        elif count == 1:
            text = "1 task"
        else:
            text = f"{count} tasks"
        
        if completed > 0:
            text += f" • {completed} completed ✓"
        else:
            text += " today"
        
        self.counter_label.config(text=text)


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()