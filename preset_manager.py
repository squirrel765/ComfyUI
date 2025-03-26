import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os

class PresetManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Prompt Preset Manager")
        self.root.geometry("700x400")

        self.preset_file = filedialog.askopenfilename(
            title="프리셋 JSON 파일 선택",
            filetypes=[("JSON files", "*.json")],
            defaultextension=".json"
        )

        if not self.preset_file:
            messagebox.showerror("파일 없음", "프리셋 JSON 파일을 선택하지 않았습니다.")
            root.destroy()
            return

        self.preset_data = self.load_presets()

        # UI 구성
        self.left_frame = tk.Frame(self.root)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.right_frame = tk.Frame(self.root)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.preset_listbox = tk.Listbox(self.left_frame, width=30)
        self.preset_listbox.pack(fill=tk.BOTH, expand=True)
        self.preset_listbox.bind("<<ListboxSelect>>", self.on_preset_select)

        self.preset_name_var = tk.StringVar()
        tk.Label(self.right_frame, text="Preset Name").pack()
        tk.Entry(self.right_frame, textvariable=self.preset_name_var).pack(fill=tk.X)

        tk.Label(self.right_frame, text="Prompt Text").pack()
        self.prompt_textbox = tk.Text(self.right_frame, height=15, state=tk.NORMAL)
        self.prompt_textbox.pack(fill=tk.BOTH, expand=True)

        self.btn_frame = tk.Frame(self.right_frame)
        self.btn_frame.pack(pady=10)

        tk.Button(self.btn_frame, text="➕ 추가", command=self.add_new_preset).pack(side=tk.LEFT, padx=5)
        tk.Button(self.btn_frame, text="💾 저장", command=self.save_preset).pack(side=tk.LEFT, padx=5)
        tk.Button(self.btn_frame, text="❌ 삭제", command=self.delete_preset).pack(side=tk.LEFT, padx=5)

        self.refresh_listbox()

    def load_presets(self):
        if os.path.exists(self.preset_file):
            with open(self.preset_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_presets(self):
        with open(self.preset_file, "w", encoding="utf-8") as f:
            json.dump(self.preset_data, f, indent=4, ensure_ascii=False)

    def refresh_listbox(self):
        self.preset_listbox.delete(0, tk.END)
        for key in sorted(self.preset_data.keys()):
            self.preset_listbox.insert(tk.END, key)

    def on_preset_select(self, event):
        selection = self.preset_listbox.curselection()
        if not selection:
            return
        key = self.preset_listbox.get(selection[0])
        self.preset_name_var.set(key)

        # 텍스트박스를 무조건 수정 가능 상태로
        self.prompt_textbox.config(state=tk.NORMAL)
        self.prompt_textbox.delete(1.0, tk.END)
        self.prompt_textbox.insert(tk.END, self.preset_data.get(key, ""))

    def add_new_preset(self):
        self.preset_listbox.selection_clear(0, tk.END)
        self.preset_name_var.set("")
        self.prompt_textbox.config(state=tk.NORMAL)
        self.prompt_textbox.delete(1.0, tk.END)
        self.root.title("Prompt Preset Manager - [새 프리셋 작성 중]")

    def save_preset(self):
        name = self.preset_name_var.get().strip()
        text = self.prompt_textbox.get(1.0, tk.END).strip()
        if not name or not text:
            messagebox.showwarning("입력 누락", "프리셋 이름과 내용 모두 필요합니다.")
            return

        if name in self.preset_data:
            if not messagebox.askyesno("덮어쓰기 확인", f"'{name}' 프리셋을 덮어쓸까요?"):
                return

        self.preset_data[name] = text
        self.save_presets()
        self.refresh_listbox()
        self.root.title("Prompt Preset Manager")
        messagebox.showinfo("저장 완료", f"프리셋 '{name}' 저장 완료.")

    def delete_preset(self):
        name = self.preset_name_var.get().strip()
        if name not in self.preset_data:
            return

        if messagebox.askyesno("삭제 확인", f"프리셋 '{name}'을 삭제할까요?"):
            del self.preset_data[name]
            self.save_presets()
            self.refresh_listbox()
            self.preset_name_var.set("")
            self.prompt_textbox.config(state=tk.NORMAL)
            self.prompt_textbox.delete(1.0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = PresetManagerApp(root)
    root.mainloop()
