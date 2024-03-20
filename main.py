from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext  
from datetime import datetime


print("Lama loading...")

# Retrieve the token from environment variables
TOKEN: Final ="7067874373:AAGZhFjc0OT2DnWJnV0ZoU-gAnF33aLuuB8"
BOT_USERNAME: Final = '@Lamageek_bot'


# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('I am a magic Lama!')
                                    
                                                             
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('I am an helping Lama!')
                                    

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('I am a hungry Lama!')


# Responses

def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'hello' in processed:
        return 'Hey! How are you?'
    
    if 'who are you' in processed:
        return 'I am a magical Lama and I am here to help you.'
    
    if 'i love lamas' in processed:
        return 'I love you too!'
    
    return 'i do not understand you!'

# async def handle_message(update: Update, context: CallbackContext):
#     message_type = update.message.chat.type
#     text = update.message.text

#     print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

#     response = handle_response(text)

#     print('Lama:', response)
#     await update.message.reply_text(response)




async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    response: str = handle_response(text)

    print('Lama', response)
    await update.message.reply_text(response)

# loging errors

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == "__main__":
    print('Materializing Lama!')
    app = Application.builder().token(TOKEN).build()


    #commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))

    #messages
    app.add_handler(MessageHandler(filters.Text(), handle_message))

    #errors
    app.add_error_handler(error)

    #Polling 
    print('Lama is polling...')
    app.run_polling(poll_interval=0.5)

