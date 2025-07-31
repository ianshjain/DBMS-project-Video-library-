import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os

# MySQL Connection
def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="video_library"
    )

# Create Table if not exists
def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            genre VARCHAR(255) NOT NULL,
            year INT,
            director VARCHAR(255),
            file_path TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Add Video
def add_video():
    title = entry_title.get()
    genre = entry_genre.get()
    year = entry_year.get()
    director = entry_director.get()
    file_path = entry_file_path.get()

    if not title or not genre:
        messagebox.showwarning("Input Error", "Title and Genre are required.")
        return

    try:
        year = int(year)
    except ValueError:
        messagebox.showwarning("Input Error", "Year must be a number.")
        return

    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO videos (title, genre, year, director, file_path)
        VALUES (%s, %s, %s, %s, %s)
    ''', (title, genre, year, director, file_path))
    conn.commit()
    conn.close()
    load_videos()
    clear_fields()

# Load Videos into Table
def load_videos():
    for row in video_table.get_children():
        video_table.delete(row)

    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM videos')
    for row in cursor.fetchall():
        video_table.insert('', tk.END, values=row)
    conn.close()

# Delete selected video
def delete_video():
    selected = video_table.selection()
    if not selected:
        messagebox.showwarning("Selection Error", "No video selected.")
        return

    video_id = video_table.item(selected[0])['values'][0]
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM videos WHERE id = %s', (video_id,))
    conn.commit()
    conn.close()
    load_videos()
    clear_fields()

# Update selected video
def update_video():
    selected = video_table.selection()
    if not selected:
        messagebox.showwarning("Selection Error", "No video selected.")
        return

    video_id = video_table.item(selected[0])['values'][0]
    title = entry_title.get()
    genre = entry_genre.get()
    year = entry_year.get()
    director = entry_director.get()
    file_path = entry_file_path.get()

    if not title or not genre:
        messagebox.showwarning("Input Error", "Title and Genre are required.")
        return

    try:
        year = int(year)
    except ValueError:
        messagebox.showwarning("Input Error", "Year must be a number.")
        return

    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE videos SET title = %s, genre = %s, year = %s, director = %s, file_path = %s
        WHERE id = %s
    ''', (title, genre, year, director, file_path, video_id))
    conn.commit()
    conn.close()
    load_videos()
    clear_fields()

# Play selected video
def play_video():
    selected = video_table.selection()
    if not selected:
        messagebox.showwarning("Selection Error", "No video selected.")
        return

    file_path = video_table.item(selected[0])['values'][5]
    if not file_path or not os.path.exists(file_path):
        messagebox.showerror("File Error", "Video file not found.")
        return

    os.startfile(file_path)

# Populate fields when row is selected
def on_row_selected(event):
    selected = video_table.selection()
    if selected:
        row = video_table.item(selected[0])['values']
        entry_title.delete(0, tk.END)
        entry_genre.delete(0, tk.END)
        entry_year.delete(0, tk.END)
        entry_director.delete(0, tk.END)
        entry_file_path.delete(0, tk.END)

        entry_title.insert(0, row[1])
        entry_genre.insert(0, row[2])
        entry_year.insert(0, row[3])
        entry_director.insert(0, row[4])
        entry_file_path.insert(0, row[5])

# Clear input fields
def clear_fields():
    entry_title.delete(0, tk.END)
    entry_genre.delete(0, tk.END)
    entry_year.delete(0, tk.END)
    entry_director.delete(0, tk.END)
    entry_file_path.delete(0, tk.END)

# Browse for video file
def browse_file():
    file_path = filedialog.askopenfilename(
        title="Select Video File",
        filetypes=[("Video files", "*.mp4 *.avi *.mkv *.mov *.wmv")]
    )
    entry_file_path.delete(0, tk.END)
    entry_file_path.insert(0, file_path)

# GUI Window
root = tk.Tk()
root.title("Video Library Management System")
root.geometry("950x550")

# Input Frame
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Title").grid(row=0, column=0)
entry_title = tk.Entry(frame)
entry_title.grid(row=0, column=1)

tk.Label(frame, text="Genre").grid(row=0, column=2)
entry_genre = tk.Entry(frame)
entry_genre.grid(row=0, column=3)

tk.Label(frame, text="Year").grid(row=1, column=0)
entry_year = tk.Entry(frame)
entry_year.grid(row=1, column=1)

tk.Label(frame, text="Director").grid(row=1, column=2)
entry_director = tk.Entry(frame)
entry_director.grid(row=1, column=3)

tk.Label(frame, text="Video File").grid(row=2, column=0)
entry_file_path = tk.Entry(frame, width=50)
entry_file_path.grid(row=2, column=1, columnspan=2)
tk.Button(frame, text="Browse", command=browse_file).grid(row=2, column=3)

# Button Frame
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add Video", command=add_video).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Update Video", command=update_video).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Delete Video", command=delete_video).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Clear Fields", command=clear_fields).grid(row=0, column=3, padx=5)
tk.Button(btn_frame, text="Play Video", command=play_video).grid(row=0, column=4, padx=5)

# Table Frame
table_frame = tk.Frame(root)
table_frame.pack(fill=tk.BOTH, expand=True)

columns = ("ID", "Title", "Genre", "Year", "Director", "File")
video_table = ttk.Treeview(table_frame, columns=columns, show="headings")

for col in columns:
    video_table.heading(col, text=col)
    video_table.column(col, anchor=tk.CENTER)

video_table.pack(fill=tk.BOTH, expand=True)
video_table.bind("<<TreeviewSelect>>", on_row_selected)

# Initialize App
create_table()
load_videos()
root.mainloop()