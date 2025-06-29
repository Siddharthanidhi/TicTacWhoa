import tkinter as tk
from tkinter import messagebox

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Tic-Tac-Toe Deluxe 🎮")
        self.root.config(bg="#1f1f2e")
        self.board = [str(i) for i in range(1, 10)]
        self.buttons = []
        self.current_player = None
        self.player_marker = None
        self.ai_marker = None
        self.mode = None

        self.create_mode_selection()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_mode_selection(self):
        self.clear_screen()
        label = tk.Label(self.root, text="Choose Game Mode", font=("Comic Sans MS", 24, "bold"), fg="#61dafb", bg="#1f1f2e")
        label.pack(pady=20)

        btn_2player = tk.Button(self.root, text="👥 2 Player", font=("Comic Sans MS", 18), bg="#21bf73", fg="white",
                                activebackground="#17a355", width=15, command=lambda: self.start_game(1))
        btn_2player.pack(pady=10)

        btn_ai = tk.Button(self.root, text="🤖 Play vs AI", font=("Comic Sans MS", 18), bg="#eb5160", fg="white",
                           activebackground="#cc3c49", width=15, command=self.choose_marker_ui)
        btn_ai.pack(pady=10)

    def choose_marker_ui(self):
        self.clear_screen()
        label = tk.Label(self.root, text="Choose Your Marker", font=("Comic Sans MS", 22, "bold"), fg="#61dafb", bg="#1f1f2e")
        label.pack(pady=20)

        btn_x = tk.Button(self.root, text="X", font=("Comic Sans MS", 18), bg="#ff6f61", fg="white",
                          activebackground="#e45549", width=10, command=lambda: self.choose_first_turn_ui("X"))
        btn_x.pack(pady=10)

        btn_o = tk.Button(self.root, text="O", font=("Comic Sans MS", 18), bg="#6f86d6", fg="white",
                          activebackground="#576eb5", width=10, command=lambda: self.choose_first_turn_ui("O"))
        btn_o.pack(pady=10)

    def choose_first_turn_ui(self, marker):
        self.player_marker = marker
        self.ai_marker = "O" if marker == "X" else "X"

        self.clear_screen()
        label = tk.Label(self.root, text="Who Should Go First?", font=("Comic Sans MS", 22, "bold"), fg="#61dafb", bg="#1f1f2e")
        label.pack(pady=20)

        btn_you = tk.Button(self.root, text="🧑 You", font=("Comic Sans MS", 18), bg="#4CAF50", fg="white",
                            activebackground="#45a049", width=12,
                            command=lambda: self.start_game(2, self.player_marker, True))
        btn_you.pack(pady=10)

        btn_ai = tk.Button(self.root, text="🤖 AI", font=("Comic Sans MS", 18), bg="#f44336", fg="white",
                           activebackground="#e53935", width=12,
                           command=lambda: self.start_game(2, self.player_marker, False))
        btn_ai.pack(pady=10)

    def start_game(self, mode, player_marker=None, player_starts=True):
        self.mode = mode
        self.board = [str(i) for i in range(1, 10)]
        self.clear_screen()
        self.create_board_ui()

        if mode == 1:
            self.player_marker = "X"
            self.ai_marker = "O"
            self.current_player = "X"
            self.status_label.config(text="2 Player Mode: Player X's Turn", fg="white")
        else:
            self.player_marker = player_marker
            self.ai_marker = "O" if player_marker == "X" else "X"
            self.current_player = self.player_marker if player_starts else self.ai_marker
            self.status_label.config(
                text=f"Player '{self.player_marker}' vs AI '{self.ai_marker}'\nPlayer '{self.current_player}' starts", fg="#f1fa8c")

            if self.current_player == self.ai_marker:
                def ai_then_switch():
                    self.ai_move()
                    self.current_player = self.player_marker
                    self.status_label.config(
                        text=f"Player '{self.player_marker}' vs AI '{self.ai_marker}'\nPlayer '{self.current_player}' turn")
                self.root.after(600, ai_then_switch)

    def create_board_ui(self):
        frame = tk.Frame(self.root, bg="#1f1f2e")
        frame.pack(pady=20)

        self.buttons = []
        for i in range(9):
            btn = tk.Button(frame, text="", font=("Comic Sans MS", 36, "bold"), bg="#282c34", fg="white",
                            activebackground="#44475a", width=4, height=2,
                            command=lambda i=i: self.player_move(i))
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(btn)

        self.status_label = tk.Label(self.root, text="", font=("Comic Sans MS", 18), bg="#1f1f2e", fg="white")
        self.status_label.pack(pady=10)

        self.restart_button = tk.Button(self.root, text="🔁 Restart", font=("Comic Sans MS", 16), bg="#61dafb", fg="#282c34",
                                        activebackground="#21bf73", width=12, command=self.create_mode_selection)
        self.restart_button.pack(pady=10)

    def player_move(self, index):
        if self.board[index] in ["X", "O"] or (self.mode == 2 and self.current_player != self.player_marker):
            return

        self.make_move(index, self.current_player)

        if self.check_winner(self.current_player):
            self.animate_winner(index)
            messagebox.showinfo("🎉 Game Over", f"Player '{self.current_player}' wins! 🎉")
            self.disable_buttons()
            return
        elif self.is_draw():
            messagebox.showinfo("🤝 Game Over", "It's a draw! 🤝")
            self.disable_buttons()
            return

        self.switch_player()

        if self.mode == 2 and self.current_player == self.ai_marker:
            self.root.after(600, self.ai_move)

    def ai_move(self):
        move = self.best_move()
        if move is not None:
            self.make_move(move, self.ai_marker)

            if self.check_winner(self.ai_marker):
                self.animate_winner(move)
                messagebox.showinfo("🤖 Game Over", "AI wins! 🤖")
                self.disable_buttons()
                return
            elif self.is_draw():
                messagebox.showinfo("🤝 Game Over", "It's a draw! 🤝")
                self.disable_buttons()
                return

            self.switch_player()

    def make_move(self, index, marker):
        self.board[index] = marker
        self.buttons[index].config(text=marker, bg="#21bf73" if marker == self.player_marker else "#eb5160")

    def animate_winner(self, win_index):
        for _ in range(3):
            self.root.after(100, lambda: self.buttons[win_index].config(bg="#ffe066"))
            self.root.update()
            self.root.after(100, lambda: self.buttons[win_index].config(bg="#eb5160" if self.current_player == self.ai_marker else "#21bf73"))
            self.root.update()

    def switch_player(self):
        self.current_player = self.ai_marker if self.current_player == self.player_marker else self.player_marker
        if self.mode == 1:
            self.status_label.config(text=f"Player '{self.current_player}' turn", fg="white")
        else:
            self.status_label.config(text=f"Player '{self.player_marker}' vs AI '{self.ai_marker}'\nPlayer '{self.current_player}' turn", fg="#f1fa8c")

    def check_winner(self, marker):
        b = self.board
        lines = [
            [b[0], b[1], b[2]],
            [b[3], b[4], b[5]],
            [b[6], b[7], b[8]],
            [b[0], b[3], b[6]],
            [b[1], b[4], b[7]],
            [b[2], b[5], b[8]],
            [b[0], b[4], b[8]],
            [b[2], b[4], b[6]],
        ]
        return [marker] * 3 in lines

    def is_draw(self):
        return all(pos in ["X", "O"] for pos in self.board)

    def disable_buttons(self):
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)

    def best_move(self):
        def minimax(board, is_maximizing):
            if self.check_winner(self.ai_marker):
                return 10
            elif self.check_winner(self.player_marker):
                return -10
            elif self.is_draw():
                return 0

            if is_maximizing:
                best_score = -float('inf')
                for i in range(9):
                    if board[i] not in ["X", "O"]:
                        temp = board[i]
                        board[i] = self.ai_marker
                        score = minimax(board, False)
                        board[i] = temp
                        best_score = max(score, best_score)
                return best_score
            else:
                best_score = float('inf')
                for i in range(9):
                    if board[i] not in ["X", "O"]:
                        temp = board[i]
                        board[i] = self.player_marker
                        score = minimax(board, True)
                        board[i] = temp
                        best_score = min(score, best_score)
                return best_score

        best_score = -float('inf')
        move = None
        for i in range(9):
            if self.board[i] not in ["X", "O"]:
                temp = self.board[i]
                self.board[i] = self.ai_marker
                score = minimax(self.board, False)
                self.board[i] = temp
                if score > best_score:
                    best_score = score
                    move = i
        return move

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeGUI(root)
    root.mainloop()


