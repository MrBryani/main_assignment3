from dotenv import load_dotenv
from groq import Groq
import discord
import os

# Load environment variables from .env file
load_dotenv()
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
DISCORD_TOKEN = os.getenv('TOKEN')

# Initialize the OpenAI client
groq_client = Groq(api_key=GROQ_API_KEY)

def call_groq(question):
    completion = groq_client.chat.completions.create(
        model="llama-3.3-0b-versatile",
        messages=[
             {
                 "role": "user",
                 "content": f"Respond like a pirate to the following question:  {question}",
            },
        ]
    )
    # Print the response
    response = completion.choices[0].message.content
    print(response)
    return response


# Set up discord
intents = discord.Intents.default()
intents.message_content = True  
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$question'):
        print(f"Message: {message.content}")                
        message_content = message.content.split("$question")[1]
        print(f"Question: {message_content}")    
        response = call_groq(message_content)   
        print(f"Assistant: {response}")    
        print("---")
        await message.channel.send(response)

client.run(DISCORD_TOKEN)
