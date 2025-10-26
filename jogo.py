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
    parado = ["player_parado0", "player_parado1", "player_parado2", "player_Parado3"]
    andando = ["player_andando0", "player_andando1", "player_andando2", "player_andando3"]
    dano = ["player_dano0", "player_dano1", "player_dano2", "player_dano3"]
    morte = ["player_morte0", "player_morte1", "player_morte2", "player_morte3"]
    ataque1 = ["player_ataque1_0", "player_ataque1_1", "player_ataque1_2", "player_ataque1_3", "player_ataque1_4"]
}
jogador = Actor("player_parado0", (WIDTH//2, HEIGHT//2))
jogador.vida = 10
jogador.estado_ani = "parado"
jogador.frame_atual = 0
jogador.tempo_animacao = 0
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
        inimigo = Actor("inimigo_parado0", (x*TILE_SIZE + TILE_SIZE//2, y*TILE_SIZE + TILE_SIZE//2))
        inimigo.vida = 3
        inimigos.append(inimigo)


gerar_inimigos()
pgzrun.go()