from tkinter import *
import tkinter.ttk as ttk
from Scripts.shop_database import *
from Scripts.chart import plot_the_graph


def is_int(s):
    """
    Проверка строки на приводимость к целочисленному числу
    :param s: входная строка
    :return:
    """
    try:
        int(s)
        return True
    except ValueError:
        return False


def destroy_widgets():
    """
    Функция удаляет виджеты, которые показывались в другом разделе
    :return:
    """
    for t in range(0, 6):
        for widget in main_window.grid_slaves(row=3, column=t):
            widget.destroy()
        for widget in main_window.grid_slaves(row=4, column=t):
            widget.destroy()
        for widget in main_window.grid_slaves(row=5, column=t):
            widget.destroy()


def form_table(data):
    """
    Функция, которая выводит датафрейм на экран приложения
    :param data: Датафрейм, который мы выводим
    :return:
    """
    for children in TABLE_FRAME.pack_slaves():
        children.destroy()
    rows = data.shape[0]
    table = ttk.Treeview(TABLE_FRAME, height=22)

    style = ttk.Style(TABLE_FRAME)
    style.theme_use("clam")
    style.configure("Treeview", background="#49464c",
                    fieldbackground="#49464c", foreground="orange")
    main_window.update_idletasks()
    current_window_width = TABLE_FRAME.winfo_width()

    table["columns"] = ("one", "two", "three", "four", "five")
    table['show'] = 'headings'
    table.heading("one", text="id")
    table.heading("two", text="type")
    table.heading("three", text="name")
    table.heading("four", text="price")
    table.heading("five", text="amount")

    def get_row_selection(event):
        selection = table.selection()[0]
        temp = int(selection.split("I")[1])
        return temp

    def set_size():
        """
        Функция устанавливает размер колонкам
        :return:
        """
        table.column("one", width=int(current_window_width / 7))
        table.column("two", width=int(2 * current_window_width / 7))
        table.column("three", width=int(2 * current_window_width / 7))
        table.column("four", width=int(current_window_width / 7))
        table.column("five", width=int(current_window_width / 7))

    set_size()
    for j in range(0, rows):
        lst = [data.index.tolist()[j]] + list(data.iloc[j])
        table.insert("", 'end', text=j, values=lst)

    def disable_table_resizing(event):
        """
        Функция, которая не дает пользователю менять размер колонок таблицы
        :param event: бинд на эту функцию
        :return:
        """
        if table.identify_region(event.x, event.y) == "separator":
            return "break"

    table.bind("<Button-1>", disable_table_resizing)
    table.bind("<Double-Button-1>", get_row_selection)
    table.pack(fill=BOTH)
    Grid.rowconfigure(main_window, 1, weight=2)


def menu_pick(event):
    """
    С помощью этой функции выводятся на экран инструменты взаимодействия с базой данных
    :param event: бинд на эту функцию
    :return:
    """
    w = event.widget
    selection = int(w.curselection()[0])

    if selection == 0:
        destroy_widgets()
        # developing new bottom widgets
        ADD_BTN = Button(main_window, text="add", background="gray", foreground="black")
        INFO_LABEL = Label(main_window, text="Вставить в базу данных",
                           background="#1c0f21",
                           foreground="orange", font="Arial 12"
                           ).grid(row=3, column=0, columnspan=7, sticky="nwe")
        Grid.rowconfigure(main_window, 3, weight=1)
        id_entry = Entry(main_window, text="id", background="gray", justify=CENTER)
        type_entry = Entry(main_window, text="type", background="gray", justify=CENTER)
        name_entry = Entry(main_window, text="name", background="gray", justify=CENTER)
        price_entry = Entry(main_window, text="price", background="gray", justify=CENTER)
        amount_entry = Entry(main_window, text="amount", background="gray", justify=CENTER)
        ADD_BTN.grid(row=4, column=5, sticky="nwe", padx=5, pady=5)
        BOTTOM_EMPTY = Label(main_window, background="#49464c", height=1
                             ).grid(row=5, column=0, columnspan=5, sticky="nswe")

        def clear_entries():
            """
            Функция очищает виджеты для ввода
            :return:
            """
            id_entry.delete(0, END)
            type_entry.delete(0, END)
            name_entry.delete(0, END)
            price_entry.delete(0, END)
            amount_entry.delete(0, END)

        def add_to_database(event):
            """
            Функция записывает значение в датафрейм,
            затем сохраняет его и обновляет базу, выведенную на экран
            :param event: бинд на эту функцию
            :return:
            """
            buff = [id_entry.get(), type_entry.get(), name_entry.get(), price_entry.get(), amount_entry.get()]
            is_empty = True
            for value in buff:
                if str(value) == "":
                    is_empty = True
                    break
                else:
                    is_empty = False
            if not is_empty:
                if not is_int(buff[0]) or not is_int(buff[3]) or not is_int(buff[4]):
                    clear_entries()
                else:
                    is_primary = False
                    for key in df.index.tolist():
                        if key == int(buff[0]):
                            is_primary = False
                            break
                        else:
                            is_primary = True
                    if is_primary:
                        save_df_as_csv(add_to_df(df, buff), "database_example")
                        form_table(load_csv_to_df())
                    else:
                        clear_entries()
            else:
                clear_entries()

        ADD_BTN.bind("<Button-1>", add_to_database)
        id_entry.grid(row=4, column=0, sticky="nwe", padx=5, pady=5)
        type_entry.grid(row=4, column=1, sticky="nwe", padx=5, pady=5)
        name_entry.grid(row=4, column=2, sticky="nwe", padx=5, pady=5)
        price_entry.grid(row=4, column=3, sticky="nwe", padx=5, pady=5)
        amount_entry.grid(row=4, column=4, sticky="nwe", padx=5, pady=5)

    if selection == 1:
        # destruction of others bottom widgets
        destroy_widgets()
        # developing new bottom widgets
        INFO_LABEL = Label(main_window, text="Удалить из базы данных",
                           background="#1c0f21",
                           foreground="orange", font="Arial 12"
                           ).grid(row=3, column=0, columnspan=7, sticky="nwe")
        Grid.rowconfigure(main_window, 3, weight=1)
        FIND_ENTRY = Entry(main_window, text="name", background="gray", justify=CENTER
                           ).grid(row=4, column=1, columnspan=2, sticky="wne", padx=5, pady=5)
        variable = StringVar(main_window)
        variable.set("Все категории")
        find_in_col = OptionMenu(main_window, variable, "Все категории", "id", "type", "name", "amount", "price")
        find_in_col.config(bg="gray")
        find_in_col["menu"].config(bg="gray")
        find_in_col.grid(row=4, column=4, sticky="nwe", padx=5, pady=5)

        FIND_BTN = Button(main_window, background="gray", text="Найти", foreground="black"
                          ).grid(row=4, column=5, sticky="nwe", padx=5, pady=5)

        BOTTOM_EMPTY = Label(main_window, background="#49464c", height=1, text="\n\n"
                             ).grid(row=5, column=0, columnspan=5, sticky="nswe")

    if selection == 2:
        # destruction of others bottom widgets
        destroy_widgets()
        # developing new bottom widgets
        # TODO сделать редактирование бд

    if selection == 3:
        # destruction of others bottom widgets
        destroy_widgets()
        # creating new window with chart options
        plot_the_graph()


main_window = Tk()
BOTTOM_FRAME = Frame(main_window, bg="#49464c", relief=FLAT).grid(row=3, column=0, columnspan=5, sticky="swe")

MENU_LIST = ["Вставить в БД", "Удалить из БД", "Редактировать БД", "Построение графиков"]

# CONFIGURE MAIN WINDOW
main_window.title(u"Vape Shop app")
main_window.configure(background="#49464c")
main_window.geometry("800x600")

HELLO_USER = Label(main_window,
                   background="#1c0f21",
                   height=4,
                   text="Vape shop app\nPowered by biv184",
                   fg="orange"
                   ).grid(row=0, column=0, columnspan=6, sticky="we")

Grid.columnconfigure(main_window, 0, weight=1)
EMPTY_SLOT = Frame(main_window,
                   background="#1c0f21",
                   ).grid(row=0, column=6, sticky="wnse")
RIGHT_MENU = Listbox(main_window,
                     background="#312b38",
                     foreground="orange",
                     font="Arial 10",
                     relief=FLAT,
                     highlightthickness=0,
                     )

TABLE_FRAME = Frame(main_window, relief=FLAT, background="#49464c")
TABLE_FRAME.grid(row=1, column=0, columnspan=6, sticky=NSEW)

df = load_csv_to_df()
form_table(df)

for i in MENU_LIST:
    RIGHT_MENU.insert(END, i)

RIGHT_MENU.grid(row=1, column=6, sticky="nswe", rowspan=5)

Grid.rowconfigure(main_window, 1, weight=2)
Grid.rowconfigure(main_window, 3, weight=1)

RIGHT_MENU.bind("<Double-Button-1>", menu_pick)

Grid.columnconfigure(main_window, 5, weight=1)
Grid.columnconfigure(main_window, 4, weight=1)
Grid.columnconfigure(main_window, 3, weight=1)
Grid.columnconfigure(main_window, 2, weight=1)
Grid.columnconfigure(main_window, 1, weight=1)
Grid.columnconfigure(main_window, 0, weight=1)

main_window.mainloop()
