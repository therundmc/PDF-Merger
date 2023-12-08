import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog

class PDFConcatenator:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Concatenation")
        self.root.geometry("800x600")

        self.pdf_files = []
        self.page_ranges = []

        # Frame for PDF list and associated buttons
        self.list_frame = tk.Frame(root, bg="white")
        self.list_frame.pack(fill=tk.BOTH, expand=True)

        # Label for PDF list
        self.list_label = tk.Label(self.list_frame, text="List of PDFs", font=("Helvetica", 16, "bold"), bg="white")
        self.list_label.pack(pady=10, anchor=tk.W)

        # Scrollable canvas for PDF list
        self.canvas = tk.Canvas(self.list_frame, bg="white")
        self.scroll_y = tk.Scrollbar(self.list_frame, orient="vertical", command=self.canvas.yview)
        self.scroll_y.pack(side="right", fill="y")

        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.configure(yscrollcommand=self.scroll_y.set)

        # Inner frame for PDF list items
        self.inner_frame = tk.Frame(self.canvas, bg="white")
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # "Add PDFs" button
        self.add_button = tk.Button(root, text="Add PDFs", command=self.add_pdfs, bg="#001f3f", fg="white", width=20,
                                    font=("Helvetica", 12))
        self.add_button.pack(pady=10, side=tk.LEFT, anchor=tk.SW)

        # "Concatenate PDFs" button
        self.concat_button = tk.Button(root, text="Concatenate PDFs", command=self.concat_pdfs, bg="#001f3f", fg="white",
                                       width=20, font=("Helvetica", 12))
        self.concat_button.pack(pady=10, side=tk.LEFT, anchor=tk.SW)

        # Status label
        self.status_label = tk.Label(root, text="", fg="green", bg="white", font=("Helvetica", 12))
        self.status_label.pack(pady=10, side=tk.BOTTOM, anchor=tk.SE)

    def add_pdfs(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        for file in files:
            self.pdf_files.append(file)
            self.page_ranges.append((1, self.get_max_page(file)))  # Initialize to all pages
        self.update_file_entries()

    def update_file_entries(self):
        for widget in self.inner_frame.winfo_children():
            widget.destroy()

        for i, (file, page_range) in enumerate(zip(self.pdf_files, self.page_ranges)):
            frame = tk.Frame(self.inner_frame, bd=2, relief=tk.GROOVE, bg="white")
            frame.pack(padx=10, pady=5, fill=tk.X)

            label = tk.Label(frame, text=f"{file} - Pages: {page_range[0]}-{page_range[1]}", wraplength=600,
                             bg="white", font=("Helvetica", 12))
            label.pack(side=tk.LEFT, padx=5)

            button_set_pages = tk.Button(frame, text="Set Pages", command=lambda i=i: self.set_pages(i),
                                         bg="#001f3f", fg="white", width=10, font=("Helvetica", 10))
            button_set_pages.pack(side=tk.LEFT, padx=5)

            button_remove = tk.Button(frame, text="Remove", command=lambda i=i: self.remove_pdf(i),
                                      bg="#001f3f", fg="white", width=10, font=("Helvetica", 10))
            button_remove.pack(side=tk.RIGHT)

    def set_pages(self, index):
        page_range = simpledialog.askstring("Set Pages", "Enter page range (e.g., 1-5):",
                                            initialvalue=f"{self.page_ranges[index][0]}-{self.page_ranges[index][1]}")
        if page_range:
            start_page, end_page = map(int, page_range.split('-'))
            self.page_ranges[index] = (start_page, end_page)
            self.update_file_entries()

    def remove_pdf(self, index):
        del self.pdf_files[index]
        del self.page_ranges[index]
        self.update_file_entries()

    def concat_pdfs(self):
        if not self.pdf_files:
            self.status_label.config(text="No PDFs selected.")
            return

        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if output_path:
            self.concat_pdf(self.pdf_files, self.page_ranges, output_path)
            self.status_label.config(text="PDFs concatenated successfully!")
            self.pdf_files = []
            self.page_ranges = []
            self.update_file_entries()

    def get_max_page(self, file_path):
        pdf_document = fitz.open(file_path)
        max_page = pdf_document.page_count
        pdf_document.close()
        return max_page

    def concat_pdf(self, input_paths, page_ranges, output_path):
        pdf_merger = fitz.open()

        for i, (path, page_range) in enumerate(zip(input_paths, page_ranges)):
            start_page, end_page = page_range
            pdf_document = fitz.open(path)

            if start_page < 1:
                start_page = 1
            if end_page > pdf_document.page_count:
                end_page = pdf_document.page_count

            pdf_merger.insert_pdf(pdf_document, from_page=start_page - 1, to_page=end_page - 1)

            pdf_document.close()

        pdf_merger.save(output_path)
        pdf_merger.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFConcatenator(root)
    root.mainloop()
import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog

class PDFConcatenator:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Concatenation")
        self.root.geometry("800x600")

        self.pdf_files = []
        self.page_ranges = []

        # Frame for PDF list and associated buttons
        self.list_frame = tk.Frame(root, bg="white")
        self.list_frame.pack(fill=tk.BOTH, expand=True)

        # Label for PDF list
        self.list_label = tk.Label(self.list_frame, text="List of PDFs", font=("Helvetica", 16, "bold"), bg="white")
        self.list_label.pack(pady=10, anchor=tk.W)

        # Scrollable canvas for PDF list
        self.canvas = tk.Canvas(self.list_frame, bg="white")
        self.scroll_y = tk.Scrollbar(self.list_frame, orient="vertical", command=self.canvas.yview)
        self.scroll_y.pack(side="right", fill="y")

        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.configure(yscrollcommand=self.scroll_y.set)

        # Inner frame for PDF list items
        self.inner_frame = tk.Frame(self.canvas, bg="white")
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # "Add PDFs" button
        self.add_button = tk.Button(root, text="Add PDFs", command=self.add_pdfs, bg="#001f3f", fg="white", width=20,
                                    font=("Helvetica", 12))
        self.add_button.pack(pady=10, side=tk.LEFT, anchor=tk.SW)

        # "Concatenate PDFs" button
        self.concat_button = tk.Button(root, text="Concatenate PDFs", command=self.concat_pdfs, bg="#222", fg="white",
                                       width=20, font=("Helvetica", 12))
        self.concat_button.pack(pady=10, side=tk.LEFT, anchor=tk.SW)

        # Status label
        self.status_label = tk.Label(root, text="", fg="green", bg="white", font=("Helvetica", 12))
        self.status_label.pack(pady=10, side=tk.BOTTOM, anchor=tk.SE)

    def add_pdfs(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        for file in files:
            self.pdf_files.append(file)
            self.page_ranges.append((1, self.get_max_page(file)))  # Initialize to all pages
        self.update_file_entries()

    def update_file_entries(self):
        for widget in self.inner_frame.winfo_children():
            widget.destroy()

        for i, (file, page_range) in enumerate(zip(self.pdf_files, self.page_ranges)):
            frame = tk.Frame(self.inner_frame, bd=2, relief=tk.GROOVE, bg="white")
            frame.pack(padx=10, pady=5, fill=tk.X)

            label = tk.Label(frame, text=f"{file} - Pages: {page_range[0]}-{page_range[1]}", wraplength=600,
                             bg="white", font=("Helvetica", 12))
            label.pack(side=tk.LEFT, padx=5)

            button_set_pages = tk.Button(frame, text="Set Pages", command=lambda i=i: self.set_pages(i),
                                         bg="#001f3f", fg="white", width=10, font=("Helvetica", 10))
            button_set_pages.pack(side=tk.LEFT, padx=5)

            button_remove = tk.Button(frame, text="Remove", command=lambda i=i: self.remove_pdf(i),
                                      bg="#001f3f", fg="white", width=10, font=("Helvetica", 10))
            button_remove.pack(side=tk.RIGHT)

    def set_pages(self, index):
        page_range = simpledialog.askstring("Set Pages", "Enter page range (e.g., 1-5):",
                                            initialvalue=f"{self.page_ranges[index][0]}-{self.page_ranges[index][1]}")
        if page_range:
            start_page, end_page = map(int, page_range.split('-'))
            self.page_ranges[index] = (start_page, end_page)
            self.update_file_entries()

    def remove_pdf(self, index):
        del self.pdf_files[index]
        del self.page_ranges[index]
        self.update_file_entries()

    def concat_pdfs(self):
        if not self.pdf_files:
            self.status_label.config(text="No PDFs selected.")
            return

        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if output_path:
            self.concat_pdf(self.pdf_files, self.page_ranges, output_path)
            self.status_label.config(text="PDFs concatenated successfully!")
            self.pdf_files = []
            self.page_ranges = []
            self.update_file_entries()

    def get_max_page(self, file_path):
        pdf_document = fitz.open(file_path)
        max_page = pdf_document.page_count
        pdf_document.close()
        return max_page

    def concat_pdf(self, input_paths, page_ranges, output_path):
        pdf_merger = fitz.open()

        for i, (path, page_range) in enumerate(zip(input_paths, page_ranges)):
            start_page, end_page = page_range
            pdf_document = fitz.open(path)

            if start_page < 1:
                start_page = 1
            if end_page > pdf_document.page_count:
                end_page = pdf_document.page_count

            pdf_merger.insert_pdf(pdf_document, from_page=start_page - 1, to_page=end_page - 1)

            pdf_document.close()

        pdf_merger.save(output_path)
        pdf_merger.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFConcatenator(root)
    root.mainloop()
import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog

class PDFConcatenator:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Concatenation")
        self.root.geometry("800x600")

        self.pdf_files = []
        self.page_ranges = []

        # Frame for PDF list and associated buttons
        self.list_frame = tk.Frame(root, bg="white")
        self.list_frame.pack(fill=tk.BOTH, expand=True)

        # Label for PDF list
        self.list_label = tk.Label(self.list_frame, text="List of PDFs", font=("Helvetica", 16, "bold"), bg="white")
        self.list_label.pack(pady=10, anchor=tk.W)

        # Scrollable canvas for PDF list
        self.canvas = tk.Canvas(self.list_frame, bg="white")
        self.scroll_y = tk.Scrollbar(self.list_frame, orient="vertical", command=self.canvas.yview)
        self.scroll_y.pack(side="right", fill="y")

        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.configure(yscrollcommand=self.scroll_y.set)

        # Inner frame for PDF list items
        self.inner_frame = tk.Frame(self.canvas, bg="white")
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # "Add PDFs" button
        self.add_button = tk.Button(root, text="Add PDFs", command=self.add_pdfs, bg="#001f3f", fg="white", width=20,
                                    font=("Helvetica", 12))
        self.add_button.pack(pady=10, side=tk.LEFT, anchor=tk.SW)

        # "Concatenate PDFs" button
        self.concat_button = tk.Button(root, text="Concatenate PDFs", command=self.concat_pdfs, bg="#001f3f", fg="white",
                                       width=20, font=("Helvetica", 12))
        self.concat_button.pack(pady=10, side=tk.LEFT, anchor=tk.SW)

        # Status label
        self.status_label = tk.Label(root, text="", fg="green", bg="white", font=("Helvetica", 12))
        self.status_label.pack(pady=10, side=tk.BOTTOM, anchor=tk.SE)

    def add_pdfs(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        for file in files:
            self.pdf_files.append(file)
            self.page_ranges.append((1, self.get_max_page(file)))  # Initialize to all pages
        self.update_file_entries()

    def update_file_entries(self):
        for widget in self.inner_frame.winfo_children():
            widget.destroy()

        for i, (file, page_range) in enumerate(zip(self.pdf_files, self.page_ranges)):
            frame = tk.Frame(self.inner_frame, bd=2, relief=tk.GROOVE, bg="white")
            frame.pack(padx=10, pady=5, fill=tk.X)

            label = tk.Label(frame, text=f"{file} - Pages: {page_range[0]}-{page_range[1]}", wraplength=600,
                             bg="white", font=("Helvetica", 12))
            label.pack(side=tk.LEFT, padx=5)

            button_set_pages = tk.Button(frame, text="Set Pages", command=lambda i=i: self.set_pages(i),
                                         bg="#001f3f", fg="white", width=10, font=("Helvetica", 10))
            button_set_pages.pack(side=tk.LEFT, padx=5)

            button_remove = tk.Button(frame, text="Remove", command=lambda i=i: self.remove_pdf(i),
                                      bg="#001f3f", fg="white", width=10, font=("Helvetica", 10))
            button_remove.pack(side=tk.RIGHT)

    def set_pages(self, index):
        page_range = simpledialog.askstring("Set Pages", "Enter page range (e.g., 1-5):",
                                            initialvalue=f"{self.page_ranges[index][0]}-{self.page_ranges[index][1]}")
        if page_range:
            start_page, end_page = map(int, page_range.split('-'))
            self.page_ranges[index] = (start_page, end_page)
            self.update_file_entries()

    def remove_pdf(self, index):
        del self.pdf_files[index]
        del self.page_ranges[index]
        self.update_file_entries()

    def concat_pdfs(self):
        if not self.pdf_files:
            self.status_label.config(text="No PDFs selected.")
            return

        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if output_path:
            self.concat_pdf(self.pdf_files, self.page_ranges, output_path)
            self.status_label.config(text="PDFs concatenated successfully!")
            self.pdf_files = []
            self.page_ranges = []
            self.update_file_entries()

    def get_max_page(self, file_path):
        pdf_document = fitz.open(file_path)
        max_page = pdf_document.page_count
        pdf_document.close()
        return max_page

    def concat_pdf(self, input_paths, page_ranges, output_path):
        pdf_merger = fitz.open()

        for i, (path, page_range) in enumerate(zip(input_paths, page_ranges)):
            start_page, end_page = page_range
            pdf_document = fitz.open(path)

            if start_page < 1:
                start_page = 1
            if end_page > pdf_document.page_count:
                end_page = pdf_document.page_count

            pdf_merger.insert_pdf(pdf_document, from_page=start_page - 1, to_page=end_page - 1)

            pdf_document.close()

        pdf_merger.save(output_path)
        pdf_merger.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFConcatenator(root)
    root.mainloop()
