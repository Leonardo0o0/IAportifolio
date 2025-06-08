##Verifica se é seguro colocar uma rainha
def is_safe(board, row, col, n):
    
    for i in range(col):
        if board[row][i] == 1:
            return False

    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False

    for i, j in zip(range(row, n, 1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False

    return True

## Função recursiva para resolver o problema das N-Rainhas usando backtracking.
def solve_n_queens_util(board, col, n):

    # Caso base: Se todas as rainhas foram colocadas, retorna True
    if col >= n:
        return True

    for i in range(n):
        if is_safe(board, i, col, n):
            board[i][col] = 1

            if solve_n_queens_util(board, col + 1, n):
                return True

            # Se colocar a rainha em board[i][col] não levar a uma solução então remove a rainha (BACKTRACK)
            board[i][col] = 0

    # Se a rainha não pode ser colocada em nenhuma linha nesta coluna, retorna False
    return False
## inicializa o tabuleiro e chama a função de backtracking
def solve_n_queens(n):

    board = [[0 for _ in range(n)] for _ in range(n)]

    if not solve_n_queens_util(board, 0, n):
        print("Não existe solução")
        return False

    print("Solução encontrada:")
    for row in board:
        print(" ".join(map(str, row)))
    return True

# Exemplos
solve_n_queens(8)
solve_n_queens(16)