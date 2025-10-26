import pgzrun
import random

WIDTH = 800
HEIGHT = 600
TILE_SIZE = 48
MAP_HEIGHT = HEIGHT//TILE_SIZE
MAP_WIDTH = WIDTH//TILE_SIZE

botao_comecar = Actor("botoes_0", (WIDTH//2, 250))
botao_sair = Actor("botoes_2", (WIDTH//2, 350))
botao_musica = Actor("som_0_ligado", (WIDTH//2+27, 436))
botao_efeitos = Actor("som_ligado", (WIDTH//2-25, 436))

musica_ativa = True
efeitos_ativos = True
estado_jogo = "menu"

player_ani = {
    "parado": ["player_parado0", "player_parado1", "player_parado2", "player_parado3"],
    "andando": ["player_andando0", "player_andando1", "player_andando2", "player_andando3"],
    "dano": ["player_dano0", "player_dano1", "player_dano2", "player_dano3"],
    "morte": ["player_morte0", "player_morte1", "player_morte2", "player_morte3"],
    "ataque1": ["player_ataque1_0", "player_ataque1_1", "player_ataque1_2", "player_ataque1_3", "player_ataque1_4"]
}
jogador = Actor("player_parado0", (WIDTH//2, HEIGHT//2))
jogador.vida = 10
jogador.estado_ani = "parado"
jogador.frame_atual = 0
jogador.tempo_ani = 0
jogador.velocidade = 2
jogador.tempo_inv = 0

inimigos = []
tempo_a_inimigos = 0
kill = 0
def draw():
    screen.clear()
    if estado_jogo == "menu":
        screen.clear()
        screen.blit("placa_0", (WIDTH//2-72, 390))
        botao_comecar.draw()
        botao_sair.draw()
        if musica_ativa:
            botao_musica.image = "som_0_ligado"
        else:
            botao_musica.image = "som_0"
        if efeitos_ativos:
            botao_efeitos.image = "som_ligado"
        else:
            botao_efeitos.image = "som_1"

        botao_musica.draw()
        botao_efeitos.draw()
    elif estado_jogo == "jogando":
        screen.clear()
        screen.fill((20, 20, 40))
        jogador.draw()
        for inimigo in inimigos:
            inimigo.draw()
        screen.draw.text(f"Vida: {jogador.vida}", (10, 10), color="white")
        screen.draw.text("WASD para mover, Espaco para atacar", (10, 40), color="yellow", fontsize=20)
        screen.draw.text(f"Kills: {kill}", (10, 70), color="red")
        if jogador.tempo_inv > 0:
            screen.draw.text("INVENCIVEL!", (WIDTH//2-60, 30), color="red", fontsize=24)

def on_mouse_down(pos):
    global estado_jogo, musica_ativa, efeitos_ativos
    if botao_comecar.collidepoint(pos):
        estado_jogo = "jogando"
    if botao_sair.collidepoint(pos):
        exit()
    if botao_musica.collidepoint(pos):
        musica_ativa = not musica_ativa
    if botao_efeitos.collidepoint(pos):
        efeitos_ativos = not efeitos_ativos

def gerar_inimigos():
    global inimigos
    inimigos = []
    for _ in range(5):
        x = random.randint(50, WIDTH - 50)
        y = random.randint(50, HEIGHT - 50)
        inimigo = Actor("inimigo_parado0", (x, y))
        inimigo.vida = 3
        inimigo.velocidade = 1.5
        inimigo.tempo_a = 0
        inimigos.append(inimigo)
        
def update():
    global tempo_a_inimigos

    if estado_jogo == "jogando":
        movimentos()
        animar_p()
        if jogador.tempo_inv > 0:
            jogador.tempo_inv -= 1
        
        tempo_a_inimigos += 1
        if tempo_a_inimigos >= 60:
            inimigos_a()
            tempo_a_inimigos = 0

def movimentos():
    mover_p()
    mover_i()
    checar_comb()

def mover_p():
    dx, dy = 0, 0

    if keyboard.a or keyboard.left:
        dx = -jogador.velocidade
    if keyboard.d or keyboard.right:
        dx = jogador.velocidade
    if keyboard.w or keyboard.up:
        dy = -jogador.velocidade
    if keyboard.s or keyboard.down:
        dy = jogador.velocidade

    x_atual = jogador.x + dx
    y_atual = jogador.y + dy

    if 0 <= x_atual <= WIDTH:
        jogador.x = x_atual
    if 0 <= y_atual <= HEIGHT:
        jogador.y = y_atual

    if dx != 0 or dy != 0:
        jogador.estado_ani = "andando"
    else:
        jogador.estado_ani = "parado"
    if keyboard.space:
        jogador.estado_ani = "ataque1"
        atacar()
        
def animar_p():
    jogador.tempo_ani += 1
    lista_frames = player_ani[jogador.estado_ani]
    if jogador.tempo_ani % 8 == 0:
        jogador.frame_atual = (jogador.frame_atual + 1) % len(lista_frames)
        jogador.image = lista_frames[jogador.frame_atual]
    if (jogador.estado_ani == "ataque1" or jogador.estado_ani == "dano") and jogador.frame_atual == len(lista_frames) - 1:
        jogador.estado_ani = "parado"
        jogador.frame_atual = 0

def mover_i():
    for inimigo in inimigos:
        dx = jogador.x - inimigo.x
        dy = jogador.y - inimigo.y
        distancia = max(1, (dx ** 2 + dy ** 2) ** 0.5)
        dx /= distancia
        dy /= distancia
        inimigo.x += dx * inimigo.velocidade
        inimigo.y += dy * inimigo.velocidade

def atacar():
    global kill
    for inimigo in inimigos[:]:
        distancia = ((jogador.x - inimigo.x)** 2 + (jogador.y - inimigo.y) ** 2) ** 0.5
        if distancia < 30:
            inimigo.vida -= 1
            if inimigo.vida <= 0:
                inimigos.remove(inimigo)
                kill += 1
                if len(inimigos) == 0:
                    gerar_inimigos()

def inimigos_a():
    for inimigo in inimigos:
            distancia = ((jogador.x - inimigo.x) ** 2 + (jogador.y - inimigo.y) ** 2) ** 0.5
            if distancia < 40:
                if jogador.tempo_inv <= 0:
                    jogador.vida -= 1
                    jogador.tempo_inv = 30
                    jogador.estado_ani = "dano"

def checar_comb():
    for inimigo in inimigos:
        distancia = ((jogador.x - inimigo.x) ** 2 + (jogador.y - inimigo.y) ** 2) ** 0.5
        if distancia < 40:
            if jogador.tempo_inv <= 0:
                jogador.vida -= 0.5
                jogador.tempo_inv = 20
            
            if jogador.vida <= 0:
                jogador.estado_ani = "morte"
                screen.draw.text("GAME OVER!", (WIDTH//2, HEIGHT//2), color="red", fontsize=100)
                game_over()

def game_over():
    global estado_jogo
    estado_jogo = "menu"
    jogador.vida = 10
    jogador.pos = (WIDTH//2, HEIGHT//2)
    jogador.tempo_inv = 0
    inimigos.clear()
gerar_inimigos()
pgzrun.go()