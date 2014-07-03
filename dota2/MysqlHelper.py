# -*- coding: utf-8 -*-  
__author__ = 'wangyang'
#  mysqlhelper.m
#  helloword
#
#  Created by 汪 洋 on 14-1-25.
#  Copyright (c) 2014年 helloword. All rights reserved.
#
import pymysql

import sqlalchemy
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import desc
from sqlalchemy.types import CHAR, Integer, String, VARCHAR, TIMESTAMP
from sqlalchemy.dialects.mysql import TINYINT,INTEGER,BIGINT

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, or_, not_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound



import logging
import traceback
from uuid import uuid4
import random
import string
import hashlib
import uuid
import os
try:
  import sae
  isSae = True
except Exception, e:
  isSae = False

##sqlalchemy 基本变量
if isSae:
  global_engine = create_engine('mysql://%s:%s@%s:%d/%s?charset=utf8' % (sae.const.MYSQL_USER,sae.const.MYSQL_PASS,sae.const.MYSQL_HOST,3307,sae.const.MYSQL_DB) , encoding='utf8', pool_recycle=10 )
else:
  global_engine = create_engine('mysql+pymysql://root:asdfghjkl@192.168.1.20/dota2?charset=utf8',echo=False)
BaseModel = declarative_base()
DB_Session = sessionmaker(bind=global_engine)
global_session = DB_Session()

global_user_id_to_baidu_map = {}

class DotaMatchModel(BaseModel):
    __tablename__ = 'dota_match'

    match_id                = Column(BIGINT(20,unsigned=True), primary_key=True)
    
    match_seq_num           = Column(BIGINT(20,unsigned=True))
    
    player0                 = Column(String(512))
    player1                 = Column(String(512))
    player2                 = Column(String(512))
    player3                 = Column(String(512))
    player4                 = Column(String(512))
    player5                 = Column(String(512))
    player6                 = Column(String(512))
    player7                 = Column(String(512))
    player8                 = Column(String(512))
    player9                 = Column(String(512))

    radiant_win             = Column(TINYINT(4,unsigned=True))
    
    duration                = Column(INTEGER(10,unsigned=True))
    start_time              = Column(TIMESTAMP())
    first_blood_time        = Column(INTEGER(10,unsigned=True))
    tower_status_radiant    = Column(INTEGER(10,unsigned=True))
    tower_status_dire       = Column(INTEGER(10,unsigned=True))
    barracks_status_radiant = Column(INTEGER(10,unsigned=True))
    barracks_status_dire    = Column(INTEGER(10,unsigned=True))
    cluster                 = Column(INTEGER(10,unsigned=True))
    lobby_type              = Column(TINYINT(4))
    human_players           = Column(TINYINT(4))
    leagueid                = Column(BIGINT(20,unsigned=True))
    positive_votes          = Column(INTEGER(10,unsigned=True))
    negative_votes          = Column(INTEGER(10,unsigned=True))
    game_mode               = Column(TINYINT(4,unsigned=True))

class MatchHandle():
  def __init__(self):
    """connection for the database"""
    self._session = DB_Session()

  def __del__(self):
    if self._session:
      self._session.close()
  
  def saveMatchToDB(self, match):
    try:
      # Execute the SQL command
      self._session.add(match)
      self._session.commit()
      # Fetch all the rows in a list of lists.
      return 0
    except IntegrityError,e:
      logging.warning("exists")
      self._session.rollback()
      self._session.commit()
      return 0



        
if __name__ == "__main__":
  BaseModel.metadata.create_all(global_engine)
