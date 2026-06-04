import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import asyncio
import os
import json
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ["TOKEN"]

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

ARCHIVO_TORNEOS = "torneos.json"

def guardar_torneos():
    with open(ARCHIVO_TORNEOS, "w", encoding="utf-8") as f:
        json.dump(torneos, f, indent=4, ensure_ascii=False)

def cargar_torneos():
    if os.path.exists(ARCHIVO_TORNEOS):
        with open(ARCHIVO_TORNEOS, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

torneos = cargar_torneos()
if not torneos:
    torneos = [
        {"hora":"15:00","nombre":"🏆 Torneo 1v1","puntos":"x1 pts","rank":"Rank F1","avisado":False,"aviso5":False},
        {"hora":"15:30","nombre":"🏆 Torneo bandas (2v2)","puntos":"x1 pts","rank":"Rank F4","avisado":False,"aviso5":False},
        {"hora":"16:15","nombre":"🥇 Domina (Bandas)","puntos":"","rank":"No rank","avisado":False,"aviso5":False},
        {"hora":"16:30","nombre":"🏆 Torneo bandas (2v2)","puntos":"x1 pts","rank":"Rank F4","avisado":False,"aviso5":False},
        {"hora":"17:15","nombre":"🥇 Domina (Bandas)","puntos":"","rank":"No rank","avisado":False,"aviso5":False},
        {"hora":"17:30","nombre":"🏆 Torneo bandas (3v3)","puntos":"x1 pts","rank":"Rank F4","avisado":False,"aviso5":False},
        {"hora":"18:30","nombre":"🏆 Torneo 1v1","puntos":"x1 pts","rank":"Rank F1","avisado":False,"aviso5":False},
        {"hora":"19:00","nombre":"⛈️ Tanda de Tormentas (8 tormentas)","puntos":"","rank":"Rank F7","avisado":False,"aviso5":False},
        {"hora":"20:00","nombre":"🏆 Torneo bandas (3v3)","puntos":"x1 pts","rank":"Rank F4","avisado":False,"aviso5":False},
        {"hora":"20:40","nombre":"🪂 x1 Battle Royale","puntos":"","rank":"Rank F7","avisado":False,"aviso5":False},
        {"hora":"21:00","nombre":"🏆 MEGA TORNEO 5v5-10v10","puntos":"x3 pts","rank":"Rank F4","avisado":False,"aviso5":False},
        {"hora":"22:00","nombre":"🪂 MEGA BATTLE ROYALE","puntos":"","rank":"Rank F7","avisado":False,"aviso5":False},
        {"hora":"22:30","nombre":"🎁 DROP DEL DÍA","puntos":"x1 pts","rank":"Rank F9","avisado":False,"aviso5":False},
        {"hora":"22:45","nombre":"🏆 Torneo bandas (4v4)","puntos":"x1 pts","rank":"Rank F4","avisado":False,"aviso5":False},
        {"hora":"23:30","nombre":"🏆 Torneo bandas (4v4)","puntos":"","rank":"","avisado":False,"aviso5":False},
        {"hora":"00:30","nombre":"🥇 Domina (Bandas)","puntos":"","rank":"No rank","avisado":False,"aviso5":False},
        {"hora":"00:45","nombre":"🏆 Torneo bandas (3v3)","puntos":"x1 pts","rank":"Rank F4","avisado":False,"aviso5":False},
        {"hora":"01:30","nombre":"🏆 Torneo 1v1","puntos":"x1 pts","rank":"Rank F1","avisado":False,"aviso5":False},
        {"hora":"02:00","nombre":"🏆 Torneo bandas (3v3)","puntos":"x1 pts","rank":"Rank F4","avisado":False,"aviso5":False},
        {"hora":"02:45","nombre":"🏆 Torneo bandas (2v2)","puntos":"","rank":"Rank F4","avisado":False,"aviso5":False}
    ]

    guardar_torneos()

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    avisos.start()

@bot.command()
async def eventos(ctx):
    if not torneos:
        await ctx.send("No hay torneos guardados.")
        return

    mensaje = "📅 **LISTADO DE EVENTOS**\n\n"

    for torneo in torneos:
        mensaje += f"🕒 {torneo['hora']} - {torneo['nombre']}\n"

    await ctx.send(mensaje)

@bot.command()
async def agregar(ctx, *, texto):
    lineas = texto.split("\n")

    for linea in lineas:
        if "-" in linea:
            partes = linea.split("-")

            hora = partes[0].strip()
            nombre = partes[1].strip()

            torneos.append({
                "hora": hora,
                "nombre": nombre,
                "avisado": False
            })

    await ctx.send("✅ Eventos agregados correctamente.")

@tasks.loop(seconds=30)
async def avisos():
    ahora = datetime.now().strftime("%H:%M")

    for torneo in torneos:

        hora_actual = datetime.now() - timedelta(hours=5)

        hora_torneo = datetime.strptime(torneo["hora"], "%H:%M")

        hora_torneo = hora_torneo.replace(
        year=hora_actual.year,
        month=hora_actual.month,
        day=hora_actual.day
    )

        faltan = (hora_torneo - hora_actual).total_seconds()

        canal = discord.utils.get(bot.get_all_channels(), name="💬-general")
        if faltan <= 300 and faltan > 0 and not torneo.get("aviso5"):

                if canal:
                    embed = discord.Embed(
                    title="⏰ FALTAN 5 MINUTOS",
                    description=f"🏆 {torneo['nombre']}",
                    color=discord.Color.gold()
                    )

                    embed.set_footer(text="Bloodys Tournament System")

                    await canal.send(embed=embed)

                torneo["aviso5"] = True


        if torneo["hora"] == ahora and not torneo["avisado"]:

            if canal:
                embed = discord.Embed(
                    title="🚨 YA COMENZÓ EL TORNEO",
                    description=f"🏆 {torneo['nombre']}",
                    color=discord.Color.red()
                )

                embed.set_footer(text="Bloodys Tournament System")

                await canal.send(embed=embed)

            torneo["avisado"] = True

        
bot.run(TOKEN)