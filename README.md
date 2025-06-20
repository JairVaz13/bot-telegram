# 📊 CSV Analyzer Bot para Telegram

![Bot Demo](/img/bot.jpg)
*Bot de análisis de datos para Telegram*

## 🌟 Descripción
Bot de Telegram que permite analizar archivos CSV directamente en el chat. Incluye:
- Exploración básica de datos
- Análisis estadístico
- Selección de columnas
- Asistente IA con Groq (Llama 3)

## 🚀 Instalación Rápida

```bash
# 1. Clonar repositorio
git clone https://github.com/JairVaz13/bot-telegram.git
cd csv-analyzer-bot

# 2. Instalar dependencias
pip install python-telegram-bot pandas python-dotenv requests

# 3. Configurar entorno
echo "TELEGRAM_TOKEN=tu_token_telegram" > .env
echo "GROQ_API_KEY=tu_api_key_groq" >> .env

# 4. Ejecutar
python bot_csv.py