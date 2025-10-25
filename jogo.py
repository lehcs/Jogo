import pgzrun
import random

WIDTH = 800
HEIGHT = 600

botao_comecar = Actor("botoes_0", (WIDTH//2, 250))
botao_sair = Actor("botoes_2", (WIDTH//2, 350))
botao_musica = Actor("som_0_ligado", (WIDTH//2+27, 436))
botao_efeitos = Actor("som_ligado", (WIDTH//2-25, 436))

musica_ativa = True
efeitos_ativos = True

estado_jogo = "menu"
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
pgzrun.go()
