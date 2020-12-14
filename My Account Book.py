from tkinter import*
from tkinter.filedialog import*
import tkinter.messagebox
import tkinter as tkr
import tkinter.ttk as tkrttk
import pyperclip
import os


root = Tk()
root.title("ID/PW Book")


# File_Dropdown
def new():
    result = tkinter.messagebox.askquestion(
        "?", "기존 문서가 사라집니다. 새로운 문서를 만들겠습니까?")

    if result == 'yes':
        for i in Table.get_children():
            temp01 = Table.index(i)
            del TableData_web[temp01]
            del TableData_ID[temp01]
            del TableData_PW[temp01]
            Table.delete(i)


def save():
    Table.clipboard_clear()
    print(SaveFileDirectory)
    file = open("SaveFileDirectory".txt, 'w')
    TableData_num = len(TableData[0])

    for i01 in range(TableData_num):
        temp_str = str(TableData[0][i01])+',' + \
            str(TableData[1][i01])+','+str(TableData[2][i01])
        print(temp_str)
        file.write(temp_str+'\n')

    file.close()


def saveme(*args):
    file = asksaveasfile(mode='w', defaultextension='.txt')
    TableData_num = len(TableData[0])

    for i01 in range(TableData_num):
        temp_str = str(TableData[0][i01])+',' + \
            str(TableData[1][i01]) + ',' + str(TableData[2][i01])
        print(temp_str)  # web,ID,PW
        file.write(temp_str+'\n')

    file.close()


def yesmyload(*args):
    file = askopenfilename(
        initialdir="C:/Users/Desktop", title="Select a File", filetypes=(("text file", "*.txt"), ("all File", "*.*")))
    f1 = open(file)
    f2 = f1.read()
    f3 = f2.split("\n")
    f3.pop(-1)

    if len(TableData_web) == 0:
        for i in range(len(f3)):
            DataBase = f3[i].split(",")
            Table.insert('', 'end', text=DataBase[0], values=(
                DataBase[1], DataBase[2]))
            TableData_web.append(DataBase[0])
            TableData_ID.append(DataBase[1])
            TableData_PW.append(DataBase[2])

    elif len(TableData_web) >= 1:
        result = tkinter.messagebox.askquestion("?", "기존 문서에 붙혀쓰시겠습니까?")

        if result == 'yes':
            for i in range(len(f3)):
                DataBase = f3[i].split(",")
                Table.insert('', 'end', text=DataBase[0], values=(
                    DataBase[1], DataBase[2]))
                TableData_web.append(DataBase[0])
                TableData_ID.append(DataBase[1])
                TableData_PW.append(DataBase[2])

        else:
            for i in Table.get_children():
                temp01 = Table.index(i)
                del TableData_web[temp01]
                del TableData_ID[temp01]
                del TableData_PW[temp01]
                Table.delete(i)

            for i in range(len(f3)):
                DataBase = f3[i].split(",")
                Table.insert('', 'end', text=DataBase[0], values=(
                    DataBase[1], DataBase[2]))
                TableData_web.append(DataBase[0])
                TableData_ID.append(DataBase[1])
                TableData_PW.append(DataBase[2])


menu = Menu(root)
menu_file = Menu(menu, tearoff=0)
menu_file.add_command(label="New...", command=new)
menu_file.add_command(label="Save...", command=save)
menu_file.add_command(label="Save As...", command=saveme)
menu_file.add_command(label="Open As...", command=yesmyload)
menu_file.add_separator()
menu_file.add_command(label="Exit", command=root.quit)

menu.add_cascade(label="File", menu=menu_file)


# View_Dropdown
def block():
    for BlockIID in Table.get_children():
        BlockIndex = Table.index(BlockIID)
        ID = TableData_ID[BlockIndex]
        PW = TableData_PW[BlockIndex]
        print(PW)
        BlockedID = "*" * len(ID)
        BlockedPW = "*" * len(PW)

        if chkValue_PW.get() == True:
            if chkValue_ID.get() == False:  # PW 체크
                Table.item(BlockIID, values=(ID, BlockedPW))

            if chkValue_ID.get() == True:  # PW ID 체크
                Table.item(BlockIID, values=(BlockedID, BlockedPW))

        elif chkValue_PW.get() == False:  # none 체크
            if chkValue_ID.get() == False:
                Table.item(BlockIID, values=(ID, PW))

            if chkValue_ID.get() == True:  # ID 체크
                Table.item(BlockIID, values=(BlockedID, PW))


menu_view = Menu(menu, tearoff=0)

chkValue_PW = BooleanVar(menu_view)
PWBlcokButton = menu_view.add_checkbutton(
    label="PW 숨기기", command=block, var=chkValue_PW)

chkValue_ID = BooleanVar(menu_view)
IDBlockButton = menu_view.add_checkbutton(
    label="ID 숨기기", command=block, var=chkValue_ID)

menu.add_cascade(label="View", menu=menu_view)


root.config(menu=menu)


# 메인프레임
MainFrame = Frame(root, bd=1, relief="ridge")
MainFrame.pack(fill="y", expand=True)

# 서치프레임


def search(*args, item=''):
    children = Table.get_children(item)
    selections = []
    for child in children:
        text = Table.item(child, 'text')
        if text.startswith(SearchEntry.get()):
            selections.append(child)
            Table.selection_set(selections)
        search(None, item=child)

    # empty
    if len(SearchEntry.get()) == 0:
        Table.selection_remove(selections)
        Status['text'] = " "

    # 하나의 결과
    elif len(selections) == 1:
        for i in Table.selection():
            temp01 = Table.index(i)

        Status['text'] = (
            "Press ENTER to copy PW".format(TableData_web[temp01]))

    # 2개 이상의 결과
    elif len(selections) >= 2:
        Status['text'] = ("result : {0}".format((len(selections))))
        Table.see(selections[0])

    else:
        pass


def copyPW_Search(*args, item=''):

    children = Table.get_children(item)
    selections = []

    for child in children:
        text = Table.item(child, 'text')
        if text.startswith(SearchEntry.get()):
            selections.append(child)

    if len(selections) == 1:
        for i in Table.selection():
            temp01 = Table.index(i)

            Table.clipboard_clear()
            Table.clipboard_append(TableData_PW[temp01])
            Status['text'] = (
                "COPY : {0}'s PW".format(TableData_web[temp01]))

    else:
        pass


SearchFrame = Frame(MainFrame, bd=1, relief="ridge")
SearchFrame.pack(fill="x")

Searchvar = StringVar(SearchFrame)

SearchEntry = Entry(SearchFrame, textvariable=Searchvar)
SearchEntry.grid(row=0, column=0, sticky='w')

Searchvar.trace_variable("w", search)
SearchEntry.bind('<Return>', copyPW_Search)


# status

Status = Label(SearchFrame, width=30)
Status.grid(row=0, column=1)


# 수정버튼
def edit(*args):

    for Widget in Table.selection():
        SelectedIID = Table.index(Widget)
        Status['text'] = ("Edit : {0}' account".format(
            TableData_web[SelectedIID]))
        SelectedBBOX = list(Table.bbox(Widget, column=0))

    EditObject = Table.selection()
    EditIID = EditObject[0]
    EditIndex = Table.index(EditObject)
    yplace = SelectedBBOX[1] + 1

    def saveedit(*args):
        Status['text'] = ("")

        if chkValue_PW.get() == True:
            if chkValue_ID.get() == True:  # PW ID
                Table.item(EditIID, text=EditEntry_web.get(), values=(
                    len(EditEntry_ID.get()) * "*", len(EditEntry_PW.get()) * "*"))
            elif chkValue_ID.get() == False:  # PW
                Table.item(EditIID, text=EditEntry_web.get(), values=(
                    EditEntry_ID.get(), len(EditEntry_PW.get()) * "*"))
        elif chkValue_PW.get() == False:
            if chkValue_ID.get() == True:  # ID
                Table.item(EditIID, text=EditEntry_web.get(), values=(
                    len(EditEntry_ID.get()) * "*", EditEntry_PW.get()))
            elif chkValue_ID.get() == False:  # none
                Table.item(EditIID, text=EditEntry_web.get(), values=(
                    EditEntry_ID.get(), EditEntry_PW.get()))

        TableData_web[EditIndex] = EditEntry_web.get()
        TableData_ID[EditIndex] = EditEntry_ID.get()
        TableData_PW[EditIndex] = EditEntry_PW.get()

        EditLabel.place_forget()

    EditLabel = Label(Table, width=61, height=1, bg='lightgray', bd=2)
    EditEntry_web = Entry(EditLabel, width=17, bg='lightgray', bd=0)
    EditEntry_web.insert(0, TableData_web[EditIndex])

    EditEntry_ID = Entry(EditLabel, width=19, bg='lightgray',
                         bd=0)
    EditEntry_ID.insert(0, TableData_ID[EditIndex])

    EditEntry_PW = Entry(EditLabel, width=14, bg='lightgray',
                         bd=0)
    EditEntry_PW.insert(0, TableData_PW[EditIndex])

    EditButton = Button(EditLabel, text='Save', width=3, bg='lightgray',
                        height=1, command=saveedit)

    EditLabel.place(x=1, y=yplace-1)
    EditEntry_web.place(x=19, y=0)
    EditEntry_ID.place(x=144, y=0)
    EditEntry_PW.place(x=288, y=0)
    EditButton.place(x=398, y=-4)

    EditEntry_web.bind('<Return>', saveedit)
    EditEntry_ID.bind('<Return>', saveedit)
    EditEntry_PW.bind('<Return>', saveedit)

    def saveedit_click_cell(event):
        Status['text'] = ("")

        if chkValue_PW.get() == True:
            if chkValue_ID.get() == True:  # PW ID
                Table.item(EditIID, text=EditEntry_web.get(), values=(
                    len(EditEntry_ID.get()) * "*", len(EditEntry_PW.get()) * "*"))
            elif chkValue_ID.get() == False:  # PW
                Table.item(EditIID, text=EditEntry_web.get(), values=(
                    EditEntry_ID.get(), len(EditEntry_PW.get()) * "*"))
        elif chkValue_PW.get() == False:
            if chkValue_ID.get() == True:  # ID
                Table.item(EditIID, text=EditEntry_web.get(), values=(
                    len(EditEntry_ID.get()) * "*", EditEntry_PW.get()))
            elif chkValue_ID.get() == False:  # none
                Table.item(EditIID, text=EditEntry_web.get(), values=(
                    EditEntry_ID.get(), EditEntry_PW.get()))

        TableData_web[EditIndex] = EditEntry_web.get()
        TableData_ID[EditIndex] = EditEntry_ID.get()
        TableData_PW[EditIndex] = EditEntry_PW.get()

        # move 함수 전 클릭 대비
        ClickedObject = event.widget
        MovefromIndex = ClickedObject.index(
            ClickedObject.identify_row(event.y))

        if Table.identify_region(event.x, event.y) == 'cell' or 'tree':
            Table.clipboard_clear()
            Table.clipboard_append(int(MovefromIndex))

        EditLabel.grid_forget()

    Table.bind('<Button-1>', saveedit_click_cell)

    EditEntry_PW.focus()


# 삭제버튼
def delete(*args):
    DeleteObjects = Table.selection()
    NextIID = Table.next(DeleteObjects[-1])

    if len(DeleteObjects) == 1:
        DeleteIndex = Table.index(DeleteObjects)

        del TableData_web[DeleteIndex]
        del TableData_ID[DeleteIndex]
        del TableData_PW[DeleteIndex]
        Table.delete(DeleteObjects)

        Table.selection_set(NextIID)
        Table.focus(NextIID)

    elif len(DeleteObjects) > 1:
        for DeleteObjects in Table.selection():
            DeleteIndex = Table.index(DeleteObjects)

            del TableData_web[DeleteIndex]
            del TableData_ID[DeleteIndex]
            del TableData_PW[DeleteIndex]
            Table.delete(DeleteObjects)
            print(DeleteIndex)

            Table.selection_set(NextIID)
            Table.focus(NextIID)


ButtonFrame = Frame(SearchFrame)
ButtonFrame.grid(row=0, column=2, sticky="e")

Button_edit = Button(ButtonFrame, text="Edit", command=edit)
Button_edit.grid(row=0, column=0, sticky='e')

Button_del = Button(ButtonFrame, text="Delete", command=delete)
Button_del.grid(row=0, column=1, sticky='e')


# 리스트프레임

ListFrame = Frame(MainFrame, bd=1, relief="ridge")
ListFrame.pack(fill="y", expand=True)

Table = tkrttk.Treeview(ListFrame)

Table["columns"] = ("Column 2", "Column 3")

Table.column("#0", width=143, minwidth=10, stretch="True")
Table.column("Column 2", width=143, minwidth=10, stretch="True")
Table.column("Column 3", width=143, minwidth=10, stretch="True")

Table.heading("#0", text="web")
Table.heading("Column 2", text="ID")
Table.heading("Column 3", text="PW")


# 더블클릭 pw복사
def copyPW_DobbleClick(*args):
    CopyObject = Table.selection()
    CopyIndex = Table.index(CopyObject)
    PW = TableData_PW[CopyIndex]

    Table.clipboard_clear()
    Table.clipboard_append(PW)

    Status['text'] = (
        "COPY : {0}'s PW".format(TableData_web[CopyIndex]))

# Drag&Drop 함수


def click(event, *args):
    ClickedObject = event.widget
    MovefromIndex = ClickedObject.index(ClickedObject.identify_row(event.y))
    Table.clipboard_clear()

    if Table.identify_region(event.x, event.y) == 'cell' or 'tree':
        Table.clipboard_append(int(MovefromIndex))

    else:  # Nothing Click
        print("nothing&heading")
        for temp01 in Table.get_children():
            Table.selection_remove(temp01)
        Table.clipboard_append("False")

    Status['text'] = ("")


def move(event, *args):
    MovingObject = event.widget  # 잡고 움직일 대상
    MovetoIndex = MovingObject.index(
        MovingObject.identify_row(event.y))  # 움직일 위치(계속 변함)
    FirstIndex = Table.index(list(Table.get_children(''))[0])  # 첫번째 인덱스
    LastIndex = Table.index(list(Table.get_children(''))[-1])  # 마지막 인덱스
    print(event.y)

    # Upper Heading
    if event.y <= 24:
        print(Table.identify_region(event.x, event.y))
        # 첫번째 인덱스로.
        for MovingIID in MovingObject.selection():
            Table.reattach(MovingIID, Table.parent(MovingIID), FirstIndex)
            Table.see(MovingIID)

        # Under Heading
    elif event.y > 25:
        for MovingIID in MovingObject.selection():
            # 지정된 인덱스로
            if Table.identify_region(event.x, event.y) == 'cell':
                Table.move(MovingIID, Table.parent(MovingIID), MovetoIndex)
                Table.reattach(MovingIID, Table.parent(MovingIID), MovetoIndex)
                Table.see(MovingIID)

            elif Table.identify_region(event.x, event.y) == 'tree':
                Table.move(MovingIID, Table.parent(MovingIID), MovetoIndex)
                Table.reattach(MovingIID, Table.parent(MovingIID), MovetoIndex)
                Table.see(MovingIID)

            # 마지막 인덱스로
            elif Table.identify_region(event.x, event.y) == 'nothing':
                Table.move(MovingIID, Table.parent(MovingIID), LastIndex)
                Table.reattach(MovingIID, Table.parent(
                    MovingIID), LastIndex)
                Table.see(MovingIID)


def moveData(event, *args):
    ReleasedObject = event.widget
    MovetoIndex = ReleasedObject.index(ReleasedObject.identify_row(event.y))
    FirstIndex = Table.index(list(Table.get_children(''))[0])  # 첫번째 인덱스
    LastIndex = Table.index(list(Table.get_children(''))[-1])  # 마지막 인덱스

    print(MovetoIndex)

    if event.y <= 24:  # Upper Heading
        print("Upper Heading")

        if Table.clipboard_get() == "False":
            print("pass")
            print(TableData_web)
            Table.clipboard_clear()

        else:
            MovefromIndex = int(Table.clipboard_get())

            web = TableData_web[MovefromIndex]
            TableData_web.insert(0, web)
            TableData_web.pop(MovefromIndex+1)

            ID = TableData_ID[MovefromIndex]
            TableData_ID.insert(0, ID)
            TableData_ID.pop(MovefromIndex+1)

            PW = TableData_PW[MovefromIndex]
            TableData_PW.insert(0, PW)
            TableData_PW.pop(MovefromIndex+1)

            Table.clipboard_clear()

    elif event.y > 24:  # Under Heading
        print("Under Heading")
        if Table.identify_region(event.x, event.y) == 'cell':
            print("In Cell")
            MovefromIndex = int(Table.clipboard_get())
            if MovetoIndex < MovefromIndex:  # up
                web = TableData_web[MovefromIndex]
                TableData_web.insert(MovetoIndex, web)
                TableData_web.pop(MovefromIndex+1)

                ID = TableData_ID[MovefromIndex]
                TableData_ID.insert(MovetoIndex, ID)
                TableData_ID.pop(MovefromIndex+1)

                PW = TableData_PW[MovefromIndex]
                TableData_PW.insert(MovetoIndex, PW)
                TableData_PW.pop(MovefromIndex+1)

                Table.clipboard_clear()

            elif MovetoIndex > MovefromIndex:  # down

                web = TableData_web[MovefromIndex]
                TableData_web.insert(MovetoIndex+1, web)
                TableData_web.pop(MovefromIndex)

                ID = TableData_ID[MovefromIndex]
                TableData_ID.insert(MovetoIndex+1, ID)
                TableData_ID.pop(MovefromIndex)

                PW = TableData_PW[MovefromIndex]
                TableData_PW.insert(MovetoIndex+1, PW)
                TableData_PW.pop(MovefromIndex)

                Table.clipboard_clear()

        elif Table.identify_region(event.x, event.y) == 'tree':
            print("In Cell")
            MovefromIndex = int(Table.clipboard_get())
            if MovetoIndex < MovefromIndex:  # up
                web = TableData_web[MovefromIndex]
                TableData_web.insert(MovetoIndex, web)
                TableData_web.pop(MovefromIndex+1)

                ID = TableData_ID[MovefromIndex]
                TableData_ID.insert(MovetoIndex, ID)
                TableData_ID.pop(MovefromIndex+1)

                PW = TableData_PW[MovefromIndex]
                TableData_PW.insert(MovetoIndex, PW)
                TableData_PW.pop(MovefromIndex+1)

                Table.clipboard_clear()

            elif MovetoIndex > MovefromIndex:  # down

                web = TableData_web[MovefromIndex]
                TableData_web.insert(MovetoIndex+1, web)
                TableData_web.pop(MovefromIndex)

                ID = TableData_ID[MovefromIndex]
                TableData_ID.insert(MovetoIndex+1, ID)
                TableData_ID.pop(MovefromIndex)

                PW = TableData_PW[MovefromIndex]
                TableData_PW.insert(MovetoIndex+1, PW)
                TableData_PW.pop(MovefromIndex)

                Table.clipboard_clear()

        elif Table.identify_region(event.x, event.y) == 'nothing':
            print("Out Cell")

            if Table.clipboard_get() == "False":
                print("pass")

                Table.clipboard_clear()

            else:
                print(LastIndex)
                MovefromIndex = int(Table.clipboard_get())
                web = TableData_web[MovefromIndex]
                TableData_web.pop(MovefromIndex)
                TableData_web.insert(LastIndex, web)

                ID = TableData_ID[MovefromIndex]
                TableData_ID.pop(MovefromIndex)
                TableData_ID.insert(LastIndex, ID)

                PW = TableData_PW[MovefromIndex]
                TableData_PW.pop(MovefromIndex)
                TableData_PW.insert(LastIndex, PW)

                Table.clipboard_clear()
                print(TableData_web)

    print(TableData_web)
    Table.clipboard_clear()


Table.bind('<Double-Button-1>', copyPW_DobbleClick)
Table.bind('<Control-c>', copyPW_DobbleClick)
Table.bind('<Return>', copyPW_DobbleClick)
root.bind('<Delete>', delete)
root.bind('<Control-e>', edit)

# Drag&Drop Bind
Table.bind('<Button-1>', click)
Table.bind('<B1-Motion>', move)
Table.bind('<ButtonRelease-1>', moveData)

Table.pack(fill='y', expand=True)


# 리스트 데이터
TableData_web = []
TableData_ID = []
TableData_PW = []
TableData = [TableData_web, TableData_ID, TableData_PW]


# 입력프레임
InsertFrame = Frame(MainFrame, bd=1, relief="ridge")
InsertFrame.pack(fill='x')

InsertEntry_web = Entry(InsertFrame)
InsertEntry_web.grid(row=0, column=0)

InsertEntry_ID = Entry(InsertFrame)
InsertEntry_ID.grid(row=0, column=1)

InsertEntry_PW = Entry(InsertFrame)
InsertEntry_PW.grid(row=0, column=2)


# 입력버튼
def insert(*args):
    # tree.insert(parent='', index='end', iid=0, text="Label", values=("Hello", "Second Col", "Third Col"))
    if chkValue_PW.get() == True:
        if chkValue_ID.get() == False:  # PW
            Table.insert('', 'end', text=InsertEntry_web.get(), values=(
                InsertEntry_ID.get(), len(InsertEntry_PW.get()) * "*"))

        if chkValue_ID.get() == True:  # ID PW
            Table.insert('', 'end', text=InsertEntry_web.get(), values=(
                len(InsertEntry_ID.get()) * "*", len(InsertEntry_PW.get()) * "*"))

    elif chkValue_PW.get() == False:
        if chkValue_ID.get() == False:  # none
            Table.insert('', 'end', text=InsertEntry_web.get(), values=(
                InsertEntry_ID.get(), InsertEntry_PW.get()))

        if chkValue_ID.get() == True:  # ID
            Table.insert('', 'end', text=InsertEntry_web.get(), values=(
                len(InsertEntry_ID.get()) * "*", InsertEntry_PW.get()))

    TableData_web.append(InsertEntry_web.get())
    TableData_ID.append(InsertEntry_ID.get())
    TableData_PW.append(InsertEntry_PW.get())

    InsertEntry_web.delete(0, END)
    InsertEntry_ID.delete(0, END)
    InsertEntry_PW.delete(0, END)

    EntireItem = Table.get_children('')
    EntireItem = list(EntireItem)
    Table.selection_set(EntireItem[-1])
    Table.see(EntireItem[-1])

    InsertEntry_web.focus()
    print(TableData)


InsertButton = Button(InsertFrame, height=1, text="insert", command=insert)
InsertButton.bind("<Return>", insert)
InsertEntry_PW.bind("<Return>", insert)
InsertButton.grid(row=1, column=0, columnspan=3, sticky=N+S+W+E)

root.mainloop()
