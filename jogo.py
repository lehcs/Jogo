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

musica_tocando = None

player_ani = {
    "parado": ["player_parado0", "player_parado1", "player_parado2", "player_parado3"],
    "paradoe": ["player_paradoe0", "player_paradoe1", "player_paradoe2", "player_paradoe3"],
    "andando": ["player_andando0", "player_andando1", "player_andando2", "player_andando3"],
    "andandoe": ["player_andando_e0", "player_andando_e1", "player_andando_e2", "player_andando_e3"],
    "dano": ["player_dano0"],
    "morte": ["player_morte0", "player_morte1", "player_morte2", "player_morte3"],
    "ataque1": ["player_ataque10", "player_ataque11", "player_ataque12", "player_ataque13"],
    "ataque2": ["player_ataque_e0", "player_ataque_e1", "player_ataque_e2", "player_ataque_e3"]
}
adv_ani = {
    "parado": ["inimigo_parado0", "inimigo_parado1", "inimigo_parado2", "inimigo_parado3", "inimigo_parado4"],
    "paradoe": ["inimigo_paradoe0", "inimigo_paradoe1", "inimigo_paradoe2", "inimigo_paradoe3"],
    "andando": ["inimigo_andando0", "inimigo_andando1", "inimigo_andando2", "inimigo_andando3", "inimigo_andando4", "inimigo_andando5"],
    "andandoe": ["inimigo_andandoe0", "inimigo_andandoe1", "inimigo_andandoe2", "inimigo_andandoe3", "inimigo_andandoe4", "inimigo_andandoe5"],
    "dano": ["inimigo_dano0", "inimigo_dano1", "inimigo_dano2", "inimigo_dano3", "inimigo_dano4"],
    "morte": ["inimigo_morte0", "inimigo_morte1", "inimigo_morte2", "inimigo_morte3", "inimigo_morte4", "inimigo_morte5", "inimigo_morte6"],
    "ataque1": ["inimigo_ataque0", "inimigo_ataque1", "inimigo_ataque2", "inimigo_ataque3", "inimigo_ataque4"],
    "ataque2": ["inimigo_ataque_e0", "inimigo_ataque_e1", "inimigo_ataque_e2", "inimigo_ataque_e3", "inimigo_ataque_e4"]
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
tempo_spawn_inimigos = 0
inimigos_ativos = False
kill = 0

round_atual = 1
inimigos_por_round = 5
max_inimigos_por_round = 20

def draw():
    screen.clear()
    if estado_jogo == "menu":
        screen.clear()
        screen.draw.text("ROGUELIKE", ((WIDTH//2)- 200, 100), color="white", fontsize=100)
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
        screen.fill((30, 25, 20))
        for x in range(0, WIDTH, 48):
            for y in range(0, HEIGHT, 48):
                screen.blit("chao_pedra", (x, y))
        jogador.draw()
        for inimigo in inimigos:
            inimigo.draw()
        screen.draw.text(f"Vida: {jogador.vida}", (10, 10), color="white")
        screen.draw.text("WASD para mover, Espaco para atacar", (10, 40), color="yellow", fontsize=20)
        screen.draw.text(f"Inimigos: {len(inimigos)}/{min(inimigos_por_round, max_inimigos_por_round)}", (10, 130), color="orange", fontsize=18)
        screen.draw.text(f"Kills: {kill}", (10, 70), color="red")
        if jogador.tempo_inv > 0:
            screen.draw.text("INVENCIVEL!", (WIDTH//2-60, 30), color="red", fontsize=24)
        if jogador.vida <= 0: 
            screen.draw.text("GAME OVER!", (WIDTH//2 - 200, HEIGHT//2), color="red", fontsize=100)

def on_mouse_down(pos):
    global estado_jogo, musica_ativa, efeitos_ativos, kill
    if botao_comecar.collidepoint(pos):
        estado_jogo = "jogando"
        kill = 0
        if efeitos_ativos:
            sounds.inicio.play()
    if botao_sair.collidepoint(pos):
        if efeitos_ativos:
            sounds.inicio.play()
        exit()
    if botao_musica.collidepoint(pos):
        musica_ativa = not musica_ativa
        if not musica_ativa:
            music.stop()
            musica_tocando = None
        if efeitos_ativos:
            sounds.inicio.play()
    if botao_efeitos.collidepoint(pos):
        efeitos_ativos = not efeitos_ativos

def gerar_inimigos():
    global inimigos, round_atual, inimigos_por_round, inimigos_ativos, tempo_spawn_inimigos
    inimigos = []
    quantidade = min(inimigos_por_round, max_inimigos_por_round)
    for _ in range(quantidade):
        x = random.randint(50, WIDTH - 50)
        y = random.randint(50, HEIGHT - 50)
        inimigo = Actor("inimigo_parado0", (x,y))
        inimigo.vida = 3
        inimigo.velocidade = 1
        inimigo.tempo_a = 0
        inimigo.estado_ani = "parado"
        inimigo.frame_atual = 0
        inimigo.tempo_ani = 0
        inimigos.append(inimigo)
    inimigos_ativos = True
        
def update():
    global tempo_a_inimigos, tempo_spawn_inimigos, inimigos_ativos, musica_tocando

    if estado_jogo == "jogando":
        movimentos()
        animar_p()
        animar_i()
        if len(inimigos) == 0:
            if not inimigos_ativos:
                tempo_spawn_inimigos += 1
                if tempo_spawn_inimigos >= 60: 
                    gerar_inimigos()
                    inimigos_ativos = True
                    tempo_spawn_inimigos = 0
            elif inimigos_ativos:
                inimigos_ativos = False
        if jogador.tempo_inv > 0:
            jogador.tempo_inv -= 1
            tempo_a_inimigos += 1
            if tempo_a_inimigos >= 0:
                inimigos_a()
                tempo_a_inimigos = 20
    if estado_jogo == "menu" and musica_ativa:
        if musica_tocando != "menu":
            music.play("musica_menu")
            music.set_volume(0.7)
            musica_tocando = "menu"
    elif estado_jogo == "jogando" and musica_ativa:
        if musica_tocando != "jogo":
            music.play("musica_jogo")
            music.set_volume(0.5)
            musica_tocando = "jogo"
    else:
        if musica_tocando is not None:
            music.stop()
            musica_tocando = None

def movimentos():
    mover_p()
    mover_i()
    checar_comb()

def mover_p():
    dx, dy = 0, 0

    if keyboard.a or keyboard.left:
        dx = -jogador.velocidade
        jogador.estado_ani = "andandoe"
    if keyboard.d or keyboard.right:
        dx = jogador.velocidade
        jogador.estado_ani = "andando"
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

    if dx == 0 and dy == 0:
        if jogador.estado_ani == "andandoe":
            jogador.estado_ani = "paradoe"
        elif jogador.estado_ani == "andando":
            jogador.estado_ani = "parado"
    if keyboard.space and (jogador.estado_ani == "parado" or jogador.estado_ani == "andando"):
        jogador.estado_ani = "ataque1"
        atacar()
    elif keyboard.space and (jogador.estado_ani == "paradoe" or jogador.estado_ani == "andandoe"):
        jogador.estado_ani = "ataque2"
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
    elif (jogador.estado_ani == "ataque2" or jogador.estado_ani == "dano") and jogador.frame_atual == len(lista_frames) - 1:
        jogador.estado_ani = "paradoe"
        jogador.frame_atual = 0

def mover_i():
    for inimigo in inimigos:
        direcao_x = jogador.x - inimigo.x
        direcao_y = jogador.y - inimigo.y
        if inimigo.estado_ani == "morte":
            continue
        if inimigo.tempo_ani % 120 < 60:
            if direcao_x > 0:
                inimigo.x += inimigo.velocidade
                inimigo.estado_ani = "andando"
            elif direcao_x < 0:
                inimigo.x -= inimigo.velocidade
                inimigo.estado_ani = "andandoe"
        else:
            if direcao_y > 0:
                inimigo.y += inimigo.velocidade
            elif direcao_y < 0:
                inimigo.y -= inimigo.velocidade
        if abs(direcao_x) < 5 and abs(direcao_y) < 5:
            if "e" in inimigo.estado_ani:
                inimigo.estado_ani = "paradoe"
            else:
                inimigo.estado_ani = "parado"
        
        inimigo.tempo_ani += 1

def animar_i():
    global kill, inimigos_ativos, round_atual, inimigos_por_round

    inimigos_mortos = []
    
    for inimigo in inimigos[:]:
        inimigo.tempo_ani += 1
        if inimigo.tempo_ani % 8 == 0:
            lista_frames = adv_ani[inimigo.estado_ani]
            inimigo.frame_atual = (inimigo.frame_atual + 1) % len(lista_frames)
            inimigo.image = lista_frames[inimigo.frame_atual]
        if inimigo.estado_ani == "morte":
            lista_frames = adv_ani["morte"]
            if inimigo.frame_atual >= len(lista_frames) - 1:
                inimigos_mortos.append(inimigo)
            
        elif (inimigo.estado_ani == "dano" or inimigo.estado_ani == "ataque1" or inimigo.estado_ani == "ataque2") and inimigo.frame_atual == len(adv_ani[inimigo.estado_ani]) - 1:
            if "e" in inimigo.estado_ani:
                inimigo.estado_ani = "paradoe"
            else:
                inimigo.estado_ani = "parado"
                inimigo.frame_atual = 0
    
    for inimigo in inimigos_mortos:
        if inimigo in inimigos:  
            inimigos.remove(inimigo)
            kill += 1
            if efeitos_ativos:
                sounds.morte.play()
    if len(inimigos_mortos) > 0 and len(inimigos) == 0 and inimigos_ativos:
        inimigos_ativos = False
        round_atual += 1
        inimigos_por_round += 2
        if efeitos_ativos:
            sounds.powerup.play()

def atacar():
    if efeitos_ativos:
        sounds.ataque.play()
    for inimigo in inimigos[:]:
        distancia = ((jogador.x - inimigo.x)** 2 + (jogador.y - inimigo.y) ** 2) ** 0.5
        if distancia < 45 and inimigo.estado_ani != "morte":
            inimigo.vida -= 1
            inimigo.estado_ani = "dano"
            if efeitos_ativos:
                sounds.dano.play()
            if inimigo.vida <= 0:
                inimigo.estado_ani = "morte"
                inimigo.frame_atual = 0
                inimigo.tempo_ani = 0
            inimigo.frame_atual = 0
            inimigo.tempo_ani = 0

def inimigos_a():
    for inimigo in inimigos[:]:
        if inimigo.estado_ani == "morte":
            continue
        distancia = ((jogador.x - inimigo.x) ** 2 + (jogador.y - inimigo.y) ** 2) ** 0.5
        if distancia < 25:
            if jogador.tempo_inv <= 0:
                jogador.vida -= 1
                jogador.tempo_inv = 30
                jogador.estado_ani = "dano"
                if efeitos_ativos:
                    sounds.dano.play()
        if jogador.x > inimigo.x:
            inimigo.estado_ani = "ataque1"
        else: 
            inimigo.estado_ani = "ataque2"

def checar_comb():
    for inimigo in inimigos:
        distancia = ((jogador.x - inimigo.x) ** 2 + (jogador.y - inimigo.y) ** 2) ** 0.5
        if distancia < 25:
            if jogador.tempo_inv <= 0:
                jogador.vida -= 0.5
                jogador.tempo_inv = 20
                jogador.estado_ani = "dano"
                if efeitos_ativos:
                    sounds.dano.play()
            
            if jogador.vida <= 0:
                jogador.estado_ani = "morte"
                if efeitos_ativos:
                    sounds.gameover.play()
                game_over()

def game_over():
    global estado_jogo, round_atual, inimigos_por_round, inimigos_ativos
    estado_jogo = "menu"
    jogador.vida = 10
    jogador.pos = (WIDTH//2, HEIGHT//2)
    jogador.tempo_inv = 0
    round_atual = 1
    inimigos_por_round = 5
    inimigos_ativos = False
    inimigos.clear()
    inimigos_ativos = False
    kill = 0

pgzrun.go()