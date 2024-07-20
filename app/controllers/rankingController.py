import disnake
from sqlalchemy import select, func
from sqlalchemy.orm import aliased
from app.controllers.baseController import PGSClient, RedisClient
from app.models.profileModel import ProfileModel
from sqlalchemy.sql import union_all


class RankingProcessing(PGSClient, RedisClient):

    @staticmethod
    async def get_top50():
        async with RedisClient() as client:
            cache = await client.get_data("global_top")
            return cache

    async def update_global_top(self, 
                                bot):
        async with RedisClient() as client:
            async with PGSClient() as session:
                async with session.begin():
                    data = []
                    subquery_top_50 = select(
                        ProfileModel.user_id,
                        ProfileModel.score,
                        ProfileModel.card,
                        ProfileModel.old_score,
                        ProfileModel.old_rank,
                        func.row_number().over(order_by=ProfileModel.score.desc())
                        .label('ranking')).order_by(ProfileModel.score.desc()).limit(50)
                    result = await session.execute(subquery_top_50)

                    for row in result.fetchall():
                        try:
                            member = await bot.fetch_user(row[0])
                            member_name = member.display_name
                            member_avatar_url = member.avatar.url if member.avatar else "https://img.icons8.com/external-justicon-flat-justicon/1x/external-discord-social-media-justicon-flat-justicon.png"
                        except disnake.errors.NotFound:
                            member_name = "Unknown user"
                            member_avatar_url = "https://img.icons8.com/external-justicon-flat-justicon/1x/external-discord-social-media-justicon-flat-justicon.png"
                        row_dict = await client.row_to_dict(row)
                        row_dict['url'] = member_avatar_url
                        row_dict['name'] = member_name
                        data.append(row_dict)
                    await client.set_data('global_top', data)

    async def get_leaders(self, 
                          guild_id: int, 
                          user_id: int, 
                          column_name: str):
        async with RedisClient() as client:
            cache = await client.get_data(f"{column_name}_{guild_id}_{user_id}")
            if cache:
                return cache

            async with PGSClient() as session:
                async with session.begin():
                    profile = aliased(ProfileModel)
                    user_subquery = (
                        select(
                            ProfileModel.user_id,
                            ProfileModel.level,
                            ProfileModel.count_msg,
                            ProfileModel.count_voice,
                            ProfileModel.voice_month,
                            ProfileModel.score,
                            (select(func.count().label('count') + 1)
                             .where((profile.score > ProfileModel.score) & (profile.guild_id == guild_id))
                             .select_from(profile)).label('ranking')
                        )
                        .where((ProfileModel.guild_id == guild_id) & (ProfileModel.user_id == user_id))
                    )
                    members_subquery = (
                        select(
                            ProfileModel.user_id,
                            ProfileModel.level,
                            ProfileModel.count_msg,
                            ProfileModel.count_voice,
                            ProfileModel.voice_month,
                            ProfileModel.score,
                            func.row_number().over(order_by=ProfileModel.score.desc()).label('ranking')
                        )
                        .where(ProfileModel.guild_id == guild_id)
                        .order_by(getattr(ProfileModel, column_name).desc())
                        .limit(50)
                    )
                    query = union_all(user_subquery, members_subquery)
                    result = await session.execute(query)
                    result = [await self.row_to_dict(row) for row in result.fetchall()]
                    await client.set_data(f"{column_name}_{guild_id}_{user_id}", result, expire=120)
                    return result

    async def get_user_top50(self, 
                             guild_id: int, 
                             user_id: int):
        async with RedisClient() as client:
            cache = await client.get_data(f"user_top_{guild_id}_{user_id}")
            if cache:
                return cache

            async with PGSClient() as session:
                async with session.begin():
                    profile = aliased(ProfileModel)
                    user_subquery = (
                        select(
                            ProfileModel.score,
                            ProfileModel.card,
                            ProfileModel.old_score,
                            ProfileModel.old_rank,
                            (select(func.count().label('count') + 1)
                             .where((profile.score > ProfileModel.score))
                             .select_from(profile)).label('ranking')
                        )
                        .where((ProfileModel.guild_id == guild_id) & (ProfileModel.user_id == user_id))
                    )
                    result = await session.execute(user_subquery)
                    result = [await client.row_to_dict(row) for row in result.fetchall()]
                    await client.set_data(f"user_top_{guild_id}_{user_id}", result, expire=120)
                    return result

