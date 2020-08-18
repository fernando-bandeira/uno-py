from os import name, system
from random import choice, randint, shuffle
from time import sleep

def limpa_tela():
    """essa função limpa a tela do terminal"""
    if name == "nt":
        system("cls")
    else:
        system("clear")

def distribui():
    """essa função distribui 7 cartas para cada jogador de forma aleatória"""
    for jogador in jogadores.values():
        for _ in range(7):
            carta = choice(baralho)
            jogador.append(carta)
            baralho.remove(carta)

def compra(jogador, quantidade):
    """essa função realiza a compra de cartas para um jogador"""
    for _ in range(quantidade):
        jogador.append(baralho[-1])
        baralho.pop()

def transforma(jogador = None):
    """essa função retorna de forma visual a última carta jogada ou as cartas de um jogador"""
    if jogador is None:
        return cores[topo["cor"]] + topo["valor"] + "\033[0m"
    else:
        leque = []
        for carta in jogador:
            leque.append(cores[carta["cor"]] + carta["valor"] + "\033[0m")
        return "  ".join(leque)

def mostra_cenario():
    """essa função exibe o cenário"""
    for i in range(1, qtd):
        if vez == i:
            print("\033[4m", end = "")
        # print(f"jogador {i}\033[0m" + f": {transforma(jogadores[i])}")
        print(f"jogador {i}" + f": {len(list(jogadores.values())[i])} cartas restantes\033[0m")
        print(atual)
    if vez == 0:
        print("\033[4m", end = "")
    print("você\033[0m: " + transforma(jogadores[0]))
    print("\ncarta atual: " + transforma(), end = "\n\n")

def analisa_jogada(jogador, carta):
    """essa função analisa a jogada do computador/usuário, verificando se ela é válida e executando os efeitos das cartas não-numéricas"""
    global cartas_compra
    global vez
    global outro
    global atual
    i = ordem.index(jogador)
    # condições para jogada poder ser feita:
    # cartas possuem mesmo valor
    cond1 = carta["valor"] == topo["valor"]
    # cartas possuem mesma cor e não há cartas a serem compradas
    cond2 = carta["cor"] == topo["cor"] and cartas_compra == 0
    # carta é um '+4' e não há compras de '+2' a serem feitas
    cond3 = carta["valor"] == "+4" and cartas_compra == 0
    # carta é um coringa e não há cartas a serem compradas
    cond4 = carta["valor"] == "C" and cartas_compra == 0
    if cond1 or cond2 or cond3 or cond4:
        # pula o jogador seguinte se a carta 'bloqueio' for jogada
        if carta["valor"] == "X":
            vez = ordem[i - (qtd - 2)]
        else:
            if carta["cor"] == "preto":
                # registra a compra de mais 4 cartas para o próximo jogador
                if carta["valor"] == "+4":
                    cartas_compra += 4
                # recebe a cor desejada para uma carta 'coringa' ou '+4'
                if jogador == 0:
                    while True:
                        desejo = input("qual cor (amarelo, azul, verde ou vermelho) você deseja? ").strip().lower()
                        if desejo in tupla_cores:
                            break
                        print("cor inválida")
                else:
                    # quantidade de cartas de cada cor
                    qtd_cores = [sum(c["cor"] == cor for c in jogadores[jogador]) for cor in tupla_cores]
                    desejo = tupla_cores[qtd_cores.index(max(qtd_cores))]
                carta["cor"] = desejo
            # registra a compra de mais 2 cartas para o próximo jogador
            elif carta["valor"] == "+2":
                cartas_compra += 2
            # inverte a ordem das jogadas se a carta 'inversão' for jogada
            elif carta["valor"] == ">":
                ordem.reverse()
                outro, atual = atual, outro
                i = ordem.index(jogador)
            vez = ordem[i - (qtd - 1)]
        return True
    else:
        return False

def jogada(jogador):
    """essa função gera e valida jogadas para os jogadores controlados pelo computador e para o usuário"""
    global topo
    global cartas_compra
    global vez
    i = ordem.index(jogador)
    # faz o jogador comprar 4 ou mais cartas após uma carta '+4' ser jogada
    if topo["valor"] == "+4" and cartas_compra > 0 and jogadores[jogador].count({"cor": "preto", "valor": "+4"}) == 0:
        print(f"mais {cartas_compra} cartas!")
        compra(jogadores[jogador], cartas_compra)
        cartas_compra = 0
        if jogador == 0:
            sleep(2)
        vez = ordem[i - (qtd - 1)]
        return None
    # faz o jogador comprar 2 ou mais cartas após uma carta '+2' ser jogada
    if topo["valor"] == "+2" and cartas_compra > 0:
        com_carta = any(c["valor"] == "+2" for c in jogadores[jogador])
        if not com_carta:
            print(f"mais {cartas_compra} cartas!")
            compra(jogadores[jogador], cartas_compra)
            cartas_compra = 0
            if jogador == 0:
                sleep(2)
            vez = ordem[i - (qtd - 1)]
            return None
    if jogador == 0:
        # recebe e valida o comando do usuário
        n = len(jogadores[0])
        intervalo = f"(1 a {n}) " if n > 1 else ""
        comando = input(f"digite a posição da carta que você quer jogar {intervalo}ou '+' para comprar: ")
        if not comando.isnumeric():
            # realiza a compra de uma carta
            if comando.strip() == "+":
                if cartas_compra > 0:
                    print(f"mais {cartas_compra} cartas!")
                    compra(jogadores[0], cartas_compra)
                    cartas_compra = 0
                    sleep(2)
                else:
                    compra(jogadores[0], 1)
                    # joga a carta comprada caso seja possível
                    if analisa_jogada(0, jogadores[0][-1]):
                        # carta da mesa é adicionada à lista das cartas antigas
                        cartas_antigas.append(topo)
                        # atualiza a carta da mesa
                        topo = jogadores[0][-1]
                        jogadores[0].pop()
                        print(f"carta comprada e jogada ({transforma()})")
                        if len(jogadores[0]) == 1:
                            print("UNO")
                        sleep(2)
                        return None
                    else:
                        print("carta comprada")
                        sleep(2)
                vez = ordem[i - (qtd - 1)]
            else:
                print("comando inválido")
                sleep(2)
        else:
            # recebe a posição de uma carta
            comando = int(comando)
            # verifica se essa posição existe
            if comando not in range(1, len(jogadores[0]) + 1):
                print("posição inexistente")
                sleep(2)
                return None
            carta = jogadores[0][comando - 1]
            # verifica se essa carta pode ser jogada
            if analisa_jogada(0, carta):
                # carta da mesa é adicionada à lista das cartas antigas
                cartas_antigas.append(topo)
                # atualiza a carta da mesa
                topo = carta
                # remove a carta da mão do usuário
                jogadores[0].remove(carta)
                if len(jogadores[0]) == 1:
                    print("UNO")
                    sleep(3.5)
            else:
                print("carta inválida")
                sleep(2)
        return None
    # computador
    else:
        # guarda cartas pretas para serem utilizadas como último recurso
        prioridades = []
        for carta in jogadores[jogador]:
            if carta["cor"] == "preto":
                # cartas pretas são inseridas no final da lista, e posteriormente serão analisadas apenas quando nenhuma carta colorida servir
                prioridades.append(carta)
            else:
                # cartas coloridas são inseridas no início da lista, e posteriormente serão analisadas primeiro
                prioridades.insert(0, carta)
        # realiza a jogada do computador, caso possível
        for carta in prioridades:
            if analisa_jogada(jogador, carta):
                # carta da mesa é adicionada à lista das cartas antigas
                cartas_antigas.append(topo)
                # atualiza a carta da mesa
                topo = carta
                print(f"carta jogada ({transforma()})")
                # remove a carta da mão do jogador
                jogadores[jogador].remove(carta)
                if len(jogadores[jogador]) == 1:
                    print("UNO")
                return None
    # caso nenhuma carta do jogador controlado pelo computador sirva, ele compra uma carta
    compra(jogadores[jogador], 1)
    if analisa_jogada(jogador, jogadores[jogador][-1]):
        # carta da mesa é adicionada à lista das cartas antigas
        cartas_antigas.append(topo)
        # atualiza a carta da mesa
        topo = jogadores[jogador][-1]
        print(f"carta comprada e jogada ({transforma()})")
        # remove a carta da mão do jogador
        jogadores[jogador].pop()
        if len(jogadores[jogador]) == 1:
            print("UNO")
        return None
    else:
        print("carta comprada")
        vez = ordem[i - (qtd - 1)]

while True:
    # as cartas são criadas e adicionadas em uma lista
    baralho = []
    tupla_cores = ("amarelo", "azul", "verde", "vermelho")
    for cor in tupla_cores:
        # cartas numéricas
        for n in range(10):
            baralho.append({"cor": cor, "valor": str(n), "id": len(baralho) + 1})
            if n != 0:
                baralho.append({"cor": cor, "valor": str(n), "id": len(baralho) + 1})
        # cartas 'bloqueio', 'inversão' e '+2'
        for n in ("X", ">", "+2"):
            baralho.append({"cor": cor, "valor": n, "id": len(baralho) + 1})
            baralho.append({"cor": cor, "valor": n, "id": len(baralho) + 1})
        # cartas 'coringa' e '+4'
        baralho.append({"cor": "preto", "valor": "C", "id": len(baralho) + 1})
        baralho.append({"cor": "preto", "valor": "+4", "id": len(baralho) + 1})
    # códigos ASCII para exibir as cores das cartas
    cores = {"amarelo": "\033[33m", "azul": "\033[34m", "verde": "\033[32m", "vermelho": "\033[31m", "preto": "\033[0m"}
    # cartas que já foram jogadas serão adicionadas a essa lista
    cartas_antigas = []
    # quantidade de jogadores
    while True:
        qtd = input("informe a quantidade de jogadores (2 a 10): ")
        if qtd.isnumeric():
            qtd = int(qtd)
            if qtd > 1 and qtd < 11:
                break
        print("entrada inválida")
    jogadores = {x: [] for x in range(qtd)}
    ordem = list(jogadores.keys())
    # símbolos que indicam o sentido de rotação das jogadas
    atual = ">"
    outro = "<"
    # cartas são distribuídas
    distribui()
    # demais cartas são embaralhadas e fornecerão cartas para compra
    shuffle(baralho)
    # carta inicial é sorteada (tem que ser um número)
    while True:
        topo = choice(baralho)
        if topo["valor"] in (str(n) for n in range(10)):
            baralho.remove(topo)
            break
    # primeiro jogador a jogar é sorteado
    x = randint(0, qtd - 1)
    vez = x
    # essa variável indica quantas cartas devem ser compradas na próxima jogada (essa quantidade é cumulativa)
    cartas_compra = 0
    fim_jogo = False
    while True:
        # caso as cartas para compra cheguem perto do fim, as cartas antigas são adicionadas ao baralho, que é embaralhado em seguida
        if len(baralho) < 5:
            baralho.extend(cartas_antigas)
            cartas_antigas.clear()
            shuffle(baralho)
        # limpa o cenário
        limpa_tela()
        # cenário é exibido
        mostra_cenario()
        # verifica se alguém já venceu
        for jogador in jogadores.keys():
            if len(jogadores[jogador]) == 0:
                vencedor = jogador
                fim_jogo = True
        if fim_jogo:
            break
        # indica de quem é a vez de jogar
        if vez == 0:
            espera = False
            print("sua vez")
        else:
            print(f"vez do jogador {vez}")
            espera = True
        # executa a jogada da vez
        jogada(vez)
        if espera:
            sleep(3.5)
    # vencedor é indicado
    nome = "você" if vencedor == 0 else f"jogador {vencedor}"
    print(f"{nome} venceu")
    comando = input("digite 's' para sair ou qualquer outro comando para reiniciar: ")
    if comando.strip().lower() == "s":
        break
    else:
        # limpa o cenário
        limpa_tela()
