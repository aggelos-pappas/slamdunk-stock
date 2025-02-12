import discord
from datetime import datetime
import pytz
from discord import app_commands
from curl_cffi import requests
import re

TOKEN = "YOUR_BOT_TOKEN"
SERVER_ID = 0 # Your server ID
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
@client.event
async def on_ready():
  await tree.sync(guild=discord.Object(id=SERVER_ID))
  print(f"We have logged in as {client.user}")

@tree.command(name="slamdunk_raffle", description="Get available sizes and stock for a raffle product",guild=discord.Object(id=SERVER_ID))
async def raffle(interaction: discord.Interaction, url: str):
    try:
        match = re.search(r"https://raffle\.slamdunk\.gr/products/([\w-]+)", url)
        if not match:
            await interaction.response.send_message("Invalid URL format.", ephemeral=True)
            return
        
        slug = match.group(1)
        api_url = f"https://raffle-api.slamdunk.gr/v1/el/products/getbyurl?url={slug}"
        response = requests.get(api_url , impersonate="chrome")
        
        if response.status_code != 200:
            await interaction.response.send_message("Failed to fetch raffle data.", ephemeral=True)
            return
        
        data = response.json()
        dimensions = data.get("dimensions", [])
        img = data.get("img2", "https://static.vecteezy.com/system/resources/previews/004/141/669/non_2x/no-photo-or-blank-image-icon-loading-images-or-missing-image-mark-image-not-available-or-image-coming-soon-sign-simple-nature-silhouette-in-frame-isolated-illustration-vector.jpg")
        img = img.split('?')[0]  # Remove query parameters if present
        prodId = data.get("id", "N/A")


        if not dimensions:
            await interaction.response.send_message("No size data available.", ephemeral=True)
            return

        sizes_info = ""
        for item in dimensions:
            size = item.get("svtxt", "Unknown")
            stock = item.get("qty", 0)
            sizes_info += f"Size {size}: {stock} in stock\n"
        
        embed = discord.Embed(title=data.get("nm", "Raffle Product"), url=url, color=discord.Color.yellow())
        embed.set_image(url=img)  # Use set_image instead of set_thumbnail
        embed.add_field(name="Price", value=f"€{data.get('prc', 'N/A')}", inline=True)

        embed.set_footer(text="Powered by Prime Notify • Aggelos")
        if prodId != "N/A":
            api_url = f"https://raffle-api.slamdunk.gr/v1/el/contests/getbyproduct?id={prodId}"
            response = requests.get(api_url , impersonate="chrome")
            print(response.status_code)
            data = response.json()
            endDate = data.get("edt", "N/A")
            dt_str = endDate
            dt = datetime.fromisoformat(dt_str)

            # Step 2: Localize to Greek timezone (Europe/Athens) using pytz
            greek_tz = pytz.timezone("Europe/Athens")
            dt_greek = greek_tz.localize(dt)

            # Step 3: Convert to Unix timestamp
            timestamp = int(dt_greek.timestamp())

            # Step 4: Format for Discord
            discord_time = f"<t:{timestamp}:f>"
            embed.add_field(name="Ends", value=discord_time, inline=True)
        embed.add_field(name="Stock Info", value=sizes_info, inline=False)
        
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)

client.run(TOKEN)