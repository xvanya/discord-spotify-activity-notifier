import discord
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bot token and target user ID
TOKEN = os.getenv("DISCORD_TOKEN")
USER_ID = int(os.getenv("USER_ID"))

# Enable required intents
# presences is required to track Spotify activity
intents = discord.Intents.default()
intents.members = True
intents.presences = True

client = discord.Client(intents=intents)

# Stores last detected Spotify track
# Used to avoid duplicate notifications
last_song = None


@client.event
async def on_ready():
    # Triggered when the bot successfully connects to Discord
    print(f"Logged in as {client.user}")
    print("Tracking user activity...")


@client.event
async def on_presence_update(before, after):
    """
    This event is triggered every time a user's presence changes.
    Spotify updates can fire multiple presence updates,
    so extra checks are required to avoid duplicate messages.
    """
    global last_song

    # Ignore presence updates from other users
    if after.id != USER_ID:
        return

    # Debug output to see all activities
    print(f"[DEBUG] Activities for {after.name}: {after.activities}")

    spotify_activity = None

    # Look for Spotify activity
    for activity in after.activities:
        if isinstance(activity, discord.Spotify):
            spotify_activity = activity
            break

    # --- USER IS LISTENING TO SPOTIFY ---
    if spotify_activity:
        current_song = f"{spotify_activity.title} - {spotify_activity.artist}"

        # Send notification only if the track has changed
        if current_song != last_song:
            last_song = current_song
            user = await client.fetch_user(USER_ID)
            await user.send(f"{after.name} is listening to {current_song}")
            print(f"[NOTIFY] {after.name} is listening to {current_song}")

    # --- USER STOPPED LISTENING ---
    else:
        # Only notify once when Spotify activity disappears
        if last_song is not None:
            user = await client.fetch_user(USER_ID)
            await user.send(f"{after.name} stopped listening to Spotify")
            print(f"[NOTIFY] {after.name} stopped listening to Spotify")
            last_song = None


# Start the bot
client.run(TOKEN)
