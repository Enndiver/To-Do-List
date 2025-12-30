import tkinter as tk
from tkinter import messagebox

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        self.tasks = []
        
        # Configure colors
        self.bg_color = "#f0f0f0"
        self.primary_color = "#4CAF50"
        self.danger_color = "#f44336"
        
        self.root.configure(bg=self.bg_color)
        
        self.create_widgets()
    
    def create_widgets(self):
        # Title
        title = tk.Label(
            self.root, 
            text="📝 My To-Do List", 
            font=("Arial", 24, "bold"),
            bg=self.bg_color,
            fg="#333"
        )
        title.pack(pady=20)
        
        # Input frame
        input_frame = tk.Frame(self.root, bg=self.bg_color)
        input_frame.pack(pady=10, padx=20, fill=tk.X)
        
        self.task_entry = tk.Entry(
            input_frame,
            font=("Arial", 12),
            width=30,
            relief=tk.FLAT,
            bd=2
        )
        self.task_entry.pack(side=tk.LEFT, padx=(0, 10), ipady=8)
        self.task_entry.bind('<Return>', lambda e: self.add_task())
        
        add_btn = tk.Button(
            input_frame,
            text="Add Task",
            font=("Arial", 12, "bold"),
            bg=self.primary_color,
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.add_task,
            padx=20,
            pady=8
        )
        add_btn.pack(side=tk.LEFT)
        
        # Task list frame
        list_frame = tk.Frame(self.root, bg=self.bg_color)
        list_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Listbox
        self.task_listbox = tk.Listbox(
            list_frame,
            font=("Arial", 11),
            selectmode=tk.SINGLE,
            bg="white",
            fg="#333",
            selectbackground="#4CAF50",
            selectforeground="white",
            yscrollcommand=scrollbar.set,
            relief=tk.FLAT,
            bd=2,
            highlightthickness=1,
            highlightbackground="#ddd"
        )
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.task_listbox.yview)
        
        # Buttons frame
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(pady=10, padx=20)
        
        delete_btn = tk.Button(
            button_frame,
            text="Delete Selected",
            font=("Arial", 11),
            bg=self.danger_color,
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.delete_task,
            padx=15,
            pady=8
        )
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(
            button_frame,
            text="Clear All",
            font=("Arial", 11),
            bg="#FF9800",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.clear_all,
            padx=15,
            pady=8
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Task counter
        self.counter_label = tk.Label(
            self.root,
            text="Total tasks: 0",
            font=("Arial", 10),
            bg=self.bg_color,
            fg="#666"
        )
        self.counter_label.pack(pady=5)
    
    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            self.tasks.append(task)
            self.task_listbox.insert(tk.END, f"  {task}")
            self.task_entry.delete(0, tk.END)
            self.update_counter()
        else:
            messagebox.showwarning("Warning", "Please enter a task!")
    
    def delete_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            task = self.tasks[selected_index]
            
            confirm = messagebox.askyesno(
                "Confirm Delete", 
                f"Delete task: '{task}'?"
            )
            
            if confirm:
                self.tasks.pop(selected_index)
                self.task_listbox.delete(selected_index)
                self.update_counter()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to delete!")
    
    def clear_all(self):
        if self.tasks:
            confirm = messagebox.askyesno(
                "Confirm Clear All", 
                "Are you sure you want to delete all tasks?"
            )
            
            if confirm:
                self.tasks.clear()
                self.task_listbox.delete(0, tk.END)
                self.update_counter()
        else:
            messagebox.showinfo("Info", "No tasks to clear!")
    
    def update_counter(self):
        count = len(self.tasks)
        self.counter_label.config(text=f"Total tasks: {count}")


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()