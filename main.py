import mysql.connector
from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as Messagebox

# CORE OF THE PROGRAM
window = Tk()
window.title("PHARMAPY")
window.minsize(width=700, height=600)
window.config(padx=20, pady=20)

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    passwd="kelompok11",
    database="pharmacydb"
)

mycursor = mydb.cursor()
"""mycursor.execute("CREATE TABLE medicine(id INT PRIMARY KEY AUTO_INCREMENT, obat VARCHAR(255), kelas VARCHAR(255), penyakit VARCHAR(255), aturan_pakai VARCHAR(255))")
mydb.commit()"""



def switch(indicator_label, page):
    for child in options_fm.winfo_children():
        if isinstance(child, tk.Label):
            child["bg"] = "SystemButtonFace"

    indicator_label["bg"] = "#0097e8"

    for fm in main_fm.winfo_children():
        fm.destroy()
        window.update()

    page()


options_fm = tk.Frame(window)

options_fm.pack(pady=5)

options_fm.propagate(False)
options_fm.configure(width=700, height=30)

main_fm = tk.Frame(window)
main_fm.pack(fill=tk.BOTH, expand=True)


def home_page():
    home_page_fm = tk.Frame(main_fm)
    home_page_label = tk.Label(home_page_fm, text="Home Page", font=("Arial", 25), fg="#0097e8")
    home_page_label.pack(pady=80)
    home_page_fm.pack(fill=tk.BOTH, expand=True)

    nama_program_label = Label(home_page_fm, text="PROGRAM FARMASI", font=("Arial", 20), fg="#0097e8")
    nama_program_label.pack(pady=20)

    nama_kelompok_label = Label(home_page_fm, text="KELOMPOK 11", font=("Arial", 20), fg="#0097e8")
    nama_kelompok_label.pack(pady=40)

def stok_page():
    stok_page_fm = tk.Frame(main_fm)
    stok_page_label = tk.Label(stok_page_fm, text="Stok Page", font=("Arial", 25), fg="#0097e8")
    stok_page_label.pack(pady=80)
    stok_page_fm.pack(fill=tk.BOTH, expand=True)

    mycursor.execute("SELECT * FROM medicine ORDER BY id")
    tree = ttk.Treeview(main_fm)
    tree["show"] = "headings"

    tree["columns"] = ("id", "obat", "kelas", "penyakit", "aturan_pakai")

    tree.column("id", width=50, minwidth=50, anchor=tk.CENTER)
    tree.column("obat", width=100, minwidth=100, anchor=tk.CENTER)
    tree.column("kelas", width=50, minwidth=50, anchor=tk.CENTER)
    tree.column("penyakit", width=100, minwidth=100, anchor=tk.CENTER)
    tree.column("aturan_pakai", width=200, minwidth=200, anchor=tk.CENTER)

    tree.heading("id", text="id", anchor=tk.CENTER)
    tree.heading("obat", text="obat", anchor=tk.CENTER)
    tree.heading("kelas", text="kelas", anchor=tk.CENTER)
    tree.heading("penyakit", text="penyakit", anchor=tk.CENTER)
    tree.heading("aturan_pakai", text="aturan_pakai", anchor=tk.CENTER)


    s = ttk.Style(main_fm)
    s.theme_use("clam")
    s.configure(".", font=("Arial", 10))
    s.configure("Treeview.Headings", fg="blue", font=("Helvetica", 11, "bold"))

    i = 0
    for ro in mycursor:
        tree.insert("", i, text="", values=(ro[0], ro[1], ro[2], ro[3], ro[4]))
        i += 1

    #scroll = ttk.Scrollbar(main_fm, orient="vertical")

    #scroll.configure(command=tree.yview)
    #tree.configure(yscrollcommand=scroll.set)
    #scroll.pack(fill=Y, side=RIGHT)

    tree.pack(side=TOP, anchor=N)

    def store():
        obat = med_entry.get()
        kelas = class_entry.get()
        penyakit = disease_entry.get()
        aturan_pakai = rules_entry.get()
        if len(obat) < 4 and obat == "":
            Messagebox.showwarning(title="Insert Status", message="Enter A Medicine Name")
        elif kelas == "":
            Messagebox.showwarning(title="Insert Status", message="Enter A Valid Class")
        else:
            med_entry.delete(0, END)
            class_entry.delete(0, END)
            disease_entry.delete(0, END)
            rules_entry.delete(0, END)
            Messagebox.showinfo(title="Insert Status", message="Successfully Added")
            sqlFormula = "INSERT INTO medicine (obat, kelas, penyakit, aturan_pakai) VALUES (%s, %s, %s, %s)"
            vals = (obat, kelas, penyakit, aturan_pakai)
            mycursor.execute(sqlFormula, vals)
            mydb.commit()

    def delete(tree):
        selected_item = tree.selection()[0]
        data_id = tree.item(selected_item)["values"][0]
        sqlFormula = "DELETE FROM medicine WHERE id=%s"
        vals = (data_id,)
        mycursor.execute(sqlFormula, vals)
        mydb.commit()
        tree.delete(selected_item)
        Messagebox.showinfo(title="Delete Status", message="Successfully Deleted")

    current_item = tree.focus()
    values = tree.item(current_item, "values")


    def refresh():
        mycursor.execute("TRUNCATE TABLE medicine")
        mydb.commit()


    def click(event):
        med_entry.config(state=NORMAL)
        med_entry.delete(0, END)

    def click_2(event):
        class_entry.config(state=NORMAL)
        class_entry.delete(0, END)

    def click_3(event):
        disease_entry.config(state=NORMAL)
        disease_entry.delete(0, END)

    def click_4(event):
        rules_entry.config(state=NORMAL)
        rules_entry.delete(0, END)

    med_entry = Entry(stok_page_fm, width=30, font=("Arial", 15))
    med_entry.insert(0, "Masukkan Nama Obat...")
    med_entry.config(state=DISABLED)
    med_entry.bind("<Button-1>", click)
    med_entry.pack(side=TOP, anchor=N)

    class_entry = Entry(stok_page_fm, width=30, font=("Arial", 15))
    class_entry.insert(0, "Masukkan Kelas (Generik /Paten)...")
    class_entry.config(state=DISABLED)
    class_entry.bind("<Button-1>", click_2)
    class_entry.pack(side=TOP, anchor=N)

    disease_entry = Entry(stok_page_fm, width=30, font=("Arial", 15))
    disease_entry.insert(0, "Masukkan nama penyakit...")
    disease_entry.config(state=DISABLED)
    disease_entry.bind("<Button-1>", click_3)
    disease_entry.pack(side=TOP, anchor=N)

    rules_entry = Entry(stok_page_fm, width=30, font=("Arial", 15))
    rules_entry.insert(0, "Aturan Pakai...")
    rules_entry.config(state=DISABLED)
    rules_entry.bind("<Button-1>", click_4)
    rules_entry.pack(side=TOP, anchor=N)

    store_button = Button(stok_page_fm, text="Store", width=20, command=store)
    store_button.pack(side=TOP, anchor=N)

    delete_button = Button(stok_page_fm, text="Delete", width=20,
                           command=lambda: delete(tree))
    delete_button.pack(side=TOP, anchor=S)

    refresh_button = Button(stok_page_fm, text="Refresh", width=20, command=refresh)
    refresh_button.pack(side=TOP, anchor=S)
    
    

    med_entry_labels = Label(stok_page_fm, text="Masukkan atau Hapus stok", font=("Arial", 15))
    med_entry_labels.pack(side=TOP, anchor=N)

def resep_page():
    resep_page_fm = tk.Frame (main_fm)
    resep_page_label = tk.Label(resep_page_fm, text="Resep Page", font=("Arial", 25), fg="#0097e8")
    resep_page_label.pack(pady=80)
    resep_page_fm.pack(fill=tk.BOTH, expand=True)

    def check():
        med_entry_2_input = med_entry_2.get()
        if str(med_entry_2_input) == "scantoma":
            answer_label.config(text=f"{med_entry_2_input} adalah obat diare")
        elif str(med_entry_2_input) == "forbetes":
            answer_label.config(text=f"{med_entry_2_input} adalah obat diabetes")
        elif str(med_entry_2_input) == "orphen":
            answer_label.config(text=f"{med_entry_2_input} adalah obat alergi")
        elif str(med_entry_2_input) == "paracetamol":
            answer_label.config(text=f"{med_entry_2_input} adalah obat demam")
        med_entry_2.delete(0, END)


    def delete(name, kelas):
        nama = med_entry_2.get()
        kelas = disease_entry_2.get()
        med_entry_2.delete(0, END)
        disease_entry_2.delete(0, END)
        Messagebox.showinfo(title="Delete Statue", message="Succesfully Deleted")
        sqlFormula = "DELETE FROM medicine WHERE name = %s AND class = %s"
        vals = (name, kelas)
        mycursor.execute(sqlFormula, vals)
        mydb.commit()

    def check_2():
        disease_entry_2_input = disease_entry_2.get()
        if str(disease_entry_2_input) == "demam":
            answer_label.config(text="Hufagesic paracetamol, dengan aturan pakai untuk dewasa dan anak diatas 12 tahun 3-4x sehari, dosis 1-2 tablet, sesudah makan")
        elif str(disease_entry_2_input) == "alergi":
            answer_label.config(text="Orphen, dengan aturan pakai untuk dewasa dan anak diatas 12 tahun 3-4x sehari, dosis 1 kaplet, saat makan")
        elif str(disease_entry_2_input) == "diare":
            answer_label.config(text="Scantoma, dengan aturan pakai untuk dewasa dan anak diatas 12 tahun maksimal 8x sehari, dosis 2 tablet setiap 1/2-1 jam")
        elif str(disease_entry_2_input) == "diabetes":
            answer_label.config(text="Forbetes, dengan aturan pakai untuk dewasa dan anak diatas 12 tahun 2x sehari, dosis 1 tablet, saat makan")
        disease_entry_2.delete(0, END)


    def click_resep(event):
        med_entry_2.config(state=NORMAL)
        med_entry_2.delete(0, END)


    def click_2_resep(event):
        disease_entry_2.config(state=NORMAL)
        disease_entry_2.delete(0, END)


    med_entry_2 = Entry(resep_page_fm, width=30, font=("Arial", 15))
    med_entry_2.insert(0, "Masukkan Nama Obat...")
    med_entry_2.config(state=DISABLED)
    med_entry_2.bind("<Button-1>", click_resep)
    med_entry_2.pack(side=TOP, anchor=N)

    check_button = Button(resep_page_fm, text="Check", width=20, command=check)
    check_button.pack(side=TOP, anchor=N)

    med_entry_labels = Label(resep_page_fm, text="Cek Penyakit Apa...", font=("Arial", 15))
    med_entry_labels.pack(side=TOP, anchor=N)

    disease_entry_2 = Entry(resep_page_fm, width=30, font=("Arial", 15))
    disease_entry_2.insert(0, "Masukkan nama penyakit...")
    disease_entry_2.config(state=DISABLED)
    disease_entry_2.bind("<Button-1>", click_2_resep)
    disease_entry_2.pack(side=TOP, anchor=N)


    check_button_2  =Button(resep_page_fm, text="Check", width=20, command=check_2)
    check_button_2.pack(side=TOP, anchor=N)

    disease_entry_labels = Label(resep_page_fm, text="Cek Obat Apa...", font=("Arial", 15))
    disease_entry_labels.pack(side=TOP, anchor=N)

    answer_label = Label(resep_page_fm, text="\nJawaban akan muncul disini", font=("Arial", 15))
    answer_label.pack(side=TOP, anchor=N)



def about_page():
    about_page_fm = tk.Frame(main_fm)
    about_page_label = tk.Label(about_page_fm, text="About Page", font=("Arial", 25), fg="#0097e8")
    about_page_label.pack(pady=80)
    about_page_fm.pack(fill=tk.BOTH, expand=True)

    ardi_label = Label(about_page_fm, text="Ardi Febriansyah 3332230119", font=("Arial", 15), fg="#0097e8")
    ardi_label.pack(pady=8)

    akmal_label = Label(about_page_fm, text="Muhammad Irfan Akmal 3332230096", font=("Arial", 15), fg="#0097e8")
    akmal_label.pack(pady=8)

    reza_label = Label(about_page_fm, text="Reza Abdillah Prastian 3332230086", font=("Arial", 15), fg="#0097e8")
    reza_label.pack(pady=8)

    meira_label = Label(about_page_fm, text="Meira Aisha Shofiya 3332230093", font=("Arial", 15), fg="#0097e8")
    meira_label.pack(pady=8)

    naida_label = Label(about_page_fm, text="Naidasyahla Andini 3332230062", font=("Arial", 15), fg="#0097e8")
    naida_label.pack(pady=8)

    dewangga_label = Label(about_page_fm, text="Dewangga Januarta 3332230111", font=("Arial", 15), fg="#0097e8")
    dewangga_label.pack(pady=8)

    ikhsan_label = Label(about_page_fm, text="Muhammad Ikhsan 3332230103", font=("Arial", 15), fg="#0097e8")
    ikhsan_label.pack(pady=8)

    ipaldi_label = Label(about_page_fm, text="Ipaldi Kuma 3332230120", font=("Arial", 15), fg="#0097e8")
    ipaldi_label.pack(pady=8)

    yasya_label = Label(about_page_fm, text="Yasya Fathul Huda Nugroho 3332230116", font=("Arial", 15), fg="#0097e8")
    yasya_label.pack(pady=8)

home_btn = tk.Button(options_fm, text="Home", font=("Arial", 13), bd=0,
                     fg="#0097e8", activeforeground="#0097e8",
                     command=lambda: switch(indicator_label=home_indicator_label, page=home_page))
home_btn.place(x=0, y=0, width=125)

home_indicator_label = tk.Label(options_fm, bg="#0097e8")
home_indicator_label.place(x=22, y=26, width=80, height=2)

stock_btn = tk.Button(options_fm, text="Stok", font=("Arial", 13), bd=0,
                     fg="#0097e8", activeforeground="#0097e8",
                     command=lambda: switch(indicator_label=stock_indicator_label, page=stok_page))
stock_btn.place(x=175, y=0, width=125)

stock_indicator_label = tk.Label(options_fm)
stock_indicator_label.place(x=195, y=26, width=80, height=2)

resep_btn = tk.Button(options_fm, text="Resep Dokter", font=("Arial", 13), bd=0,
                     fg="#0097e8", activeforeground="#0097e8",
                     command=lambda: switch(indicator_label=resep_indicator_label, page=resep_page))
resep_btn.place(x=350, y=0, width=125)

resep_indicator_label = tk.Label(options_fm)
resep_indicator_label.place(x=357, y=26, width=110, height=2)

about_btn = tk.Button(options_fm, text="Tentang", font=("Arial", 13), bd=0,
                     fg="#0097e8", activeforeground="#0097e8",
                      command=lambda: switch(indicator_label=about_indicator_label, page=about_page))
about_btn.place(x=525, y=0, width=125)

about_indicator_label = tk.Label(options_fm)
about_indicator_label.place(x=547, y=26, width=80, height=2)


#mycursor.execute("")

#for tb in mycursor:
    #print(tb)





# CHAPTER 2 : DELETING ITEM FROM THE STOCK




home_page()
#stok_page()

window.mainloop()


