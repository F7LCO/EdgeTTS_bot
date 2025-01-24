import edge_tts
import tempfile
import os
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
)

TOKEN = "7768230218:AAEl2r7lVXgqeENv6cCIP-2O0XVjRMvnSg4"
USERNAME = "@EdgeTTS_free_bot"
voice_models = ["af-ZA-AdriNeural", "af-ZA-WillemNeural", "am-ET-AmehaNeural", "am-ET-MekdesNeural", "ar-AE-FatimaNeural", "ar-AE-HamdanNeural", "ar-BH-AliNeural", "ar-BH-LailaNeural", "ar-DZ-AminaNeural", "ar-DZ-IsmaelNeural", "ar-EG-SalmaNeural", "ar-EG-ShakirNeural", "ar-IQ-BasselNeural", "ar-IQ-RanaNeural", "ar-JO-SanaNeural", "ar-JO-TaimNeural", "ar-KW-FahedNeural", "ar-KW-NouraNeural", "ar-LB-LaylaNeural", "ar-LB-RamiNeural", "ar-LY-ImanNeural", "ar-LY-OmarNeural", "ar-MA-JamalNeural", "ar-MA-MounaNeural", "ar-OM-AbdullahNeural", "ar-OM-AyshaNeural", "ar-QA-AmalNeural", "ar-QA-MoazNeural", "ar-SA-HamedNeural", "ar-SA-ZariyahNeural", "ar-SY-AmanyNeural", "ar-SY-LaithNeural", "ar-TN-HediNeural", "ar-TN-ReemNeural", "ar-YE-MaryamNeural", "ar-YE-SalehNeural", "az-AZ-BabekNeural", "az-AZ-BanuNeural", "bg-BG-BorislavNeural", "bg-BG-KalinaNeural", "bn-BD-NabanitaNeural", "bn-BD-PradeepNeural", "bn-IN-BashkarNeural", "bn-IN-TanishaaNeural", "bs-BA-GoranNeural", "bs-BA-VesnaNeural", "ca-ES-EnricNeural", "ca-ES-JoanaNeural", "cs-CZ-AntoninNeural", "cs-CZ-VlastaNeural", "cy-GB-AledNeural", "cy-GB-NiaNeural", "da-DK-ChristelNeural", "da-DK-JeppeNeural", "de-AT-IngridNeural", "de-AT-JonasNeural", "de-CH-JanNeural", "de-CH-LeniNeural", "de-DE-AmalaNeural", "de-DE-ConradNeural", "de-DE-FlorianMultilingualNeural", "de-DE-KatjaNeural", "de-DE-KillianNeural", "de-DE-SeraphinaMultilingualNeural", "el-GR-AthinaNeural", "el-GR-NestorasNeural", "en-AU-NatashaNeural", "en-AU-WilliamNeural", "en-CA-ClaraNeural", "en-CA-LiamNeural", "en-GB-LibbyNeural", "en-GB-MaisieNeural", "en-GB-RyanNeural", "en-GB-SoniaNeural", "en-GB-ThomasNeural", "en-HK-SamNeural", "en-HK-YanNeural", "en-IE-ConnorNeural", "en-IE-EmilyNeural", "en-IN-NeerjaExpressiveNeural", "en-IN-NeerjaNeural", "en-IN-PrabhatNeural", "en-KE-AsiliaNeural", "en-KE-ChilembaNeural", "en-NG-AbeoNeural", "en-NG-EzinneNeural", "en-NZ-MitchellNeural", "en-NZ-MollyNeural", "en-PH-JamesNeural", "en-PH-RosaNeural", "en-SG-LunaNeural", "en-SG-WayneNeural", "en-TZ-ElimuNeural", "en-TZ-ImaniNeural", "en-US-AnaNeural", "en-US-AndrewMultilingualNeural", "en-US-AndrewNeural", "en-US-AriaNeural", "en-US-AvaMultilingualNeural", "en-US-AvaNeural", "en-US-BrianMultilingualNeural", "en-US-BrianNeural", "en-US-ChristopherNeural", "en-US-EmmaMultilingualNeural", "en-US-EmmaNeural", "en-US-EricNeural", "en-US-GuyNeural", "en-US-JennyNeural", "en-US-MichelleNeural", "en-US-RogerNeural", "en-US-SteffanNeural", "en-ZA-LeahNeural", "en-ZA-LukeNeural", "es-AR-ElenaNeural", "es-AR-TomasNeural", "es-BO-MarceloNeural", "es-BO-SofiaNeural", "es-CL-CatalinaNeural", "es-CL-LorenzoNeural", "es-CO-GonzaloNeural", "es-CO-SalomeNeural", "es-CR-JuanNeural", "es-CR-MariaNeural", "es-CU-BelkysNeural", "es-CU-ManuelNeural", "es-DO-EmilioNeural", "es-DO-RamonaNeural", "es-EC-AndreaNeural", "es-EC-LuisNeural", "es-ES-AlvaroNeural", "es-ES-ElviraNeural", "es-ES-XimenaNeural", "es-GQ-JavierNeural", "es-GQ-TeresaNeural", "es-GT-AndresNeural", "es-GT-MartaNeural", "es-HN-CarlosNeural", "es-HN-KarlaNeural", "es-MX-DaliaNeural", "es-MX-JorgeNeural", "es-NI-FedericoNeural", "es-NI-YolandaNeural", "es-PA-MargaritaNeural", "es-PA-RobertoNeural", "es-PE-AlexNeural", "es-PE-CamilaNeural", "es-PR-KarinaNeural", "es-PR-VictorNeural", "es-PY-MarioNeural", "es-PY-TaniaNeural", "es-SV-LorenaNeural", "es-SV-RodrigoNeural", "es-US-AlonsoNeural", "es-US-PalomaNeural", "es-UY-MateoNeural", "es-UY-ValentinaNeural", "es-VE-PaolaNeural", "es-VE-SebastianNeural", "et-EE-AnuNeural", "et-EE-KertNeural", "fa-IR-DilaraNeural", "fa-IR-FaridNeural", "fi-FI-HarriNeural", "fi-FI-NooraNeural", "fil-PH-AngeloNeural", "fil-PH-BlessicaNeural", "fr-BE-CharlineNeural", "fr-BE-GerardNeural", "fr-CA-AntoineNeural", "fr-CA-JeanNeural", "fr-CA-SylvieNeural", "fr-CA-ThierryNeural", "fr-CH-ArianeNeural", "fr-CH-FabriceNeural", "fr-FR-DeniseNeural", "fr-FR-EloiseNeural", "fr-FR-HenriNeural", "fr-FR-RemyMultilingualNeural", "fr-FR-VivienneMultilingualNeural", "ga-IE-ColmNeural", "ga-IE-OrlaNeural", "gl-ES-RoiNeural", "gl-ES-SabelaNeural", "gu-IN-DhwaniNeural", "gu-IN-NiranjanNeural", "he-IL-AvriNeural", "he-IL-HilaNeural", "hi-IN-MadhurNeural", "hi-IN-SwaraNeural", "hr-HR-GabrijelaNeural", "hr-HR-SreckoNeural", "hu-HU-NoemiNeural", "hu-HU-TamasNeural", "id-ID-ArdiNeural", "id-ID-GadisNeural", "is-IS-GudrunNeural", "is-IS-GunnarNeural", "it-IT-DiegoNeural", "it-IT-ElsaNeural", "it-IT-GiuseppeMultilingualNeural", "it-IT-IsabellaNeural", "iu-Cans-CA-SiqiniqNeural", "iu-Cans-CA-TaqqiqNeural", "iu-Latn-CA-SiqiniqNeural", "iu-Latn-CA-TaqqiqNeural", "ja-JP-KeitaNeural", "ja-JP-NanamiNeural", "jv-ID-DimasNeural", "jv-ID-SitiNeural", "ka-GE-EkaNeural", "ka-GE-GiorgiNeural", "kk-KZ-AigulNeural", "kk-KZ-DauletNeural", "km-KH-PisethNeural", "km-KH-SreymomNeural", "kn-IN-GaganNeural", "kn-IN-SapnaNeural", "ko-KR-HyunsuMultilingualNeural", "ko-KR-InJoonNeural", "ko-KR-SunHiNeural", "lo-LA-ChanthavongNeural", "lo-LA-KeomanyNeural", "lt-LT-LeonasNeural", "lt-LT-OnaNeural", "lv-LV-EveritaNeural", "lv-LV-NilsNeural", "mk-MK-AleksandarNeural", "mk-MK-MarijaNeural", "ml-IN-MidhunNeural", "ml-IN-SobhanaNeural", "mn-MN-BataaNeural", "mn-MN-NarantsetsegNeural", "mr-IN-AarohiNeural", "mr-IN-ManoharNeural", "ms-MY-OsmanNeural", "ms-MY-YasminNeural", "mt-MT-GabrielNeural", "mt-MT-GraceNeural", "my-MM-NilarNeural", "my-MM-ThihaNeural", "nb-NO-FinnNeural", "nb-NO-IselinNeural", "ne-NP-HemkalaNeural", "ne-NP-SagarNeural", "nl-BE-ArnaudNeural", "nl-BE-DenaNeural", "nl-NL-ColetteNeural", "nl-NL-FennaNeural", "pl-PL-ZofiaNeural", "pl-PL-MarekNeural"]
# Conversation states
CHOOSING_VOICE = 1

# Initialize the default voice
selected_voice = "en-US-AndrewNeural"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! Welcome to EdgeTTS.\n\n"
        "EdgeTTS is a free text-to-speech bot created using the Edge TTS library. "
        "It is developed by @F9LCO. Enter /help for more details.\n\n"
        "Send the text you want to convert to speech."
    )


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "EdgeTTS is a free text-to-speech Telegram bot created using Python's Edge TTS library. "
        "It is intended for educational purposes, so please avoid overuse as the library has limitations.\n\n"
        "This bot is created by @F9LCO.\n\n"
        "Command list:\n"
        "/help - Information about the bot.\n"
        "/voices - List of available voices.\n"
        "/set_voice - Set a specific voice.\n"
        "/start - Start the bot."
    )


async def voice_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = "Available voices:\n"
    message_chunks = []
    for index, voice in enumerate(voice_models, 1):
        response += f"[{index}] {voice}\n"
        if len(response) > 4000:  # Split into smaller chunks
            message_chunks.append(response)
            response = ""
    if response:
        message_chunks.append(response)

    for chunk in message_chunks:
        await update.message.reply_text(chunk)


async def set_voice_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Please choose a voice by sending its number from the list below:\n"
    )
    await voice_list(update, context)
    return CHOOSING_VOICE


async def set_voice_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global selected_voice
    try:
        voice_number = int(update.message.text) - 1  # Convert to 0-based index
        if 0 <= voice_number < len(voice_models):
            selected_voice = voice_models[voice_number]
            await update.message.reply_text(f"Voice set to: {selected_voice}")
            await update.message.reply_text("Send the text you want to convert to speech.")
            return ConversationHandler.END
        else:
            await update.message.reply_text("Invalid voice number. Please send a valid number.")
            return CHOOSING_VOICE
    except ValueError:
        await update.message.reply_text("Invalid input. Please send a number.")
        return CHOOSING_VOICE


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global selected_voice
    text = update.message.text

    # Show a loading message
    loading_message = await update.message.reply_text("Generating voice, please wait...")

    # Generate speech using the selected voice
    communicate = edge_tts.Communicate(text, voice=selected_voice)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        await communicate.save(tmp_file.name)
        tmp_file_path = tmp_file.name

    # Send the generated speech as a voice message to the user
    with open(tmp_file_path, "rb") as audio_file:
        await update.message.reply_voice(voice=audio_file, caption=f"Voice used: {selected_voice}")
        await update.message.reply_text("Send new text if you want another conversion.")

    # Delete the loading message
    await context.bot.delete_message(chat_id=update.message.chat.id, message_id=loading_message.message_id)

    # Clean up the temporary file
    os.remove(tmp_file_path)


async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Sorry, I didn't understand that.")


def main():
    app = Application.builder().token(TOKEN).build()

    # Define a conversation handler for /set_voice
    set_voice_handler = ConversationHandler(
        entry_points=[CommandHandler("set_voice", set_voice_start)],
        states={
            CHOOSING_VOICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_voice_end)],
        },
        fallbacks=[MessageHandler(filters.COMMAND, unknown_command)],
    )

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("voices", voice_list))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(set_voice_handler)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    app.add_handler(MessageHandler(filters.COMMAND, unknown_command))

    app.run_polling()


if __name__ == "__main__":
    main()
