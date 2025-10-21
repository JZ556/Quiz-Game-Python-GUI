import tkinter as tk
from tkinter import ttk


class QuizApp(tk.Tk):
	def __init__(self): 
		super().__init__()
		self.title("Study Assistant Quiz")
		self.geometry("800x800")
		self.resizable(False, False)

		self.container = ttk.Frame(self)
		self.container.pack(fill=tk.BOTH, expand=True)
		
		# Configure grid weights so frames can expand
		self.container.grid_rowconfigure(0, weight=1)
		self.container.grid_columnconfigure(0, weight=1)

		self.frames: dict[str, tk.Frame] = {}
		for FrameClass in (StartFrame, QuestionFrame, ScoreFrame):
			frame = FrameClass(parent=self.container, controller=self)
			self.frames[FrameClass.__name__] = frame
			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame("StartFrame")

	def show_frame(self, name: str): 
		frame = self.frames[name]
		frame.tkraise()


class StartFrame(ttk.Frame):
	def __init__(self, parent: tk.Widget, controller: QuizApp): 
		super().__init__(parent)
		self.controller = controller

		# Create a container frame for centering
		center_frame = ttk.Frame(self)
		center_frame.pack(expand=True, fill=tk.BOTH)

		# Center content vertically and horizontally
		center_frame.grid_rowconfigure(0, weight=1)
		center_frame.grid_columnconfigure(0, weight=1)
		
		content_frame = ttk.Frame(center_frame)
		content_frame.grid(row=0, column=0)

		title = ttk.Label(content_frame, text="Welcome to the Quiz", font=("Segoe UI", 20, "bold"))
		title.pack(pady=20)

		info = ttk.Label(
			content_frame,
			text=(
				"You will answer 5 questions.\n"
				"Questions are multiple choice. Your score will be shown at the end."
			),
			justify=tk.CENTER,
		)
		info.pack(pady=10)

		start_btn = ttk.Button(content_frame, text="Start Quiz", command=self.start_quiz)
		start_btn.pack(pady=30)

	def start_quiz(self): 
		self.controller.show_frame("QuestionFrame")


class QuestionFrame(ttk.Frame):
	def __init__(self, parent: tk.Widget, controller: QuizApp): 
		super().__init__(parent)
		self.controller = controller

		# Create a container frame for centering
		center_frame = ttk.Frame(self)
		center_frame.pack(expand=True, fill=tk.BOTH)

		# Center content vertically and horizontally
		center_frame.grid_rowconfigure(0, weight=1)
		center_frame.grid_columnconfigure(0, weight=1)
		
		content_frame = ttk.Frame(center_frame)
		content_frame.grid(row=0, column=0)

		placeholder = ttk.Label(content_frame, text="Question screen placeholder", font=("Segoe UI", 12))
		placeholder.pack(pady=20)

		go_score = ttk.Button(content_frame, text="Go to Score (temp)", command=self.to_score)
		go_score.pack(pady=10)

	def to_score(self):
		self.controller.show_frame("ScoreFrame")


class ScoreFrame(ttk.Frame):
	def __init__(self, parent: tk.Widget, controller: QuizApp): 
		super().__init__(parent)
		self.controller = controller

		# Create a container frame for centering
		center_frame = ttk.Frame(self)
		center_frame.pack(expand=True, fill=tk.BOTH)

		# Center content vertically and horizontally
		center_frame.grid_rowconfigure(0, weight=1)
		center_frame.grid_columnconfigure(0, weight=1)
		
		content_frame = ttk.Frame(center_frame)
		content_frame.grid(row=0, column=0)

		label = ttk.Label(content_frame, text="Score screen placeholder", font=("Segoe UI", 12))
		label.pack(pady=20)

		back_btn = ttk.Button(content_frame, text="Back to Start", command=self.back_to_start)
		back_btn.pack(pady=10)

	def back_to_start(self):
		self.controller.show_frame("StartFrame")


if __name__ == "__main__":
	app = QuizApp()
	app.mainloop()
