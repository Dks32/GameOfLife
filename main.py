import pyray as pr


class Game:
	def __init__(self):
		pr.init_window(800, 600, 'Game of Life')
		pr.set_target_fps(120)
		self.__iniciar_juego()

	def __iniciar_juego(self):
		self.tablero = Tablero(self, 60, 45, 12,
			pr.Color(80, 40, 160, 255), pr.Color(255, 255, 255, 32))
		self.pausa = True

	def mainloop(self):
		while not pr.window_should_close():
			self.__update()
			self.__frame()

	def __frame(self):
		pr.begin_drawing()
		self.tablero.update()
		pr.clear_background(pr.BLACK)
		pr.draw_fps(10, 10)
		self.tablero.dibujar()
		pr.end_drawing()

	def __update(self):
		if pr.is_key_released(32):
			self.pausa = not self.pausa
			self.tablero.color = pr.Color(80, 160, 40, 255) if not self.pausa else pr.Color(80, 40, 160, 255)


class Tablero:
	def __init__(self, master, width, height, block_size, color, grid_color):
		self.master = master
		self.width = width
		self.height = height
		self.block_size = block_size
		self.color = color
		self.grid_color = grid_color
		self.cells:list[list[bool]] = [[False for _ in range(width)] for _ in range(height)]
		self.pos_x = (pr.get_screen_width() - (self.block_size * self.width)) // 2
		self.pos_y = (pr.get_screen_height() - (self.block_size * self.height)) // 2
		self.selected = (-1, -1)
		self.last_tic = 0
		self.tic_time = .15
		self.pausa = False

	def set_cell(self, cell_x:int, cell_y:int, value:bool) -> None:
		cell_x %= self.width
		cell_y %= self.height
		self.cells[cell_y][cell_x] = value

	def get_cell(self, cell_x:int, cell_y:int) -> bool:
		cell_x %= self.width
		cell_y %= self.height
		return self.cells[cell_y][cell_x]

	def dibujar(self):
		tam = self.block_size
		for x in range(self.width):
			for y in range(self.height):
				pos_x = self.pos_x + (self.block_size * x)
				pos_y = self.pos_y + (self.block_size * y)
				selected = (self.selected[0] == x) and (self.selected[1] == y)
				if selected and pr.is_mouse_button_down(0):
					# self.cells[y][x] = True
					self.set_cell(x, y, True)
				if selected and pr.is_mouse_button_down(1):
					# self.cells[y][x] = False
					self.set_cell(x, y, False)
				col = self.color if self.get_cell(x, y) else pr.BLACK
				gcol = self.grid_color if not selected else pr.Color(255,255,255,128)
				pr.draw_rectangle(pos_x, pos_y, tam, tam, col)
				pr.draw_rectangle_lines(pos_x, pos_y, tam, tam, gcol)

	def update(self):
		cur_pos = pr.get_mouse_position()
		self.selected = (
			int((cur_pos.x - self.pos_x) // self.block_size),
			int((cur_pos.y - self.pos_y) // self.block_size)
		)

		if self.master.pausa:
			return

		if (pr.get_time() - self.last_tic) > self.tic_time:
			self.tic()
			self.last_tic = pr.get_time()

	def tic(self):
		nuevo_estado:list[list[bool]] = [[False for _ in range(self.width)] for _ in range(self.height)]

		for x in range(self.width):
			for y in range(self.height):
				cell = self.get_cell(x, y)
				vecinas = self.count_cells(x, y)
				if not cell and vecinas == 3:
					nuevo_estado[y][x] = True
				if cell and (1 < vecinas < 3):
					nuevo_estado[y][x] = False
				if cell and (vecinas == 2 or vecinas == 3):
					nuevo_estado[y][x] = True

		self.cells = nuevo_estado.copy()

	def count_cells(self, cell_x:int, cell_y:int) -> int:
		cell_x %= self.width
		cell_y %= self.height
		cells:int = 0
		for x in range(-1, 2):
			for y in range(-1, 2):
				if x == 0 and y == 0:
					continue
				cell:bool = self.get_cell(cell_x + x, cell_y + y)
				cells += 1 if cell else 0
		return cells

if __name__ == "__main__":
	juego = Game()
	juego.mainloop()
