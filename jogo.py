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
jogador.velocidade = 3
inimigo = Actor("inimigo_parado0", (100, 100))

inimigos = []
def draw():
    screen.clear()
    if estado_jogo == "menu":
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
        jogador.draw()
        for inimigo in inimigos:
            inimigo.draw()
        screen.draw.text(f"Vida: {jogador.vida}", (10, 10), color="white")
        screen.draw.text("WASD para mover, Espaço para atacar", (10, 40), color="white", fontsize=20)    

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
        x = random.randint(3, MAP_WIDTH - 2)
        y = random.randint(3, MAP_HEIGHT - 2)
        inimigo = Actor("inimigo_parado0", (x, y))
        inimigo.vida = 3
        inimigo.velocidade = 1
        inimigos.append(inimigo)
        
def update():
    if estado_jogo == "jogando":
        movimentos()
        animar_p()

def movimentos():
    mover_p

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

    if 0 <= nova_x <= WIDTH:
        jogador.x = nova_x
    if 0 <= nova_y <= HEIGHT:
        jogador.y = nova_y

    if dx != 0 or dy != 0:
        jogador.estado_ani = "andando"
    else:
        jogador.estado_ani = "parado"
    if keyboard.space:
        jogador.estado_ani = "ataque"
        atacar()
def animar_p():
    jogador.tempo_ani += 1
    lista_frames = player_ani[jogador.estado_ani]
    if jogador.tempo_ani % 8 == 0:
        jogador.frame_atual = (jogador.frame_atual + 1) % len(lista_frames)
        jogador.image = lista_frames[jogador.frame_atual]
    if jogador.estado_ani == "ataque" and jogador.frame_atual == len(lista_frames) - 1:
        jogador.estado_ani = "parado"
        jogador.frame_atual = 0

gerar_inimigos()
pgzrun.go()