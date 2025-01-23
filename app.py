# from pyrogram.types import User,Chat,Message,InlineKeyboardMarkup
from pyrogram import Client,filters,enums
from modules.utils import *
from icecream import ic
import asyncio

#insert new data else update if alredy exists
def insertOrUpdate(data:dict):
    records = mongoClient.fetch({"userid":data['userid']})
    if len(records)>0:
        # mqtt_client.unsubscribe_topics(token=data['token'])
        resp = mongoClient.update(prev={"userid":data['userid']},nxt=data)
        if resp:return "✔️ Data Updated"
    resp = mongoClient.insert(data)
    if resp:return "✔️ New Data Inserted"
    return False


# Main Method 
async def main():
    app = Client("tg_bot",api_id=API_ID, api_hash=API_HASH,bot_token=BOT_TOKEN)
        
    async with app:
        ic("Listening to messages on @mstapibot")  
        await app.send_message(chat_id=6848546800, text="🟢 Bot is Online",parse_mode=enums.ParseMode.MARKDOWN)
    
        @app.on_message()
        async def handle(client,message):
            mid,uid,uname,cid = message.id,message.from_user.id,message.from_user.username,message.chat.id
            # me = await app.get_me()
            
            #Breakdown the message into parts
            parts = message.text.split()
            list_len = len(parts)
            try:username = uname
            except:username = None 
            
            # Start the bot
            if parts[0] == "/start":
                await message.reply_text("👋**__Welcome to Bot__** ", quote=True,parse_mode=enums.ParseMode.MARKDOWN)

            # Attach your token to bot
            elif parts[0] == "/settoken" and list_len == 2:   
                token = parts[1]
                data = {"username":username,"userid":uid,"token":token}
                resp = insertOrUpdate(data)
                if resp: 
                    # mqtt_client.subscribe_topics(token=token)
                    await message.reply_text(resp, quote=False,parse_mode=enums.ParseMode.MARKDOWN)
                else: await message.reply_text("⚠️ Unable to set Token", quote=False)    

            # Fetch Current Token attached to Bot
            elif parts[0] == "/gettoken" and list_len == 1: 
                user = mongoClient.fetch({"userid":uid})  
                if user:
                    await message.reply_text(user[0]['token'], quote=True,parse_mode=enums.ParseMode.MARKDOWN)
                else:await message.reply_text("⚠️ No Token Added", quote=True,parse_mode=enums.ParseMode.MARKDOWN)

            # Detach Token attached to the bot
            elif parts[0] == "/revoketoken" and list_len == 1: 
                # mqtt_client.unsubscribe_topics(token=user['token'])
                response = mongoClient.delete({"userid":uid}) 
                if response:await message.reply_text("✔️ Done", quote=True,parse_mode=enums.ParseMode.MARKDOWN)
                else:await message.reply_text("⚠️ No Token Added", quote=True,parse_mode=enums.ParseMode.MARKDOWN)
        
            elif parts[0].upper() in PINS and list_len==2 and int(parts[1]) in [0,1]: 
                # await message.reply_text(parts[1], quote=False) 
                user = mongoClient.fetch({"userid":uid})   
                ic(parts)   
                switch =  parts[0].upper()
                switch_value = int(parts[1])
                print(switch,switch_value)
                if user:
                    mqtt_client.update_topic_value(f"{user[0]['token']}/{switch}",switch_value)
                    await message.reply_text(f"✔️Triggerred \n {switch}:{switch_value} ", quote=False,parse_mode=enums.ParseMode.MARKDOWN)
                else:await message.reply_text("⚠️ No Token Added", quote=False,parse_mode=enums.ParseMode.MARKDOWN)

                # await client.edit_message_text(chat_id=cid, message_id=sentdata.id, text=f"Exception: {e}")
                # await message.reply_text(msg, quote=True,parse_mode=enums.ParseMode.MARKDOWN)

            else:
                await message.reply_text("No Valid Command\ntry /help for Help", quote=True,parse_mode=enums.ParseMode.MARKDOWN) 

        # Use asyncio to keep the program running
        try:
            await asyncio.Future()  # Keeps the program running indefinitely
        except KeyboardInterrupt:
            print("Bot stopping...")
                       
if __name__ == "__main__":
    asyncio.run(main())