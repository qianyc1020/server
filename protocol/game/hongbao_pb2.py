# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: game/hongbao.proto

import sys

_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()

from protocol.base import game_base_pb2 as base_dot_game__base__pb2

DESCRIPTOR = _descriptor.FileDescriptor(
    name='game/hongbao.proto',
    package='',
    syntax='proto3',
    serialized_pb=_b(
        '\n\x12game/hongbao.proto\x1a\x14\x62\x61se/game_base.proto\"#\n\x12\x42\x61iRenHongbaoScore\x12\r\n\x05score\x18\x01 \x01(\x05\"O\n\x12\x42\x61iRenHongbaoQiang\x12\r\n\x05score\x18\x01 \x01(\x05\x12*\n\x04user\x18\x02 \x01(\x0b\x32\x1c.RecUpdateGameUsers.UserInfoB\x02H\x03\x62\x06proto3')
    ,
    dependencies=[base_dot_game__base__pb2.DESCRIPTOR, ])

_BAIRENHONGBAOSCORE = _descriptor.Descriptor(
    name='BaiRenHongbaoScore',
    full_name='BaiRenHongbaoScore',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='score', full_name='BaiRenHongbaoScore.score', index=0,
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
    serialized_start=44,
    serialized_end=79,
)

_BAIRENHONGBAOQIANG = _descriptor.Descriptor(
    name='BaiRenHongbaoQiang',
    full_name='BaiRenHongbaoQiang',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='score', full_name='BaiRenHongbaoQiang.score', index=0,
            number=1, type=5, cpp_type=1, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None, file=DESCRIPTOR),
        _descriptor.FieldDescriptor(
            name='user', full_name='BaiRenHongbaoQiang.user', index=1,
            number=2, type=11, cpp_type=10, label=1,
            has_default_value=False, default_value=None,
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
    serialized_start=81,
    serialized_end=160,
)

_BAIRENHONGBAOQIANG.fields_by_name['user'].message_type = base_dot_game__base__pb2._RECUPDATEGAMEUSERS_USERINFO
DESCRIPTOR.message_types_by_name['BaiRenHongbaoScore'] = _BAIRENHONGBAOSCORE
DESCRIPTOR.message_types_by_name['BaiRenHongbaoQiang'] = _BAIRENHONGBAOQIANG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

BaiRenHongbaoScore = _reflection.GeneratedProtocolMessageType('BaiRenHongbaoScore', (_message.Message,), dict(
    DESCRIPTOR=_BAIRENHONGBAOSCORE,
    __module__='game.hongbao_pb2'
    # @@protoc_insertion_point(class_scope:BaiRenHongbaoScore)
))
_sym_db.RegisterMessage(BaiRenHongbaoScore)

BaiRenHongbaoQiang = _reflection.GeneratedProtocolMessageType('BaiRenHongbaoQiang', (_message.Message,), dict(
    DESCRIPTOR=_BAIRENHONGBAOQIANG,
    __module__='game.hongbao_pb2'
    # @@protoc_insertion_point(class_scope:BaiRenHongbaoQiang)
))
_sym_db.RegisterMessage(BaiRenHongbaoQiang)

DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('H\003'))
# @@protoc_insertion_point(module_scope)
