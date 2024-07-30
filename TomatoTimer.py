import tkinter as tk
import pygame

class PomodoroTimer:
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.load("alarm.mp3")

        self.root = tk.Tk()
        self.root.title("Tomato Timer")

        self.is_running = False
        self.is_work_period = True
        self.work_time = 25 * 60  # Default 25 minutes
        self.break_time = 5 * 60  # Default 5 minutes
        self.repetitions = 1  # Default 1 repetition
        self.current_repetition = 0
        self.time_left = self.work_time

        self.create_input_widgets()
        self.root.mainloop()

    def create_input_widgets(self):
        self.label = tk.Label(self.root, text="Tomato Timer", font=("Helvetica", 24))
        self.label.pack(pady=20, padx=20)

        self.work_label = tk.Label(self.root, text="Work Time (minutes):", font=("Helvetica", 14))
        self.work_label.pack(pady=5)
        self.work_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.work_entry.insert(0, "25")
        self.work_entry.pack(pady=5)

        self.break_label = tk.Label(self.root, text="Break Time (minutes):", font=("Helvetica", 14))
        self.break_label.pack(pady=5)
        self.break_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.break_entry.insert(0, "5")
        self.break_entry.pack(pady=5)

        self.reps_label = tk.Label(self.root, text="Repetitions:", font=("Helvetica", 14))
        self.reps_label.pack(pady=5)
        self.reps_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.reps_entry.insert(0, "1")
        self.reps_entry.pack(pady=5)

        self.start_button = tk.Button(self.root, text="Start", command=self.start_timer, font=("Helvetica", 14))
        self.start_button.pack(side=tk.BOTTOM, padx=20, pady=20)

    def create_timer_widgets(self):
        self.state_label = tk.Label(self.root, text="Work", font=("Helvetica", 30, "bold"))
        self.state_label.pack(side=tk.TOP, pady=10)
        
        self.time_label = tk.Label(self.root, text=self.format_time(self.time_left), font=("Helvetica", 48))
        self.time_label.pack(pady=20)

        self.reps_remaining_label = tk.Label(self.root, text=f"Repetitions Remaining: {self.repetitions - self.current_repetition}", font=("Helvetica", 14))
        self.reps_remaining_label.pack(pady=5, padx=10)

    def format_time(self, seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    def start_timer(self):
        if not self.is_running:
            try:
                self.cancel_button = tk.Button(self.root, text="Cancel", command=self.cancel_timer, font=("Helvetica", 14))
                self.cancel_button.pack(side=tk.BOTTOM, padx=20, pady=20)

                work_minutes = int(self.work_entry.get())
                break_minutes = int(self.break_entry.get())
                repetitions = int(self.reps_entry.get())
                self.work_time = work_minutes * 60
                self.break_time = break_minutes * 60
                self.repetitions = repetitions
                self.time_left = self.work_time
                self.is_running = True
                self.is_work_period = True
                self.current_repetition = 0

                # Hide input widgets and buttons
                self.label.pack_forget()
                self.work_label.pack_forget()
                self.work_entry.pack_forget()
                self.break_label.pack_forget()
                self.break_entry.pack_forget()
                self.reps_label.pack_forget()
                self.reps_entry.pack_forget()
                self.start_button.pack_forget()

                self.create_timer_widgets()
                self.countdown()
            except ValueError:
                self.time_label.config(text="Invalid Input")

    def cancel_timer(self):
        self.is_running = False
        self.is_work_period = True
        self.time_left = self.work_time

        # Destroy timer widgets if they exist
        if hasattr(self, 'time_label'):
            self.time_label.pack_forget()
            self.state_label.pack_forget()
            self.reps_remaining_label.pack_forget()
            self.cancel_button.pack_forget()

        # Show input widgets and buttons
        self.label.pack(pady=20, padx=20)
        self.work_label.pack(pady=5)
        self.work_entry.pack(pady=5)
        self.break_label.pack(pady=5)
        self.break_entry.pack(pady=5)
        self.reps_label.pack(pady=5)
        self.reps_entry.pack(pady=5)
        self.start_button.pack(side=tk.BOTTOM, padx=20, pady=20)


    def countdown(self):
        if self.is_running:
            if self.time_left > 0:
                self.time_left -= 1
                self.time_label.config(text=self.format_time(self.time_left))
                self.root.after(1000, self.countdown)
            else:
                pygame.mixer.music.play()  # Play the alarm sound
                if self.is_work_period:
                    self.current_repetition += 1
                    if self.current_repetition < self.repetitions:
                        self.is_work_period = False
                        self.time_left = self.break_time
                    else:
                        self.is_running = False
                else:
                    self.is_work_period = True
                    self.time_left = self.work_time

                self.update_state_label()
                self.update_reps_remaining_label()
                self.countdown()

    def update_state_label(self):
        if self.is_work_period:
            self.state_label.config(text="Work")

        else:
            self.state_label.config(text="Rest")

    def update_reps_remaining_label(self):
        self.reps_remaining_label.config(text=f"Repetitions Remaining: {self.repetitions - self.current_repetition}")


if __name__ == "__main__":
    PomodoroTimer()