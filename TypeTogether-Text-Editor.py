import tkinter as tk
from tkinter import *
from tkinter import filedialog, colorchooser,scrolledtext, messagebox
from tkinter.font import Font


class text_editor: # class
    current_open_file = "No File"

    #functions for file menu
    #new file
    def new_file(self):
        self.text_area.delete(1.0, END)
        self.current_open_file = "No File"
        self.update_counts()
        
    #open file
    def open_file(self):
        try:
            open_return = filedialog.askopenfile(initialdir="/", title="Select File to Open", filetypes=(("Text Files", ".txt"),("All Files", ".*")))
            if open_return != None:
                self.text_area.delete(1.0, END)
            for line in open_return:
                self.text_area.insert(END, line)
            self.current_open_file = open_return.name
            open_return.close()
            self.update_counts()
        except:
            pass

    #save file
    def save_file(self):
        if self.current_open_file == "No File":
            self.save_as_file()
        else:
            f = open(self.current_open_file, "w+")
            f.write(self.text_area.get(1.0, END))
            f.close()

    #save as file            
    def save_as_file(self):
        f= filedialog.asksaveasfile(mode="w", defaultextension=".txt") 
        if f is None:
            return
        text2save = self.text_area.get(1.0, END)
        self.current_open_file = f.name
        f.write(text2save)
        f.close()

    #exit file
    def exit_app(self):
        if messagebox.askokcancel("Exit", "Do you really want to exit?"):
            self.master.destroy()

    #functions for edit menu
    #undo
    def undo_text(self):
        try:
            self.text_area.edit_undo()
            self.update_counts()
        except:
            pass

    #redo
    def redo_text(self):
        try:
            self.text_area.edit_redo()
            self.update_counts()
        except:
            pass

    #cut
    def cut_text(self):
        try:
            self.copy_text()
            self.text_area.delete("sel.first", "sel.last")
            self.update_counts()
        except:
            pass

    #copy        
    def copy_text(self):
        self.text_area.clipboard_clear()
        self.text_area.clipboard_append(self.text_area.selection_get())

    #paste
    def paste_text(self):
        self.text_area.insert(INSERT, self.text_area.clipboard_get())
        self.update_counts()

    #select all
    def select_all(self):
        self.text_area.tag_add(tk.SEL, "1.0", tk.END)
        self.text_area.mark_set(tk.INSERT, "1.0")
        self.text_area.see(tk.INSERT)

    #clear
    def clear(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear the text?"):
            self.text_area.delete("1.0", tk.END)
            self.update_counts()


    #functions for format menu
    #bold
    def toggle_bold(self):
        try:
            current_tags = self.text_area.tag_names(tk.SEL_FIRST)
            if "bold" in current_tags:
                self.text_area.tag_remove("bold", tk.SEL_FIRST, tk.SEL_LAST)
            else:
                self.text_area.tag_add("bold", tk.SEL_FIRST, tk.SEL_LAST)
                self.text_area.tag_configure("bold", font=(self.current_font, self.current_size, "bold"))

        except:
            pass

    #italic
    def toggle_italic(self):
        try:
            current_tags = self.text_area.tag_names(tk.SEL_FIRST)
            if "italic" in current_tags:
                self.text_area.tag_remove("italic", tk.SEL_FIRST, tk.SEL_LAST)
            else:
                self.text_area.tag_add("italic", tk.SEL_FIRST, tk.SEL_LAST)
                self.text_area.tag_configure("italic", font=(self.current_font, self.current_size, "italic"))
        except:
            pass

    #underline
    def toggle_underline(self):
        try:
            current_tags = self.text_area.tag_names(tk.SEL_FIRST)
            if "underline" in current_tags:
                self.text_area.tag_remove("underline", tk.SEL_FIRST, tk.SEL_LAST)
            else:
                self.text_area.tag_add("underline", tk.SEL_FIRST, tk.SEL_LAST)
                self.text_area.tag_configure("underline", font=(self.current_font, self.current_size, "underline"))
        except:
            pass

    #update counts
    def update_counts(self, event=None):
        text = self.text_area.get(1.0, tk.END).strip()  
        word_count = len(text.split()) 
        self.count_stack.append(word_count)  

    #show counts
    def show_word_count(self):
        if self.count_stack:
            current_word_count = self.count_stack[-1]
            messagebox.showinfo("Word Count", f"Current word count: {current_word_count}")
        else:
            messagebox.showinfo("Word Count", "No words typed yet.")

    #colpr    
    def text_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.text_area.tag_add("color", tk.SEL_FIRST, tk.SEL_LAST)
            self.text_area.tag_configure("color", foreground=color)

    #highlight
    def highlight_text(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.text_area.tag_add("highlight", tk.SEL_FIRST, tk.SEL_LAST)
            self.text_area.tag_configure("highlight", background=color)

    #remove highlight
    def remove_highlight(self):
        try:
            self.text_area.tag_remove("highlight", tk.SEL_FIRST, tk.SEL_LAST)
        except:
            pass

    #function for style
    def change_font(self, font_name):
        self.current_font = font_name
        self.update_font()

    #function for size
    def change_size(self, size):
        self.current_size = size
        self.update_font()

    #update font
    def update_font(self):
        font = (self.current_font, self.current_size)
        self.text_area.config(font=font)

    
    #function for help
    def show_about(self):
        messagebox.showinfo("About", "TypeTogether Text Editor\nCreated with Python and Tkinter\n\nProject By:\nSobia Kamali & Nabeha Faisal")

            
    def __init__(self, master): # constructor, self represents object
        # Font settings
        self.current_font = "Arial"
        self.current_size = 12

        self.master = master
        master.title("TypeTogether")
        master.geometry("800x600")

        self.count_stack = []
        
        self.text_area = Text(self.master, wrap = "word", undo=True, fg ="blue", font=(self.current_font, self.current_size))
        self.text_area.pack(fill=BOTH, expand=1)


        self.current_file = None
        self.bold_font = Font(self.text_area, weight="bold")
        self.italic_font = Font(self.text_area, slant="italic")
        self.underline_font = Font(self.text_area, underline=True)

        self.scrollbar = tk.Scrollbar(self.text_area)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text_area.yview)

        #main menu
        self.main_menu = Menu()
        self.master.config(menu = self.main_menu)


        #file menu
        self.file_menu = Menu(self.main_menu, tearoff = False)       
        self.main_menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.exit_app)

        
        #edit menu
        self.edit_menu = Menu(self.main_menu, tearoff = False)
        self.main_menu.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", command=self.undo_text)
        self.edit_menu.add_command(label="Redo", command=self.redo_text)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=self.cut_text)
        self.edit_menu.add_command(label="Copy", command=self.copy_text)
        self.edit_menu.add_command(label="Paste", command=self.paste_text)
        self.edit_menu.add_command(label="Select All..", command=self.select_all)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Clear", command=self.clear)

        #format menu
        self.format_menu = Menu(self.main_menu, tearoff = False)
        self.main_menu.add_cascade(label="Format", menu=self.format_menu)
        self.format_menu.add_command(label="Bold", command=self.toggle_bold)
        self.format_menu.add_command(label="Italic", command=self.toggle_italic)
        self.format_menu.add_command(label="Underline", command=self.toggle_underline)
        self.format_menu.add_separator()
        self.format_menu.add_command(label="Word Count", command=self.show_word_count)
        self.format_menu.add_separator()
        self.format_menu.add_command(label="Font Color", command=self.text_color)
        self.format_menu.add_command(label="Highlight Text", command=self.highlight_text)
        self.format_menu.add_command(label="Remove Highlight", command=self.remove_highlight)
        
        
        #font style menu
        self.font_style_menu = Menu(self.main_menu, tearoff = False)
        self.main_menu.add_cascade(label="Style", menu=self.font_style_menu)
        self.font_style_menu.add_command(label="Arial", command=lambda: self.change_font("Arial"))
        self.font_style_menu.add_command(label="Calibri", command=lambda: self.change_font("Calibri"))
        self.font_style_menu.add_command(label="Cambria", command=lambda: self.change_font("Cambria"))
        self.font_style_menu.add_command(label="Courier", command=lambda: self.change_font("Courier"))
        self.font_style_menu.add_command(label="Forte", command=lambda: self.change_font("Forte"))
        self.font_style_menu.add_command(label="Helvetica", command=lambda: self.change_font("Helvetica"))
        self.font_style_menu.add_command(label="Times New Roman", command=lambda: self.change_font("Times New Roman"))
        self.font_style_menu.add_command(label="Verdana", command=lambda: self.change_font("Verdana"))

        #font size menu
        self.font_size_menu = Menu(self.main_menu, tearoff = False)
        self.main_menu.add_cascade(label="Size", menu=self.font_size_menu)
        self.font_size_menu.add_command(label="6", command=lambda: self.change_size(6))
        self.font_size_menu.add_command(label="8", command=lambda: self.change_size(8))
        self.font_size_menu.add_command(label="10", command=lambda: self.change_size(10))
        self.font_size_menu.add_command(label="12", command=lambda: self.change_size(12))
        self.font_size_menu.add_command(label="14", command=lambda: self.change_size(14))
        self.font_size_menu.add_command(label="16", command=lambda: self.change_size(16))
        self.font_size_menu.add_command(label="18", command=lambda: self.change_size(18))
        self.font_size_menu.add_command(label="20", command=lambda: self.change_size(20))
        

        #help menu
        self.help_menu = tk.Menu(self.main_menu, tearoff=False)
        self.main_menu.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About", command=self.show_about)

        self.update_counts()
        self.text_area.bind("<KeyRelease>", self.update_counts)


        
root = Tk()
te = text_editor(root) # object
root.mainloop()


