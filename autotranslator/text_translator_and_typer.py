import tkinter as tk
from googletrans import Translator

def translate_text(text, dest_language):
    translator = Translator(dest=dest_language)
    return translator.translate(text).text

class TranslationApp(tk.Tk):
    def __init__(self, parent):
        tk.Tk.__init__(self, parent)
        self.parent = parent

        self.text_entry = tk.Text(self)
        self.text_entry.pack()

        self.translated_text = tk.StringVar()
        self.translated_text_label = tk.Label(self, textvariable=self.translated_text)
        self.translated_text_label.pack()

        self.translate_button = tk.Button(self, text="Translate", command=self.translate)
        self.translate_button.pack()

    def translate(self):
        text = self.text_entry.get("1.0", "end")
        translated_text = translate_text(text, self.selected_language.get())
        self.translated_text.set(translated_text)

    def toggle_stay_on_top(self):
        if self.toggle_var.get():
            self.attributes("-topmost", True)
        else:
            self.attributes("-topmost", False)

if __name__ == "__main__":
    root = tk.Tk()
    app = TranslationApp(root)
    app.mainloop()
