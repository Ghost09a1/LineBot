from typing import Final
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    CallbackContext,
)
from datetime import datetime
from googleapiclient.discovery import build
import random
import requests
import json
from requests import (
    get,
    post
)
import base64



print("Lama loading...")

# Retrieve the token from environment variables
TOKEN: Final = "7067874373:AAGZhFjc0OT2DnWJnV0ZoU-gAnF33aLuuB8"
BOT_USERNAME: Final = "@Lamageek_bot"

# Provide your Spotify API key
SPOTIFY_CLIENT_ID = "d843ee9f564640e2b78522d11a103549"
SPOTIFY_CLIENT_Secret = "b3e15ab5a5194500852c823cd36ee4ae"

#Provide your RandomFact API
RANDOM_FACT_API_KEY =  "9gE1Y+oGrDxZqvi6LBXESw==HtvwTX4mlphHJUei"

# Provide your YouTube API key
YOUTUBE_API_KEY = "AIzaSyAhr7ZqL5ec8Q309AOa9SE7MMGv0HKrVkQ"

# Initialize the YouTube service
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)


#RFact API Logic

def get_facts(limit=1):
    api_url = 'https://api.api-ninjas.com/v1/facts?limit={}'.format(limit)
    response = requests.get(api_url, headers={'X-Api-Key'=='RANDOM_FACT_API_KEY'})
    if response.status_code == requests.codes.ok:
        print(response.text)



# Youtube API Logic


def search_workout_videos():
    # Search for workout videos on YouTube
    request = youtube.search().list(
        q="workout",
        type="video",
        part="snippet",
        maxResults=10,  # You can adjust the number of results as needed
    )
    response = request.execute()

    # Get the list of video IDs from the search results
    video_ids = [item["id"]["videoId"] for item in response["items"]]

    return video_ids


async def youtube_command(update: Update, context: CallbackContext):
    # Search for workout videos
    video_ids = search_workout_videos()

    # Select a random video ID
    random_video_id = random.choice(video_ids)

    # Construct the video URL
    video_url = f"https://www.youtube.com/watch?v={random_video_id}"

    # Reply to the user with the video URL
    await update.message.reply_text(f"Here's a random workout video for you: {video_url}")


# Radom Fact API logic:

async def rfact_command(update: Update, context: CallbackContext):
    await.update. messagea= get_facts()
    return update.message.reply_text(f"Here's a random fact for you:{messagea}")



# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I am a magic Lama!")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I am an helping Lama!")


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I am a hungry Lama!")


# API Command


async def spotify_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("reply Api outPUT")


# Responses


def handle_response(text: str) -> str:
    processed: str = text.lower()

    if "hello" in processed:
        return "Hey! How are you?"

    if "who are you" in processed:
        return "I am a magical Lama and I am here to help you."

    if "i love lamas" in processed:
        return "I love you too!"

    return "i do not understand you!"


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

    print("Lama", response)
    await update.message.reply_text(response)


# loging errors


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


if __name__ == "__main__":
    print("Materializing Lama!")
    app = Application.builder().token(TOKEN).build()

    # commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))
    app.add_handler(CommandHandler("spotify", spotify_command))
    app.add_handler(CommandHandler("youtube", youtube_command))
    app.add_handler(CommandHandler("fact", rfact_command))

    # messages
    app.add_handler(MessageHandler(filters.Text(), handle_message))

    # errors
    app.add_error_handler(error)

    # Polling
    print("Lama is polling...")
    app.run_polling(poll_interval=0.5)
