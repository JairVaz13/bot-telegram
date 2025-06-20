import os
import pandas as pd
import requests
from telegram import (
    Update, ReplyKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

BOTONES = [
    ["📄 Primeras N filas", "📄 Últimas N filas"],
    ["ℹ️ Información básica", "🧾 Lista de columnas"],
    ["📐 Forma del dataset", "📊 Descripción estadística"],
    ["🔍 Seleccionar 1 columna", "🧮 Seleccionar N columnas"],
    ["🤖 Hacer pregunta IA","🚀 /start"]
]
reply_markup = ReplyKeyboardMarkup(BOTONES, resize_keyboard=True)

user_data = {}

def escape_md(text):
    escape_chars = r"_*[]()~`>#+-=|{}.!\\"  # Ajustado para MarkdownV2
    return ''.join(f"\\{c}" if c in escape_chars else c for c in str(text))

def generar_respuesta_con_groq(pregunta, df):
    prompt = f"Aquí tienes una tabla:\n{df.head(100).to_csv(index=False)}\n\nPregunta: {pregunta}"
    res = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "meta-llama/llama-4-scout-17b-16e-instruct",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.5,
            "max_tokens": 512
        }
    )
    return res.json()['choices'][0]['message']['content']

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome = (
        "👋 ¡Hola! Soy tu bot para analizar archivos CSV.\n\n"
        "Envía un archivo `.csv` y usa los botones para explorar.\n"
        "También puedes hacer preguntas con IA 🤖"
    )
    await update.message.reply_text(welcome, reply_markup=reply_markup)

async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = (
        "*📌 Instrucciones:*\n"
        "1. Envía un archivo `.csv`\n"
        "2. Usa los botones del teclado\n"
        "3. También puedes hacer preguntas con IA 🤖"
    )
    await update.message.reply_text(texto, parse_mode="MarkdownV2", reply_markup=reply_markup)

async def handle_csv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    archivo = update.message.document
    if not archivo.file_name.lower().endswith(".csv"):
        await update.message.reply_text("❌ El archivo debe ser .csv")
        return
    file = await archivo.get_file()
    df = pd.read_csv(file.file_path)
    user_id = update.message.from_user.id
    user_data[user_id] = df
    await update.message.reply_text("✅ CSV recibido. Usa los botones para explorar.", reply_markup=reply_markup)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    df = user_data.get(user_id)
    text = update.message.text.strip()

    if df is None:
        await update.message.reply_text("⚠️ Aún no has enviado un archivo CSV.", reply_markup=reply_markup)
        return

    # Estados para inputs
    if context.user_data.get("awaiting_n_head"):
        if text.isdigit():
            n = int(text)
            contenido = escape_md(df.head(n).to_string())
            await update.message.reply_text(f"*Primeras {n} filas:*\n```\n{contenido}\n```", parse_mode="MarkdownV2", reply_markup=reply_markup)
        else:
            await update.message.reply_text("⚠️ Ingresa un número válido.", reply_markup=reply_markup)
        context.user_data["awaiting_n_head"] = False
        return

    if context.user_data.get("awaiting_n_tail"):
        if text.isdigit():
            n = int(text)
            contenido = escape_md(df.tail(n).to_string())
            await update.message.reply_text(f"*Últimas {n} filas:*\n```\n{contenido}\n```", parse_mode="MarkdownV2", reply_markup=reply_markup)
        else:
            await update.message.reply_text("⚠️ Ingresa un número válido.", reply_markup=reply_markup)
        context.user_data["awaiting_n_tail"] = False
        return

    if context.user_data.get("awaiting_column"):
        col_input = text.strip().lower()
        cols_lower = [c.lower() for c in df.columns]
        if col_input in cols_lower:
            col = df.columns[cols_lower.index(col_input)]
            contenido = escape_md(df[col].to_string())
            await update.message.reply_text(f"*Columna {col}:*\n```\n{contenido}\n```", parse_mode="MarkdownV2", reply_markup=reply_markup)
        else:
            await update.message.reply_text("❌ Columna no encontrada. Revisa la ortografía.", reply_markup=reply_markup)
        context.user_data["awaiting_column"] = False
        return

    if context.user_data.get("awaiting_columns_sel"):
        cols_input = [c.strip().lower() for c in text.split(",")]
        cols_lower = [c.lower() for c in df.columns]
        cols_validas = []
        for c in cols_input:
            if c in cols_lower:
                cols_validas.append(df.columns[cols_lower.index(c)])
            else:
                await update.message.reply_text(f"❌ La columna '{c}' no es válida. Revisa la ortografía.", reply_markup=reply_markup)
                context.user_data["awaiting_columns_sel"] = False
                return
        contenido = escape_md(df[cols_validas].to_string())
        await update.message.reply_text(f"*Columnas seleccionadas:*\n```\n{contenido}\n```", parse_mode="MarkdownV2", reply_markup=reply_markup)
        context.user_data["awaiting_columns_sel"] = False
        return

    if context.user_data.get("awaiting_pregunta"):
        await update.message.reply_text("🤔 Pensando...", reply_markup=reply_markup)
        respuesta = generar_respuesta_con_groq(text, df)
        await update.message.reply_text(escape_md(respuesta), parse_mode="MarkdownV2", reply_markup=reply_markup)
        context.user_data["awaiting_pregunta"] = False
        return

    # Comandos simples
    if text == "📄 Primeras N filas":
        await update.message.reply_text("📥 ¿Cuántas primeras filas deseas ver?", reply_markup=reply_markup)
        context.user_data["awaiting_n_head"] = True

    elif text == "📄 Últimas N filas":
        await update.message.reply_text("📥 ¿Cuántas últimas filas deseas ver?", reply_markup=reply_markup)
        context.user_data["awaiting_n_tail"] = True

    elif text == "ℹ️ Información básica":
        import io
        buffer = io.StringIO()
        df.info(buf=buffer)
        await update.message.reply_text(f"```\n{escape_md(buffer.getvalue())}\n```", parse_mode="MarkdownV2", reply_markup=reply_markup)

    elif text == "🧾 Lista de columnas":
        await update.message.reply_text(f"*Columnas:* {escape_md(', '.join(df.columns))}", parse_mode="MarkdownV2", reply_markup=reply_markup)

    elif text == "📐 Forma del dataset":
        await update.message.reply_text(f"*Forma:* `{df.shape}`", parse_mode="MarkdownV2", reply_markup=reply_markup)

    elif text == "📊 Descripción estadística":
        desc = escape_md(df.describe(include='all').to_string())
        await update.message.reply_text(f"```\n{desc}\n```", parse_mode="MarkdownV2", reply_markup=reply_markup)

    elif text == "🔍 Seleccionar 1 columna":
        await update.message.reply_text("✏️ Escribe el nombre de la columna que quieres ver:", reply_markup=reply_markup)
        context.user_data["awaiting_column"] = True

    elif text == "🧮 Seleccionar N columnas":
        await update.message.reply_text("✏️ Escribe los nombres de las columnas que quieres ver, separados por coma:", reply_markup=reply_markup)
        context.user_data["awaiting_columns_sel"] = True

    elif text == "🤖 Hacer pregunta IA":
        await update.message.reply_text("❓ ¿Qué deseas preguntar sobre el dataset?", reply_markup=reply_markup)
        context.user_data["awaiting_pregunta"] = True

    else:
        await update.message.reply_text("⚠️ No entendí. Usa los botones del teclado.", reply_markup=reply_markup)

if __name__ == "__main__":
    print("🚀 Bot iniciado...")
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ayuda", ayuda))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_csv))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))

    app.run_polling()
