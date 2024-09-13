import discord
from discord.ext import commands
import sqlite3
import random

intents = discord.Intents.default()

conn = sqlite3.connect('carbon_footprint.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY, carbon_footprint REAL)''')

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def s(ctx, footprint: float):
    """Установить углеродный след пользователя."""
    c.execute("INSERT INTO users VALUES (?, ?)", (ctx.author.id, footprint))
    conn.commit()
    await ctx.send(f'Углеродный след установлен на {footprint} тонн CO2.')

@bot.command()
async def r(ctx, reduction: float):
    """Уменьшить углеродный след пользователя."""
    c.execute("SELECT carbon_footprint FROM users WHERE id = ?", (ctx.author.id,))
    footprint = c.fetchone()[0]
    footprint -= reduction
    c.execute("UPDATE users SET carbon_footprint = ? WHERE id = ?", (footprint, ctx.author.id))
    conn.commit()
    await ctx.send(f'Углеродный след уменьшен на {reduction} тонн CO2.')

@bot.command()
async def g(ctx):
    """Получить текущий углеродный след пользователя."""
    c.execute("SELECT carbon_footprint FROM users WHERE id = ?", (ctx.author.id,))
    footprint = c.fetchone()[0]
    await ctx.send(f'Ваш текущий углеродный след составляет {footprint} тонн CO2.')

@bot.command()
async def t(ctx):
    """Получить советы по уменьшению углеродного следа."""
    tips = [
        "Используйте общественный транспорт вместо автомобиля.",
        "Сократите потребление мяса и молочных продуктов.",
        "Используйте энергосберегающие лампы и приборы.",
        "Сократите потребление воды.",
        "Покупайте продукты с меньшим углеродным следом."
    ]
    await ctx.send("\n".join(tips))

@bot.command(name='f')
async def f(ctx):
    """Получить случайный интересный факт о природе."""
    facts = [
        "Самое большое дерево в мире, General Sherman, весит более 6000 тонн.",
        "Амазонский дождевой лес производит 20% всего кислорода в атмосфере Земли.",
        "Океаны покрывают более 70% поверхности Земли.",
        "На Земле насчитывается около 3 триллионов деревьев.",
        "Самое большое животное на Земле - синий кит. Он также самое громкое животное, издавая звуки, достигающие 188 децибел."
    ]
    fact = random.choice(facts)
    await ctx.send(fact)

bot.run('token') 
