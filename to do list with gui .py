import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog

DATABASE = "Task.json"
tasks = []


def load_data():
    global tasks
    if os.path.exists(DATABASE):
        with open(DATABASE, "r") as f:
            raw = json.load(f)
        # Support old format (list of strings) and new format (list of dicts)
        tasks = [
            t if isinstance(t, dict) else {"text": t, "done": False}
            for t in raw
        ]


def save_data():
    with open(DATABASE, "w") as f:
        json.dump(tasks, f, indent=4)
    messagebox.showinfo("Saved", "Tasks saved successfully!")


def refresh_list():
    listbox.delete(0, tk.END)
    for i, task in enumerate(tasks):
        status = "✓" if task.get("done") else "○"
        listbox.insert(tk.END, f"  {status}  {task['text']}")
        if task.get("done"):
            listbox.itemconfig(i, fg="#999999")
    update_count()


def add_task():
    text = entry.get().strip()
    if not text:
        return
    tasks.append({"text": text, "done": False})
    entry.delete(0, tk.END)
    refresh_list()


def toggle_done():
    sel = listbox.curselection()
    if not sel:
        messagebox.showwarning("No selection", "Select a task first.")
        return
    idx = sel[0]
    tasks[idx]["done"] = not tasks[idx]["done"]
    refresh_list()
    listbox.selection_set(idx)


def delete_task():
    sel = listbox.curselection()
    if not sel:
        messagebox.showwarning("No selection", "Select a task to delete.")
        return
    idx = sel[0]
    confirm = messagebox.askyesno("Delete", f"Delete \"{tasks[idx]['text']}\"?")
    if confirm:
        tasks.pop(idx)
        refresh_list()


def edit_task():
    sel = listbox.curselection()
    if not sel:
        messagebox.showwarning("No selection", "Select a task to edit.")
        return
    idx = sel[0]
    new_text = simpledialog.askstring("Edit Task", "Update task:", initialvalue=tasks[idx]["text"])
    if new_text and new_text.strip():
        tasks[idx]["text"] = new_text.strip()
        refresh_list()
        listbox.selection_set(idx)


def clear_done():
    global tasks
    before = len(tasks)
    tasks = [t for t in tasks if not t.get("done")]
    after = len(tasks)
    refresh_list()
    messagebox.showinfo("Cleared", f"Removed {before - after} completed task(s).")


def update_count():
    done = sum(1 for t in tasks if t.get("done"))
    total = len(tasks)
    count_label.config(text=f"{done} of {total} done")


def on_enter(event):
    add_task()


# --- Main window ---
root = tk.Tk()
root.title("To-Do List")
root.geometry("480x540")
root.resizable(False, False)
root.configure(bg="#f7f7f5")

FONT = ("Segoe UI", 11)
FONT_BOLD = ("Segoe UI", 11, "bold")
BG = "#f7f7f5"
CARD = "#ffffff"
ACCENT = "#2563eb"
DANGER = "#dc2626"
MUTED = "#888888"
BORDER = "#e0e0e0"

# --- Title ---
tk.Label(root, text="To-Do List", font=("Segoe UI", 16, "bold"),
         bg=BG, fg="#1a1a1a").pack(pady=(18, 2))
count_label = tk.Label(root, text="0 of 0 done", font=("Segoe UI", 10),
                       bg=BG, fg=MUTED)
count_label.pack()

# --- Entry row ---
entry_frame = tk.Frame(root, bg=BG)
entry_frame.pack(padx=20, pady=12, fill="x")

entry = tk.Entry(entry_frame, font=FONT, relief="solid", bd=1,
                 highlightthickness=1, highlightcolor=ACCENT,
                 highlightbackground=BORDER)
entry.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 8))
entry.bind("<Return>", on_enter)
entry.focus()

add_btn = tk.Button(entry_frame, text="+ Add", font=FONT_BOLD,
                    bg=ACCENT, fg="white", relief="flat",
                    padx=14, pady=6, cursor="hand2",
                    activebackground="#1d4ed8", activeforeground="white",
                    command=add_task)
add_btn.pack(side="left")

# --- Task listbox ---
list_frame = tk.Frame(root, bg=CARD, relief="solid", bd=1,
                      highlightthickness=1, highlightbackground=BORDER)
list_frame.pack(padx=20, fill="both", expand=True)

scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")

listbox = tk.Listbox(list_frame, font=FONT, selectmode="single",
                     activestyle="none", relief="flat", bd=0,
                     yscrollcommand=scrollbar.set,
                     selectbackground="#dbeafe", selectforeground="#1e40af",
                     bg=CARD, fg="#1a1a1a", cursor="hand2")
listbox.pack(fill="both", expand=True, padx=4, pady=4)
scrollbar.config(command=listbox.yview)

# --- Action buttons ---
btn_frame = tk.Frame(root, bg=BG)
btn_frame.pack(padx=20, pady=10, fill="x")

def make_btn(parent, text, color, command):
    return tk.Button(parent, text=text, font=("Segoe UI", 10),
                     bg=color, fg="white", relief="flat",
                     padx=10, pady=5, cursor="hand2",
                     activebackground=color, activeforeground="white",
                     command=command)

make_btn(btn_frame, "✓  Done", "#16a34a", toggle_done).pack(side="left", padx=(0, 6))
make_btn(btn_frame, "✎  Edit", "#d97706", edit_task).pack(side="left", padx=(0, 6))
make_btn(btn_frame, "✕  Delete", DANGER, delete_task).pack(side="left", padx=(0, 6))
make_btn(btn_frame, "Clear done", MUTED, clear_done).pack(side="left")

# --- Save button ---
save_frame = tk.Frame(root, bg=BG)
save_frame.pack(padx=20, pady=(0, 16), fill="x")

tk.Button(save_frame, text="💾  Save", font=FONT_BOLD,
          bg="#1a1a1a", fg="white", relief="flat",
          padx=16, pady=7, cursor="hand2",
          activebackground="#333333", activeforeground="white",
          command=save_data).pack(side="right")

# --- Boot ---
load_data()
refresh_list()
root.mainloop()