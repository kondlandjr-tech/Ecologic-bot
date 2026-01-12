import discord
import random
import json
import os
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

#Configura qual que vai ser o prefixo (!@#$%¨¨&*) que vai ser usado antes do comando "/meme", "$meme","@meme"
bot = commands.Bot(command_prefix = "$", intents=intents)

#Diz se quando o bot está ligado (o discord precisa estar aberto)
@bot.event
async def on_ready():
    print(f"O{bot.user}acabou de ser ligado(Digite algum comando pro comando ser executado. Ex: $meme)")

    channel_id = 1447698629799186542 # ID do canal
    channel = bot.get_channel(channel_id)

    if channel:
        await channel.send("Digite <$help> para ver os comandos")

#Envia um dos memes que está na pasta "images" se o comando $meme for digitado NO SERVIDOR
#Na linha 19 (Desse código) altera qual o nome do comando "async def !meme!(ctx)". Se ele (o nome do comando) for alterado
#Exclua o terminal (deligue o bot) e inicie o bot (ligue o bot)
@bot.command(description="Te mostra 1 de 2 memes sobre programação")
async def meme(ctx):
    """Mostra memes sobre programação."""
    image_name = random.choice(os.listdir('images'))
    with open (f'images/{image_name}', 'rb') as f:
        picture = discord.File(f)
    await ctx.send(file=picture)

#Escolhe um nome se digitar $choose op1 op2 op3. Se for opções com espaços Ex: "op1 espaço1" "op2 espaço2 " "op3 espaço3"
#Ou Ex: op1_espaço1 op2_espaço2 op3_espaço3
@bot.command(description="Escolhe uma das opções que foram dadas. Ex: $choose op1 op2 op3. Ex: 'op1 op' 'op2 op' 'op3 op'") 
async def choose(ctx, *choices: str):
    """Escolhe entre múltiplas escolhas."""
    if len(choices) <= 2:
        await ctx.send("Você precisa passar pelo menos 2 opções. Para mais detalhes digite $help choose")
        return
    await ctx.send(random.choice(choices))

#Gera uma senha aleatória usando os dígitos da linha 38
@bot.command(description="Cria uma senha (escolhendo os caracteres disponíveis) com o número de dígitos que foi digitado (mas tendo que ser maior que 2)")
async def password(ctx, *pass_length: int):
    """Cria uma senha com no mínimo 3 dígitos."""
    elements = "+-/*!&$#?=@<>"
    password = ""
    if not pass_length:
        await ctx.send("Você precisa colocar o número de caracteres que sua senha terá")
        return
    if pass_length:
        pass_length = int(pass_length[0])
        if pass_length >= 2:
            for i in range(pass_length):
                password += random.choice(elements)
        else:
            await ctx.send("A senha precisa ter mais de 2 caracteres")
            return
    await ctx.send(password)

#Faz um quiz improvisado sobre o que jogar e onde jogar cada tipo de lixo
@bot.command()
async def eco_quiz(ctx):
    await ctx.send("Em qual lixeira é possível reciclar uma garrafa pet?(Responda com: 'lixeira' e cor que achar colocando o '$' e separados por underline)")
    await ctx.send("Se a resposta errada for digitada, nada aparecerá")

#Primeira pergunta
@bot.command()
async def lixeira_vermelha(ctx):
    await ctx.send("Resposta correta! Tendo em vista que a lixeira vermelha é responsável por reciclar plástico")
    await ctx.send("Qual tipo de resíduo é possível reciclar na lixeira preta?(Digite tudo minúsculo)")
    await ctx.send("Em casos como a da lixeira azul que há mais de um tipo de resíduo que pode ser reciclado, os dois serão nescessários: residuo_residuo)")

#Segunda pergunta
@bot.command()
async def madeira(ctx):
    await ctx.send("Resposta correta! Já a lixeira preta recilca madeira")
    await ctx.send("Quantas cores de lixeiras existem?(Digite o número por extenso)")

#Terceira pergunta

@bot.command()
async def dez(ctx):
    await ctx.send("Resposta certa! Existem atualmente 10 cores de lixeiras")
    await ctx.send("Você finalizou o quiz!")

def carregar_residuos():
    try:
        with open("residuos.json", "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def salvar_residuos(dados):
    with open("residuos.json", "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)

@bot.command()
async def descarte_lixo(ctx):
    '''Informa o que cada cor de lixeira recicla.'''
    mensagem = (
        "🟦 Azul: Papel e papelão.\n"
        "🟥 Vermelho: Plástico.\n"
        "🟩 Verde: Vidro.\n"
        "🟨 Amarelo: Metal.\n"
        "🟫 Marrom: Resíduos orgânicos (restos de comida, podas).\n"
        "⬛ Preto: Madeira.\n"
        "⬜ Cinza: Lixo geral não reciclável ou misturado.\n"
        "⚪ Branco: Resíduos ambulatoriais e de serviços de saúde.\n"
        "🟧 Laranja: Resíduos perigosos (pilhas, baterias, produtos químicos).\n"
        "🟪 Roxo: Resíduos radioativos."
    )

    await ctx.send(mensagem)

@bot.command()
async def recicla(ctx, palavra: str = "Vazio", objeto: str = "Vazio", lixeira: str = "Vazio", cor: str = "Vazio"):
    '''Informa onde descartar um objeto ou adiciona um novo objeto ao banco de dados.'''

    residuos = carregar_residuos()

    palavra = palavra.lower()
    objeto = objeto.lower()

    cores = ["vermelha", "azul", "verde", "amarela", "marrom", "preta", "cinza", "branca", "laranja", "roxa"]

    #O que o bot reponderá sem nenhum argumento
    if palavra == "Vazio":
        await ctx.send(
            "Use '$recicla [objeto]' para saber onde descartar."
            "Ou '$recicla adicionar [objeto] [lixeira] [cor]' para adicionar algo novo."
        )
        return

    #O que o bot responderá ao adicionar um novo objeto
    if palavra == "adicionar" and objeto != "Vazio" and lixeira != "Vazio" and cor != "Vazio":

        if lixeira != "lixeira":
            await ctx.send("Você deve escrever corretamente a palavra 'lixeira'.")
            return

        elif cor not in cores:
            await ctx.send("Por favor, informe uma cor válida para a lixeira.")
            await ctx.send(cores)
            return

        else:
            residuos[objeto] = f"{lixeira} {cor}"
            salvar_residuos(residuos)
            await ctx.send(f"Agora sei que o objeto {objeto} vai na {lixeira} {cor}")
            return
    
    #O que o bot responderá ao perguntar onde descartar um objeto (que estiver no banco de dados)
    if palavra in residuos:
        await ctx.send(f"O objeto {palavra} pode ser jogado na {residuos[palavra]}")
    
    #O que o bot responderá ao perguntar onde descartar um objeto (que não estiver no banco de dados)
    else:
        await ctx.send(
            "Não tenho informação sobre esse objeto  ou você não digitou nada após o comando."
            "Use '$recicla adicionar [objeto] [lixeira] [cor]' para adicionar esse objeto ao meu banco de dados."
        )




















bot.run("MTQ0Njk3NDUyNjI5MzU0MDg4Ng.G34Jry.lbqpLk3c21Uugrrafm-mVxOeDG3iPHc6J4qO9s")