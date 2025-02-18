# from pyrogram.types import User,Chat,Message,InlineKeyboardMarkup
from pyrogram import Client,enums
from modules.utils import *
from icecream import ic
import asyncio
import time

system_stats = get_system_usage()
print("===========SYSTEM STATUS============")
print(f"CPU Usage: {system_stats['cpu_usage_percent']}%")
print(f"RAM Usage: {system_stats['ram_usage_percent']}%")
print(f"Disk Usage: {system_stats['disk_usage_percent']}%")
print(f"Space Free: {system_stats['disk_available_space']}/{system_stats['disk_total_space']}")
print(f"Space Used: {system_stats['disk_used_space']}/{system_stats['disk_total_space']}")
print("======================================")
# Main Method 
async def main():
    app = Client("tg_bot",api_id=API_ID, api_hash=API_HASH,bot_token=BOT_TOKEN)

    # loop = asyncio.get_running_loop()  # Get the main event loop
    
    mqtt_client = MQTTWebSocketClient(
        host=WEBSOCK_BROKER_ADDRESS,
        port=WEBSOCK_PORT,
        username=MQTT_USER,
        password=MQTT_PASS,
        use_ssl=WEBSOCK_USE_SSL,
        clean_session=CLEAN_SESSION,
        retained=RETAINED,
        qos=QOS,
        use_creds=USE_CREDS
    )
    # Connect to MQTT client
    await mqtt_client.connect()

    # Subscribe to online for all the tokens
    async def subscribe_online():
        dataset = mongoClient.fetch()
        for data in dataset:
            await mqtt_client.subscribe_to_online_topic(token=data['token'])
    await subscribe_online()   

    #insert new data else update if alredy exists
    async def insertOrUpdate(data:dict):
        records = mongoClient.fetch({"userid":data['userid']})
        await mqtt_client.subscribe_to_online_topic(token=data['token'])
        if len(records)>0:
            # mqtt_client.unsubscribe_topics(token=data['token'])
            resp = mongoClient.update(prev={"userid":data['userid']},nxt=data)
            if resp:return "✔️ Data Updated"
        resp = mongoClient.insert(data)
        if resp:return "✔️ New Data Inserted"
        return False 

    async with app:
        # Send message When Board Goes Offline And Comes Back Online
        async def mqtt_message_callback(topic, payload):
            dataset = mongoClient.fetch()
            for data in dataset:
                db_topic = data["token"]+"/online"
                if db_topic == topic:
                    # print(f"📩 MQTT Message Received: Topic -> {topic}, Payload -> {payload}")
                    print(f"Sending message to {data['userid']} for {topic} with value: {payload}")
                    if int(payload) ==  1:
                        await app.send_message(chat_id=data['userid'], text=f"🟢 Device is Online",parse_mode=enums.ParseMode.MARKDOWN)
                    elif int(payload) ==  0:
                        await app.send_message(chat_id=data['userid'], text=f"🔴 Device is Offline",parse_mode=enums.ParseMode.MARKDOWN)    
        
        mqtt_client.set_message_callback(mqtt_message_callback) 

        ic("Listening to messages on @mstapibot")  
        await app.send_message(chat_id=6848546800, text="🤖 Bot is Running 😊",parse_mode=enums.ParseMode.MARKDOWN)
    
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
                resp = await insertOrUpdate(data)
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
        
            # Trigger the switches
            elif parts[0].upper() in PINS and list_len==2 and int(parts[1]) in [0,1]: 
                # await message.reply_text(parts[1], quote=False) 
                user = mongoClient.fetch({"userid":uid})   
                switch =  parts[0].upper()
                switch_value = int(parts[1])
                if user:
                    await mqtt_client.update_topic_value(f"{user[0]['token']}/{switch}",switch_value)
                    await message.reply_text(f"✔️Triggerred \n {switch}:{switch_value} ", quote=False,parse_mode=enums.ParseMode.MARKDOWN)
                else:await message.reply_text("⚠️ No Token Added", quote=False,parse_mode=enums.ParseMode.MARKDOWN)

                # await client.edit_message_text(chat_id=cid, message_id=sentdata.id, text=f"Exception: {e}")
                # await message.reply_text(msg, quote=True,parse_mode=enums.ParseMode.MARKDOWN)

            # Do a speedtest
            elif parts[0] == "/speedtest" and list_len == 1:
                sentdata = await message.reply_text("Running the Horses. Please Wait", quote=True,parse_mode=enums.ParseMode.MARKDOWN)
                start_time = time.time()
                # ic("Performing Speedtest")
                speedtest = perform_speedtest()
                # ic("Speedtest Done")
                stop_time = time.time()-start_time
                if speedtest:
                    msg = (
                        f"**📥 Download Speed:** {get_file_size(speedtest['download_speed']/8)}/s \n"
                        f"**📤 Upload Speed:** {get_file_size(speedtest['upload_speed']/8)}/s\n"
                        f"**🏓 Ping:** {speedtest['ping']} ms\n"
                        f"**⌛ Time Taken:** {stop_time:.0f}s"
                    )
                    await client.edit_message_text(chat_id=cid, message_id=sentdata.id, text=msg)
                else:    
                    await client.edit_message_text(chat_id=cid, message_id=sentdata.id, text="Unable to Fetch Speed :-( ")

            # Fetch Server Stats
            elif parts[0] == "/stats" and list_len == 1:
                    stats = get_system_usage()
                    msg = (
                        f"**CPU Usage:** {stats['cpu_usage_percent']}%\n"
                        f"**RAM Usage:** {stats['ram_usage_percent']}%\n"
                        f"**Disk Usage:** {stats['disk_usage_percent']}%\n"
                        f"**Disk Used:** {stats['disk_used_space']}/{stats['disk_total_space']}\n"
                        f"**Disk Free:** {stats['disk_available_space']}/{stats['disk_total_space']}\n"
                    )
                    await message.reply_text(msg, quote=True,parse_mode=enums.ParseMode.MARKDOWN)

            else:
                await message.reply_text("No Valid Command\ntry /help for Help", quote=True,parse_mode=enums.ParseMode.MARKDOWN) 

        # Use asyncio to keep the program running
        try:
            await asyncio.Future()  # Keeps the program running indefinitely
        except KeyboardInterrupt:
            print("Bot stopping...")
                       
if __name__ == "__main__":
    asyncio.run(main())