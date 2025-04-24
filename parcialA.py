import tkinter as tk
from tkinter import simpledialog, messagebox
import random

# ---------------------------- OPERACIONES DE MATRICES ----------------------------
class MatrixOperations:
    @staticmethod
    def transpose(matrix):
        filas = len(matrix)
        columnas = len(matrix[0])
        MatrixOperations.steps = ["Matriz original:", MatrixOperations.format_matrix(matrix), "Transpuesta:"]
        result = [[matrix[j][i] for j in range(filas)] for i in range(columnas)]
        MatrixOperations.steps.append(MatrixOperations.format_matrix(result))
        return result

    @staticmethod
    def inverse(matrix):
        n = len(matrix)
        identity = [[float(i == j) for i in range(n)] for j in range(n)]
        steps = ["Matriz original:", MatrixOperations.format_matrix(matrix), "Inicializamos la matriz identidad:", MatrixOperations.format_matrix(identity)]

        for i in range(n):
            factor = matrix[i][i]
            if factor == 0:
                raise Exception("No se puede calcular la inversa (división por cero).")
            for j in range(n):
                matrix[i][j] /= factor
                identity[i][j] /= factor
            steps.append(f"Hacemos que el pivote {i+1},{i+1} sea 1 dividiendo toda la fila {i+1} por {factor}")
            steps.append(MatrixOperations.format_matrix(identity))

            for k in range(n):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(n):
                        matrix[k][j] -= factor * matrix[i][j]
                        identity[k][j] -= factor * identity[i][j]
                    steps.append(f"Restamos {factor} veces la fila {i+1} de la fila {k+1}")
                    steps.append(MatrixOperations.format_matrix(identity))
        MatrixOperations.steps = steps + ["Matriz inversa:", MatrixOperations.format_matrix(identity)]
        return identity

    @staticmethod
    def add(matrix1, matrix2):
        rows = len(matrix1)
        cols = len(matrix1[0])
        MatrixOperations.steps = ["Matriz A:", MatrixOperations.format_matrix(matrix1), "Matriz B:", MatrixOperations.format_matrix(matrix2), "Suma elemento a elemento:"]
        result = []
        for i in range(rows):
            row = []
            for j in range(cols):
                row.append(matrix1[i][j] + matrix2[i][j])
                MatrixOperations.steps.append(f"{matrix1[i][j]} + {matrix2[i][j]} = {row[-1]}")
            result.append(row)
        MatrixOperations.steps += ["Resultado:", MatrixOperations.format_matrix(result)]
        return result

    @staticmethod
    def subtract(matrix1, matrix2):
        rows = len(matrix1)
        cols = len(matrix1[0])
        MatrixOperations.steps = ["Matriz A:", MatrixOperations.format_matrix(matrix1), "Matriz B:", MatrixOperations.format_matrix(matrix2), "Resta elemento a elemento:"]
        result = []
        for i in range(rows):
            row = []
            for j in range(cols):
                row.append(matrix1[i][j] - matrix2[i][j])
                MatrixOperations.steps.append(f"{matrix1[i][j]} - {matrix2[i][j]} = {row[-1]}")
            result.append(row)
        MatrixOperations.steps += ["Resultado:", MatrixOperations.format_matrix(result)]
        return result

    @staticmethod
    def multiply(matrix1, matrix2):
        MatrixOperations.steps = ["Matriz A:", MatrixOperations.format_matrix(matrix1), "Matriz B:", MatrixOperations.format_matrix(matrix2), "Multiplicación de matrices:"]
        result = []
        for i in range(len(matrix1)):
            row = []
            for j in range(len(matrix2[0])):
                total = 0
                formula = []
                for k in range(len(matrix2)):
                    partial = matrix1[i][k] * matrix2[k][j]
                    total += partial
                    formula.append(f"{matrix1[i][k]}*{matrix2[k][j]}")
                row.append(total)
                MatrixOperations.steps.append(f"Elemento {i+1},{j+1}: {' + '.join(formula)} = {total}")
            result.append(row)
        MatrixOperations.steps += ["Resultado:", MatrixOperations.format_matrix(result)]
        return result

    @staticmethod
    def format_matrix(matrix):
        return '\n'.join(['\t'.join(f"{val:.2f}" for val in row) for row in matrix])

# ---------------------------- APLICACIÓN PRINCIPAL ----------------------------
class MatrixApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x400")  # Ancho x Alto
        self.root.configure(bg="beige")
        self.root.title("Calculadora y Juego de Matrices")

        tk.Label(root, text="\n \n Selecciona una opción:").pack()

        tk.Button(root, text="\n \n         Calculadora de Matrices             ", command=self.matrix_calculator).pack(pady=40)
        tk.Button(root, text="\n \n        Juego de Adivinanza de Matriz           ", command=self.guessing_game).pack(pady=40)

    def matrix_calculator(self):
        operations = ["Transpuesta", "Inversa", "Suma", "Resta", "Multiplicación"]
        choice = simpledialog.askstring("Operación", f"Selecciona una operación:\n{', '.join(operations)}")

        if choice not in operations:
            messagebox.showerror("no hay nada en el espacio porfavor rellenalo otra vez", "\nOperación inválida")
            return

        filas = simpledialog.askinteger("Dimensiones", "Filas de la matriz:")
        columnas = simpledialog.askinteger("Dimensiones", "Columnas de la matriz:")

        matrix1 = self.input_matrix(filas, columnas , "Matriz A")

        if choice in ["Suma", "Resta", "Multiplicación"]:
            matrix2 = self.input_matrix(filas, columnas if choice != "Multiplicación" else filas, "Matriz B")

        try:
            if choice == "Transpuesta":
                result = MatrixOperations.transpose(matrix1)
                steps = MatrixOperations.steps
            elif choice == "Inversa":
                if filas != columnas :
                    raise Exception("La matriz debe ser cuadrada.")
                result = MatrixOperations.inverse([row[:] for row in matrix1])
                steps = MatrixOperations.steps
            elif choice == "Suma":
                result = MatrixOperations.add(matrix1, matrix2)
                steps = MatrixOperations.steps
            elif choice == "Resta":
                result = MatrixOperations.subtract(matrix1, matrix2)
                steps = MatrixOperations.steps
            elif choice == "Multiplicación":
                result = MatrixOperations.multiply(matrix1, matrix2)
                steps = MatrixOperations.steps

            self.show_matrix(result, f"Resultado de {choice}")
            self.show_procedure("\n".join(steps))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def input_matrix(self, rows, cols, name):
        matrix = []
        for i in range(rows):
            row = []
            for j in range(cols):
                val = simpledialog.askfloat(f"{name}", f"Valor en {i+1},{j+1}:")
                row.append(val)
            matrix.append(row)
        return matrix

    def show_matrix(self, matrix, title):
        result_str = f"{title}\n"
        for row in matrix:
            result_str += "\t".join(f"{val:.2f}" for val in row) + "\n"
        messagebox.showinfo(title, result_str)

    def show_procedure(self, text):
        top = tk.Toplevel(self.root)
        top.title("Procedimiento paso a paso")
        text_widget = tk.Text(top, wrap=tk.WORD)
        text_widget.insert(tk.END, text)
        text_widget.pack(expand=True, fill=tk.BOTH)
        tk.Button(top, text="Cerrar", command=top.destroy).pack(pady=5)

    def guessing_game(self):
        size_choice = simpledialog.askinteger("Juego", "¿Qué tamaño de matriz quieres adivinar? (2 a 4)")
        if not (2 <= size_choice <= 4):
            messagebox.showerror("Error", "Tamaño no válido")
            return

        matrix = [[random.randint(1, 9) for _ in range(size_choice)] for _ in range(size_choice)]
        masked = [row[:] for row in matrix]
        blanks = random.sample(range(size_choice ** 2), k=size_choice)
        options = list(set([random.randint(1, 9) for _ in range(10)] + [val for row in matrix for val in row]))
        random.shuffle(options)

        for i in blanks:
            r, c = divmod(i, size_choice)
            masked[r][c] = 0

        msg = "Adivina los números faltantes (0 representa un valor oculto):\n"
        for row in masked:
            msg += "\t".join(str(val) for val in row) + "\n"
        msg += "\nOpciones posibles: " + ", ".join(map(str, options))

        messagebox.showinfo("Juego de Adivinanza", msg)

# ---------------------------- INICIAR APLICACIÓN ----------------------------
root = tk.Tk()
app = MatrixApp(root)
root.mainloop()

#santiago fonseca y joseph helmont 