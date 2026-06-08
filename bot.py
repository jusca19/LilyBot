import os
import json
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- CONFIGURACIÓN ---
TOKEN = os.environ.get("TELEGRAM_TOKEN", "8890486963:AAFD7gzT9vZvLUBwag6GXp6l1vWXL71_cyI")
ADMIN_ID = 1258090630

# --- FUNCIONES DE DATOS ---
def cargar_info_gato():
    try:
        with open('mi_gato.json', 'r', encoding='utf-8') as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        info_default = {
            "nombre": "Lily",
            "fecha_nacimiento": "15 de marzo de 2021",
            "edad": "3 años",
            "comida_favorita": "Atún y pollo",
            "comida_diaria": ["9:00 AM - Alimento seco", "3:00 PM - Comida húmeda", "9:00 PM - Alimento seco"],
            "horas_siesta": ["11:00 AM a 1:00 PM", "4:00 PM a 7:00 PM"],
            "fotos": [],
            "datos_curiosos": ["Le encanta mirar por la ventana", "Su juguete favorito es una pluma"]
        }
        with open('mi_gato.json', 'w', encoding='utf-8') as archivo:
            json.dump(info_default, archivo, indent=2, ensure_ascii=False)
        return info_default
    except json.JSONDecodeError:
        return {"nombre": "Lily", "error": "JSON dañado"}

# --- COMANDOS DEL BOT ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    info = cargar_info_gato()
    mensaje = f"🐱 *¡Hola! Soy el bot de {info['nombre']}*\n\n/sobre - Información\n/comida - Horarios\n/siesta - Siestas\n/foto - Fotos\n/dato - Datos curiosos\n/menu - Menú interactivo"
    await update.message.reply_text(mensaje, parse_mode='Markdown')

async def sobre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    info = cargar_info_gato()
    mensaje = f"📋 *Sobre {info['nombre']}*\n\n🎂 {info['fecha_nacimiento']}\n📅 {info['edad']}\n🍽️ {info['comida_favorita']}"
    await update.message.reply_text(mensaje, parse_mode='Markdown')

async def comida(update: Update, context: ContextTypes.DEFAULT_TYPE):
    info = cargar_info_gato()
    horarios = "\n".join([f"🍽️ {h}" for h in info['comida_diaria']])
    mensaje = f"🍗 *Horario de comidas*\n\n{horarios}"
    await update.message.reply_text(mensaje, parse_mode='Markdown')

async def siesta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    info = cargar_info_gato()
    siestas = "\n".join([f"😴 {h}" for h in info['horas_siesta']])
    mensaje = f"💤 *Horas de siesta*\n\n{siestas}"
    await update.message.reply_text(mensaje, parse_mode='Markdown')

async def foto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    info = cargar_info_gato()
    
    if not info['fotos']:
        await update.message.reply_text("😿 Aún no tengo fotos. ¡Pronto agregaré algunas!")
        return
    
    foto_seleccionada = random.choice(info['fotos'])
    
    if foto_seleccionada.startswith(('http://', 'https://')):
        await update.message.reply_photo(photo=foto_seleccionada, caption=f"🐱 {info['nombre']}")
    else:
        ruta_foto = os.path.join("fotos", foto_seleccionada)
        if os.path.exists(ruta_foto):
            with open(ruta_foto, 'rb') as foto_file:
                await update.message.reply_photo(photo=foto_file, caption=f"🐱 {info['nombre']}")
        else:
            await update.message.reply_text("😿 No encuentro la foto")

async def dato(update: Update, context: ContextTypes.DEFAULT_TYPE):
    info = cargar_info_gato()
    if info['datos_curiosos']:
        dato_aleatorio = random.choice(info['datos_curiosos'])
        await update.message.reply_text(f"🐱 *Dato curioso:*\n\n{dato_aleatorio}", parse_mode='Markdown')
    else:
        await update.message.reply_text("😿 No hay datos curiosos aún")

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    teclado = [
        [InlineKeyboardButton("📋 Sobre", callback_data='sobre')],
        [InlineKeyboardButton("🍗 Comida", callback_data='comida'), InlineKeyboardButton("💤 Siesta", callback_data='siesta')],
        [InlineKeyboardButton("📸 Foto", callback_data='foto'), InlineKeyboardButton("🐱 Dato", callback_data='dato')]
    ]
    await update.message.reply_text("🐱 *Menú*", reply_markup=InlineKeyboardMarkup(teclado), parse_mode='Markdown')

async def boton_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    funciones = {'sobre': sobre, 'comida': comida, 'siesta': siesta, 'foto': foto, 'dato': dato}
    
    if query.data in funciones:
        await funciones[query.data](update, context)

# --- MAIN ---
def main():
    print("🐱 Bot de Gatos iniciando...")
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("sobre", sobre))
    app.add_handler(CommandHandler("comida", comida))
    app.add_handler(CommandHandler("siesta", siesta))
    app.add_handler(CommandHandler("foto", foto))
    app.add_handler(CommandHandler("dato", dato))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CallbackQueryHandler(boton_callback))
    
    print("✅ Bot listo! Ve a Telegram y prueba /start")
    app.run_polling()

if __name__ == "__main__":
    main()
