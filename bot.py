from telethon import TelegramClient, events

api_id = 17754061
api_hash = "5bed653b0b489617b09791468a289dfd"

source_chat = -1002833781652
source_topic = None          # None for no-topic groups

target_chat = -1003304114621
target_topic = None          # None for no-topic groups

start_id = 121750
end_id = None

client = TelegramClient("session", api_id, api_hash)


async def send_clean(msg):
    try:
        if target_topic:
            await client.send_message(
                target_chat,
                msg.text or "",
                file=msg.media,
                reply_to=target_topic
            )
        else:
            await client.send_message(
                target_chat,
                msg.text or "",
                file=msg.media
            )
    except Exception as e:
        print("Error:", e)


def match_topic(msg):
    if not source_topic:
        return True
    if not msg.reply_to:
        return False
    return msg.reply_to.reply_to_msg_id == source_topic


async def main():
    await client.start()

    async for msg in client.iter_messages(
        source_chat,
        reverse=True
    ):
        if not match_topic(msg):
            continue
        if start_id and msg.id < start_id:
            continue
        if end_id and msg.id > end_id:
            continue

        await send_clean(msg)

    @client.on(events.NewMessage(chats=source_chat))
    async def handler(event):
        if not match_topic(event.message):
            return
        if start_id and event.message.id < start_id:
            return
        if end_id and event.message.id > end_id:
            return
        await send_clean(event.message)

    await client.run_until_disconnected()


client.loop.run_until_complete(main())
