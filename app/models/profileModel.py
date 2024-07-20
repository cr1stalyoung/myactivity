from sqlalchemy import Column, Integer, BigInteger, DateTime, Boolean, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class ProfileModel(Base):
    __tablename__ = 'profile'

    id = Column(Integer, nullable=False, primary_key=True)
    guild_id = Column(BigInteger, nullable=False)
    user_id = Column(BigInteger, nullable=False)
    last_entry = Column(DateTime(timezone=False), nullable=False)
    experience = Column(Integer, nullable=False)
    coin = Column(Integer, nullable=False)
    level = Column(Integer, nullable=False)
    count_msg = Column(Integer, nullable=False)
    count_voice = Column(Integer, nullable=False)
    voice_month = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False)
    score_month = Column(Integer, nullable=False)
    longest = Column(Integer, nullable=False)
    decal = Column(String, nullable=False)
    card = Column(String, nullable=True)
    operator = Column(String, nullable=False)
    old_score = Column(Integer, nullable=True)
    old_rank = Column(Integer, nullable=True)

    cards = relationship('CardModel', back_populates='profile')
    decals = relationship('DecalModel', back_populates='profile')
    operators = relationship('OperatorModel', back_populates='profile')
    trophies = relationship('TrophyModel', back_populates='profile')


class CardModel(Base):
    __tablename__ = 'card'

    profile_id = Column(Integer, ForeignKey('profile.id'), nullable=False, primary_key=True)
    raid = Column(Boolean, nullable=False)
    cybergirl = Column(Boolean, nullable=False)
    dangerous = Column(Boolean, nullable=False)
    wtf = Column(Boolean, nullable=False)
    leaves = Column(Boolean, nullable=False)
    neonmeet = Column(Boolean, nullable=False)
    lags = Column(Boolean, nullable=False)
    richmedium = Column(Boolean, nullable=False)
    accurate = Column(Boolean, nullable=False)
    zeus = Column(Boolean, nullable=False)
    shot = Column(Boolean, nullable=False)
    season_one_50 = Column(Boolean, nullable=False)
    season_one_1 = Column(Boolean, nullable=False)
    contract = Column(Boolean, nullable=False)
    zombie_nuke = Column(Boolean, nullable=False)
    abomination = Column(Boolean, nullable=False)
    happy_day = Column(Boolean, nullable=False)
    cyborg = Column(Boolean, nullable=False)
    king = Column(Boolean, nullable=False)
    unbreakable = Column(Boolean, nullable=False)
    inhibitor = Column(Boolean, nullable=False)
    hard_work = Column(Boolean, nullable=False)
    ethereal = Column(Boolean, nullable=False)
    zombie_hunt = Column(Boolean, nullable=False)
    crystal_clear = Column(Boolean, nullable=False)
    pure_right = Column(Boolean, nullable=False)
    zombie_mastery = Column(Boolean, nullable=False)
    portal = Column(Boolean, nullable=False)
    cave = Column(Boolean, nullable=False)
    tilt = Column(Boolean, nullable=False)
    cyberpunk = Column(Boolean, nullable=False)
    hot = Column(Boolean, nullable=False)
    angry = Column(Boolean, nullable=False)
    stats = Column(Boolean, nullable=False)
    smoke = Column(Boolean, nullable=False)
    champion = Column(Boolean, nullable=False)
    perks = Column(Boolean, nullable=False)
    hi = Column(Boolean, nullable=False)
    friendship = Column(Boolean, nullable=False)
    cyber_angry = Column(Boolean, nullable=False)
    shadow_lord = Column(Boolean, nullable=False)
    crazy_girl = Column(Boolean, nullable=False)
    dune = Column(Boolean, nullable=False)
    jump = Column(Boolean, nullable=False)
    victory = Column(Boolean, nullable=False)
    friday = Column(Boolean, nullable=False)
    element = Column(Boolean, nullable=False)

    profile = relationship('ProfileModel', back_populates='cards')


class DecalModel(Base):
    __tablename__ = 'decal'

    profile_id = Column(Integer, ForeignKey('profile.id'), nullable=False, primary_key=True)
    default = Column(Boolean, nullable=False)
    rangers = Column(Boolean, nullable=False)
    west = Column(Boolean, nullable=False)
    shadow = Column(Boolean, nullable=False)
    infographic = Column(Boolean, nullable=False)
    classy = Column(Boolean, nullable=False)
    shark = Column(Boolean, nullable=False)
    leaves = Column(Boolean, nullable=False)
    youready = Column(Boolean, nullable=False)
    maskoff = Column(Boolean, nullable=False)
    classified = Column(Boolean, nullable=False)
    cyberstalker = Column(Boolean, nullable=False)
    emperor = Column(Boolean, nullable=False)
    galaxy = Column(Boolean, nullable=False)
    outbroken = Column(Boolean, nullable=False)
    cryptoinvestor = Column(Boolean, nullable=False)
    anime = Column(Boolean, nullable=False)
    anomaly = Column(Boolean, nullable=False)
    experiment = Column(Boolean, nullable=False)
    medusa = Column(Boolean, nullable=False)
    perk = Column(Boolean, nullable=False)
    secret = Column(Boolean, nullable=False)
    verdansk = Column(Boolean, nullable=False)

    profile = relationship('ProfileModel', back_populates='decals')


class OperatorModel(Base):
    __tablename__ = 'operators'

    profile_id = Column(Integer, ForeignKey('profile.id'), nullable=False, primary_key=True)
    default = Column(Boolean, nullable=False)
    ranger = Column(Boolean, nullable=False)
    sheriff = Column(Boolean, nullable=False)
    ghost = Column(Boolean, nullable=False)
    coup = Column(Boolean, nullable=False)
    popmaster = Column(Boolean, nullable=False)
    izzy = Column(Boolean, nullable=False)
    smoky = Column(Boolean, nullable=False)
    cupid = Column(Boolean, nullable=False)
    zeus = Column(Boolean, nullable=False)
    whimsy = Column(Boolean, nullable=False)
    sinister = Column(Boolean, nullable=False)
    imperator = Column(Boolean, nullable=False)
    mind = Column(Boolean, nullable=False)
    outbroken = Column(Boolean, nullable=False)
    king = Column(Boolean, nullable=False)
    toxic = Column(Boolean, nullable=False)
    coral = Column(Boolean, nullable=False)
    jellyfish = Column(Boolean, nullable=False)
    hunter = Column(Boolean, nullable=False)
    rabbit = Column(Boolean, nullable=False)
    snow_queen = Column(Boolean, nullable=False)

    profile = relationship('ProfileModel', back_populates='operators')


class TrophyModel(Base):
    __tablename__ = 'trophy'

    profile_id = Column(Integer, ForeignKey('profile.id'), nullable=False, primary_key=True)
    season_one = Column(Boolean, nullable=False)

    profile = relationship('ProfileModel', back_populates='trophies')