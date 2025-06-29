def print_board(board):
    print("\n")
    for i in range(3):
        print(" | ".join(board[i]))
        if i < 2:
            print("--+---+--")
    print("\n")


def create_board():
    return [["1", "2", "3"],
            ["4", "5", "6"],
            ["7", "8", "9"]]


def choose_game_mode():
    while True:
        print("Choose Game Mode:")
        print("1. Play with another player")
        print("2. Play with AI")
        mode = input("Enter 1 or 2: ").strip()
        if mode in ["1", "2"]:
            return int(mode)
        print("Invalid input. Try again.\n")


def choose_marker():
    while True:
        player_marker = input("Choose your marker (X/O): ").upper().strip()
        if player_marker in ["X", "O"]:
            ai_marker = "O" if player_marker == "X" else "X"
            return player_marker, ai_marker
        print("Invalid input. Try again.\n")


def get_position_from_box_number(box_number):
    box_number = int(box_number) - 1
    return box_number // 3, box_number % 3


def is_valid_move(board, box_number):
    if not box_number.isdigit() or not (1 <= int(box_number) <= 9):
        return False
    row, col = get_position_from_box_number(box_number)
    return board[row][col] not in ["X", "O"]


def make_move(board, marker):
    while True:
        box = input(f"Enter the box number (1-9) to place '{marker}': ").strip()
        if is_valid_move(board, box):
            row, col = get_position_from_box_number(box)
            board[row][col] = marker
            break
        else:
            print("❌ Invalid move! Try again.")


def check_winner(board, marker):
    for i in range(3):
        if all([cell == marker for cell in board[i]]):
            return True
        if all([board[j][i] == marker for j in range(3)]):
            return True
    if all([board[i][i] == marker for i in range(3)]):
        return True
    if all([board[i][2 - i] == marker for i in range(3)]):
        return True
    return False


def is_draw(board):
    return all(cell in ["X", "O"] for row in board for cell in row)


def get_available_moves(board):
    moves = []
    for i in range(3):
        for j in range(3):
            if board[i][j] not in ["X", "O"]:
                moves.append((i, j))
    return moves


def minimax(board, depth, is_maximizing, ai_marker, player_marker):
    if check_winner(board, ai_marker):
        return 10 - depth
    if check_winner(board, player_marker):
        return depth - 10
    if is_draw(board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for (i, j) in get_available_moves(board):
            board[i][j] = ai_marker
            score = minimax(board, depth + 1, False, ai_marker, player_marker)
            board[i][j] = str(i * 3 + j + 1)
            if score > best_score:
                best_score = score
        return best_score
    else:
        best_score = float('inf')
        for (i, j) in get_available_moves(board):
            board[i][j] = player_marker
            score = minimax(board, depth + 1, True, ai_marker, player_marker)
            board[i][j] = str(i * 3 + j + 1)
            if score < best_score:
                best_score = score
        return best_score


def ai_move(board, ai_marker, player_marker):
    best_score = -float('inf')
    best_move = None
    for (i, j) in get_available_moves(board):
        board[i][j] = ai_marker
        score = minimax(board, 0, False, ai_marker, player_marker)
        board[i][j] = str(i * 3 + j + 1)
        if score > best_score:
            best_score = score
            best_move = (i, j)
    if best_move:
        i, j = best_move
        board[i][j] = ai_marker
        print(f"AI places '{ai_marker}' in box {i * 3 + j + 1}")


if __name__ == "__main__":
    board = create_board()
    mode = choose_game_mode()

    if mode == 1:
        print("\n2-Player Mode Selected!\n")
        player1 = "X"
        player2 = "O"
    else:
        print("\nPlayer vs AI Mode Selected!\n")
        player1, player2 = choose_marker()
        print(f"You are '{player1}', AI is '{player2}'\n")

    current_player = player1
    print_board(board)

    while True:
        if mode == 2 and current_player == player2:
            ai_move(board, player2, player1)
        else:
            make_move(board, current_player)

        print_board(board)

        if check_winner(board, current_player):
            print(f"🎉 Player '{current_player}' wins!")
            break

        if is_draw(board):
            print("🤝 It's a draw!")
            break

        current_player = player2 if current_player == player1 else player1
