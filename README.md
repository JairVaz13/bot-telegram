# 📊 CSV Análisis Bot para Telegram

![Bot Demo](img/bot.jpg)
*Bot de análisis de datos para Telegram*

## 🌟 Descripción
Bot de Telegram que permite analizar archivos CSV directamente en el chat. Con este bot podrás:

- Explorar y visualizar tus datos fácilmente
- Obtener análisis estadísticos automáticos
- Seleccionar columnas específicas para análisis
- Consultar un asistente IA integrado (usando Groq con Llama 3)
- Generar insights rápidos sobre tus conjuntos de datos

## 🚀 Instalación Rápida

1. Clona el repositorio:
```bash
git clone https://github.com/JairVaz13/bot-telegram.git
cd bot-telegram
```

2. Instala las dependencias:
```bash
pip install python-telegram-bot pandas python-dotenv requests
```

3. Configura tus variables de entorno:
```bash
echo "TELEGRAM_TOKEN=tu_token_telegram" > .env
echo "GROQ_API_KEY=tu_api_key_groq" >> .env
```

4. Ejecuta el bot:
```bash
python bot_csv.py
```

## 🔧 Requisitos
- Python 3.8 o superior
- Cuenta en [Groq](https://console.groq.com/) para obtener una API key
- Token de bot de Telegram (obtenido a través de [@BotFather](https://t.me/BotFather))

## 🛠️ Funcionalidades Principales

### 📊 Exploración de Datos
| Comando | Descripción |
|---------|-------------|
| `📄 Primeras N filas` | Muestra las primeras N filas del CSV |
| `📄 Últimas N filas` | Muestra las últimas N filas del CSV |
| `ℹ️ Información básica` | Muestra metadatos del dataset |
| `🧾 Lista de columnas` | Enumera todas las columnas disponibles |
| `📐 Forma del dataset` | Muestra (filas, columnas) |

### 📈 Análisis Estadístico
| Comando | Descripción |
|---------|-------------|
| `📊 Descripción estadística` | Muestra estadísticas descriptivas |
| `🔍 Seleccionar 1 columna` | Analiza una columna específica |
| `🧮 Seleccionar N columnas` | Analiza múltiples columnas |

### 🤖 Asistente IA
| Comando | Descripción |
|---------|-------------|
| `🤖 Hacer pregunta IA` | Consulta sobre tus datos usando IA |

## 🗂️ Formatos Soportados
- Archivos CSV (hasta 20MB)
- Codificación UTF-8 recomendada

## 💡 Ejemplos de Preguntas IA
Puedes hacer preguntas como:
- "¿Cuál es la correlación entre X e Y?"
- "Muéstrame las tendencias principales"
- "¿Hay valores atípicos en los datos?"
- "Genera 3 insights clave de estos datos"
- "¿Cuál es la distribución de la columna Z?"

## ⚠️ Limitaciones
1. Tamaño máximo de archivo: 20MB
2. Para datasets muy grandes, considera usar una muestra
3. La API gratuita de Groq tiene límites de uso
4. El bot no modifica tus archivos originales

## 📌 Ejemplo de Uso
1. Envía tu archivo CSV al bot
2. Explora los datos con los botones del menú
3. Haz preguntas específicas usando el asistente IA
4. Descubre patrones y insights en tus datos

## 🛠️ Solución de Problemas
Si encuentras errores:
- Verifica que tu archivo CSV esté bien formado
- Comprueba que tienes las dependencias instaladas
- Asegúrate de que tus API keys sean válidas
- Revisa los permisos de los archivos

## 📜 Licencia
MIT License © 2023 [JairVaz13](https://github.com/JairVaz13)