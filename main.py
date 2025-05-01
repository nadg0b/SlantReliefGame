import curses


class FontGame(object):
    def __init__(self):
        self._screen = None

        self.running = False

        self.map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
                    [1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
                    [1, 0, 3, 0, 3, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
                    [1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                    [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
        
        self.map_maxY = len(self.map)-1
        self.map_maxX = len(self.map[0])-1

        self.player_Y = 1
        self.player_X = 1

        self.player_pos = [1, 1]
    

    def curses_init(self):
        curses.noecho()
        curses.cbreak()
        curses.curs_set(False)

        curses.start_color()
        curses.use_default_colors()
        for i in range(0, 255):
            curses.init_pair(i + 1, i, -1)

        self._screen.keypad(True)
        self._screen.nodelay(True)
        self._screen.idcok(False)
        self._screen.idlok(False)


    def draw_block(self, y, x, color):
        self._screen.addch(y,   x,   '\u002F', color)
        self._screen.addch(y,   x+1, '\u005c', color)
        self._screen.addch(y,   x+2, '\u005c', color)
        self._screen.addch(y,   x+3, '\u005c', color)

        self._screen.addch(y+1, x,   '\u005c', color)
        self._screen.addch(y+1, x+1, '\u002F', color)
        self._screen.addch(y+1, x+2, '\u002F', color)
        self._screen.addch(y+1, x+3, '\u002F', color) 


    def draw_environment(self):
        for y, line in enumerate(self.map):
            for x, tile in reversed(list(enumerate(line))):
                if tile == 1:
                    self.draw_block(y, x*3+y, curses.color_pair(197))
                if tile == 2:
                    self.draw_block(y, x*3+y, curses.color_pair(47))
                if tile == 3:
                    self.draw_block(y, x*3+y, curses.color_pair(22))


    def draw_player(self):
        self.player_Y = max(0, self.player_Y)
        self.player_Y = min(self.map_maxY, self.player_Y)

        self.player_X = max(0, self.player_X)
        self.player_X = min(self.map_maxX, self.player_X)

        self._screen.addch(self.player_Y, self.player_X*3+self.player_Y, 'A')


    def move(self, dy=0, dx=0):
        next_entity = self.map[self.player_Y+dy][self.player_X+dx]
        if next_entity == 0:
            self.player_Y += dy
            self.player_X += dx
        elif next_entity == 3:
            count = 1
            can_move = False
            while True:
                next = self.map[self.player_Y+dy*(count+1)][self.player_X+dx*(count+1)]
                if next == 3:
                    count += 1
                    continue
                if next == 0:
                    can_move = True
                    break
                if next == 1:
                    break
            if can_move:
                for c in range(count+1, 0, -1):
                    self.map[self.player_Y+dy*c][self.player_X+dx*c] = self.map[self.player_Y+dy*(c-1)][self.player_X+dx*(c-1)]
                self.player_Y += dy
                self.player_X += dx

    def update(self):
        key = self._screen.getch() 
        
        prev_pos_Y = self.player_Y
        prev_pos_X = self.player_X

        if key == curses.KEY_UP:
            self.move(-1, 0)
                
        if key == curses.KEY_DOWN:
            self.move(1, 0)

        if key == curses.KEY_LEFT:
            self.move(0, -1)

        if key == curses.KEY_RIGHT:
            self.move(0, 1)

        if key == 27:
            self.running = False
        
        self.map[prev_pos_Y   ][prev_pos_X   ] = 0
        self.map[self.player_Y][self.player_X] = 2
        # self._screen.addstr(28, 0, f"{self.player_X}:{self.player_Y}")
        # self._screen.refresh()


    def render(self):
        self._screen.erase()
        self.draw_environment()
        
        self._screen.refresh()
        curses.napms(30)


    def _run(self, screen):
        if self._screen == None:
            self._screen = screen
        self._screen_maxY = self._screen.getmaxyx()[0]
        self._screen_maxX = self._screen.getmaxyx()[1]

        self._screen.bkgd('_', curses.color_pair(8))

        self.curses_init()

        self.running = True
        while self.running:
            self.update()
            self.render()


    def run(self):
        from curses import wrapper
        wrapper(self._run)
            

# if key == curses.KEY_RESIZE:
#     curses.resize_term(*screen.getmaxyx())
#     screen.clear()
#     screen.addstr(0, 0, f"{str(screen.getmaxyx())}")
#     screen.refresh()


def main():
    fg = FontGame()
    fg.run()


if __name__ == "__main__":
    main()
