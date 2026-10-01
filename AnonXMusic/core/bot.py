from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode

import config

from ..logging import LOGGER


class Anony(Client):
    def __init__(self):
        LOGGER(__name__).info("Starting Bot...")

        super().__init__(
            name="AnonXMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            parse_mode=ParseMode.HTML,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        await super().start()

        self.id = self.me.id
        self.name = (
            self.me.first_name
            + " "
            + (self.me.last_name or "")
        )
        self.username = self.me.username
        self.mention = self.me.mention

        # Check and send message to LOGGER_ID
        try:
            await self.send_message(
                chat_id=config.LOGGER_ID,
                text=(
                    f"<u><b>» {self.mention} ʙᴏᴛ sᴛᴀʀᴛᴇᴅ :</b></u>\n\n"
                    f"ɪᴅ : <code>{self.id}</code>\n"
                    f"ɴᴀᴍᴇ : {self.name}\n"
                    f"ᴜsᴇʀɴᴀᴍᴇ : @{self.username}"
                ),
            )

        except errors.ChannelInvalid:
            LOGGER(__name__).error(
                "LOGGER_ID is invalid or the channel/group cannot be accessed."
            )
            raise

        except errors.PeerIdInvalid:
            LOGGER(__name__).error(
                "LOGGER_ID is invalid. Use the numeric Telegram chat ID "
                "such as -100xxxxxxxxxx."
            )
            raise

        except errors.ChatAdminRequired:
            LOGGER(__name__).error(
                "Bot does not have permission to access the LOGGER_ID chat."
            )
            raise

        except Exception as ex:
            LOGGER(__name__).error(
                "Bot failed to access LOGGER_ID.\n"
                f"Error Type: {type(ex).__name__}\n"
                f"Error: {ex}"
            )
            raise

        # Check whether bot is administrator
        try:
            member = await self.get_chat_member(
                config.LOGGER_ID,
                self.id,
            )

            if member.status != ChatMemberStatus.ADMINISTRATOR:
                LOGGER(__name__).error(
                    "Please promote the bot as an administrator "
                    "in your log group/channel."
                )
                raise RuntimeError(
                    "Bot is not an administrator in LOGGER_ID."
                )

        except Exception as ex:
            LOGGER(__name__).error(
                "Failed to check bot administrator status.\n"
                f"Error Type: {type(ex).__name__}\n"
                f"Error: {ex}"
            )
            raise

        LOGGER(__name__).info(
            f"Music Bot Started as {self.name}"
        )

    async def stop(self):
        LOGGER(__name__).info("Stopping Bot...")
        await super().stop()
