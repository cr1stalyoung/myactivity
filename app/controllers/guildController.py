from sqlalchemy import delete
from sqlalchemy.dialects.postgresql import insert
from app.controllers.baseController import PGSClient
from app.models.guildModel import GuildModel


class UpdateGuild(PGSClient):

    async def insert_new_guild(self, 
                               guild_id: int) -> None:
        async with PGSClient() as session:
            async with session.begin():
                await session.execute(
                    insert(GuildModel)
                    .values(guild_id=guild_id)
                    .on_conflict_do_nothing(index_elements=[GuildModel.guild_id])
                )

    async def delete_guild(self, 
                           guild_id: int) -> None:
        async with PGSClient() as session:
            async with session.begin():
                await session.execute(delete(GuildModel).where(GuildModel.guild_id == guild_id))
