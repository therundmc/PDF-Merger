import PyPDF2
import tkinter as tk
from tkinter import filedialog

class PDFConcatenator:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Concatenation")

        self.pdf_files = []

        self.file_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, width=50)
        self.file_listbox.pack(padx=10, pady=10)

        self.add_button = tk.Button(root, text="Add PDFs", command=self.add_pdfs)
        self.add_button.pack()

        self.concat_button = tk.Button(root, text="Concatenate PDFs", command=self.concat_pdfs)
        self.concat_button.pack()

        self.status_label = tk.Label(root, text="", fg="green")
        self.status_label.pack()

    def add_pdfs(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        self.pdf_files.extend(files)
        self.update_file_listbox()

    def update_file_listbox(self):
        self.file_listbox.delete(0, tk.END)
        for file in self.pdf_files:
            self.file_listbox.insert(tk.END, file)

    def concat_pdfs(self):
        if not self.pdf_files:
            self.status_label.config(text="No PDFs selected.")
            return

        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if output_path:
            concat_pdf(self.pdf_files, output_path)
            self.status_label.config(text="PDFs concatenated successfully!")
            self.pdf_files = []
            self.update_file_listbox()

def concat_pdf(input_paths, output_path):
    pdf_merger = PyPDF2.PdfMerger()
    
    for path in input_paths:
        pdf_merger.append(path)
        
    with open(output_path, 'wb') as output_file:
        pdf_merger.write(output_file)

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFConcatenator(root)
    root.mainloop()
