from telegram import *
from telegram.ext import *

CONFIRMATION_TRIGGERED, WELCOMED = range(2)

def start(update, context):
    if 'user_data' in context.chat_data and context.chat_data['user_data'].get('bot_confirmed'):
        update.message.reply_text('Welcome!')
    else:
        update.message.reply_text('Please confirm you are not a bot by sharing your phone number contact.', reply_markup=ReplyKeyboardMarkup([[KeyboardButton('Share contact', request_contact=True)]]))
        return CONFIRMATION_TRIGGERED

def bot_confirmation(update, context):
    user_data = context.chat_data.setdefault('user_data', {})
    if update.message.contact:
        user_data['bot_confirmed'] = True
        update.message.reply_text('Thank you for confirming! Welcome!')
        return WELCOMED
    else:
        update.message.reply_text('Please share your phone number to confirm you are not a bot.')
        return CONFIRMATION_TRIGGERED

def cancel(update, context):
    update.message.reply_text('Bot confirmation canceled.')
    return ConversationHandler.END

def main():
    updater = Updater("6424653885:AAFqnHilrl7CbmEsk-ZOwC-NoOFOoivjTps", use_context=True)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CONFIRMATION_TRIGGERED: [MessageHandler(Filters.contact, bot_confirmation)],
            WELCOMED: []
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
