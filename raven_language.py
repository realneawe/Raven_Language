import random
from tkinter import *
import pandas
from tkinter import messagebox
import csv
import pandas as pd
import pyperclip
import webbrowser

# <------------------------------------------------> App Parameters <------------------------------------------------->
# Uygulama Parametreleri Kod Kısmı

FONT_GROUND = "black"
BACK_GROUND = "white"
FONT = "Helvetica"
RETURN_BUTTON = "Geri"
EXIT_BUTTON = "Çıkış"
cor_count = 0
fal_count = 0

# <---------------------------------------------> Turkish Version Code <---------------------------------------------->
# Dil Özelleştirmeleri
def turkish_lower(s):
    replacements = {
        'I': 'ı',
        'İ': 'i',
        'O': 'o',
        'Ö': 'ö',
        'U': 'u',
        'Ü': 'ü',
    }
    for original, replaced in replacements.items():
        s = s.replace(original, replaced)
    return s.lower()

def turkish_capitalize(s):
    if len(s) == 0:
        return s

    first_char = s[0]

    if first_char == 'i':
        first_char = 'İ'
    elif first_char == 'ı':
        first_char = 'I'
    elif first_char == 'o':
        first_char = 'O'
    elif first_char == 'ö':
        first_char = 'Ö'
    elif first_char == 'u':
        first_char = 'U'
    elif first_char == 'ü':
        first_char = 'Ü'
    else:
        first_char = first_char.upper()

    return first_char + s[1:].lower()

# <--------------------------------------------------> Mods Page <---------------------------------------------------->
# Modlar Sayfası Fonksiyonu
def mods_page():
    home_logo_label.destroy(), home_canvas.destroy(), mods_page_button.destroy(), repo_page_button.destroy()
    settings_page_button.destroy(), app_about_button.destroy(), exit_button.destroy()
    cor_counter = Label()
    fal_counter = Label()

    # Kelimeler için Quiz Fonksiyonu
    def word_quiz():
        global fal_count
        global cor_count
        fal_count = 0
        cor_count = 0
        mods_page_label.destroy(), word_quiz_button.destroy(), mould_quiz_button.destroy()
        data = pandas.read_csv("word_repository.csv", encoding='utf-8')

        if data.shape[0] == 0:
            w_empty_warning = Label(text="Kelime Deposu Boş!", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 25, "bold"))
            w_empty_warning.grid(column=0, row=0, pady=10)

            return_button = Button(text=RETURN_BUTTON, fg=FONT_GROUND, bg=BACK_GROUND, width=7, font=(FONT, 17),
                                   activebackground=BACK_GROUND, activeforeground=FONT_GROUND,
                                   command=lambda: (mods_page(), w_empty_warning.destroy(), return_button.destroy()))
            return_button.grid(column=0, row=1)
            return

        w_eng_list = data["Word"].to_list()
        w_mean_list = data["Mean"].to_list()
        total = len(w_eng_list)

        # Kelimeler için Soru Oluşturma Fonksiyonu
        def w_create_question():
            global ran
            global question
            ran = random.randint(0, len(w_eng_list) - 1)

            question = Label(text=f"{w_eng_list[ran].capitalize()}", fg=FONT_GROUND, bg=BACK_GROUND,
                             font=(FONT, 20), anchor="w")
            question.grid(column=1, row=0, sticky=W)
            answer_button.grid(column=1, row=3, pady=2, padx=2, sticky=E)

        # Kelime Cevaplarının Kontrol Edildiği Fonksiyon
        def w_answer():
            if turkish_lower(answer.get()) == w_mean_list[ran]:
                global cor_count
                cor_count = cor_count + 1

                correct_lab.config(text="Doğru!", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 17))
                correct_lab.grid(column=2, row=1)
                cor_counter.config(text=f"{total}/{cor_count}", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 20))
                answer.delete(0, 'end')
                w_eng_list.remove(w_eng_list[ran])
                w_mean_list.remove(w_mean_list[ran])
                question.destroy()

                if len(w_eng_list) == 0:
                    answer_lab.destroy(), answer.destroy(), question.destroy(), correct_lab.destroy()
                    fal_counter.destroy(), quest_lab.destroy(), answer_button.destroy(), cor_counter.destroy()
                    finish_lab.config(text="TEBRİKLER!\nTesti bitirdiniz!")
                    finish_lab.grid(column=2, row=0, pady=10)
                else:
                    w_create_question()

            else:
                global fal_count
                fal_count += 1

                correct_lab.config(text="Yanlış!!!", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 17))
                correct_lab.grid(column=2, row=1)

                fal_counter.config(text=f"Hatalı Denemeler:{fal_count}", fg=FONT_GROUND, bg=BACK_GROUND,
                                   font=(FONT, 20),  anchor="w")
                fal_counter.grid(column=0, row=3, sticky=W, columnspan=2)

                answer.delete(0, 'end')
                question.destroy()
                w_create_question()

        # Kelimeler için Quiz Fonksiyonunun Devamı
        answer_button = Button(text="Kontrol Et", fg=FONT_GROUND, bg=BACK_GROUND, width=12, font=(FONT, 17),
                               activebackground=BACK_GROUND, activeforeground=FONT_GROUND, command=w_answer)
        finish_lab = Label(fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 17))

        answer_lab = Label(text="Anlam:", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 25), anchor="w")
        answer_lab.grid(column=0, row=1)

        correct_lab = Label()

        quest_lab = Label(text="Kelime:", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 25), anchor="w")
        quest_lab.grid(column=0, row=0)

        answer = Entry(width=30, font=(FONT, 20), fg=FONT_GROUND, bg=BACK_GROUND)
        answer.grid(column=1, row=1, sticky=W)

        cor_counter.config(text=f"{total}/{cor_count}", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 20))
        cor_counter.grid(column=2, row=0)

        answer.bind("<Return>", lambda event=None: w_answer())
        w_create_question()

        return_button = Button(text=RETURN_BUTTON, fg=FONT_GROUND, bg=BACK_GROUND, width=7, font=(FONT, 17),
                               activebackground=BACK_GROUND, activeforeground=FONT_GROUND,
                               command=lambda: (mods_page(), correct_lab.destroy(), answer_lab.destroy(),
                                                question.destroy(), answer.destroy(), cor_counter.destroy(),
                                                fal_counter.destroy(), answer_button.destroy(), finish_lab.destroy(),
                                                quest_lab.destroy(), return_button.destroy()))
        return_button.grid(column=2, row=3, pady=2, padx=2)

    # Kalıp Cümleler için Quiz Fonksiyonu
    def mould_quiz():
        global fal_count
        global cor_count
        fal_count = 0
        cor_count = 0
        mods_page_label.destroy(), word_quiz_button.destroy(), mould_quiz_button.destroy()
        data = pandas.read_csv("mould_repository.csv", encoding='utf-8')

        if data.shape[0] == 0:
            m_empty_warning = Label(text="Kalıp Cümle Deposu Boş!", fg=FONT_GROUND, bg=BACK_GROUND,
                                    font=(FONT, 25, "bold"))
            m_empty_warning.grid(column=0, row=0, pady=10)

            return_button = Button(text=RETURN_BUTTON, fg=FONT_GROUND, bg=BACK_GROUND, width=7, font=(FONT, 17),
                                   activebackground=BACK_GROUND, activeforeground=FONT_GROUND,
                                   command=lambda: (mods_page(), m_empty_warning.destroy(), return_button.destroy()))
            return_button.grid(column=0, row=1)
            return

        m_eng_list = data["Mould"].to_list()
        m_mean_list = data["Mean"].to_list()
        total = len(m_eng_list)

        # Kalıp Cümleler için Soru Oluşturma Fonksiyonu
        def m_create_question():
            global ran
            global question
            ran = random.randint(0, len(m_eng_list) - 1)

            question = Label(text=f"{m_eng_list[ran].capitalize()}", fg=FONT_GROUND, bg=BACK_GROUND,
                             font=(FONT, 20), anchor="w")
            question.grid(column=1, row=0, sticky=W)
            answer_button.grid(column=1, row=3, pady=2, padx=2, sticky=E)

        # Kalıp Cümle Cevaplarının Kontrol Edildiği Fonksiyon
        def m_answer():
            if turkish_lower(answer.get()) == m_mean_list[ran]:
                global cor_count
                cor_count = cor_count + 1

                correct_lab.config(text="Doğru!", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 17))
                correct_lab.grid(column=2, row=1)
                cor_counter.config(text=f"{total}/{cor_count}", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 20))
                answer.delete(0, 'end')
                m_eng_list.remove(m_eng_list[ran])
                m_mean_list.remove(m_mean_list[ran])
                question.destroy()

                if len(m_eng_list) == 0:
                    answer_lab.destroy(), answer.destroy(), question.destroy(), correct_lab.destroy()
                    fal_counter.destroy(), quest_lab.destroy(), answer_button.destroy(), cor_counter.destroy()
                    finish_lab.config(text="TEBRİKLER!\nTesti bitirdiniz!")
                    finish_lab.grid(column=2, row=0, pady=10)
                else:
                    m_create_question()

            else:
                global fal_count
                fal_count += 1

                correct_lab.config(text="Yanlış!!!", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 17))
                correct_lab.grid(column=2, row=1)

                fal_counter.config(text=f"Hatalı Denemeler:{fal_count}", fg=FONT_GROUND, bg=BACK_GROUND,
                                   font=(FONT, 20),  anchor="w")
                fal_counter.grid(column=0, row=3, sticky=W, columnspan=2)

                answer.delete(0, 'end')
                question.destroy()
                m_create_question()

        # Kalıp Cümleler İçin Quiz Fonksiyonunun Devamı
        answer_button = Button(text="Kontrol Et", fg=FONT_GROUND, bg=BACK_GROUND, width=12, font=(FONT, 17),
                               activebackground=BACK_GROUND, activeforeground=FONT_GROUND, command=m_answer)
        finish_lab = Label(fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 17))

        answer_lab = Label(text="Anlam:", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 25), anchor="w")
        answer_lab.grid(column=0, row=1)

        correct_lab = Label()

        quest_lab = Label(text="Kelime:", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 25), anchor="w")
        quest_lab.grid(column=0, row=0)

        answer = Entry(width=30, font=(FONT, 20), fg=FONT_GROUND, bg=BACK_GROUND)
        answer.grid(column=1, row=1, sticky=W)

        cor_counter.config(text=f"{total}/{cor_count}", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 20))
        cor_counter.grid(column=2, row=0)

        answer.bind("<Return>", lambda event=None: m_answer())
        m_create_question()

        return_button = Button(text=RETURN_BUTTON, fg=FONT_GROUND, bg=BACK_GROUND, width=7, font=(FONT, 17),
                               activebackground=BACK_GROUND, activeforeground=FONT_GROUND,
                               command=lambda: (mods_page(), correct_lab.destroy(), answer_lab.destroy(),
                                                question.destroy(), answer.destroy(), fal_counter.destroy(),
                                                cor_counter.destroy(), answer_button.destroy(), finish_lab.destroy(),
                                                quest_lab.destroy(), return_button.destroy()))
        return_button.grid(column=2, row=3, pady=2, padx=2)

    # Modlar Sayfası Fonksiyonunun Devamı
    mods_page_label = Label(text="Modlar", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 30, "bold"))
    mods_page_label.grid(column=0, row=0, pady=5)

    word_quiz_button = Button(text="Kelime Sınavı", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 17), width=30,
                              activebackground=BACK_GROUND, activeforeground=FONT_GROUND,
                              command=lambda: (word_quiz(), return_button.destroy()))
    word_quiz_button.grid(column=0, row=1, pady=2)

    mould_quiz_button = Button(text="Kalıp Cümle Sınavı", fg=FONT_GROUND, bg=BACK_GROUND, width=30,
                               activebackground=BACK_GROUND, activeforeground=FONT_GROUND,
                               font=(FONT, 17), command=lambda: (mould_quiz(), return_button.destroy()))
    mould_quiz_button.grid(column=0, row=2, pady=2)

    return_button = Button(text=RETURN_BUTTON, fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 17), width=30,
                           activebackground=BACK_GROUND, activeforeground=FONT_GROUND,
                           command=lambda: (home_page(), mods_page_label.destroy(), word_quiz_button.destroy(),
                                            mould_quiz_button.destroy(), return_button.destroy()))
    return_button.grid(column=0, row=3, pady=2)

# <---------------------------------------------> Repository Page <--------------------------------------------------->
# Repository Sayfası Fonksiyonu
def repo_page():
    home_logo_label.destroy(), home_canvas.destroy(), mods_page_button.destroy(), repo_page_button.destroy()
    settings_page_button.destroy(), app_about_button.destroy(), exit_button.destroy()

    # Kelime Ekleme Fonksiyonu
    def add_word():
        repo_title_label.destroy(), repo_top_label.destroy(), repo_mid_label.destroy(), word_add_button.destroy()
        mould_add_button.destroy(), look_word_button.destroy(), look_mould_button.destroy()

        word_label = Label(text="Kelime:", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 20))
        word_label.grid(column=0, row=0)

        w_eng_input = Entry(width=30, font=(FONT, 20), fg=FONT_GROUND, bg=BACK_GROUND)
        w_eng_input.grid(column=1, row=0)

        w_mean_label = Label(text="Anlam:", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 20))
        w_mean_label.grid(column=0, row=1)

        w_mean_input = Entry(width=30, font=(FONT, 20), fg=FONT_GROUND, bg=BACK_GROUND)
        w_mean_input.grid(column=1, row=1)

        # Kelimelerin Dosyaya Ekleme İşleminin Yapıldığı Fonksiyon
        def w_clean_input(input_str):
            stripped_str = input_str.strip()
            cleaned_str = ' '.join(stripped_str.split())
            return cleaned_str

        def add_save():
            new_word = w_clean_input(w_eng_input.get().lower())
            new_mean = w_clean_input(turkish_lower(w_mean_input.get()))

            is_ok = messagebox.askokcancel(title="Uyarı!",
                                           message=f"İngilizce kelimeniz: {new_word.capitalize()}\n\n"
                                                   f"Türkçe anlamı: {turkish_capitalize(new_mean)}\n\n"
                                                   f"Onaylıyor musunuz?")

            if is_ok:
                if new_word == "" or new_mean == "":
                    messagebox.showinfo(title="Uyarı!", message="Girişlerden biri veya birkaçı boş!!!\n"
                                                                "Lütfen boşlukları tam doldurduğunuzdan emin olun!")
                    return
                data = pandas.read_csv("word_repository.csv", encoding='utf-8')
                sorted_data = data.sort_values(by="Word")

                if sorted_data.empty or (len(data) == 1 and sorted_data["Word"].iloc[0] == "Word"
                                         and sorted_data["Mean"].iloc[0] == "Mean"):
                    sorted_data.loc[0] = [new_word, new_mean]
                else:
                    w_eng_list = sorted_data["Word"].to_list()
                    w_a_list = [letter for letter in w_eng_list if letter == new_word]
                    if w_a_list == []:
                        w_a_list.append("0")
                    if new_word != w_a_list[0]:
                        if w_eng_list[-1] == "" and len(w_eng_list) > 1:
                            sorted_data.loc[len(data) - 1] = [new_word, new_mean]
                        else:
                            sorted_data.loc[len(data)] = [new_word, new_mean]
                    else:
                        messagebox.showinfo(title="Uyarı!", message="Eklemek istenilen kelime depo içerisinde "
                                                                    "bulunmakta!\nLütfen farklı bir kelime deneyin!")
                        return

                sorted_data.to_csv("word_repository.csv", index=False, encoding='utf-8')

            w_eng_input.delete(0, END)
            w_mean_input.delete(0, END)
            w_eng_input.focus_set()

        def on_enter(event):
            add_save()
        w_eng_input.bind("<Return>", on_enter)
        w_mean_input.bind("<Return>", on_enter)

        w_add_button = Button(text="Ekle", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 17), width=20,
                              activebackground=BACK_GROUND, activeforeground=FONT_GROUND, command=add_save)
        w_add_button.grid(column=0, row=2, columnspan=2, sticky=E, pady=4)

        return_button = Button(text=RETURN_BUTTON, fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 17), width=20,
                               activebackground=BACK_GROUND, activeforeground=FONT_GROUND,
                               command=lambda: (repo_page(), word_label.destroy(), w_eng_input.destroy(),
                                                w_mean_label.destroy(), w_mean_input.destroy(),
                                                w_add_button.destroy(), return_button.destroy()))
        return_button.grid(column=0, row=2, columnspan=2, sticky=W, pady=4)

    # Kalıp Cümle Ekleme Fonksiyonu
    def add_mould():
        repo_title_label.destroy(), repo_top_label.destroy(), repo_mid_label.destroy(), word_add_button.destroy()
        mould_add_button.destroy(), look_word_button.destroy(), look_mould_button.destroy()

        mould_label = Label(text="Cümle:", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 20))
        mould_label.grid(column=0, row=0)

        m_eng_input = Entry(width=30, font=(FONT, 20), fg=FONT_GROUND, bg=BACK_GROUND)
        m_eng_input.grid(column=1, row=0)

        m_mean_label = Label(text="Anlam:", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 20))
        m_mean_label.grid(column=0, row=1)

        m_mean_input = Entry(width=30, font=(FONT, 20), fg=FONT_GROUND, bg=BACK_GROUND)
        m_mean_input.grid(column=1, row=1)

        # Kalıp Cümlelerin Dosyaya Ekleme İşleminin Yapıldığı Fonksiyon
        def m_clean_input(input_str):
            stripped_str = input_str.strip()
            cleaned_str = ' '.join(stripped_str.split())
            return cleaned_str

        def add_save():
            new_word = m_clean_input(m_eng_input.get().lower())
            new_mean = m_clean_input(turkish_lower(m_mean_input.get()))

            is_ok = messagebox.askokcancel(title="Uyarı!",
                                           message=f"İngilizce cümleniz: {new_word.capitalize()}\n\n"
                                                   f"Türkçe anlamı: {turkish_capitalize(new_mean)}\n\n"
                                                   f"Onaylıyor musunuz?")

            if is_ok:
                if new_word == "" or new_mean == "":
                    messagebox.showinfo(title="Uyarı!", message="Girişlerden biri veya birkaçı boş!!!\n"
                                                                "Lütfen boşlukları tam doldurduğunuzdan emin olun!")
                    return
                data = pandas.read_csv("mould_repository.csv", encoding='utf-8')

                if data.empty or (len(data) == 1 and data["Mould"].iloc[0] == "Mould"
                                  and data["Mean"].iloc[0] == "Mean"):
                    data.loc[0] = [new_word, new_mean]
                else:
                    m_eng_list = data["Mould"].to_list()
                    m_a_list = [letter for letter in m_eng_list if letter == new_word]
                    if m_a_list == []:
                        m_a_list.append("0")
                    if new_word != m_a_list[0]:
                        if m_eng_list[-1] == "" and len(m_eng_list) > 1:
                            data.loc[len(data) - 1] = [new_word, new_mean]
                        else:
                            data.loc[len(data)] = [new_word, new_mean]
                    else:
                        messagebox.showinfo(title="Uyarı!", message="Eklemek istenilen cümle depo içerisinde "
                                                                    "bulunmakta!\nLütfen farklı bir cümle deneyin!")
                        return

                data.to_csv("mould_repository.csv", index=False, encoding='utf-8')

            m_eng_input.delete(0, END)
            m_mean_input.delete(0, END)
            m_eng_input.focus_set()

        def on_enter(event):
            add_save()
        m_eng_input.bind("<Return>", on_enter)
        m_mean_input.bind("<Return>", on_enter)

        m_add_button = Button(text="Ekle", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 17), width=20,
                              activebackground=BACK_GROUND, activeforeground=FONT_GROUND, command=add_save)
        m_add_button.grid(column=0, row=2, columnspan=2, sticky=E, pady=4)

        return_button = Button(text=RETURN_BUTTON, fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 17), width=20,
                               activebackground=BACK_GROUND, activeforeground=FONT_GROUND,
                               command=lambda: (repo_page(), mould_label.destroy(), m_eng_input.destroy(),
                                                m_mean_label.destroy(), m_mean_input.destroy(),
                                                m_add_button.destroy(), return_button.destroy()))
        return_button.grid(column=0, row=2, columnspan=2, sticky=W, pady=4)

    # Kelimeleri Görüntüleme Fonksiyonu
    def look_word():
        repo_title_label.destroy(), repo_top_label.destroy(), repo_mid_label.destroy(), word_add_button.destroy()
        mould_add_button.destroy(), look_word_button.destroy(), look_mould_button.destroy()

        # Kelime Düzenlemelerinin Dosyaya Kaydedildiği Fonksiyon
        def update_csv(row_num, new_word, new_mean):
            with open("word_repository.csv", 'r', newline='', encoding='utf-8') as file:
                data = list(csv.reader(file))
                sort_data = sorted(data)

            sort_data[row_num] = [new_word, new_mean]

            with open("word_repository.csv", 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(sort_data)

        # Kelimeleri Düzenleme Sayfası
        def edit_word():
            w_edit_window = Toplevel()
            w_edit_window.title("Kelime Düzenleme Penceresi")
            w_edit_window.config(padx=30, pady=30, bg=BACK_GROUND)
            w_edit_window.resizable(False, False)

            w_edit_title_label = Label(w_edit_window, text="Düzenlenleme Penceresi", fg=FONT_GROUND, bg=BACK_GROUND,
                                       font=(FONT, 30, "bold"))
            w_edit_title_label.grid(column=0, row=0, columnspan=2, pady=5)

            w_edit_row_label = Label(w_edit_window, text="Kelimenin Sırası:", fg=FONT_GROUND, bg=BACK_GROUND,
                                     font=(FONT, 20))
            w_edit_row_label.grid(column=0, row=1, pady=2)

            w_edit_word_label = Label(w_edit_window, text="Düzenlenmiş Kelime:", fg=FONT_GROUND, bg=BACK_GROUND,
                                      font=(FONT, 20))
            w_edit_word_label.grid(column=0, row=2, pady=2)

            w_edit_mean_label = Label(w_edit_window, text="Düzenlenmiş Anlam:", fg=FONT_GROUND, bg=BACK_GROUND,
                                      font=(FONT, 20))
            w_edit_mean_label.grid(column=0, row=3, pady=2)

            w_edit_exit_button = Button(w_edit_window, text="Pencereyi Kapat", fg=FONT_GROUND, bg=BACK_GROUND,
                                        activebackground=BACK_GROUND, activeforeground=FONT_GROUND, width=25,
                                        font=(FONT, 17), command=lambda: (w_edit_window.destroy()))
            w_edit_exit_button.grid(column=0, row=4, pady=2, columnspan=2, sticky=W)

            w_edit_row = Entry(w_edit_window, width=30, font=(FONT, 20), fg=FONT_GROUND, bg=BACK_GROUND)
            w_edit_row.grid(column=1, row=1)
            w_edit_row.focus_set()

            w_edit_word = Entry(w_edit_window, width=30, font=(FONT, 20), fg=FONT_GROUND, bg=BACK_GROUND)
            w_edit_word.grid(column=1, row=2)

            w_edit_mean = Entry(w_edit_window, width=30, font=(FONT, 20), fg=FONT_GROUND, bg=BACK_GROUND)
            w_edit_mean.grid(column=1, row=3)

            def w_clean_input(input_str):
                stripped_str = input_str.strip()
                cleaned_str = ' '.join(stripped_str.split())
                return cleaned_str

            # Kelime Düzenlemelerinin Alındığı ve Kayıt Fonksiyonunun Çağırıldığı Fonksiyon
            def save_changes():
                try:
                    row_num = int(w_edit_row.get())
                    new_word = w_clean_input(w_edit_word.get().lower())
                    new_mean = w_clean_input(turkish_lower(w_edit_mean.get()))

                    if not row_num or not new_word or not new_mean:
                        messagebox.showwarning("Uyarı!", "Girişlerden biri veya birkaçı boş!!!")
                        return

                    with open("word_repository.csv", 'r', newline='', encoding='utf-8') as file:
                        data = list(csv.reader(file))

                    if row_num > len(data):
                        raise ValueError("Girdiğiniz satır numarası geçerli değil!")

                    update_csv(row_num, new_word, new_mean)
                    messagebox.showinfo("Bilgi", "Kayıt başarıyla güncellendi!")

                    w_edit_window.destroy(), w_show_title_label.destroy(), w_look_scroll.destroy()
                    w_look_canvas.destroy(), w_show_label.destroy(), w_edit_button.destroy(), w_remove_button.destroy()
                    return_button.destroy(), look_word()

                except ValueError as ve:
                    messagebox.showwarning("Hata!", "Geçersiz bir sıra numarası girdiniz!")
                except Exception as e:
                    messagebox.showwarning("Bilinmeyen Hata!", "Geçersiz bir sıra numarası girdiniz!")

            def on_return(event):
                save_changes()
            w_edit_window.bind("<Return>", on_return)

            w_save_button = Button(w_edit_window, text="Kaydet", fg=FONT_GROUND, bg=BACK_GROUND, width=25,
                                   activebackground=BACK_GROUND, activeforeground=FONT_GROUND,
                                   font=(FONT, 17), command=save_changes)
            w_save_button.grid(column=0, row=4, pady=2, columnspan=2, sticky=E)

        # Kelimeleri Kaldırma Sayfası
        def remove_word():
            w_remove_window = Toplevel()
            w_remove_window.title("Kelime Kaldırma Penceresi")
            w_remove_window.config(padx=30, pady=30, bg=BACK_GROUND)
            w_remove_window.resizable(False, False)

            w_remove_title = Label(w_remove_window, text="Kaldırma Penceresi", fg=FONT_GROUND,
                                   bg=BACK_GROUND, font=(FONT, 30, "bold"))
            w_remove_title.grid(column=0, row=0, columnspan=2, pady=5)

            w_remove_label = Label(w_remove_window, text="Kelimenin Sırası:", fg=FONT_GROUND,
                                   bg=BACK_GROUND, font=(FONT, 20))
            w_remove_label.grid(column=0, row=1, pady=2)

            w_remove_row = Entry(w_remove_window, width=10, font=(FONT, 20), fg=FONT_GROUND, bg=BACK_GROUND)
            w_remove_row.grid(column=1, row=1, sticky=W)
            w_remove_row.focus_set()

            def w_remove_entry():
                try:
                    row_num = int(w_remove_row.get())

                    data = pd.read_csv("word_repository.csv", encoding='utf-8')
                    data_list = data["Word"].to_list()
                    sorted_data = data.sort_values(by='Word')
                    sorted_list = sorted_data["Word"].to_list()
                    sorted_word = sorted_list[row_num-1]
                    row_index = data_list.index(sorted_word)

                    if row_num > len(data) or row_num <= 0:
                        raise ValueError("Invalid row number.")

                    data.drop(index=row_index, inplace=True)
                    data.reset_index(drop=True, inplace=True)
                    data.to_csv("word_repository.csv", index=False, encoding='utf-8')
                    messagebox.showinfo("Bilgi", "Kelime başarıyla kaldırıldı!")

                    w_remove_window.destroy(), w_show_title_label.destroy(), w_look_scroll.destroy()
                    w_look_canvas.destroy(), w_show_label.destroy(), w_edit_button.destroy(), w_remove_button.destroy()
                    return_button.destroy(), look_word()

                except ValueError:
                    messagebox.showwarning("Uyarı!", "Geçersiz bir sıra numarası girdiniz!")
                except Exception as e:
                    messagebox.showwarning("Hata!", "Bir hata meydana geldi!")

            def on_return(event):
                w_remove_entry()
            w_remove_window.bind("<Return>", on_return)

            w_remove_in_button = Button(w_remove_window, text="Kaldır", fg=FONT_GROUND, bg=BACK_GROUND, width=10,
                                        font=(FONT, 17), command=w_remove_entry)
            w_remove_in_button.grid(column=1, row=2, pady=2)

            w_remove_exit_button = Button(w_remove_window, text="Pencereyi Kapat", fg=FONT_GROUND, bg=BACK_GROUND,
                                          activebackground=BACK_GROUND, activeforeground=FONT_GROUND, width=15,
                                          font=(FONT, 17), command=lambda: (w_remove_window.destroy()))
            w_remove_exit_button.grid(column=0, row=2, pady=2)

        # Kelimeleri Görüntüleme Fonksiyonunun Devamı
        w_show_title_label = Label(text="Kelimeleriniz", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 30, "bold"))
        w_show_title_label.grid(column=0, row=0, columnspan=2)

        w_look_scroll = Scrollbar(orient="vertical", troughcolor=BACK_GROUND, bg=FONT_GROUND)
        w_look_scroll.grid(column=2, row=1, sticky="ns")

        w_look_canvas = Canvas(yscrollcommand=w_look_scroll.set, bg=BACK_GROUND, width=500, highlightthickness=0)
        w_look_canvas.grid(column=0, row=1, columnspan=2)
        w_look_scroll.config(command=w_look_canvas.yview)

        w_show_label = Label(w_look_canvas, text="", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 20),
                             anchor="w", justify="left")
        w_look_canvas.create_window((0, 0), window=w_show_label, anchor="nw")

        all_rows_text = ""

        def w_on_mousewheel(event):
            w_look_canvas.yview_scroll(-1 * (event.delta // 120), "units")

        w_look_canvas.bind_all("<MouseWheel>", w_on_mousewheel)

        # Kelimeleri Görüntüleme Fonksiyonunun Dosyaları Okuduğu Kısmı
        with open("word_repository.csv", 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            sort_list = sorted(reader)
            i = 0
            for row in sort_list:
                i += 1
                english_word = row[0].capitalize()
                turkish_word = turkish_capitalize(row[1])
                all_rows_text += f"{i}. {english_word} = {turkish_word}\n"

        w_show_label.config(text=all_rows_text)

        w_show_label.update_idletasks()
        w_look_canvas.config(scrollregion=w_look_canvas.bbox("all"))

        w_edit_button = Button(text="Kelime Düzenle", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 17), width=19,
                               activebackground=BACK_GROUND, activeforeground=FONT_GROUND, command=edit_word)
        w_edit_button.grid(column=0, row=3, pady=2, padx=2)

        w_remove_button = Button(text="Kelime Kaldır", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 17), width=19,
                                 activebackground=BACK_GROUND, activeforeground=FONT_GROUND, command=remove_word)
        w_remove_button.grid(column=1, row=3, pady=2, padx=2)

        return_button = Button(text=RETURN_BUTTON, fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 17), width=19,
                               activebackground=BACK_GROUND, activeforeground=FONT_GROUND,
                               command=lambda: (repo_page(), w_show_title_label.destroy(), w_look_canvas.destroy(),
                                                w_show_label.destroy(), w_look_scroll.destroy(),
                                                w_edit_button.destroy(), w_remove_button.destroy(),
                                                return_button.destroy()))
        return_button.grid(column=0, row=4, pady=2, columnspan=2)

    # Kalıp Cümleleri Görüntüleme Fonksiyonu
    def look_mould():
        repo_title_label.destroy(), repo_top_label.destroy(), repo_mid_label.destroy(), word_add_button.destroy()
        mould_add_button.destroy(), look_word_button.destroy(), look_mould_button.destroy()

        # Kalıp Cümle Düzenlemelerinin Dosyaya Kaydedildiği Fonksiyon
        def update_csv(row_num, new_word, new_mean):
            with open("mould_repository.csv", 'r', newline='', encoding='utf-8') as file:
                data = list(csv.reader(file))
                sorted_data = sorted(data)

            sorted_data[row_num] = [new_word, new_mean]

            with open("mould_repository.csv", 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(sorted_data)

        # Kalıp Cümleleri Düzenleme Penceresi
        def edit_mould():
            m_edit_window = Toplevel()
            m_edit_window.title("Kalıp Cümle Düzenleme Penceresi")
            m_edit_window.config(padx=30, pady=30, bg=BACK_GROUND)
            m_edit_window.resizable(False, False)

            m_edit_title_label = Label(m_edit_window, text="Düzenleme Penceresi", fg=FONT_GROUND, bg=BACK_GROUND,
                                       font=(FONT, 30, "bold"))
            m_edit_title_label.grid(column=0, row=0, columnspan=2, pady=5)

            m_edit_row_label = Label(m_edit_window, text="Cümlenin Sırası:", fg=FONT_GROUND, bg=BACK_GROUND,
                                     font=(FONT, 20))
            m_edit_row_label.grid(column=0, row=1, pady=2)

            m_edit_word_label = Label(m_edit_window, text="Düzenlenmiş Cümle:", fg=FONT_GROUND, bg=BACK_GROUND,
                                      font=(FONT, 20))
            m_edit_word_label.grid(column=0, row=2, pady=2)

            m_edit_mean_label = Label(m_edit_window, text="Düzenlenmiş Anlam:", fg=FONT_GROUND, bg=BACK_GROUND,
                                      font=(FONT, 20))
            m_edit_mean_label.grid(column=0, row=3, pady=2)

            m_edit_exit_button = Button(m_edit_window, text="Pencereyi Kapat", fg=FONT_GROUND, bg=BACK_GROUND,
                                        activebackground=BACK_GROUND, activeforeground=FONT_GROUND, width=25,
                                        font=(FONT, 17), command=lambda: (m_edit_window.destroy()))
            m_edit_exit_button.grid(column=0, row=4, pady=2, columnspan=2, sticky=W)

            m_edit_row = Entry(m_edit_window, width=30, font=(FONT, 20), fg=FONT_GROUND, bg=BACK_GROUND)
            m_edit_row.grid(column=1, row=1)
            m_edit_row.focus_set()

            m_edit_word = Entry(m_edit_window, width=30, font=(FONT, 20), fg=FONT_GROUND, bg=BACK_GROUND)
            m_edit_word.grid(column=1, row=2)

            m_edit_mean = Entry(m_edit_window, width=30, font=(FONT, 20), fg=FONT_GROUND, bg=BACK_GROUND)
            m_edit_mean.grid(column=1, row=3)

            def m_clean_input(input_str):
                stripped_str = input_str.strip()
                cleaned_str = ' '.join(stripped_str.split())
                return cleaned_str

            # Kalıp Cümle Düzenlemelerinin Alındığı ve Kayıt Fonksiyonunun Çağırıldığı Fonksiyon
            def save_changes():
                try:
                    row_num = int(m_edit_row.get())
                    new_word = m_clean_input(m_edit_word.get().lower())
                    new_mean = m_clean_input(turkish_lower(m_edit_mean.get()))

                    if not row_num or not new_word or not new_mean:
                        messagebox.showwarning("Uyarı!", "Girişlerden biri veya birkaçı boş!!!")
                        return

                    with open("mould_repository.csv", 'r', newline='', encoding='utf-8') as file:
                        data = list(csv.reader(file))

                    if row_num > len(data):
                        raise ValueError("Girdiğiniz satır numarası geçerli değil!")

                    update_csv(row_num, new_word, new_mean)
                    messagebox.showinfo("Bilgi", "Kayıt başarıyla güncellendi!")

                    m_edit_window.destroy(), m_show_title_label.destroy(), m_look_scroll.destroy()
                    m_look_canvas.destroy(), m_show_label.destroy(), m_edit_button.destroy(), m_remove_button.destroy()
                    return_button.destroy(), look_mould()

                except ValueError as ve:
                    messagebox.showwarning("Hata!", "Geçersiz bir sıra numarası girdiniz!")
                except Exception as e:
                    messagebox.showwarning("Bilinmeyen Hata!", "Geçersiz bir sıra numarası girdiniz!")

            def on_return(event):
                save_changes()
            m_edit_window.bind("<Return>", on_return)

            m_save_button = Button(m_edit_window, text="Kaydet", fg=FONT_GROUND, bg=BACK_GROUND, width=25,
                                   activebackground=BACK_GROUND, activeforeground=FONT_GROUND,
                                   font=(FONT, 17), command=save_changes)
            m_save_button.grid(column=0, row=4, pady=2, columnspan=2, sticky=E)

        # Kalıp Cümleleri Kaldırma Sayfası
        def remove_mould():
            m_remove_window = Toplevel()
            m_remove_window.title("Kalıp Cümle Kaldırma Penceresi")
            m_remove_window.config(padx=30, pady=30, bg=BACK_GROUND)
            m_remove_window.resizable(False, False)

            m_remove_title = Label(m_remove_window, text="Kaldırma Penceresi", fg=FONT_GROUND,
                                   bg=BACK_GROUND, font=(FONT, 30, "bold"))
            m_remove_title.grid(column=0, row=0, columnspan=2, pady=5)

            m_remove_label = Label(m_remove_window, text="Cümlenin Sırası:", fg=FONT_GROUND,
                                   bg=BACK_GROUND, font=(FONT, 20))
            m_remove_label.grid(column=0, row=1, pady=2)

            m_remove_row = Entry(m_remove_window, width=10, font=(FONT, 20), fg=FONT_GROUND, bg=BACK_GROUND)
            m_remove_row.grid(column=1, row=1, sticky=W)
            m_remove_row.focus_set()

            def m_remove_entry():
                try:
                    row_num = int(m_remove_row.get())

                    data = pd.read_csv("mould_repository.csv", encoding='utf-8')
                    data_list = data["Mould"].to_list()
                    sorted_data = data.sort_values(by='Mould')
                    sorted_list = sorted_data["Mould"].to_list()
                    sorted_mould = sorted_list[row_num-1]
                    row_index = data_list.index(sorted_mould)

                    if row_num > len(data) or row_num <= 0:
                        raise ValueError("Invalid row number.")

                    data.drop(index=row_index, inplace=True)
                    data.reset_index(drop=True, inplace=True)
                    data.to_csv("mould_repository.csv", index=False, encoding='utf-8')
                    messagebox.showinfo("Bilgi", "Kelime başarıyla kaldırıldı!")

                    m_remove_window.destroy(), m_show_title_label.destroy(), m_look_scroll.destroy()
                    m_look_canvas.destroy(), m_show_label.destroy(), m_edit_button.destroy(), m_remove_button.destroy()
                    return_button.destroy(), look_mould()

                except ValueError:
                    messagebox.showwarning("Uyarı!", "Geçersiz bir sıra numarası girdiniz!")
                except Exception as e:
                    messagebox.showwarning("Hata!", "Bir hata meydana geldi!")

            def on_return(event):
                m_remove_entry()
            m_remove_window.bind("<Return>", on_return)

            m_remove_in_button = Button(m_remove_window, text="Kaldır", fg=FONT_GROUND, bg=BACK_GROUND, width=10,
                                        font=(FONT, 17), command=m_remove_entry)
            m_remove_in_button.grid(column=1, row=2, pady=2)

            m_remove_exit_button = Button(m_remove_window, text="Pencereyi Kapat", fg=FONT_GROUND, bg=BACK_GROUND,
                                          activebackground=BACK_GROUND, activeforeground=FONT_GROUND, width=15,
                                          font=(FONT, 17), command=lambda: (m_remove_window.destroy()))
            m_remove_exit_button.grid(column=0, row=2, pady=2)

        # Kalıp Cümleleri Görüntüleme Fonksiyonunun Devamı
        m_show_title_label = Label(text="Kalıp Cümleleriniz", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 30, "bold"))
        m_show_title_label.grid(column=0, row=0, columnspan=2)

        m_look_scroll = Scrollbar(orient="vertical")
        m_look_scroll.grid(column=2, row=1, sticky="ns")

        m_look_canvas = Canvas(yscrollcommand=m_look_scroll.set, bg=BACK_GROUND, width=500, highlightthickness=0)
        m_look_canvas.grid(column=0, row=1, columnspan=2)
        m_look_scroll.config(command=m_look_canvas.yview)

        m_show_label = Label(m_look_canvas, text="", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 20),
                             anchor="w", justify="left")
        m_look_canvas.create_window((0, 0), window=m_show_label, anchor="nw")

        all_rows_text = ""

        def m_on_mousewheel(event):
            m_look_canvas.yview_scroll(-1 * (event.delta // 120), "units")

        m_look_canvas.bind_all("<MouseWheel>", m_on_mousewheel)

        # Kalıp Cümleleri Görüntüleme Fonksiyonunun Dosyaları Okuduğu Kısmı
        with open("mould_repository.csv", 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            sort_list = sorted(reader)
            i = 0
            for row in sort_list:
                i += 1
                english_word = row[0].capitalize()
                turkish_word = turkish_capitalize(row[1])
                all_rows_text += f"{i}. {english_word} = {turkish_word}\n"

        m_show_label.config(text=all_rows_text)

        m_show_label.update_idletasks()
        m_look_canvas.config(scrollregion=m_look_canvas.bbox("all"))

        m_edit_button = Button(text="Kalıp Cümle Düzenle", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 17), width=19,
                               activebackground=BACK_GROUND, activeforeground=FONT_GROUND, command=edit_mould)
        m_edit_button.grid(column=0, row=3, pady=2, padx=2)

        m_remove_button = Button(text="Kalıp Cümle Kaldır", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 17), width=19,
                                 activebackground=BACK_GROUND, activeforeground=FONT_GROUND, command=remove_mould)
        m_remove_button.grid(column=1, row=3, pady=2, padx=2)

        return_button = Button(text=RETURN_BUTTON, fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 17), width=19,
                               activebackground=BACK_GROUND, activeforeground=FONT_GROUND,
                               command=lambda: (repo_page(), m_show_title_label.destroy(), m_look_canvas.destroy(),
                                                m_show_label.destroy(), m_look_scroll.destroy(),
                                                m_edit_button.destroy(), m_remove_button.destroy(),
                                                return_button.destroy()))
        return_button.grid(column=0, row=4, pady=2, columnspan=2)

    # Repository Sayfası Fonksiyonunun Devamı
    repo_title_label = Label(text="Uygulama Deposu", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 30, "bold"))
    repo_title_label.grid(column=0, row=0, columnspan=2, pady=10)

    repo_top_label = Label(text="İçerik Ekleme;", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 25))
    repo_top_label.grid(column=0, row=1, columnspan=2, pady=10)

    word_add_button = Button(text="Kelime Ekle", fg=FONT_GROUND, bg=BACK_GROUND,
                             activebackground=BACK_GROUND, activeforeground=FONT_GROUND,
                             font=(FONT, 17), width=30, command=lambda: (add_word(), return_button.destroy()))
    word_add_button.grid(column=0, row=2, pady=2)

    mould_add_button = Button(text="Kalıp Cümle Ekle", fg=FONT_GROUND, bg=BACK_GROUND,
                              activebackground=BACK_GROUND, activeforeground=FONT_GROUND,
                              font=(FONT, 17), width=30, command=lambda: (add_mould(), return_button.destroy()))
    mould_add_button.grid(column=0, row=3, pady=2)

    repo_mid_label = Label(text="İçerik Kontrolü;", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 25))
    repo_mid_label.grid(column=0, row=4, columnspan=2, pady=10)

    look_word_button = Button(text="Kelimeleriniz", fg=FONT_GROUND, bg=BACK_GROUND,
                              activebackground=BACK_GROUND, activeforeground=FONT_GROUND,
                              font=(FONT, 17), width=30, command=lambda: (look_word(), return_button.destroy()))
    look_word_button.grid(column=0, row=5, pady=2)

    look_mould_button = Button(text="Kalıp Cümleleriniz", fg=FONT_GROUND, bg=BACK_GROUND,
                               activebackground=BACK_GROUND, activeforeground=FONT_GROUND,
                               font=(FONT, 17), width=30, command=lambda: (look_mould(), return_button.destroy()))
    look_mould_button.grid(column=0, row=6, pady=2)

    return_button = Button(text=RETURN_BUTTON, fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 17), width=30,
                           activebackground=BACK_GROUND, activeforeground=FONT_GROUND,
                           command=lambda: (home_page(), repo_title_label.destroy(), word_add_button.destroy(),
                                            look_word_button.destroy(), mould_add_button.destroy(),
                                            look_mould_button.destroy(), repo_mid_label.destroy(),
                                            repo_top_label.destroy(), return_button.destroy()))
    return_button.grid(column=0, row=7, pady=2)

# <----------------------------------------------> Settings Page <---------------------------------------------------->
# Ayarlar Sayfası Fonksiyonu
def settings_page():
    home_logo_label.destroy(), home_canvas.destroy(), mods_page_button.destroy(), repo_page_button.destroy()
    settings_page_button.destroy(), app_about_button.destroy(), exit_button.destroy()

    def save_settings():
        try:
            data = pd.DataFrame({
                'FONT_GROUND': [FONT_GROUND],
                'BACK_GROUND': [BACK_GROUND],
                'FONT': [FONT]
            })
            data.to_csv("app_parameters.csv", index=False, encoding='utf-8')
        except Exception as e:
            print(f"An error occurred: {e}")

    # Yazıtipini Değiştirdiğimiz Fonksiyon
    def font_select(value):
        global FONT
        if value == "Helvetica":
            FONT = "Helvetica"
        elif value == "Times New Roman":
            FONT = "Times New Roman"
        elif value == "Comic Sans MS":
            FONT = "Comic Sans MS"
        elif value == "Verdana":
            FONT = "Verdana"
        elif value == "Courier":
            FONT = "Courier"
        elif value == "Georgia":
            FONT = "Georgia"
        elif value == "Trebuchet MS":
            FONT = "Trebuchet MS"
        elif value == "Lucida Sans":
            FONT = "Lucida Sans"
        elif value == "Palatino":
            FONT = "Palatino"
        elif value == "Garamond":
            FONT = "Garamond"
        elif value == "Tahoma":
            FONT = "Tahoma"
        save_settings()

    font_options = ["Seçiminiz", "Helvetica", "Times New Roman", "Comic Sans MS", "Verdana", "Courier",
                    "Georgia", "Trebuchet MS", "Lucida Sans", "Palatino", "Garamond", "Tahoma"]
    select_font_option = StringVar(window)
    select_font_option.set(font_options[0])

    font_select_menu = OptionMenu(window, select_font_option, *font_options, command=font_select)
    font_select_menu.config(fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 17), width=15, highlightthickness=0,
                            activebackground=BACK_GROUND, activeforeground=FONT_GROUND)
    font_select_menu["menu"].config(fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 15))
    font_select_menu.grid(column=1, row=1)

    # Yazıtipi Rengini Değiştirdiğimiz Fonksiyon
    def font_ground_select(value):
        global FONT_GROUND
        if value == "Siyah":
            FONT_GROUND = "black"
        elif value == "Beyaz":
            FONT_GROUND = "white"
        elif value == "Kırmızı":
            FONT_GROUND = "#FF1E1E"
        elif value == "Turuncu":
            FONT_GROUND = "#FF6D28"
        elif value == "Kahverengi":
            FONT_GROUND = "#9E6F21"
        elif value == "Açık Kahverengi":
            FONT_GROUND = "#A47E3B"
        elif value == "Sarı":
            FONT_GROUND = "#FFED00"
        elif value == "Yeşil":
            FONT_GROUND = "#16FF00"
        elif value == "Turkuaz":
            FONT_GROUND = "#00F5FF"
        elif value == "Mavi":
            FONT_GROUND = "#0028FF"
        elif value == "Mor":
            FONT_GROUND = "purple"
        elif value == "Pembe":
            FONT_GROUND = "pink"
        save_settings()

    font_ground_options = ["Seçiminiz", "Siyah", "Beyaz", "Kırmızı", "Turuncu", "Kahverengi", "Açık Kahverengi", "Sarı",
                           "Yeşil", "Turkuaz", "Mavi", "Mor", "Pembe"]
    select_font_ground_option = StringVar(window)
    select_font_ground_option.set(font_ground_options[0])

    font_ground_select_menu = OptionMenu(window, select_font_ground_option, *font_ground_options,
                                         command=font_ground_select)
    font_ground_select_menu.config(fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 17), width=15, highlightthickness=0,
                                   activebackground=BACK_GROUND, activeforeground=FONT_GROUND)
    font_ground_select_menu["menu"].config(fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 15))
    font_ground_select_menu.grid(column=1, row=2)

    # Arkaplan Rengini Değiştirdiğimiz Fonksiyon
    def back_ground_select(value):
        global BACK_GROUND
        if value == "Siyah":
            BACK_GROUND = "black"
        elif value == "Gri":
            BACK_GROUND = "#61677A"
        elif value == "Beyaz":
            BACK_GROUND = "white"
        elif value == "Kırmızı":
            BACK_GROUND = "#ED2B2A"
        elif value == "Su Kırmızısı":
            BACK_GROUND = "#EB4747"
        elif value == "Turuncu":
            BACK_GROUND = "#FF6000"
        elif value == "Sarı":
            BACK_GROUND = "#FFEC85"
        elif value == "Fildişi":
            BACK_GROUND = "#FBF0B2"
        elif value == "Yeşil":
            BACK_GROUND = "#379237"
        elif value == "Su Yeşili":
            BACK_GROUND = "#ACFADF"
        elif value == "Turkuaz":
            BACK_GROUND = "#40F8FF"
        elif value == "Mavi":
            BACK_GROUND = "#068FFF"
        elif value == "Gece Mavisi":
            BACK_GROUND = "#7091F5"
        elif value == "Mor":
            BACK_GROUND = "#D67BFF"
        elif value == "Pembe":
            BACK_GROUND = "#FF8FE5"
        window.configure(bg=BACK_GROUND)
        save_settings()

    back_ground_options = ["Seçiminiz", "Siyah", "Gri", "Beyaz", "Kırmızı", "Su Kırmızısı", "Turuncu", "Sarı",
                           "Fildişi", "Yeşil", "Su Yeşili", "Turkuaz", "Mavi", "Gece Mavisi", "Mor", "Pembe"]
    select_back_ground_option = StringVar(window)
    select_back_ground_option.set(back_ground_options[0])

    back_ground_select_menu = OptionMenu(window, select_back_ground_option, *back_ground_options,
                                         command=back_ground_select)
    back_ground_select_menu.config(fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 17), width=15, highlightthickness=0,
                                   activebackground=BACK_GROUND, activeforeground=FONT_GROUND)
    back_ground_select_menu["menu"].config(fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 15))
    back_ground_select_menu.grid(column=1, row=3)

    # Ayarlar Sayfası Fonksiyonunun Devamı
    settings_page_label = Label(text="Ayarlar", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 30, "bold"))
    settings_page_label.grid(column=0, row=0, columnspan=2, pady=10)

    font_ground_select_label = Label(text="Yazıtipi Rengi:", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 20))
    font_ground_select_label.grid(column=0, row=2, pady=2)

    back_ground_select_label = Label(text="Arka Plan Rengi:", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 20))
    back_ground_select_label.grid(column=0, row=3, pady=2)

    font_select_label = Label(text="Yazıtipi:", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 20))
    font_select_label.grid(column=0, row=1, pady=2)

    return_button = Button(text=RETURN_BUTTON, fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 17), width=16,
                           activebackground=BACK_GROUND, activeforeground=FONT_GROUND,
                           command=lambda: (home_page(), font_ground_select_menu.destroy(), font_select_label.destroy(),
                                            back_ground_select_menu.destroy(), font_ground_select_label.destroy(),
                                            back_ground_select_label.destroy(), font_select_menu.destroy(),
                                            settings_page_label.destroy(), return_button.destroy()))
    return_button.grid(column=0, row=4, pady=2, columnspan=2)

# <-----------------------------------------------> About Page <------------------------------------------------------>
# Hakkında Sayfası Fonksiyonu
def about_page():
    home_logo_label.destroy(), home_canvas.destroy(), mods_page_button.destroy(), repo_page_button.destroy()
    settings_page_button.destroy(), app_about_button.destroy(), exit_button.destroy()

    # Bize Dair Açıklamanın bulunduğu Paragraf Bölümü Fonksiyonu
    def about_us():
        about_us_page.destroy(), about_app_page.destroy(), about_page_title_label.destroy()
        social_profiles_label.destroy(), social_profiles1_button1.destroy(), social_profiles1_button2.destroy()
        social_profiles2_button1.destroy(), social_profiles2_button2.destroy(), sk_social_profiles_label.destroy()
        kse_social_profiles_label.destroy(), send_email_label.destroy(), email_send_button_sk.destroy()
        email_send_button_kse.destroy()

        about_us_page_top_label = Label(text="Bize Dair", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 30, "bold"))
        about_us_page_top_label.grid(column=0, row=0, columnspan=2, pady=10)

        about_us_scroll = Scrollbar(orient="vertical")
        about_us_scroll.grid(column=2, row=1, sticky="ns")

        about_us_canvas = Canvas(yscrollcommand=about_us_scroll.set, bg=BACK_GROUND, width=523, highlightthickness=0)
        about_us_canvas.grid(column=0, row=1, columnspan=2)
        about_us_scroll.config(command=about_us_canvas.yview)

        about_us_label = Label(about_us_canvas, text="", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 20),
                               anchor="w", justify="left", wraplength=523)
        about_us_canvas.create_window((0, 0), window=about_us_label, anchor="nw")

        with open("us_about.txt", 'r', encoding='utf-8') as file:
            about_text = file.read()

        about_us_label.config(text=about_text)

        about_us_label.update_idletasks()
        about_us_canvas.config(scrollregion=about_us_canvas.bbox("all"))

        def about_us_on_mousewheel(event):
            about_us_canvas.yview_scroll(-1 * (event.delta // 120), "units")

        about_us_canvas.bind_all("<MouseWheel>", about_us_on_mousewheel)

        return_button = Button(text=RETURN_BUTTON, fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 17), width=10,
                               activebackground=BACK_GROUND, activeforeground=FONT_GROUND,
                               command=lambda: (about_page(), about_us_page_top_label.destroy(),
                                                about_us_scroll.destroy(), about_us_canvas.destroy(),
                                                about_us_label.destroy(), return_button.destroy()))
        return_button.grid(column=0, columnspan=2, row=2, pady=10)

    # Uygulamaya Dair Açıklamanın bulunduğu Paragraf Bölümü Fonksiyonu
    def about_app():
        about_us_page.destroy(), about_app_page.destroy(), about_page_title_label.destroy()
        social_profiles_label.destroy(), social_profiles1_button1.destroy(), social_profiles1_button2.destroy()
        social_profiles2_button1.destroy(), social_profiles2_button2.destroy(), sk_social_profiles_label.destroy()
        kse_social_profiles_label.destroy(), send_email_label.destroy(), email_send_button_sk.destroy()
        email_send_button_kse.destroy()

        about_app_page_top_label = Label(text="Uygulamaya Dair", fg=FONT_GROUND, bg=BACK_GROUND,
                                         font=(FONT, 30, "bold"))
        about_app_page_top_label.grid(column=0, row=0, columnspan=2, pady=10)

        about_app_scroll = Scrollbar(orient="vertical")
        about_app_scroll.grid(column=2, row=1, sticky="ns")

        about_app_canvas = Canvas(yscrollcommand=about_app_scroll.set, bg=BACK_GROUND, width=523, highlightthickness=0)
        about_app_canvas.grid(column=0, row=1, columnspan=2)
        about_app_scroll.config(command=about_app_canvas.yview)

        about_app_label = Label(about_app_canvas, text="", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 20),
                                anchor="w", justify="left", wraplength=523)
        about_app_canvas.create_window((0, 0), window=about_app_label, anchor="nw")

        with open("app_about.txt", 'r', encoding='utf-8') as file:
            about_text = file.read()

        about_app_label.config(text=about_text)

        about_app_label.update_idletasks()
        about_app_canvas.config(scrollregion=about_app_canvas.bbox("all"))

        def about_app_on_mousewheel(event):
            about_app_canvas.yview_scroll(-1 * (event.delta // 120), "units")

        about_app_canvas.bind_all("<MouseWheel>", about_app_on_mousewheel)

        return_button = Button(text=RETURN_BUTTON, fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 17), width=10,
                               activebackground=BACK_GROUND, activeforeground=FONT_GROUND,
                               command=lambda: (about_page(), about_app_page_top_label.destroy(),
                                                about_app_scroll.destroy(), about_app_canvas.destroy(),
                                                about_app_label.destroy(), return_button.destroy()))
        return_button.grid(column=0, columnspan=2, row=2, pady=10)

    # Hakkında Sayfası Fonksiyonunun Devamı Part I
    about_page_title_label = Label(text="Bize & Uygulamaya Dair", fg=FONT_GROUND, bg=BACK_GROUND,
                                   font=(FONT, 30, "bold"))
    about_page_title_label.grid(column=0, row=0, columnspan=2, pady=10)

    about_us_page = Button(text="Bize Dair", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 17),
                           width=20, activebackground=BACK_GROUND, activeforeground=FONT_GROUND,
                           command=lambda: (about_us(), return_button.destroy()))
    about_us_page.grid(column=0, row=1, padx=2)

    about_app_page = Button(text="Uygulamaya Dair", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 17),
                            width=20, activebackground=BACK_GROUND, activeforeground=FONT_GROUND,
                            command=lambda: (about_app(), return_button.destroy()))
    about_app_page.grid(column=1, row=1, padx=2)

    social_profiles_label = Label(text="Sosyal Medyalarımız", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 30, "bold"))
    social_profiles_label.grid(column=0, row=2, columnspan=2, pady=10)

    sk_social_profiles_label = Label(text="Sait Kaplan", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 20))
    sk_social_profiles_label.grid(column=0, row=3)

    kse_social_profiles_label = Label(text="Kemal Sait Eser", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 20))
    kse_social_profiles_label.grid(column=1, row=3)

    def open_click(url):
        webbrowser.open(url)

    social_profiles1_button1 = Button(text="LinkedIn", fg=FONT_GROUND, bg=BACK_GROUND,
                                      font=(FONT, 17), width=20, activebackground=BACK_GROUND,
                                      activeforeground=FONT_GROUND,
                                      command=lambda: open_click("https://www.linkedin.com/in/sait-kaplan/"))
    social_profiles1_button1.grid(column=0, row=4, padx=2, pady=2)

    social_profiles2_button1 = Button(text="LinkedIn", fg=FONT_GROUND, bg=BACK_GROUND,
                                      font=(FONT, 17), width=20, activebackground=BACK_GROUND,
                                      activeforeground=FONT_GROUND,
                                      command=lambda: open_click("https://www.linkedin.com/in/kemal-said-eser/"))
    social_profiles2_button1.grid(column=1, row=4, padx=2, pady=2)

    social_profiles1_button2 = Button(text="GitHub", fg=FONT_GROUND, bg=BACK_GROUND,
                                      font=(FONT, 17), width=20, activebackground=BACK_GROUND,
                                      activeforeground=FONT_GROUND,
                                      command=lambda: open_click("https://github.com/realneawe"))
    social_profiles1_button2.grid(column=0, row=5, padx=2, pady=2)

    social_profiles2_button2 = Button(text="GitHub", fg=FONT_GROUND, bg=BACK_GROUND,
                                      font=(FONT, 17), width=20, activebackground=BACK_GROUND,
                                      activeforeground=FONT_GROUND,
                                      command=lambda: open_click("https://github.com/esercibiri"))
    social_profiles2_button2.grid(column=1, row=5, padx=2, pady=2)

    send_email_label = Label(text="Bize e-Posta Yaz", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 30, "bold"))
    send_email_label.grid(column=0, row=6, columnspan=2, pady=10)

    # e-Posta Gönderme Fonksiyonu Sait Kaplan
    def ask_send_email_sk():
        email_address = "kaplan.sait40@gmail.com"

        def open_provider(provider):
            if provider == "gmail":
                webbrowser.open("https://mail.google.com/mail/u/0/#inbox?compose=new")
            elif provider == "hotmail":
                webbrowser.open("https://outlook.live.com/mail/0/deeplink/compose")
            elif provider == "yandex":
                webbrowser.open("https://mail.yandex.com/?addMultiUserFromDropdown=false")
            elif provider == "yahoo":
                webbrowser.open("https://mail.yahoo.com/")
            elif provider == "yaani":
                webbrowser.open("https://mail.yaani.com/")

        pyperclip.copy(email_address)
        messagebox.showinfo("Bilgi", "E-posta adresi kopyalandı!")

        sk_send_email_window = Toplevel()
        sk_send_email_window.title("E-posta Gönderme Penceresi")
        sk_send_email_window.config(padx=30, pady=30, bg=BACK_GROUND)
        sk_send_email_window.resizable(False, False)

        ask_label = Label(sk_send_email_window, text="E-postayı hangi sağlayıcı üzerinden\n göndermek istiyorsunuz?",
                          fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 20))
        ask_label.grid(column=0, row=0, pady=20)

        gmail_button = Button(sk_send_email_window, text="Gmail ile Gönder", fg=FONT_GROUND, bg=BACK_GROUND,  width=20,
                              font=(FONT, 17), activebackground=BACK_GROUND, activeforeground=FONT_GROUND,
                              command=lambda: open_provider("gmail"))
        gmail_button.grid(column=0, row=1, pady=2)

        hotmail_button = Button(sk_send_email_window, text="Hotmail ile Gönder", fg=FONT_GROUND, bg=BACK_GROUND,
                                width=20, font=(FONT, 17), activebackground=BACK_GROUND, activeforeground=FONT_GROUND,
                                command=lambda: open_provider("hotmail"))
        hotmail_button.grid(column=0, row=2, pady=2)

        yandex_button = Button(sk_send_email_window, text="Yandex ile Gönder", fg=FONT_GROUND, bg=BACK_GROUND,
                               width=20, font=(FONT, 17), activebackground=BACK_GROUND, activeforeground=FONT_GROUND,
                               command=lambda: open_provider("yandex"))
        yandex_button.grid(column=0, row=3, pady=2)

        yahoo_button = Button(sk_send_email_window, text="Yahoo ile Gönder", fg=FONT_GROUND, bg=BACK_GROUND,  width=20,
                              font=(FONT, 17), activebackground=BACK_GROUND, activeforeground=FONT_GROUND,
                              command=lambda: open_provider("yahoo"))
        yahoo_button.grid(column=0, row=4, pady=2)

        yaani_button = Button(sk_send_email_window, text="Yaani ile Gönder", fg=FONT_GROUND, bg=BACK_GROUND,  width=20,
                              font=(FONT, 17), activebackground=BACK_GROUND, activeforeground=FONT_GROUND,
                              command=lambda: open_provider("yaani"))
        yaani_button.grid(column=0, row=5, pady=2)

        cancel_button = Button(sk_send_email_window, text="İptal", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 17),
                               width=20, activebackground=BACK_GROUND, activeforeground=FONT_GROUND,
                               command=lambda: (sk_send_email_window.destroy()))
        cancel_button.grid(column=0, row=6, pady=2)

    # e-Posta Gönderme Fonksiyonu Kemal Sait Eser
    def ask_send_email_kse():
        email_address = "kse_kml_esr@hotmail.com"

        def open_provider(provider):
            if provider == "gmail":
                webbrowser.open("https://mail.google.com/mail/u/0/#inbox?compose=new")
            elif provider == "hotmail":
                webbrowser.open("https://outlook.live.com/mail/0/deeplink/compose")
            elif provider == "yandex":
                webbrowser.open("https://mail.yandex.com/?addMultiUserFromDropdown=false")
            elif provider == "yahoo":
                webbrowser.open("https://mail.yahoo.com/")
            elif provider == "yaani":
                webbrowser.open("https://mail.yaani.com/")

        pyperclip.copy(email_address)
        messagebox.showinfo("Bilgi", "E-posta adresi kopyalandı!")

        kse_send_email_window = Toplevel()
        kse_send_email_window.title("E-posta Gönderme Penceresi")
        kse_send_email_window.config(padx=30, pady=30, bg=BACK_GROUND)
        kse_send_email_window.resizable(False, False)

        ask_label = Label(kse_send_email_window, text="E-postayı hangi sağlayıcı üzerinden\n göndermek istiyorsunuz?",
                          fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 20))
        ask_label.grid(column=0, row=0, pady=20)

        gmail_button = Button(kse_send_email_window, text="Gmail ile Gönder", fg=FONT_GROUND, bg=BACK_GROUND,  width=20,
                              font=(FONT, 17), activebackground=BACK_GROUND, activeforeground=FONT_GROUND,
                              command=lambda: open_provider("gmail"))
        gmail_button.grid(column=0, row=1, pady=2)

        hotmail_button = Button(kse_send_email_window, text="Hotmail ile Gönder", fg=FONT_GROUND, bg=BACK_GROUND,
                                width=20, font=(FONT, 17), activebackground=BACK_GROUND, activeforeground=FONT_GROUND,
                                command=lambda: open_provider("hotmail"))
        hotmail_button.grid(column=0, row=2, pady=2)

        yandex_button = Button(kse_send_email_window, text="Yandex ile Gönder", fg=FONT_GROUND, bg=BACK_GROUND,
                               width=20, font=(FONT, 17), activebackground=BACK_GROUND, activeforeground=FONT_GROUND,
                               command=lambda: open_provider("yandex"))
        yandex_button.grid(column=0, row=3, pady=2)

        yahoo_button = Button(kse_send_email_window, text="Yahoo ile Gönder", fg=FONT_GROUND, bg=BACK_GROUND,
                              width=20, font=(FONT, 17), activebackground=BACK_GROUND, activeforeground=FONT_GROUND,
                              command=lambda: open_provider("yahoo"))
        yahoo_button.grid(column=0, row=4, pady=2)

        yaani_button = Button(kse_send_email_window, text="Yaani ile Gönder", fg=FONT_GROUND, bg=BACK_GROUND, width=20,
                              font=(FONT, 17), activebackground=BACK_GROUND, activeforeground=FONT_GROUND,
                              command=lambda: open_provider("yaani"))
        yaani_button.grid(column=0, row=5, pady=2)

        cancel_button = Button(kse_send_email_window, text="İptal", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 17),
                               width=20, activebackground=BACK_GROUND, activeforeground=FONT_GROUND,
                               command=lambda: (kse_send_email_window.destroy()))
        cancel_button.grid(column=0, row=6, pady=2)

    # Hakkında Sayfası Fonksiyonunun Devamı Part II
    email_send_button_sk = Button(text="Sait Kaplan", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 17),
                                  width=20, activebackground=BACK_GROUND, activeforeground=FONT_GROUND,
                                  command=ask_send_email_sk)
    email_send_button_sk.grid(column=0, row=7, padx=2)

    email_send_button_kse = Button(text="Kemal Sait Eser", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 17),
                                   width=20, activebackground=BACK_GROUND, activeforeground=FONT_GROUND,
                                   command=ask_send_email_kse)
    email_send_button_kse.grid(column=1, row=7, padx=2)

    return_button = Button(text=RETURN_BUTTON, fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 17), width=20,
                           activebackground=BACK_GROUND, activeforeground=FONT_GROUND,
                           command=lambda: (home_page(), about_page_title_label.destroy(), about_us_page.destroy(),
                                            about_app_page.destroy(), social_profiles_label.destroy(),
                                            social_profiles1_button1.destroy(), social_profiles2_button1.destroy(),
                                            social_profiles1_button2.destroy(), social_profiles2_button2.destroy(),
                                            send_email_label.destroy(), email_send_button_sk.destroy(),
                                            email_send_button_kse.destroy(), sk_social_profiles_label.destroy(),
                                            kse_social_profiles_label.destroy(), return_button.destroy()))
    return_button.grid(column=0, columnspan=2, row=8, pady=4)

# <------------------------------------------------> Home Page <------------------------------------------------------>
# Ana Pencere

# Ayarların Ana Pencereye Çağrıldığı Fonksiyon
def load_settings():
    global FONT_GROUND, BACK_GROUND, FONT
    try:
        data = pd.read_csv("app_parameters.csv", encoding='utf-8')
        FONT_GROUND = data['FONT_GROUND'][0]
        BACK_GROUND = data['BACK_GROUND'][0]
        FONT = data['FONT'][0]
    except:
        FONT_GROUND = "black"
        BACK_GROUND = "white"
        FONT = "Helvetica"
load_settings()

window = Tk()
window.title("Raven Language")
window.config(padx=30, pady=30, bg=BACK_GROUND)
window.resizable(False, False)

# Ana Sayfa Fonksiyonu
def home_page():
    global home_logo_label, home_canvas, home_logo_img, mods_page_button, repo_page_button
    global settings_page_button, app_about_button, exit_button, FONT_GROUND, BACK_GROUND, FONT

    home_logo_label = Label(text="Raven Language", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 30, "bold"))
    home_logo_label.grid(column=0, row=0, pady=5)

    home_canvas = Canvas(width=304, height=304, bg=BACK_GROUND, highlightthickness=0)
    home_logo_img = PhotoImage(file="raven_project_logo.png")
    home_canvas.create_image(152, 152, image=home_logo_img)
    home_canvas.grid(column=0, row=1, pady=5)

    mods_page_button = Button(text="Modlar", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 17), width=30,
                              activebackground=BACK_GROUND, activeforeground=FONT_GROUND, command=mods_page)
    mods_page_button.grid(column=0, row=2, pady=2)

    repo_page_button = Button(text="Uygulama Deposu", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 17), width=30,
                              activebackground=BACK_GROUND, activeforeground=FONT_GROUND, command=repo_page)
    repo_page_button.grid(column=0, row=3, pady=2)

    settings_page_button = Button(text="Ayarlar", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 17), width=30,
                                  activebackground=BACK_GROUND, activeforeground=FONT_GROUND, command=settings_page)
    settings_page_button.grid(column=0, row=4, pady=2)

    app_about_button = Button(text="Bize & Uygulamaya Dair", fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 17), width=30,
                              activebackground=BACK_GROUND, activeforeground=FONT_GROUND, command=about_page)
    app_about_button.grid(column=0, row=5, pady=2)

    exit_button = Button(text=EXIT_BUTTON, fg=FONT_GROUND, bg=BACK_GROUND, font=(FONT, 17), width=30,
                         activebackground=BACK_GROUND, activeforeground=FONT_GROUND, command=lambda: (window.destroy()))
    exit_button.grid(column=0, row=6, pady=2)

home_page()
window.mainloop()