import tkinter as tk
from tkinter import ttk
import random
from dataclasses import dataclass
from typing import List, Union


@dataclass
class Question:
	"""Question model supporting both multiple choice and short answer types"""
	text: str
	question_type: str  # "mcq" or "short_answer"
	options: List[str] = None  # For MCQ questions
	correct_answer: Union[int, str] = None  # Index for MCQ, string for short answer
	explanation: str = ""


# Sample questions - 7 total, we'll pick 5 randomly each time
QUESTIONS = [
	# 5 Multiple Choice Questions
	Question(
		text="What is the output of: print(2 + 3 * 4)",
		question_type="mcq",
		options=["14", "20", "11", "24"],
		correct_answer=0,  # 14
		explanation="Order of operations: multiplication first (3*4=12), then addition (2+12=14)"
	),
	Question(
		text="Which keyword is used to define a function in Python?",
		question_type="mcq",
		options=["function", "def", "define", "func"],
		correct_answer=1,  # def
		explanation="The 'def' keyword is used to define functions in Python"
	),
	Question(
		text="Which data type is mutable in Python?",
		question_type="mcq",
		options=["tuple", "string", "list", "int"],
		correct_answer=2,  # list
		explanation="Lists are mutable (can be changed), while tuples, strings, and ints are immutable"
	),
	Question(
		text="Which method adds an item to the end of a list?",
		question_type="mcq",
		options=["append()", "add()", "insert()", "push()"],
		correct_answer=0,  # append()
		explanation="The append() method adds an item to the end of a list"
	),
	Question(
		text="What is the value of x after: x = 5",
		question_type="mcq",
		options=["5", "x", "None", "Error"],
		correct_answer=0,  # 5
		explanation="The variable x is assigned the value 5"
	),
	# 2 Short Answer Questions
	Question(
		text="What will this code output: a=10, b=20, c=a+b",
		question_type="short_answer",
		correct_answer="30",
		explanation="Simple addition: 10 + 20 = 30"
	),
	Question(
		text="What is the result of: 15 // 4",
		question_type="short_answer",
		correct_answer="3",
		explanation="Floor division (//) returns the integer part: 15 ÷ 4 = 3.75, so 15 // 4 = 3"
	)
]


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

		# Quiz state
		self.quiz_questions = []
		self.current_question_index = 0
		self.selected_answers = []
		self.start_time = None
		self.timer_seconds = 180  # 3 minutes = 180 seconds
		self.timer_job = None

		self.frames: dict[str, tk.Frame] = {}
		for FrameClass in (StartFrame, QuestionFrame, ScoreFrame):
			frame = FrameClass(parent=self.container, controller=self)
			self.frames[FrameClass.__name__] = frame
			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame("StartFrame")

	def show_frame(self, name: str): 
		frame = self.frames[name]
		frame.tkraise()

	def start_quiz(self):
		"""Initialize quiz with 5 random questions"""
		# Pick 5 random questions from the 7 available
		self.quiz_questions = random.sample(QUESTIONS, 5)
		
		# Reset quiz state
		self.current_question_index = 0
		self.selected_answers = [None] * 5
		self.start_time = None
		
		# Go to first question
		self.show_frame("QuestionFrame")
		self.frames["QuestionFrame"].display_question()
		
		# Start the timer
		self.start_timer()

	def start_timer(self):
		"""Start the 3-minute countdown timer"""
		self.timer_seconds = 180  # Reset to 3 minutes
		self.update_timer()

	def update_timer(self):
		"""Update the timer display and check if time is up"""
		if self.timer_seconds > 0:
			# Update timer display in QuestionFrame
			if hasattr(self.frames["QuestionFrame"], 'update_timer_display'):
				self.frames["QuestionFrame"].update_timer_display(self.timer_seconds)
			
			# Schedule next update in 1 second
			self.timer_job = self.after(1000, self.update_timer)
			self.timer_seconds -= 1
		else:
			# Time's up! End the quiz
			self.end_quiz_by_timer()

	def end_quiz_by_timer(self):
		"""End the quiz when timer runs out"""
		# Cancel any pending timer updates
		if self.timer_job:
			self.after_cancel(self.timer_job)
			self.timer_job = None
		
		# Go to score screen
		self.show_frame("ScoreFrame")
		self.frames["ScoreFrame"].display_score()

	def stop_timer(self):
		"""Stop the timer (when quiz is completed normally)"""
		if self.timer_job:
			self.after_cancel(self.timer_job)
			self.timer_job = None


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
		self.controller.start_quiz()


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
		
		self.content_frame = ttk.Frame(center_frame)
		self.content_frame.grid(row=0, column=0)

		# Widgets will be created in display_question()
		self.question_label = None
		self.radio_var = None
		self.radio_buttons = []
		self.entry_var = None
		self.entry = None
		self.progress_label = None
		self.timer_label = None

	def display_question(self):
		"""Display the current question"""
		# Clear previous widgets (except timer)
		for widget in self.content_frame.winfo_children():
			if widget != self.timer_label:  # Keep timer label
				widget.destroy()
		
		# Get current question
		question = self.controller.quiz_questions[self.controller.current_question_index]
		
		# Create timer display only if it doesn't exist
		if not self.timer_label:
			self.timer_label = ttk.Label(
				self.content_frame, 
				text="Time: 3:00",
				font=("Segoe UI", 12, "bold"),
				foreground="red"
			)
			self.timer_label.pack(pady=5)
		
		# Progress indicator
		remaining = 5 - self.controller.current_question_index
		self.progress_label = ttk.Label(
			self.content_frame, 
			text=f"{remaining} more questions to go",
			font=("Segoe UI", 12, "bold")
		)
		self.progress_label.pack(pady=10)
		
		# Question text
		self.question_label = ttk.Label(
			self.content_frame, 
			text=question.text,
			font=("Segoe UI", 14),
			wraplength=500,
			justify=tk.CENTER
		)
		self.question_label.pack(pady=20)
		
		# Create answer widgets based on question type
		if question.question_type == "mcq":
			self.create_mcq_widgets(question)
		else:  # short_answer
			self.create_short_answer_widgets(question)

	def create_mcq_widgets(self, question):
		"""Create radio buttons for MCQ questions"""
		self.radio_var = tk.IntVar()
		self.radio_buttons = []
		
		for i, option in enumerate(question.options):
			radio = ttk.Radiobutton(
				self.content_frame,
				text=option,
				variable=self.radio_var,
				value=i,
				command=self.on_answer_selected
			)
			radio.pack(pady=5)
			self.radio_buttons.append(radio)

	def create_short_answer_widgets(self, question):
		"""Create text entry for short answer questions"""
		self.entry_var = tk.StringVar()
		self.entry = ttk.Entry(
			self.content_frame,
			textvariable=self.entry_var,
			font=("Segoe UI", 12),
			width=20
		)
		self.entry.pack(pady=20)
		self.entry.bind('<Return>', lambda e: self.on_answer_selected())
		self.entry.focus()

	def on_answer_selected(self):
		"""Handle when user selects an answer"""
		question = self.controller.quiz_questions[self.controller.current_question_index]
		
		# Get the answer
		if question.question_type == "mcq":
			answer = self.radio_var.get()
		else:  # short_answer
			answer = self.entry_var.get().strip()
		
		# Store the answer
		self.controller.selected_answers[self.controller.current_question_index] = answer
		
		# Auto-advance to next question or finish quiz
		self.controller.current_question_index += 1
		
		if self.controller.current_question_index < 5:
			# More questions - show next one
			self.display_question()
		else:
			# Quiz finished - stop timer and go to score screen
			self.controller.stop_timer()
			self.controller.show_frame("ScoreFrame")
			self.controller.frames["ScoreFrame"].display_score()

	def update_timer_display(self, seconds_remaining):
		"""Update the timer display with remaining time"""
		if self.timer_label:
			minutes = seconds_remaining // 60
			seconds = seconds_remaining % 60
			time_text = f"Time: {minutes}:{seconds:02d}"
			self.timer_label.config(text=time_text)
			
			# Change color to red when time is running low
			if seconds_remaining <= 30:
				self.timer_label.config(foreground="red")
			elif seconds_remaining <= 60:
				self.timer_label.config(foreground="orange")
			else:
				self.timer_label.config(foreground="black")


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
		
		self.content_frame = ttk.Frame(center_frame)
		self.content_frame.grid(row=0, column=0)

		# Do not display score immediately; it will be rendered when navigated to

	def display_score(self):
		"""Calculate and display the quiz score"""
		# Clear previous contents (in case of multiple runs back to this frame)
		for widget in self.content_frame.winfo_children():
			widget.destroy()

		# Calculate score
		correct_count = 0
		total_questions = len(self.controller.quiz_questions)
		if total_questions == 0:
			# Defensive guard: nothing to score yet
			notice = ttk.Label(self.content_frame, text="No quiz results to display.", font=("Segoe UI", 12))
			notice.pack(pady=20)
			back_btn = ttk.Button(self.content_frame, text="Back to Start", command=self.back_to_start)
			back_btn.pack(pady=10)
			return
		
		for i, question in enumerate(self.controller.quiz_questions):
			user_answer = self.controller.selected_answers[i]
			correct_answer = question.correct_answer
			
			# Check if answer is correct
			if question.question_type == "mcq":
				# For MCQ, compare the selected index
				if user_answer == correct_answer:
					correct_count += 1
			else:  # short_answer
				# For short answer, compare the string (case-insensitive)
				if str(user_answer).strip().lower() == str(correct_answer).strip().lower():
					correct_count += 1
		
		# Display results - simple score only
		title = ttk.Label(
			self.content_frame, 
			text="Quiz Complete!", 
			font=("Segoe UI", 20, "bold")
		)
		title.pack(pady=20)
		
		score_text = ttk.Label(
			self.content_frame, 
			text=f"Your Score: {correct_count}/{total_questions}",
			font=("Segoe UI", 16, "bold")
		)
		score_text.pack(pady=30)
		
		# Back to start button
		back_btn = ttk.Button(
			self.content_frame, 
			text="Back to Start", 
			command=self.back_to_start
		)
		back_btn.pack(pady=20)

	def back_to_start(self):
		self.controller.show_frame("StartFrame")


if __name__ == "__main__":
	app = QuizApp()
	app.mainloop()
