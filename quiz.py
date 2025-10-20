import tkinter as tk
from tkinter import ttk


class QuizApp(tk.Tk):
	def __init__(self) -> None:
		super().__init__()
		self.title("Study Assistant Quiz")
		self.geometry("600x400")
		self.resizable(False, False)

		self.container = ttk.Frame(self)
		self.container.pack(fill=tk.BOTH, expand=True)

		self.frames: dict[str, tk.Frame] = {}
		for FrameClass in (StartFrame, QuestionFrame, ScoreFrame):
			frame = FrameClass(parent=self.container, controller=self)
			self.frames[FrameClass.__name__] = frame
			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame("StartFrame")

	def show_frame(self, name: str) -> None:
		frame = self.frames[name]
		frame.tkraise()


class StartFrame(ttk.Frame):
	def __init__(self, parent: tk.Widget, controller: QuizApp) -> None:
		super().__init__(parent)
		self.controller = controller

		title = ttk.Label(self, text="Welcome to the Quiz", font=("Segoe UI", 20, "bold"))
		title.pack(pady=20)

		info = ttk.Label(
			self,
			text=(
				"You will answer 5 questions.\n"
				"Questions are multiple choice. Your score will be shown at the end."
			),
			justify=tk.CENTER,
		)
		info.pack(pady=10)

		start_btn = ttk.Button(self, text="Start Quiz", command=self.start_quiz)
		start_btn.pack(pady=30)

	def start_quiz(self) -> None:
		self.controller.show_frame("QuestionFrame")


class QuestionFrame(ttk.Frame):
	def __init__(self, parent: tk.Widget, controller: QuizApp) -> None:
		super().__init__(parent)
		self.controller = controller

		placeholder = ttk.Label(self, text="Question screen placeholder", font=("Segoe UI", 12))
		placeholder.pack(pady=20)

		go_score = ttk.Button(self, text="Go to Score (temp)", command=self.to_score)
		go_score.pack(pady=10)

	def to_score(self) -> None:
		self.controller.show_frame("ScoreFrame")


class ScoreFrame(ttk.Frame):
	def __init__(self, parent: tk.Widget, controller: QuizApp) -> None:
		super().__init__(parent)
		self.controller = controller

		label = ttk.Label(self, text="Score screen placeholder", font=("Segoe UI", 12))
		label.pack(pady=20)

		back_btn = ttk.Button(self, text="Back to Start", command=self.back_to_start)
		back_btn.pack(pady=10)

	def back_to_start(self) -> None:
		self.controller.show_frame("StartFrame")


if __name__ == "__main__":
	app = QuizApp()
	app.mainloop()
