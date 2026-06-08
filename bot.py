"""from telegram.ext import Application, CommandHandler

import os
TOKEN = os.environ.get("TELEGRAM_TOKEN", "8890486963:AAFD7gzT9vZvLUBwag6GXp6l1vWXL71_cyI")
async def start(update, context):
    await update.message.reply_text("✅ Bot funcionando! Las fotos se arreglarán después.")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

print("Bot iniciado. Envía /start en Telegram")
app.run_polling()"""

import os
import json
import random
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- CONFIGURACIÓN ---
TOKEN = "8890486963:AAFD7gzT9vZvLUBwag6GXp6l1vWXL71_cyI" 
# Cargar la información de tu gato desde el archivo JSON
def cargar_info_gato():
    try:
        with open('mi_gato.json', 'r', encoding='utf-8') as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        # Si no existe el archivo, crear uno por defecto
        info_default = {
            "nombre": "Sin Nombre",
            "fecha_nacimiento": "No especificada",
            "edad": "No especificada",
            "comida_favorita": "No especificada",
            "comida_diaria": ["No hay horarios configurados"],
            "horas_siesta": ["No hay horarios configurados"],
            "fotos": [],
            "datos_curiosos": ["¡Usa /configurar para agregar información de tu gato!"]
        }
        with open('mi_gato.json', 'w', encoding='utf-8') as archivo:
            json.dump(info_default, archivo, indent=2, ensure_ascii=False)
        return info_default
    except json.JSONDecodeError:
        return {"error": "El archivo JSON está dañado"}

# Guardar nueva información (cuando el admin la actualice)
def guardar_info_gato(nueva_info):
    with open('mi_gato.json', 'w', encoding='utf-8') as archivo:
        json.dump(nueva_info, archivo, indent=2, ensure_ascii=False)

# --- COMANDOS DEL BOT ---

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    info = cargar_info_gato()
    
    mensaje = f"""
🐱 *¡Hola! Soy el bot de {info['nombre']}*

Puedo contarte todo sobre {info['nombre']}:

/sobre - Información general
/cumpleaños - Fecha de nacimiento y edad
/comida - Qué come y horarios
/siesta - Horas de siesta
/foto - Una foto de {info['nombre']}
/dato - Un dato curioso
/menu - Mostrar este menú otra vez
    """
    
    await update.message.reply_text(mensaje, parse_mode='Markdown')

# Comando /sobre - Información general
async def sobre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    info = cargar_info_gato()
    
    mensaje = f"""
📋 *Sobre {info['nombre']}*

🎂 *Fecha de nacimiento:* {info['fecha_nacimiento']}
📅 *Edad:* {info['edad']}
🍽️ *Comida favorita:* {info['comida_favorita']}

{info['nombre']} es una gatita consentida y juguetona. 
Para más detalles usa /comida, /siesta o /dato.
    """
    
    await update.message.reply_text(mensaje, parse_mode='Markdown')

# Comando /cumpleaños
async def cumpleaños(update: Update, context: ContextTypes.DEFAULT_TYPE):
    info = cargar_info_gato()
    
    # Calcular días hasta el próximo cumpleaños (si la fecha está en formato "día de mes")
    mensaje = f"🎂 *Cumpleaños de {info['nombre']}:*\n\n📅 {info['fecha_nacimiento']}\n🎉 {info['edad']}\n\n¡No olvides darle un mimo especial ese día! 🎁"
    
    await update.message.reply_text(mensaje, parse_mode='Markdown')

# Comando /comida - Horarios de comida
async def comida(update: Update, context: ContextTypes.DEFAULT_TYPE):
    info = cargar_info_gato()
    
    horarios = "\n".join([f"🍽️ {h}" for h in info['comida_diaria']])
    
    mensaje = f"""
🍗 *Horario de comidas de {info['nombre']}:*

{horarios}

*Comida favorita:* {info['comida_favorita']}

Recuerda: ¡siempre debe tener agua fresca disponible! 💧
    """
    
    await update.message.reply_text(mensaje, parse_mode='Markdown')

# Comando /siesta - Horas de siesta
async def siesta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    info = cargar_info_gato()
    
    siestas = "\n".join([f"😴 {h}" for h in info['horas_siesta']])
    
    mensaje = f"""
💤 *Horas de siesta de {info['nombre']}:*

{siestas}

¡Los gatos duermen entre 12 y 16 horas al día! 
{info['nombre']} se toma muy en serio su descanso. 🛌
    """
    
    await update.message.reply_text(mensaje, parse_mode='Markdown')

# Comando /foto - Enviar una foto aleatoria del gato
async def foto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    info = cargar_info_gato()
    
    if not info['fotos']:
        await update.message.reply_text("😿 Aún no tengo fotos de {info['nombre']}. ¡Mi super Mami debe agregarlas!")
        return
    
    # Elegir una foto aleatoria de la lista
    foto_seleccionada = random.choice(info['fotos'])
    ruta_foto= os.path.join("fotos", foto_seleccionada)
    
    # Opción 1: Si las fotos están en la misma carpeta
    if os.path.exists(ruta_foto):
        with open(ruta_foto, 'rb') as foto_file:
            await update.message.reply_photo(
                photo=foto_file, 
                caption=f"🐱 ¡Aquí tienes una foto de {info['nombre']}!"
            )
    else:
        # Opción 2: Si es una URL (ej. de Imgur)
        await update.message.reply_photo(
            photo=foto_seleccionada,
            caption=f"🐱 {info['nombre']} en todo su esplendor"
        )

# Comando /dato - Dato curioso del gato
async def dato(update: Update, context: ContextTypes.DEFAULT_TYPE):
    info = cargar_info_gato()
    
    if info['datos_curiosos']:
        dato_aleatorio = random.choice(info['datos_curiosos'])
        mensaje = f"🐱 *Dato curioso sobre {info['nombre']}:*\n\n{dato_aleatorio}"
    else:
        mensaje = f"🐱 {info['nombre']} es un gato misterioso... ¡sin datos curiosos aún!"
    
    await update.message.reply_text(mensaje, parse_mode='Markdown')

# --- COMANDO PARA ADMIN: Actualizar información fácilmente ---
# (Solo tú puedes usarlo, verificando tu user_id)
ADMIN_ID = 1258090630 # <--- PON AQUÍ TU ID DE TELEGRAM
# Comando /menu - Menú interactivo con botones
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    teclado = [
        [InlineKeyboardButton("📋 Sobre", callback_data='sobre')],
        [InlineKeyboardButton("🎂 Cumpleaños", callback_data='cumple'),
         InlineKeyboardButton("🍗 Comida", callback_data='comida')],
        [InlineKeyboardButton("💤 Siesta", callback_data='siesta'),
         InlineKeyboardButton("📸 Foto", callback_data='foto')],
        [InlineKeyboardButton("🐱 Dato", callback_data='dato')]
    ]
    await update.message.reply_text(
        "🐱 *Menú de información*", 
        reply_markup=InlineKeyboardMarkup(teclado), 
        parse_mode='Markdown'
    )

# Manejador de botones (callback)
async def boton_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    funciones = {
        'sobre': sobre,
        'cumple': cumpleaños,
        'comida': comida,
        'siesta': siesta,
        'foto': foto,
        'dato': dato
    }
    
    if query.data in funciones:
        await funciones[query.data](update, context)
async def configurar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Verificar que el usuario sea el admin
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ No tienes permiso para usar este comando.")
        return
# --- MAIN ---
def main():
    print("🐱 Bot de Lily iniciando...")
    app = Application.builder().token(TOKEN).build()
    
    # Comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("sobre", sobre))
    #app.add_handler(CommandHandler("cumpleaños", cumpleaños))
    app.add_handler(CommandHandler("comida", comida))
    app.add_handler(CommandHandler("siesta", siesta))
    app.add_handler(CommandHandler("foto", foto))
    app.add_handler(CommandHandler("dato", dato))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("configurar", configurar))
    #app.add_handler(CommandHandler("reload", reload))
    app.add_handler(CallbackQueryHandler(boton_callback))
    
    print("✅ Bot listo! Ve a Telegram y prueba /start")
    app.run_polling()

if __name__ == "__main__":
    main()
