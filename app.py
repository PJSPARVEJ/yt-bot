import discord
from discord.ext import tasks
import requests
import os

# সেটিংস
TOKEN = 'MTQ2NDk1OTcwOTI5ODgxOTIwNQ.G6fSYj.Hx1isumDfShqHYK'
CHANNEL_ID = 1474106188843974659  # ডিসকর্ড চ্যানেল আইডি
YT_API_KEY = 'AIzaSyAscOzV562qSrbOfJY9OUfZlk5JTUkHAWY'
CHANNEL_ID_YT = 'UC5OsmUsmg7h97p2N1gPNe3w'
FILE_NAME = "last_video_id.txt" # সর্বশেষ ভিডিওর আইডি সেভ রাখার ফাইল

client = discord.Client(intents=discord.Intents.default())

@tasks.loop(minutes=5) # প্রতি ৫ মিনিট পর পর চেক করবে
async def check_youtube():
    try:
        # ইউটিউব এপিআই থেকে ডাটা আনা (শুধু ভিডিওর জন্য type=video যোগ করা হয়েছে)
        url = f"https://www.googleapis.com/youtube/v3/search?key={YT_API_KEY}&channelId={CHANNEL_ID_YT}&part=snippet,id&order=date&maxResults=1&type=video"
        response = requests.get(url).json()
        
        # ডাটা আছে কি না চেক করা
        if 'items' not in response or not response['items']:
            return

        latest_video_id = response['items'][0]['id']['videoId']
        video_url = f"https://www.youtube.com/watch?v={latest_video_id}"

        # ফাইল থেকে আগের ভিডিও আইডি পড়া
        last_id = ""
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "r") as f:
                last_id = f.read().strip()

        # যদি বর্তমান আইডি আগের আইডির সাথে না মিলে (তার মানে নতুন ভিডিও)
        if latest_video_id != last_id:
            channel = client.get_channel(CHANNEL_ID)
            if channel:
                await channel.send(f"@everyone 📢 নতুন ভিডিও আপলোড! 🎬 CODEVERSE YouTube চ্যানেলে নতুন ভিডিও এসেছে: {video_url}")
                
                # নতুন আইডিটি ফাইলে লিখে রাখা যাতে পরে আর না পাঠায়
                with open(FILE_NAME, "w") as f:
                    f.write(latest_video_id)
                print(f"New video found and posted: {latest_video_id}")

    except Exception as e:
        print(f"Error checking YouTube: {e}")

@client.event
async def on_ready():
    print(f'{client.user} হিসেবে লগইন হয়েছে!')
    
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening, 
            name='CodeVerse & RedOx ❤️'
        )
    )
    
    if not check_youtube.is_running():
        check_youtube.start()

client.run(TOKEN)
