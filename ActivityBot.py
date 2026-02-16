import discord
import os
from dotenv import load_dotenv

# Load our environment variables from .env
load_dotenv()

# Grab the important IDs and token from environment
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TRACK_USER_ID = os.getenv("TRACK_USER_ID")    # the user we are tracking
CHANNEL_ID = os.getenv("CHANNEL_ID")          # the channel to post updates
NOTIFY_USER_ID = os.getenv("NOTIFY_USER_ID")  # optional: DM me as well

# Validate required info
if not DISCORD_TOKEN:
    raise RuntimeError("DISCORD_TOKEN is missing in .env!")

if not TRACK_USER_ID:
    raise RuntimeError("TRACK_USER_ID is missing in .env!")

if not CHANNEL_ID:
    raise RuntimeError("CHANNEL_ID is missing in .env!")

# Convert IDs to integers
TRACK_USER_ID = int(TRACK_USER_ID)
CHANNEL_ID = int(CHANNEL_ID)
NOTIFY_USER_ID = int(NOTIFY_USER_ID) if NOTIFY_USER_ID else None

# Discord intents: we need presence updates and member info
intents = discord.Intents.default()
intents.members = True
intents.presences = True

# Create the bot client
client = discord.Client(intents=intents)

# Keep track of the last song to avoid spamming messages
last_song = None


@client.event
async def on_ready():
    # This runs when the bot successfully logs in
    print(f"Logged in as {client.user}")
    print(f"Tracking user ID: {TRACK_USER_ID}")
    print(f"Channel notifications ID: {CHANNEL_ID}")
    print(f"DM notifications ID: {NOTIFY_USER_ID}")


async def send_notification(message: str):
    """
    Send a message either to the channel, or DM if configured.
    DM has priority, channel is fallback if DM fails or is missing.
    """
    # First, send to the channel
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(message)

    # Then, if NOTIFY_USER_ID is set, send a DM as well
    if NOTIFY_USER_ID:
        try:
            user = await client.fetch_user(NOTIFY_USER_ID)
            await user.send(message)
        except Exception as e:
            # Don't crash if DM fails, just log
            print(f"[WARN] Could not send DM: {e}")


@client.event
async def on_presence_update(before, after):
    """
    Fires every time someone's presence changes (status, activities, Spotify, etc.)
    We only care about the tracked user and Spotify activity.
    """
    global last_song

    # Ignore everyone else
    if after.id != TRACK_USER_ID:
        return

    # Check if the user is listening to Spotify
    spotify_activity = None
    for activity in after.activities:
        if isinstance(activity, discord.Spotify):
            spotify_activity = activity
            break

    # --- User is listening to a song ---
    if spotify_activity:
        current_song = f"{spotify_activity.title} - {spotify_activity.artist}"

        # Only notify if the song changed
        if current_song != last_song:
            last_song = current_song
            msg = f"🎵 **{after.name}** is listening to:\n{current_song}"
            await send_notification(msg)
            print(f"[NOTIFY] {msg}")

    # --- User stopped listening to Spotify ---
    else:
        if last_song is not None:
            msg = f"⏹ **{after.name}** stopped listening to Spotify"
            await send_notification(msg)
            print(f"[NOTIFY] {msg}")
            last_song = None


# Start the bot
client.run(DISCORD_TOKEN)
