import pgzrun
import random

WIDTH = 800
HEIGHT = 600
TILE_SIZE = 48
MAP_WIDTH = WIDTH//TILE_SIZE
MAP_HEIGHT = WIDTH//TILE_SIZE

botao_comecar = Actor("botoes_0", (WIDTH//2, 250))
botao_sair = Actor("botoes_2", (WIDTH//2, 350))
botao_musica = Actor("som_0_ligado", (WIDTH//2+27, 436))
botao_efeitos = Actor("som_ligado", (WIDTH//2-25, 436))

tile_chao = [
    ["chao_1", "chao_2", "chao_3"],
    ["chao_1", "chao_2", "chao_3"],
    ["chao_1", "chao_2", "chao_3"]
]
tile_paredeE= [
    ["paredee_1","chao_1", "chao_2"],
    ["paredee_2","chao_1", "chao_2"],
    ["paredee_2","chao_1", "chao_2"]
]
tile_paredeC= [
    ["parede1","parede2", "parede3"],
    ["chao_3","chao_1", "chao_2"],
    ["chao_3","chao_1", "chao_2"]
]
tile_paredeB= [
    ["chao_3","chao_1", "chao_2"],
    ["chao_3","chao_1", "chao_2"],
    ["paredeb_1","paredeb_2", "paredeb_3"]
]
tile_cantoEC = [
    ["cantoe","parede1", "parede2"],
    ["paredee_1","chao_1", "chao_2"],
    ["paredee_2","chao_1", "chao_2"]
]
tile_paredeD= [
    ["chao_1", "chao_2", "pareded_1"],
    ["chao_1", "chao_2", "pareded_2"],
    ["chao_1", "chao_2", "pareded_2"]
]
tile_cantoDC = [
    ["parede1", "parede2", "cantoe"],
    ["chao_1", "chao_2", "paredee_1"],
    ["chao_1", "chao_2", "paredee_2"]
]
tile_cantoDB = [ 
    ["chao_1", "chao_2", "pareded_1"],
    ["chao_1", "chao_2", "pareded_2"],
    ["paredeb_1", "paredeb_2", "cantodb"]
]
tile_cantoEB = [
    ["paredee_1","chao_1", "chao_2"],
    ["paredee_2","chao_1", "chao_2"],
    ["cantoeb","paredeb_1", "paredeb_2"]
]
tile_mapa = {
    "F": tile_paredeC,
    ".": tile_chao,
    "f": tile_paredeB,
    "E": tile_paredeE,
    "D": tile_paredeD,
    "B": tile_cantoEB,
    "b": tile_cantoDB,
    "C": tile_cantoEC,
    "c": tile_cantoDC
}

mapa_base = [
    "CFFFFFFFFFFFFFFc",
    "E..............D",
    "E..............D",
    "E..............D",
    "E..............D",
    "E..............D",
    "Bffffffffffffffb"
]
mapa_largura_px = len(mapa_base[0]) * TILE_SIZE
mapa_altura_px = len(mapa_base) * TILE_SIZE
offset_x = (WIDTH - mapa_largura_px) // 2
offset_y = (HEIGHT - mapa_altura_px) // 2


musica_ativa = True
efeitos_ativos = True
estado_jogo = "menu"

player_parado = ["player_parado0", "player_parado1", "player_parado2", "player_Parado3"]
frame_atual = 0 
tempo_animacao = 0
player_andando = ["player_andando0", "player_andando1", "player_andando2", "player_andando3"]
frame_atual = 0 
tempo_animacao = 0
player_dano = ["player_dano0", "player_dano1", "player_dano2", "player_dano3"]
frame_atual = 0 
tempo_animacao = 0
player_morte = ["player_morte0", "player_morte1", "player_morte2", "player_morte3"]
frame_atual = 0 
tempo_animacao = 0
player_ataque1 = ["player_ataque1_0", "player_ataque1_1", "player_ataque1_2", "player_ataque1_3", "player_ataque1_4"]
frame_atual = 0 
tempo_animacao = 0

jogador = Actor("player_parado0", (100, 100))
jogador.vida = 10
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
        for y, linha in enumerate(mapa_base):
            for x, simbolo in enumerate(linha):
                tile_lista = tile_mapa.get(simbolo, [["chao_1"]])
                for linha_tile in tile_lista:
                    for imagem in linha_tile:
                        screen.blit(imagem, (offset_x + x * TILE_SIZE, offset_y + y * TILE_SIZE))
        for inimigo in inimigos:
            inimigo.draw()
        screen.draw.text(f"Vida: {jogador.vida}", (10, 10), color="white")      

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
        inimigo = Actor("inimigo_parado0", (x*TILE_SIZE + TILE_SIZE//2, y*TILE_SIZE + TILE_SIZE//2))
        inimigo.vida = 3
        inimigos.append(inimigo)
def movimentos():
    mover_jogador()
    mover_inimigos()
    checar_combate()

def mover_jogador():
    dx, dy = 0, 0
    if keyboard.left:
        dx = -TILE_SIZE
    elif keyboard.right:
        dx = TILE_SIZE
    elif keyboard.up:
        dy = -TILE_SIZE
    elif keyboard.down:
        dy = TILE_SIZE
    if keyboard.left or keyboard.right or keyboard.up or keyboard.down:
        animar_p =(player_andando)
    else:
        animar_p(player_parado)

def animar_p():
    global frame_atual, tempo_animacao
    tempo_animacao += 1

    if tempo_animacao % 8 == 0:
        frame_atual = (frame_atual+1) % len(lista)
        player.image = lista[frame_atual]

gerar_inimigos()
pgzrun.go()