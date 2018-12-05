# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: base/server_to_game.proto

import sys

_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()

DESCRIPTOR = _descriptor.FileDescriptor(
    name='base/server_to_game.proto',
    package='',
    syntax='proto3',
    serialized_pb=_b(
        '\n\x19\x62\x61se/server_to_game.proto\"C\n\x0fReqRegisterGame\x12\x10\n\x08\x61lloc_id\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x10\n\x08password\x18\x03 \x01(\t\" \n\x0fResRegisterGame\x12\r\n\x05state\x18\x01 \x01(\x08\".\n\x0fReqServiceState\x12\x1b\n\x05state\x18\x01 \x01(\x0e\x32\x0c.ServerState\"D\n\x0fReqChangeOnline\x12\x11\n\tplayer_id\x18\x01 \x01(\x05\x12\r\n\x05state\x18\x02 \x01(\x08\x12\x0f\n\x07game_id\x18\x03 \x01(\x05\"\x1e\n\x0b\x44ismissGame\x12\x0f\n\x07game_id\x18\x01 \x01(\x05\";\n\x08UserExit\x12\x10\n\x08playerId\x18\x01 \x01(\x05\x12\x0e\n\x06roomNo\x18\x02 \x01(\x05\x12\r\n\x05level\x18\x03 \x01(\x05*5\n\x0bServerState\x12\x0b\n\x07RUNNING\x10\x00\x12\x0c\n\x08\x42LOCKING\x10\x01\x12\x0b\n\x07\x45XITING\x10\x02\x42\x02H\x03\x62\x06proto3')
)

_SERVERSTATE = _descriptor.EnumDescriptor(
    name='ServerState',
    full_name='ServerState',
    filename=None,
    file=DESCRIPTOR,
    values=[
        _descriptor.EnumValueDescriptor(
            name='RUNNING', index=0, number=0,
            options=None,
            type=None),
        _descriptor.EnumValueDescriptor(
            name='BLOCKING', index=1, number=1,
            options=None,
            type=None),
        _descriptor.EnumValueDescriptor(
            name='EXITING', index=2, number=2,
            options=None,
            type=None),
    ],
    containing_type=None,
    options=None,
    serialized_start=343,
    serialized_end=396,
)
_sym_db.RegisterEnumDescriptor(_SERVERSTATE)

ServerState = enum_type_wrapper.EnumTypeWrapper(_SERVERSTATE)
RUNNING = 0
BLOCKING = 1
EXITING = 2

_REQREGISTERGAME = _descriptor.Descriptor(
    name='ReqRegisterGame',
    full_name='ReqRegisterGame',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='alloc_id', full_name='ReqRegisterGame.alloc_id', index=0,
            number=1, type=5, cpp_type=1, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None, file=DESCRIPTOR),
        _descriptor.FieldDescriptor(
            name='name', full_name='ReqRegisterGame.name', index=1,
            number=2, type=9, cpp_type=9, label=1,
            has_default_value=False, default_value=_b("").decode('utf-8'),
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None, file=DESCRIPTOR),
        _descriptor.FieldDescriptor(
            name='password', full_name='ReqRegisterGame.password', index=2,
            number=3, type=9, cpp_type=9, label=1,
            has_default_value=False, default_value=_b("").decode('utf-8'),
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
    serialized_start=29,
    serialized_end=96,
)

_RESREGISTERGAME = _descriptor.Descriptor(
    name='ResRegisterGame',
    full_name='ResRegisterGame',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='state', full_name='ResRegisterGame.state', index=0,
            number=1, type=8, cpp_type=7, label=1,
            has_default_value=False, default_value=False,
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
    serialized_start=98,
    serialized_end=130,
)

_REQSERVICESTATE = _descriptor.Descriptor(
    name='ReqServiceState',
    full_name='ReqServiceState',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='state', full_name='ReqServiceState.state', index=0,
            number=1, type=14, cpp_type=8, label=1,
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
    serialized_start=132,
    serialized_end=178,
)

_REQCHANGEONLINE = _descriptor.Descriptor(
    name='ReqChangeOnline',
    full_name='ReqChangeOnline',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='player_id', full_name='ReqChangeOnline.player_id', index=0,
            number=1, type=5, cpp_type=1, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None, file=DESCRIPTOR),
        _descriptor.FieldDescriptor(
            name='state', full_name='ReqChangeOnline.state', index=1,
            number=2, type=8, cpp_type=7, label=1,
            has_default_value=False, default_value=False,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None, file=DESCRIPTOR),
        _descriptor.FieldDescriptor(
            name='game_id', full_name='ReqChangeOnline.game_id', index=2,
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
    serialized_start=180,
    serialized_end=248,
)

_DISMISSGAME = _descriptor.Descriptor(
    name='DismissGame',
    full_name='DismissGame',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='game_id', full_name='DismissGame.game_id', index=0,
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
    serialized_start=250,
    serialized_end=280,
)

_USEREXIT = _descriptor.Descriptor(
    name='UserExit',
    full_name='UserExit',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='playerId', full_name='UserExit.playerId', index=0,
            number=1, type=5, cpp_type=1, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None, file=DESCRIPTOR),
        _descriptor.FieldDescriptor(
            name='roomNo', full_name='UserExit.roomNo', index=1,
            number=2, type=5, cpp_type=1, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None, file=DESCRIPTOR),
        _descriptor.FieldDescriptor(
            name='level', full_name='UserExit.level', index=2,
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
    serialized_start=282,
    serialized_end=341,
)

_REQSERVICESTATE.fields_by_name['state'].enum_type = _SERVERSTATE
DESCRIPTOR.message_types_by_name['ReqRegisterGame'] = _REQREGISTERGAME
DESCRIPTOR.message_types_by_name['ResRegisterGame'] = _RESREGISTERGAME
DESCRIPTOR.message_types_by_name['ReqServiceState'] = _REQSERVICESTATE
DESCRIPTOR.message_types_by_name['ReqChangeOnline'] = _REQCHANGEONLINE
DESCRIPTOR.message_types_by_name['DismissGame'] = _DISMISSGAME
DESCRIPTOR.message_types_by_name['UserExit'] = _USEREXIT
DESCRIPTOR.enum_types_by_name['ServerState'] = _SERVERSTATE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ReqRegisterGame = _reflection.GeneratedProtocolMessageType('ReqRegisterGame', (_message.Message,), dict(
    DESCRIPTOR=_REQREGISTERGAME,
    __module__='base.server_to_game_pb2'
    # @@protoc_insertion_point(class_scope:ReqRegisterGame)
))
_sym_db.RegisterMessage(ReqRegisterGame)

ResRegisterGame = _reflection.GeneratedProtocolMessageType('ResRegisterGame', (_message.Message,), dict(
    DESCRIPTOR=_RESREGISTERGAME,
    __module__='base.server_to_game_pb2'
    # @@protoc_insertion_point(class_scope:ResRegisterGame)
))
_sym_db.RegisterMessage(ResRegisterGame)

ReqServiceState = _reflection.GeneratedProtocolMessageType('ReqServiceState', (_message.Message,), dict(
    DESCRIPTOR=_REQSERVICESTATE,
    __module__='base.server_to_game_pb2'
    # @@protoc_insertion_point(class_scope:ReqServiceState)
))
_sym_db.RegisterMessage(ReqServiceState)

ReqChangeOnline = _reflection.GeneratedProtocolMessageType('ReqChangeOnline', (_message.Message,), dict(
    DESCRIPTOR=_REQCHANGEONLINE,
    __module__='base.server_to_game_pb2'
    # @@protoc_insertion_point(class_scope:ReqChangeOnline)
))
_sym_db.RegisterMessage(ReqChangeOnline)

DismissGame = _reflection.GeneratedProtocolMessageType('DismissGame', (_message.Message,), dict(
    DESCRIPTOR=_DISMISSGAME,
    __module__='base.server_to_game_pb2'
    # @@protoc_insertion_point(class_scope:DismissGame)
))
_sym_db.RegisterMessage(DismissGame)

UserExit = _reflection.GeneratedProtocolMessageType('UserExit', (_message.Message,), dict(
    DESCRIPTOR=_USEREXIT,
    __module__='base.server_to_game_pb2'
    # @@protoc_insertion_point(class_scope:UserExit)
))
_sym_db.RegisterMessage(UserExit)

DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('H\003'))
# @@protoc_insertion_point(module_scope)
