class Block:
    def __init__(self, color, x, y, w, h):
        self.color = color
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.speed = 0.05
        self.moving = False
        self.health = 100
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.exp = 0
        self.expgain = 1
        self.expmax = 3
        self.level = 1

        self.points = 0

    def draw(self):
        gameDisplay.fill(self.color, rect=[self.x, self.y, self.width, self.height])

    def show_health(self):
        if player.health <= 35:
            tmp_color = Colors.red
        else:
            tmp_color = Colors.green
        gameDisplay.fill(Colors.black, rect=[10, 30, 100, 10])
        gameDisplay.fill(tmp_color, rect=[10, 30, self.health, 10])

    def auto_kill(self):
        self.health -= 2
        if self.health <= 0:
            self.health = 100

    def check_level_up(self):
        if player.exp >= player.expmax:
            player.level += 1
            player.exp = player.exp - player.expmax
            player.expmax += player.expgain
            player.expgain += 1*random.randint(1, 5)
            return True
        else:
            return False

    def level_bar(self):
        gameDisplay.fill(Colors.black, rect=[120, 30, 100, 10])
        tmp_exp = (float(player.exp) / float(player.expmax)) * 100
        gameDisplay.fill(Colors.nice_blue, rect=[120, 30, tmp_exp, 10])

    def move(self):
        if self.moving:
            Mousex, Mousey = pygame.mouse.get_pos()
            player.x += -(player.x - Mousex) * player.speed
            player.y += -(player.y - Mousey) * player.speed

            self.rect.x = self.x
            self.rect.y = self.y

    def dont_move_into_walls(self):
        if self.x <= 0:
            self.x = 0
        elif self.x >= 800 - self.width:
            self.x = 800 - self.width
        if self.y <= 0 + 50:
            self.y = 0 + 50
        elif self.y >= 600 - self.height:
            self.y = 600 - self.height