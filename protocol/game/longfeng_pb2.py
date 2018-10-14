# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: game/longfeng.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from base import game_base_pb2 as base_dot_game__base__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='game/longfeng.proto',
  package='',
  syntax='proto3',
  serialized_pb=_b('\n\x13game/longfeng.proto\x1a\x14\x62\x61se/game_base.proto\"R\n\x18\x42\x61iRenLongFengCreateRoom\x12\x11\n\tbaseScore\x18\x01 \x01(\x05\x12\x0f\n\x07inScore\x18\x02 \x01(\x05\x12\x12\n\nleaveScore\x18\x03 \x01(\x05\"\"\n\x12\x42\x61iRenLongFengDice\x12\x0c\n\x04\x64ice\x18\x01 \x03(\x05\"-\n\x1c\x42\x61iRenLongFengDealCardAction\x12\r\n\x05\x63\x61rds\x18\x01 \x03(\x05\"2\n\x14\x42\x61iRenLongFengRecAsk\x12\x0c\n\x04time\x18\x01 \x01(\x05\x12\x0c\n\x04type\x18\x02 \x01(\x05\"H\n\x16\x42\x61iRenLongFengBetScore\x12\r\n\x05score\x18\x01 \x01(\x05\x12\r\n\x05index\x18\x02 \x01(\x05\x12\x10\n\x08playerId\x18\x03 \x01(\x05\"I\n\x1c\x42\x61iRenLongFengBetScoreAction\x12)\n\x08\x62\x65tScore\x18\x01 \x03(\x0b\x32\x17.BaiRenLongFengBetScore\"b\n\x17\x42\x61iRenLongFengPositions\x12*\n\tpositions\x18\x01 \x03(\x0b\x32\x17.BaiRenLongFengBetScore\x12\x1b\n\x13shensuanziPositions\x18\x02 \x01(\x05\"\xad\x01\n BaiRenLongFengPlayerOneSetResult\x12\x30\n\x07players\x18\x01 \x03(\x0b\x32\x1f.BaiRenLongFengSettlePlayerInfo\x12/\n\tdayingjia\x18\x02 \x01(\x0b\x32\x1c.RecUpdateGameUsers.UserInfo\x12\x11\n\tbankerWin\x18\x03 \x01(\x05\x12\x13\n\x0bpositionWin\x18\x04 \x03(\x05\"U\n\x1e\x42\x61iRenLongFengSettlePlayerInfo\x12\x10\n\x08playerId\x18\x01 \x01(\x05\x12\r\n\x05score\x18\x02 \x01(\x05\x12\x12\n\ntotalScore\x18\x03 \x01(\x05\"$\n\x13\x42\x61iRenLongFengScore\x12\r\n\x05score\x18\x01 \x03(\x05\",\n\x17\x42\x61iRenLongFengWatchSize\x12\x11\n\twatchSize\x18\x01 \x01(\x05\"i\n\x13\x42\x61iRenLongFengTrend\x12/\n\x06trends\x18\x01 \x03(\x0b\x32\x1f.BaiRenLongFengTrend.SigleTrend\x1a!\n\nSigleTrend\x12\x13\n\x0bpositionWin\x18\x01 \x03(\x05\"W\n\rBankerConfirm\x12,\n\x06\x62\x61nker\x18\x01 \x01(\x0b\x32\x1c.RecUpdateGameUsers.UserInfo\x12\x18\n\x10shangzhuangScore\x18\x02 \x01(\x05\"5\n\x0fShangZhuangList\x12\"\n\nbankerList\x18\x01 \x03(\x0b\x32\x0e.BankerConfirmB3\n\x11zhipai.mode.protoH\x03P\x01\xaa\x02\x19\x43huangMi.GuiYangNiuNiu.V1b\x06proto3')
  ,
  dependencies=[base_dot_game__base__pb2.DESCRIPTOR,])




_BAIRENLONGFENGCREATEROOM = _descriptor.Descriptor(
  name='BaiRenLongFengCreateRoom',
  full_name='BaiRenLongFengCreateRoom',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='baseScore', full_name='BaiRenLongFengCreateRoom.baseScore', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='inScore', full_name='BaiRenLongFengCreateRoom.inScore', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='leaveScore', full_name='BaiRenLongFengCreateRoom.leaveScore', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=45,
  serialized_end=127,
)


_BAIRENLONGFENGDICE = _descriptor.Descriptor(
  name='BaiRenLongFengDice',
  full_name='BaiRenLongFengDice',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='dice', full_name='BaiRenLongFengDice.dice', index=0,
      number=1, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=129,
  serialized_end=163,
)


_BAIRENLONGFENGDEALCARDACTION = _descriptor.Descriptor(
  name='BaiRenLongFengDealCardAction',
  full_name='BaiRenLongFengDealCardAction',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='cards', full_name='BaiRenLongFengDealCardAction.cards', index=0,
      number=1, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=165,
  serialized_end=210,
)


_BAIRENLONGFENGRECASK = _descriptor.Descriptor(
  name='BaiRenLongFengRecAsk',
  full_name='BaiRenLongFengRecAsk',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='time', full_name='BaiRenLongFengRecAsk.time', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type', full_name='BaiRenLongFengRecAsk.type', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=212,
  serialized_end=262,
)


_BAIRENLONGFENGBETSCORE = _descriptor.Descriptor(
  name='BaiRenLongFengBetScore',
  full_name='BaiRenLongFengBetScore',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='score', full_name='BaiRenLongFengBetScore.score', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='index', full_name='BaiRenLongFengBetScore.index', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='playerId', full_name='BaiRenLongFengBetScore.playerId', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=264,
  serialized_end=336,
)


_BAIRENLONGFENGBETSCOREACTION = _descriptor.Descriptor(
  name='BaiRenLongFengBetScoreAction',
  full_name='BaiRenLongFengBetScoreAction',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='betScore', full_name='BaiRenLongFengBetScoreAction.betScore', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=338,
  serialized_end=411,
)


_BAIRENLONGFENGPOSITIONS = _descriptor.Descriptor(
  name='BaiRenLongFengPositions',
  full_name='BaiRenLongFengPositions',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='positions', full_name='BaiRenLongFengPositions.positions', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='shensuanziPositions', full_name='BaiRenLongFengPositions.shensuanziPositions', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=413,
  serialized_end=511,
)


_BAIRENLONGFENGPLAYERONESETRESULT = _descriptor.Descriptor(
  name='BaiRenLongFengPlayerOneSetResult',
  full_name='BaiRenLongFengPlayerOneSetResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='players', full_name='BaiRenLongFengPlayerOneSetResult.players', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='dayingjia', full_name='BaiRenLongFengPlayerOneSetResult.dayingjia', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='bankerWin', full_name='BaiRenLongFengPlayerOneSetResult.bankerWin', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='positionWin', full_name='BaiRenLongFengPlayerOneSetResult.positionWin', index=3,
      number=4, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=514,
  serialized_end=687,
)


_BAIRENLONGFENGSETTLEPLAYERINFO = _descriptor.Descriptor(
  name='BaiRenLongFengSettlePlayerInfo',
  full_name='BaiRenLongFengSettlePlayerInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='playerId', full_name='BaiRenLongFengSettlePlayerInfo.playerId', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='score', full_name='BaiRenLongFengSettlePlayerInfo.score', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='totalScore', full_name='BaiRenLongFengSettlePlayerInfo.totalScore', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=689,
  serialized_end=774,
)


_BAIRENLONGFENGSCORE = _descriptor.Descriptor(
  name='BaiRenLongFengScore',
  full_name='BaiRenLongFengScore',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='score', full_name='BaiRenLongFengScore.score', index=0,
      number=1, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=776,
  serialized_end=812,
)


_BAIRENLONGFENGWATCHSIZE = _descriptor.Descriptor(
  name='BaiRenLongFengWatchSize',
  full_name='BaiRenLongFengWatchSize',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='watchSize', full_name='BaiRenLongFengWatchSize.watchSize', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=814,
  serialized_end=858,
)


_BAIRENLONGFENGTREND_SIGLETREND = _descriptor.Descriptor(
  name='SigleTrend',
  full_name='BaiRenLongFengTrend.SigleTrend',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='positionWin', full_name='BaiRenLongFengTrend.SigleTrend.positionWin', index=0,
      number=1, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=932,
  serialized_end=965,
)

_BAIRENLONGFENGTREND = _descriptor.Descriptor(
  name='BaiRenLongFengTrend',
  full_name='BaiRenLongFengTrend',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='trends', full_name='BaiRenLongFengTrend.trends', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_BAIRENLONGFENGTREND_SIGLETREND, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=860,
  serialized_end=965,
)


_BANKERCONFIRM = _descriptor.Descriptor(
  name='BankerConfirm',
  full_name='BankerConfirm',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='banker', full_name='BankerConfirm.banker', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='shangzhuangScore', full_name='BankerConfirm.shangzhuangScore', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=967,
  serialized_end=1054,
)


_SHANGZHUANGLIST = _descriptor.Descriptor(
  name='ShangZhuangList',
  full_name='ShangZhuangList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='bankerList', full_name='ShangZhuangList.bankerList', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1056,
  serialized_end=1109,
)

_BAIRENLONGFENGBETSCOREACTION.fields_by_name['betScore'].message_type = _BAIRENLONGFENGBETSCORE
_BAIRENLONGFENGPOSITIONS.fields_by_name['positions'].message_type = _BAIRENLONGFENGBETSCORE
_BAIRENLONGFENGPLAYERONESETRESULT.fields_by_name['players'].message_type = _BAIRENLONGFENGSETTLEPLAYERINFO
_BAIRENLONGFENGPLAYERONESETRESULT.fields_by_name['dayingjia'].message_type = base_dot_game__base__pb2._RECUPDATEGAMEUSERS_USERINFO
_BAIRENLONGFENGTREND_SIGLETREND.containing_type = _BAIRENLONGFENGTREND
_BAIRENLONGFENGTREND.fields_by_name['trends'].message_type = _BAIRENLONGFENGTREND_SIGLETREND
_BANKERCONFIRM.fields_by_name['banker'].message_type = base_dot_game__base__pb2._RECUPDATEGAMEUSERS_USERINFO
_SHANGZHUANGLIST.fields_by_name['bankerList'].message_type = _BANKERCONFIRM
DESCRIPTOR.message_types_by_name['BaiRenLongFengCreateRoom'] = _BAIRENLONGFENGCREATEROOM
DESCRIPTOR.message_types_by_name['BaiRenLongFengDice'] = _BAIRENLONGFENGDICE
DESCRIPTOR.message_types_by_name['BaiRenLongFengDealCardAction'] = _BAIRENLONGFENGDEALCARDACTION
DESCRIPTOR.message_types_by_name['BaiRenLongFengRecAsk'] = _BAIRENLONGFENGRECASK
DESCRIPTOR.message_types_by_name['BaiRenLongFengBetScore'] = _BAIRENLONGFENGBETSCORE
DESCRIPTOR.message_types_by_name['BaiRenLongFengBetScoreAction'] = _BAIRENLONGFENGBETSCOREACTION
DESCRIPTOR.message_types_by_name['BaiRenLongFengPositions'] = _BAIRENLONGFENGPOSITIONS
DESCRIPTOR.message_types_by_name['BaiRenLongFengPlayerOneSetResult'] = _BAIRENLONGFENGPLAYERONESETRESULT
DESCRIPTOR.message_types_by_name['BaiRenLongFengSettlePlayerInfo'] = _BAIRENLONGFENGSETTLEPLAYERINFO
DESCRIPTOR.message_types_by_name['BaiRenLongFengScore'] = _BAIRENLONGFENGSCORE
DESCRIPTOR.message_types_by_name['BaiRenLongFengWatchSize'] = _BAIRENLONGFENGWATCHSIZE
DESCRIPTOR.message_types_by_name['BaiRenLongFengTrend'] = _BAIRENLONGFENGTREND
DESCRIPTOR.message_types_by_name['BankerConfirm'] = _BANKERCONFIRM
DESCRIPTOR.message_types_by_name['ShangZhuangList'] = _SHANGZHUANGLIST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

BaiRenLongFengCreateRoom = _reflection.GeneratedProtocolMessageType('BaiRenLongFengCreateRoom', (_message.Message,), dict(
  DESCRIPTOR = _BAIRENLONGFENGCREATEROOM,
  __module__ = 'game.longfeng_pb2'
  # @@protoc_insertion_point(class_scope:BaiRenLongFengCreateRoom)
  ))
_sym_db.RegisterMessage(BaiRenLongFengCreateRoom)

BaiRenLongFengDice = _reflection.GeneratedProtocolMessageType('BaiRenLongFengDice', (_message.Message,), dict(
  DESCRIPTOR = _BAIRENLONGFENGDICE,
  __module__ = 'game.longfeng_pb2'
  # @@protoc_insertion_point(class_scope:BaiRenLongFengDice)
  ))
_sym_db.RegisterMessage(BaiRenLongFengDice)

BaiRenLongFengDealCardAction = _reflection.GeneratedProtocolMessageType('BaiRenLongFengDealCardAction', (_message.Message,), dict(
  DESCRIPTOR = _BAIRENLONGFENGDEALCARDACTION,
  __module__ = 'game.longfeng_pb2'
  # @@protoc_insertion_point(class_scope:BaiRenLongFengDealCardAction)
  ))
_sym_db.RegisterMessage(BaiRenLongFengDealCardAction)

BaiRenLongFengRecAsk = _reflection.GeneratedProtocolMessageType('BaiRenLongFengRecAsk', (_message.Message,), dict(
  DESCRIPTOR = _BAIRENLONGFENGRECASK,
  __module__ = 'game.longfeng_pb2'
  # @@protoc_insertion_point(class_scope:BaiRenLongFengRecAsk)
  ))
_sym_db.RegisterMessage(BaiRenLongFengRecAsk)

BaiRenLongFengBetScore = _reflection.GeneratedProtocolMessageType('BaiRenLongFengBetScore', (_message.Message,), dict(
  DESCRIPTOR = _BAIRENLONGFENGBETSCORE,
  __module__ = 'game.longfeng_pb2'
  # @@protoc_insertion_point(class_scope:BaiRenLongFengBetScore)
  ))
_sym_db.RegisterMessage(BaiRenLongFengBetScore)

BaiRenLongFengBetScoreAction = _reflection.GeneratedProtocolMessageType('BaiRenLongFengBetScoreAction', (_message.Message,), dict(
  DESCRIPTOR = _BAIRENLONGFENGBETSCOREACTION,
  __module__ = 'game.longfeng_pb2'
  # @@protoc_insertion_point(class_scope:BaiRenLongFengBetScoreAction)
  ))
_sym_db.RegisterMessage(BaiRenLongFengBetScoreAction)

BaiRenLongFengPositions = _reflection.GeneratedProtocolMessageType('BaiRenLongFengPositions', (_message.Message,), dict(
  DESCRIPTOR = _BAIRENLONGFENGPOSITIONS,
  __module__ = 'game.longfeng_pb2'
  # @@protoc_insertion_point(class_scope:BaiRenLongFengPositions)
  ))
_sym_db.RegisterMessage(BaiRenLongFengPositions)

BaiRenLongFengPlayerOneSetResult = _reflection.GeneratedProtocolMessageType('BaiRenLongFengPlayerOneSetResult', (_message.Message,), dict(
  DESCRIPTOR = _BAIRENLONGFENGPLAYERONESETRESULT,
  __module__ = 'game.longfeng_pb2'
  # @@protoc_insertion_point(class_scope:BaiRenLongFengPlayerOneSetResult)
  ))
_sym_db.RegisterMessage(BaiRenLongFengPlayerOneSetResult)

BaiRenLongFengSettlePlayerInfo = _reflection.GeneratedProtocolMessageType('BaiRenLongFengSettlePlayerInfo', (_message.Message,), dict(
  DESCRIPTOR = _BAIRENLONGFENGSETTLEPLAYERINFO,
  __module__ = 'game.longfeng_pb2'
  # @@protoc_insertion_point(class_scope:BaiRenLongFengSettlePlayerInfo)
  ))
_sym_db.RegisterMessage(BaiRenLongFengSettlePlayerInfo)

BaiRenLongFengScore = _reflection.GeneratedProtocolMessageType('BaiRenLongFengScore', (_message.Message,), dict(
  DESCRIPTOR = _BAIRENLONGFENGSCORE,
  __module__ = 'game.longfeng_pb2'
  # @@protoc_insertion_point(class_scope:BaiRenLongFengScore)
  ))
_sym_db.RegisterMessage(BaiRenLongFengScore)

BaiRenLongFengWatchSize = _reflection.GeneratedProtocolMessageType('BaiRenLongFengWatchSize', (_message.Message,), dict(
  DESCRIPTOR = _BAIRENLONGFENGWATCHSIZE,
  __module__ = 'game.longfeng_pb2'
  # @@protoc_insertion_point(class_scope:BaiRenLongFengWatchSize)
  ))
_sym_db.RegisterMessage(BaiRenLongFengWatchSize)

BaiRenLongFengTrend = _reflection.GeneratedProtocolMessageType('BaiRenLongFengTrend', (_message.Message,), dict(

  SigleTrend = _reflection.GeneratedProtocolMessageType('SigleTrend', (_message.Message,), dict(
    DESCRIPTOR = _BAIRENLONGFENGTREND_SIGLETREND,
    __module__ = 'game.longfeng_pb2'
    # @@protoc_insertion_point(class_scope:BaiRenLongFengTrend.SigleTrend)
    ))
  ,
  DESCRIPTOR = _BAIRENLONGFENGTREND,
  __module__ = 'game.longfeng_pb2'
  # @@protoc_insertion_point(class_scope:BaiRenLongFengTrend)
  ))
_sym_db.RegisterMessage(BaiRenLongFengTrend)
_sym_db.RegisterMessage(BaiRenLongFengTrend.SigleTrend)

BankerConfirm = _reflection.GeneratedProtocolMessageType('BankerConfirm', (_message.Message,), dict(
  DESCRIPTOR = _BANKERCONFIRM,
  __module__ = 'game.longfeng_pb2'
  # @@protoc_insertion_point(class_scope:BankerConfirm)
  ))
_sym_db.RegisterMessage(BankerConfirm)

ShangZhuangList = _reflection.GeneratedProtocolMessageType('ShangZhuangList', (_message.Message,), dict(
  DESCRIPTOR = _SHANGZHUANGLIST,
  __module__ = 'game.longfeng_pb2'
  # @@protoc_insertion_point(class_scope:ShangZhuangList)
  ))
_sym_db.RegisterMessage(ShangZhuangList)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\021zhipai.mode.protoH\003P\001\252\002\031ChuangMi.GuiYangNiuNiu.V1'))
# @@protoc_insertion_point(module_scope)
