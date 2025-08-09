import tkinter as tk
from tkinter import messagebox
import threading

# Quiz data
QUIZ_DATA = {
    "Computer": [
        {
            "question": "Which programming language is known as the backbone of web development?",
            "options": ["Python", "JavaScript", "C++", "Java"],
            "answer": "JavaScript"
        },
        {
            "question": "What does CPU stand for?",
            "options": ["Central Processing Unit", "Central Programming Unit", "Computer Personal Unit", "Core Processing Utility"],
            "answer": "Central Processing Unit"
        },
        {
            "question": "Which company developed the Windows operating system?",
            "options": ["Microsoft", "Apple", "IBM", "Google"],
            "answer": "Microsoft"
        },
        {
            "question": "What is the primary function of RAM in a computer?",
            "options": ["Store permanent data", "Store temporary data", "Process data", "Display data"],
            "answer": "Store temporary data"
        },
        {
            "question": "Which of these is an open-source operating system?",
            "options": ["Linux", "Windows", "macOS", "ChromeOS"],
            "answer": "Linux"
        }
    ],
    "Science": [
        {
            "question": "What is the chemical symbol for water?",
            "options": ["H2O", "CO2", "O2", "NaCl"],
            "answer": "H2O"
        },
        {
            "question": "What planet is known as the Red Planet?",
            "options": ["Earth", "Mars", "Jupiter", "Venus"],
            "answer": "Mars"
        },
        {
            "question": "What is the powerhouse of the cell?",
            "options": ["Nucleus", "Mitochondria", "Ribosome", "Golgi apparatus"],
            "answer": "Mitochondria"
        },
        {
            "question": "What is the speed of light in a vacuum?",
            "options": ["300,000 km/s", "150,000 km/s", "450,000 km/s", "600,000 km/s"],
            "answer": "300,000 km/s"
        },
        {
            "question": "What gas do plants absorb from the atmosphere?",
            "options": ["Oxygen", "Carbon Dioxide", "Nitrogen", "Hydrogen"],
            "answer": "Carbon Dioxide"
        }
    ],
    "English": [
        {
            "question": "What is the synonym of 'happy'?",
            "options": ["Sad", "Joyful", "Angry", "Tired"],
            "answer": "Joyful"
        },
        {
            "question": "What is the antonym of 'difficult'?",
            "options": ["Easy", "Hard", "Complex", "Challenging"],
            "answer": "Easy"
        },
        {
            "question": "Which word is a noun?",
            "options": ["Quickly", "Beautiful", "Happiness", "Run"],
            "answer": "Happiness"
        },
        {
            "question": "What is the past tense of 'go'?",
            "options": ["Gone", "Went", "Going", "Goes"],
            "answer": "Went"
        },
        {
            "question": "Which of these is a preposition?",
            "options": ["Quickly", "Under", "Beautifully", "Happiness"],
            "answer": "Under"
        }
    ]
}

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Game")
        self.root.geometry("600x400")
        self.root.configure(bg="#262643")
        self.score = 0
        self.question_index = 0
        self.selected_category = None
        self.timer_seconds = 12
        self.timer_id = None

        self.title_label = tk.Label(root, text="Welcome to the Quiz Game!", font=("Arial Rounded MT Bold", 22), fg="#f2e9e4", bg="#22223b")
        self.title_label.pack(pady=20)

        self.category_label = tk.Label(root, text="Choose a category:", font=("Arial", 16), fg="#c9ada7", bg="#22223b")
        self.category_label.pack(pady=10)

        self.category_var = tk.StringVar()
        self.category_buttons = []
        for cat in QUIZ_DATA.keys():
            btn = tk.Radiobutton(root, text=cat, variable=self.category_var, value=cat, font=("Arial", 14),
                                 fg="#4a4e69", bg="#f2e9e4", selectcolor="#9a8c98", indicatoron=0, width=15, pady=5)
            btn.pack(pady=5)
            self.category_buttons.append(btn)

        self.start_button = tk.Button(root, text="Start Quiz", font=("Arial", 14, "bold"), bg="#9a8c98", fg="#22223b", command=self.start_quiz)
        self.start_button.pack(pady=20)

        self.timer_label = tk.Label(root, text="", font=("Arial", 16, "bold"), fg="#f2e9e4", bg="#22223b")
        self.question_label = tk.Label(root, text="", font=("Arial", 16), fg="#f2e9e4", bg="#22223b", wraplength=500)
        self.option_buttons = []
        for i in range(4):
            btn = tk.Button(root, text="", font=("Arial", 14), width=30, bg="#c9ada7", fg="#22223b", command=lambda idx=i: self.check_answer(idx))
            self.option_buttons.append(btn)

    def start_quiz(self):
        cat = self.category_var.get()
        if not cat:
            messagebox.showwarning("No Category", "Please select a category to start.")
            return
        self.selected_category = cat
        self.score = 0
        self.question_index = 0
        self.title_label.pack_forget()
        self.category_label.pack_forget()
        for btn in self.category_buttons:
            btn.pack_forget()
        self.start_button.pack_forget()
        self.show_question()

    def show_question(self):
        questions = QUIZ_DATA[self.selected_category]
        if self.question_index >= len(questions):
            self.show_result()
            return

        q = questions[self.question_index]
        self.timer_seconds = 12
        self.timer_label.config(text=f"Time left: {self.timer_seconds} seconds", fg="#f2e9e4")
        self.timer_label.pack(pady=10)
        self.update_timer()

        self.question_label.config(text=f"Q{self.question_index+1}: {q['question']}")
        self.question_label.pack(pady=10)

        for i, opt in enumerate(q["options"]):
            self.option_buttons[i].config(text=opt, state=tk.NORMAL, bg="#c9ada7")
            self.option_buttons[i].pack(pady=5)

    def update_timer(self):
        self.timer_label.config(text=f"Time left: {self.timer_seconds} seconds")
        if self.timer_seconds > 0:
            self.timer_seconds -= 1
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.disable_options()
            self.timer_label.config(text="Time's up!", fg="#e63946")
            self.root.after(1500, self.next_question)

    def check_answer(self, idx):
        questions = QUIZ_DATA[self.selected_category]
        q = questions[self.question_index]
        selected = q["options"][idx]
        correct = q["answer"]
        self.disable_options()
        if selected == correct:
            self.score += 1
            self.option_buttons[idx].config(bg="#38b000")
        else:
            self.option_buttons[idx].config(bg="#e63946")
            for i, opt in enumerate(q["options"]):
                if opt == correct:
                    self.option_buttons[i].config(bg="#38b000")
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.root.after(1500, self.next_question)

    def disable_options(self):
        for btn in self.option_buttons:
            btn.config(state=tk.DISABLED)

    def next_question(self):
        self.question_label.pack_forget()
        self.timer_label.pack_forget()
        for btn in self.option_buttons:
            btn.pack_forget()
        self.question_index += 1
        self.show_question()

    def show_result(self):
        messagebox.showinfo("Quiz Finished", f"Your score: {self.score} out of {len(QUIZ_DATA[self.selected_category])}")
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()