from sqlalchemy import select, update, insert, func
from app.controllers.baseController import PGSClient, RedisClient
from app.models.guildModel import GuildModel
from app.models.profileModel import ProfileModel, CardModel, DecalModel, OperatorModel


class Cases(PGSClient, RedisClient):

    async def get_guild(self, 
                        guild_id:int):
        async with RedisClient() as client:
            cache = await client.get_data(f"get_guild_{guild_id}")
            if cache:
                return cache

            async with PGSClient() as session:
                async with session.begin():
                    guild = select(GuildModel.guild_id).filter(GuildModel.guild_id == guild_id)
                    result = await session.execute(guild)
                    result = result.scalar()
                    if result is not None:
                        await client.set_data(f"get_guild_{guild_id}", result, expire=300)
                        return result
                    else:
                        return None

    async def insert_new_guild(self, 
                               guild_id: int) -> None:
        async with PGSClient() as session:
            async with session.begin():
                profile = insert(GuildModel).values(guild_id=guild_id)
                await session.execute(profile)

    async def get_count_cases(self, 
                              guild_id: int):
        async with RedisClient() as client:
            cache = await client.get_data(f"count_case_{guild_id}")
            if cache:
                return cache

            async with PGSClient() as session:
                async with session.begin():
                    result = select(
                        func.sum(GuildModel.first_case).label('first_case'),
                        func.sum(GuildModel.second_case).label('second_case'),
                        func.sum(GuildModel.third_case).label('third_case'),
                        func.sum(GuildModel.total_case).label('total_case'),
                        func.sum(GuildModel.fourth_case).label('fourth_case'),
                        func.sum(GuildModel.fifth_case).label('fifth_case'),
                        func.sum(GuildModel.sixth_case).label('sixth_case')
                    )
                    result = await session.execute(result)
                    result = result.first()
                    result = await self.row_to_dict(result)
                    await client.set_data(f"count_case_{guild_id}", result, expire=300)
                    return result

    async def get_user_coin(self, 
                            guild_id: int, 
                            user_id: int):
        async with PGSClient() as session:
            result = select(ProfileModel.coin).where(
                ProfileModel.guild_id == guild_id,
                ProfileModel.user_id == user_id
            )
            result = await session.execute(result)
            coin = result.first()
            return coin

    async def get_case_coin(self, 
                            guild_id: int, 
                            user_id: int, 
                            count: int, 
                            case_name: str) -> None:
        async with PGSClient() as session:
            async with session.begin():
                update(ProfileModel).where(ProfileModel.guild_id ==  guild_id, ProfileModel.user_id == user_id).values(coin=ProfileModel.coin - count)
                update(GuildModel).where(GuildModel.guild_id == guild_id).values({case_name: getattr(GuildModel, case_name) + 1, 'total_case': GuildModel.total_case + 1})
                await session.commit()

    async def get_case_item(self, 
                            guild_id: int, 
                            user_id: int, 
                            case_name: str, 
                            model: str, 
                            column_name: str) -> None:
        async with PGSClient() as session:
            async with session.begin():
                models = {
                    'ProfileModel': ProfileModel,
                    'CardModel': CardModel,
                    'DecalModel': DecalModel,
                    'OperatorModel': OperatorModel

                }

                subquery = select(ProfileModel.id).filter(
                    ProfileModel.guild_id == guild_id,
                    ProfileModel.user_id == user_id
                ).scalar_subquery()

                await session.execute(
                    update(ProfileModel)
                    .where(ProfileModel.guild_id == guild_id, ProfileModel.user_id == user_id)
                    .values(coin=ProfileModel.coin - 500)
                )

                model_class = models[model]
                await session.execute(
                    update(model_class)
                    .where(model_class.profile_id == subquery)
                    .values({column_name: True})
                )

                await session.execute(
                    update(GuildModel)
                    .where(GuildModel.guild_id == guild_id)
                    .values({case_name: getattr(GuildModel, case_name) + 1, 'total_case': GuildModel.total_case + 1})
                )

                await session.commit()
