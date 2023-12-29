import tkinter as tk
from tkinter import messagebox
import ast

class CodeCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Checker App")
        
        self.code_label = tk.Label(root, text="Nhập code:")
        self.code_label.pack()
 
        self.code_text = tk.Text(root, height=10, width=40)
        self.code_text.pack()

        self.code_text.bind("<KeyRelease>", self.check_code)

        self.result_text = tk.Label(root, text="", anchor="sw", justify="left")
        self.result_text.pack(fill="both", expand=True)

    def check_code(self, event):
        code = self.code_text.get("1.0", "end-1c")  # Get code from the Text widget
        if code.strip() == "":
            self.result_text.config(text="")
            return

        try:
            # Kiểm tra lỗi cú pháp bằng cách cố gắng biên dịch thành cây cú pháp AST
            ast.parse(code)
            result = "Không có lỗi cú pháp."
        except SyntaxError as e:
            result = f"Lỗi cú pháp: {e}"

        self.result_text.config(text=result)

if __name__ == "__main__":
    root = tk.Tk()
    app = CodeCheckerApp(root)
    root.mainloop()
