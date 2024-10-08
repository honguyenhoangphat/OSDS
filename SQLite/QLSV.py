from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3

root = Tk()
root.title("Hệ thống quản lý địa chỉ")
root.geometry("1500x1200")

# Kết nối tới db
conn = sqlite3.connect('QLSV.db')
c = conn.cursor()

#Tao bang de luu tru
# c.execute('''
#      CREATE TABLE QLSV(
#         Ma_SV integer primary key autoincrement,
#         first_name text,
#         last_name text,
#         class_id integer,
#         year_commenced integer,
#         average_score interger
#     )
# ''')

def them():
    #Ket noi va lay du lieu
    conn = sqlite3.connect('QLSV.db')
    c = conn.cursor()
    #Lay du lieu da nhap
    Ma_SV_value = Ma_SV.get()
    firstname_value = f_name.get()
    lastName_value = l_name.get()
    class_id_value = class_id.get()
    year_commenced_value = year_commenced.get()
    average_score_value = average_score.get()

    #Thuc hien cau lenh de ADD
    c.execute('''
        INSERT INTO
        QLSV (Ma_SV, first_name, last_name, class_id, year_commenced, average_score)
        VALUES
        (:Ma_SV,:first_name, :last_name, :class_id, :year_commenced, :average_score)
    ''',  {
        'Ma_SV': Ma_SV_value,
        'first_name': firstname_value,
        'last_name': lastName_value,
        'class_id': class_id_value,
        'year_commenced': year_commenced_value,
        'average_score': average_score_value,

    }

    )

    conn.commit()
    conn.close()

    #Read
    Ma_SV.delete(0, END)
    f_name.delete(0, END)
    l_name.delete(0, END)
    class_id.delete(0, END)
    year_commenced.delete(0, END)
    average_score.delete(0, END)


    #Hienthilai data
    truy_van()
def xoa():
    conn = sqlite3.connect('QLSV.db')
    c = conn.cursor()
    c.execute('''
    DELETE FROM student
    WHERE Ma_SV=:Ma_SV''',
              { 'Ma_SV': delete_box.get()})
    delete_box.delete(0, END)
    conn.commit()
    conn.close()

    messagebox.showinfo("Thong bao", "Da Xoa!!")
    truy_van()

def truy_van():
    # Xóa đi các dữ liệu trong TreeView
    for row in tree.get_children():
        tree.delete(row)

    # Kết nối và lấy dữ liệu
    conn = sqlite3.connect('QLSV.db')
    c = conn.cursor()
    c.execute("SELECT * FROM QLSV")
    records = c.fetchall()

    # Hien thi du lieu
    for r in records:
        tree.insert("", END, values=(r[0], r[1], r[2]))

    # Ngat ket noi
    conn.close()

def chinh_sua():
    global editor
    editor = Tk()
    editor.title("Cap nhat ban ghi ")
    editor.geometry("400x300")

    conn = sqlite3.connect('QLSV.db')
    c = conn.cursor()
    record_id = delete_box.get()
    c.execute("SELECT * FROM QLSV WHERE Ma_SV=:Ma_SV", { 'Ma_SV': record_id})
    records = c.fetchall()

    global Ma_SV_editor, f_name_editor, l_name_editor, class_id_editor, year_commenced_editor, average_score_editor

    Ma_SV_editor = Entry(editor, width=30)
    Ma_SV_editor.grid(row=0, column=1, padx = 20, pady = (10, 0))
    f_name_editor = Entry(editor, width=30)
    f_name_editor.grid(row=1, column=1, padx = 20, pady = 20)
    l_name_editor = Entry(editor, width=30)
    l_name_editor.grid(row=2, column=1)
    class_id_editor = Entry(editor, width=30)
    class_id_editor.grid(row=3, column=1)
    year_commenced_editor = Entry(editor, width=30)
    year_commenced_editor.grid(row=4, column=1)
    average_score_editor = Entry(editor, width=30)
    average_score_editor.grid(row=5, column=1)


    ##LABEL
    Ma_SV_label = Label(editor, text = 'Ma Sinh Vien')
    Ma_SV_label.grid(row = 0, column=0, pady=(10,0))
    f_name_label = Label(editor,text='Ho')
    f_name_label.grid(row=1,column=0)
    l_name_label = Label(editor, text="Ten")
    l_name_label.grid(row=2, column=0)
    class_id_label = Label(editor, text="Lop")
    class_id_label.grid(row=3, column=0)
    year_commenced_label = Label(editor, text="Nam Nhap Hoc")
    year_commenced_label.grid(row=4, column=0)
    average_score_label = Label(editor, text="Diem Trung Binh")
    average_score_label.grid(row=5, column=0)


    for record in records:
        Ma_SV_editor.insert(0, record[0])
        f_name_editor.insert(0, record[1])
        l_name_editor.insert(0, record[2])
        class_id_editor.insert(0, record[3])
        year_commenced_editor.insert(0, record[4])
        average_score_editor.insert(0, record[5])

    edit_btn = Button(editor, text="Luu ban ghi", command = cap_nhat)
    edit_btn.grid(row = 7, column = 0, columnspan=2, pady = 10, padx = 10, ipadx = 10, ipady = 150)

    truy_van()
def cap_nhat():
    conn = sqlite3.connect('QLSV.db')
    c = conn.cursor()
    record_id = Ma_SV_editor.get()

    c.excute(""" UPDATE QLSV
        Set first_name = :first,
            last_name = :last,
            class = :class_id,
            yearcommenced = :year_commenced,
            averagescore = :average_score,
            WHERE Ma_SV = :MaSV
            """,
             {
                 'first': f_name_editor.get(),
                 'last': l_name_editor.get(),
                 'class': class_id_editor.get(),
                 'yearcommenced': year_commenced_editor.get(),
                 'averagescore': average_score_editor.get(),
                 'MaSV': record_id
             }
        )
    conn.commit()
    conn.close()
    editor.destroy()

    truy_van()
# Khung cho các ô nhập liệu
input_frame = Frame(root)
input_frame.pack(pady=20)

# Các ô nhập liệu cho cửa sổ chính
Ma_SV = Entry(input_frame, width=30)
Ma_SV.grid(row=0, column=1)
f_name = Entry(input_frame, width=30)
f_name.grid(row=1, column=1, padx=20, pady=(10, 0))
l_name = Entry(input_frame, width=30)
l_name.grid(row=2, column=1)
class_id = Entry(input_frame, width=30)
class_id.grid(row=3, column=1)
year_commenced = Entry(input_frame, width=30)
year_commenced.grid(row=4, column=1)
average_score = Entry(input_frame, width=30)
average_score.grid(row=5, column=1)


# Các nhãn
Ma_SV_label = Label(input_frame, text="Ma Sinh Vien")
Ma_SV_label.grid(row=0, column=0, pady=(10, 0))
f_name_label = Label(input_frame, text="Ho")
f_name_label.grid(row=1, column=0)
l_name_label = Label(input_frame, text="Ten")
l_name_label.grid(row=2, column=0)
class_id_label = Label(input_frame, text="Ma Lop")
class_id_label.grid(row=3, column=0)
year_commenced_label = Label(input_frame, text="Nam Nhap Hoc")
year_commenced_label.grid(row=4, column=0)
average_score_label = Label(input_frame, text="Diem Trung Binh")
average_score_label.grid(row=5, column=0)

# Khung cho các nút chức năng
button_frame = Frame(root)
button_frame.pack(pady=10)

# Các nút chức năng
submit_btn = Button(button_frame, text="Thêm bản ghi", command=them)
submit_btn.grid(row=0, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
query_btn = Button(button_frame, text="Hiển thị bản ghi", command=truy_van)
query_btn.grid(row=1, column=0, columnspan=2, pady=10, padx=10, ipadx=137)
delete_box_label = Label(button_frame, text="Chọn Ma Sinh Vien để xóa")
delete_box_label.grid(row=2, column=0, pady=5)
delete_box = Entry(button_frame, width=30)
delete_box.grid(row=2, column=1, pady=5)
delete_btn = Button(button_frame, text="Xóa bản ghi", command=xoa)
delete_btn.grid(row=3, column=0, columnspan=2, pady=10, padx=10, ipadx=136)
edit_btn = Button(button_frame, text="Chỉnh sửa bản ghi", command=chinh_sua)
edit_btn.grid(row=4, column=0, columnspan=2, pady=10, padx=10, ipadx=125)

# Khung cho Treeview
tree_frame = Frame(root)
tree_frame.pack(pady=10)

# Treeview để hiển thị bản ghi
columns = ("MaSV", "Họ", "Tên", "Lop", "Nam nhap hoc", "Diem Trung Binh")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)

# Hien thi ban ghi
for column in columns:
    tree.column(column, anchor=CENTER) # This will center text in rows
    tree.heading(column, text=column)
tree.pack()

for col in columns:
    tree.heading(col, text = col)
# Gọi hàm truy vấn để hiển thị bản ghi khi khởi động
truy_van()

root.mainloop()