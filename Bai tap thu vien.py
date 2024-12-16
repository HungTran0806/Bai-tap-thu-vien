import tkinter as tk
from tkinter import messagebox
import pandas as pd
from datetime import datetime
import csv

CSV_FILE = "employee_data.csv"
root = tk.Tk(); root.title("Nhân Viên"); root.geometry("400x300")
fields = ["Mã", "Tên", "Đơn vị", "Chức danh", "Ngày sinh", "Số CMND"]
entries = {}

def save():
    data = {f: entries[f].get() for f in fields}
    if "" in data.values(): return messagebox.showwarning("Lỗi", "Nhập đầy ")
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fields); w.writeheader() if f.tell() == 0 else None; w.writerow(data)
    messagebox.showinfo("OK", "Lưu thành công"); [e.delete(0, tk.END) for e in entries.values()]

def show_today():
    try:
        df = pd.read_csv(CSV_FILE)
        today = datetime.now().strftime("%d/%m")
        df = df[pd.to_datetime(df["Ngày sinh"], errors='coerce').dt.strftime("%d/%m") == today]
        messagebox.showinfo("Sinh nhật", df.to_string(index=False) if not df.empty else "Không có ai")
    except: messagebox.showerror("Lỗi", "File trống")

def export_excel():
    try:
        pd.read_csv(CSV_FILE).to_excel("employee_list.xlsx", index=False)
        messagebox.showinfo("OK", "Xuất file Excel")
    except: messagebox.showerror("Lỗi", "Không thể xuất")

for i, f in enumerate(fields):
    tk.Label(root, text=f).grid(row=i, column=0)
    entries[f] = tk.Entry(root); entries[f].grid(row=i, column=1)

tk.Button(root, text="Lưu", command=save).grid(row=len(fields), column=0)
tk.Button(root, text="Sinh nhật", command=show_today).grid(row=len(fields), column=1)
tk.Button(root, text="Xuất Excel", command=export_excel).grid(row=len(fields)+1, column=0)

root.mainloop()
