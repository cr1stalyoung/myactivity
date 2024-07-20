from sqlalchemy import select, update, insert, func
from sqlalchemy.orm import aliased
from app.controllers.baseController import PGSClient, RedisClient
from app.models.profileModel import ProfileModel, TrophyModel, DecalModel, OperatorModel, CardModel
from datetime import datetime
from typing import Tuple, Optional


class UpdateProfileMember(PGSClient):

    async def update_per_message(self, 
                                 guild_id:int, 
                                 user_id: int) -> Tuple[Optional[int], Optional[int]]:
        async with PGSClient() as session:
            async with session.begin():
                profile = (
                    update(ProfileModel)
                    .filter(
                        ProfileModel.guild_id == guild_id,
                        ProfileModel.user_id == user_id
                    )
                    .values(
                        experience=ProfileModel.experience + 5,
                        count_msg=ProfileModel.count_msg + 1
                    )
                    .returning(ProfileModel.experience, ProfileModel.level)
                )
                result = await session.execute(profile)
                result = result.first()
                return (None, None) if result is None else (result.experience, result.level)

    async def get_member_data(self, 
                              guild_id: int, 
                              user_id: int) -> Tuple[Optional[int], Optional[int]]:
        async with PGSClient() as session:
            async with session.begin():
                profile = select(ProfileModel.last_entry, ProfileModel.score).filter(ProfileModel.guild_id == guild_id, ProfileModel.user_id == user_id)
                result = await session.execute(profile)
                result = result.first()
                return (None, None) if result is None else (result.last_entry, result.score)

    async def insert_new_profile(self, 
                                 guild_id: int, 
                                 user_id: int) -> None:
        async with PGSClient() as session:
            async with session.begin():
                profile = insert(ProfileModel).values(guild_id=guild_id, user_id=user_id, last_entry=datetime.utcnow())
                await session.execute(profile)

    async def update_level_profile(self, 
                                   guild_id: int, 
                                   user_id: int, 
                                   level: int) -> None:
        async with PGSClient() as session:
            async with session.begin():
                profile = update(ProfileModel).where(ProfileModel.guild_id == guild_id, ProfileModel.user_id == user_id).values(coin=ProfileModel.coin + 50, level=level)
                await session.execute(profile)

    async def update_member_before(self, 
                                   guild_id: int, 
                                   user_id: int, 
                                   last_entry: datetime, 
                                   score: int) -> None:
        async with PGSClient() as session:
            async with session.begin():
                profile = update(ProfileModel).filter(ProfileModel.guild_id == guild_id, ProfileModel.user_id == user_id).values(last_entry=last_entry, score=score)
                await session.execute(profile)

    async def update_member_after(self, 
                                  guild_id: int, 
                                  user_id: int, 
                                  new_value: int, 
                                  score: int) -> Tuple[Optional[int], Optional[int], Optional[int]]:
        async with PGSClient() as session:
            async with session.begin():
                profile = aliased(ProfileModel)
                pos = (select(func.count().label('count') + 1).where((profile.score > ProfileModel.score)).select_from(profile)).label('ranking')

                profile = (
                    update(ProfileModel)
                    .filter(
                        ProfileModel.guild_id == guild_id,
                        ProfileModel.user_id == user_id
                    )
                    .values(
                        experience=ProfileModel.experience + new_value,
                        coin=ProfileModel.coin + new_value,
                        count_voice=ProfileModel.count_voice + new_value,
                        voice_month=ProfileModel.voice_month + new_value,
                        score=ProfileModel.score + score,
                        score_month=ProfileModel.score_month + score,
                        old_score=ProfileModel.score,
                        old_rank=pos
                    )
                    .returning(ProfileModel.experience, ProfileModel.level, ProfileModel.longest)
                )
                result = await session.execute(profile)
                result = result.first()
                return (None, None, None) if result is None else (result.experience, result.level, result.longest)

    async def update_member_time(self, 
                                 guild_id: int,
                                 user_id: int,
                                 last_entry: datetime) -> None:
        async with PGSClient() as session:
            async with session.begin():
                profile = update(ProfileModel).filter(ProfileModel.guild_id == guild_id, ProfileModel.user_id == user_id).values(last_entry=last_entry)
                await session.execute(profile)

    async def update_member_longest(self, 
                                    guild_id: int, 
                                    user_id: int, 
                                    longest: int) -> None:
        async with PGSClient() as session:
            async with session.begin():
                profile = update(ProfileModel).filter(ProfileModel.guild_id == guild_id, ProfileModel.user_id == user_id).values(longest=longest)
                await session.execute(profile)


class ProfileGetData(PGSClient, RedisClient):

    async def get_profile(self, 
                          guild_id: int, 
                          user_id: int):
        async with RedisClient() as client:
            cache = await client.get_data(f"me_{guild_id}_{user_id}")
            if cache:
                return cache

            async with PGSClient() as session:
                async with session.begin():
                    profile_alias = aliased(ProfileModel)

                    pos_server_subquery = (
                        select(func.count(profile_alias.id) + 1)
                        .filter(profile_alias.score > ProfileModel.score)
                        .filter(profile_alias.guild_id == ProfileModel.guild_id)
                        .correlate(ProfileModel)
                        .scalar_subquery()
                    )

                    pos_world_subquery = (
                        select(func.count(profile_alias.id) + 1)
                        .filter(profile_alias.score > (
                            select(ProfileModel.score)
                            .filter(ProfileModel.guild_id == guild_id, ProfileModel.user_id == user_id)
                            .scalar_subquery()
                        ))
                        .scalar_subquery()
                    )

                    query = (
                        select(
                            ProfileModel.experience,
                            ProfileModel.level,
                            ProfileModel.count_msg,
                            ProfileModel.count_voice,
                            ProfileModel.voice_month,
                            ProfileModel.score,
                            ProfileModel.score_month,
                            ProfileModel.longest,
                            ProfileModel.decal,
                            ProfileModel.card,
                            ProfileModel.operator,
                            TrophyModel.season_one,
                            pos_server_subquery.label('pos_server'),
                            pos_world_subquery.label('pos_world')
                        )
                        .join(TrophyModel, TrophyModel.profile_id == ProfileModel.id)
                        .filter(
                            ProfileModel.guild_id == guild_id,
                            ProfileModel.user_id == user_id
                        )
                    )

                    result = await session.execute(query)
                    result = result.fetchone()
                    if result is not None:
                        result = await self.row_to_dict(result)
                        await client.set_data(f"me_{guild_id}_{user_id}", result, expire=120)
                        return result
                    else:
                        return None

    async def get_decals(self, 
                         guild_id: int, 
                         user_id: int):
        async with PGSClient() as session:
            async with session.begin():
                decal = select(DecalModel).join(ProfileModel).filter(
                    ProfileModel.guild_id == guild_id,
                    ProfileModel.user_id == user_id
                )
                result = await session.execute(decal)
                decal = result.scalars().first()
                if decal:
                    decals = [
                        (column.name, getattr(decal, column.name))
                        for column in DecalModel.__table__.columns
                    ]
                    return decals

    async def get_operators(self, 
                            guild_id: int, 
                            user_id: int):
        async with PGSClient() as session:
            async with session.begin():
                operators = select(OperatorModel).join(ProfileModel).filter(
                    ProfileModel.guild_id == guild_id,
                    ProfileModel.user_id == user_id
                )
                result = await session.execute(operators)
                operators = result.scalars().first()
                if operators:
                    decals = [
                        (column.name, getattr(operators, column.name))
                        for column in OperatorModel.__table__.columns
                    ]
                    return decals

    async def get_cards(self, 
                        guild_id: int, 
                        user_id: int):
        async with PGSClient() as session:
            async with session.begin():
                card = select(CardModel).join(ProfileModel).filter(
                    ProfileModel.guild_id == guild_id,
                    ProfileModel.user_id == user_id
                )
                result = await session.execute(card)
                card = result.scalars().first()
                if card:
                    decals = [
                        (column.name, getattr(card, column.name))
                        for column in CardModel.__table__.columns
                    ]
                    return decals

    async def update_general(self, 
                             guild_id: int, 
                             user_id: int, 
                             column_name: str, 
                             value: str) -> None:
        async with PGSClient() as session:
            async with session.begin():
                profile = update(ProfileModel).filter(ProfileModel.guild_id == guild_id, ProfileModel.user_id == user_id).values({column_name: value})
                await session.execute(profile)

            async with RedisClient() as client:
                me = await client.get_data(f"me_{guild_id}_{user_id}")
                if me:
                    me[column_name] = value
                    await client.set_data(f"me_{guild_id}_{user_id}", me, expire=120)
                    me = await client.get_data(f"me_{guild_id}_{user_id}")

