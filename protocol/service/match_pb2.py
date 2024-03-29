# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: service/match.proto

import sys

_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()

DESCRIPTOR = _descriptor.FileDescriptor(
    name='service/match.proto',
    package='mahjong',
    syntax='proto3',
    serialized_pb=_b(
        '\n\x13service/match.proto\x12\x07mahjong\"R\n\x12ReqApplyEnterMatch\x12\x0f\n\x07\x61llocId\x18\x01 \x01(\x05\x12\r\n\x05level\x18\x02 \x01(\x05\x12\x0e\n\x06reject\x18\x03 \x01(\x05\x12\x0c\n\x04type\x18\x04 \x01(\x05\"~\n\x12RecApplyEnterMatch\x12\x35\n\x05state\x18\x01 \x01(\x0e\x32&.mahjong.RecApplyEnterMatch.EnterState\"1\n\nEnterState\x12\x0b\n\x07SUCCESS\x10\x00\x12\t\n\x05\x46\x41ILD\x10\x01\x12\x0b\n\x07\x41LREADY\x10\x02\"\x14\n\x12ReqApplyLeaveMatch\"q\n\x12RecApplyLeaveMatch\x12\x35\n\x05state\x18\x01 \x01(\x0e\x32&.mahjong.RecApplyLeaveMatch.LeaveState\"$\n\nLeaveState\x12\x0b\n\x07SUCCESS\x10\x00\x12\t\n\x05\x46\x41ILD\x10\x01\"w\n\x12ReqUpdateMatchInfo\x12\x34\n\x05infos\x18\x01 \x03(\x0b\x32%.mahjong.ReqUpdateMatchInfo.MatchInfo\x1a+\n\tMatchInfo\x12\x0f\n\x07\x61llocId\x18\x01 \x01(\x05\x12\r\n\x05level\x18\x02 \x01(\x05\"\xad\x01\n\x12RecUpdateMatchInfo\x12\x34\n\x05infos\x18\x06 \x03(\x0b\x32%.mahjong.RecUpdateMatchInfo.MatchInfo\x1a\x61\n\tMatchInfo\x12\x0f\n\x07\x61llocId\x18\x01 \x01(\x05\x12\r\n\x05level\x18\x02 \x01(\x05\x12\r\n\x05games\x18\x03 \x01(\x05\x12\x0f\n\x07players\x18\x04 \x01(\x05\x12\x14\n\x0ctotalPlayers\x18\x05 \x01(\x05\"&\n\x12ReqMatchRecordInfo\x12\x10\n\x08\x61llocIds\x18\x02 \x03(\x05\"S\n\x12RecMatchRecordInfo\x12\r\n\x05state\x18\x01 \x01(\x05\x12.\n\x0cmatchRecords\x18\x02 \x03(\x0b\x32\x18.mahjong.UGameRecordInfo\"\xb8\x01\n\x0fUGameRecordInfo\x12\x10\n\x08recordId\x18\x01 \x01(\t\x12\x0f\n\x07\x61llocId\x18\x02 \x01(\x05\x12\x0e\n\x06gameId\x18\x03 \x01(\x05\x12\x12\n\nteahouseId\x18\x04 \x01(\x05\x12\x0e\n\x06lookId\x18\x05 \x01(\x05\x12\x10\n\x08playTime\x18\x06 \x01(\x05\x12+\n\x0bplayerDatas\x18\x07 \x03(\x0b\x32\x16.mahjong.URecordPlayer\x12\x0f\n\x07\x63ontent\x18\x08 \x01(\x0c\">\n\rURecordPlayer\x12\x10\n\x08playerId\x18\x01 \x01(\x05\x12\x0c\n\x04nick\x18\x02 \x01(\t\x12\r\n\x05score\x18\x03 \x01(\x05\x42\x02H\x03\x62\x06proto3')
)

_RECAPPLYENTERMATCH_ENTERSTATE = _descriptor.EnumDescriptor(
    name='EnterState',
    full_name='mahjong.RecApplyEnterMatch.EnterState',
    filename=None,
    file=DESCRIPTOR,
    values=[
        _descriptor.EnumValueDescriptor(
            name='SUCCESS', index=0, number=0,
            options=None,
            type=None),
        _descriptor.EnumValueDescriptor(
            name='FAILD', index=1, number=1,
            options=None,
            type=None),
        _descriptor.EnumValueDescriptor(
            name='ALREADY', index=2, number=2,
            options=None,
            type=None),
    ],
    containing_type=None,
    options=None,
    serialized_start=193,
    serialized_end=242,
)
_sym_db.RegisterEnumDescriptor(_RECAPPLYENTERMATCH_ENTERSTATE)

_RECAPPLYLEAVEMATCH_LEAVESTATE = _descriptor.EnumDescriptor(
    name='LeaveState',
    full_name='mahjong.RecApplyLeaveMatch.LeaveState',
    filename=None,
    file=DESCRIPTOR,
    values=[
        _descriptor.EnumValueDescriptor(
            name='SUCCESS', index=0, number=0,
            options=None,
            type=None),
        _descriptor.EnumValueDescriptor(
            name='FAILD', index=1, number=1,
            options=None,
            type=None),
    ],
    containing_type=None,
    options=None,
    serialized_start=343,
    serialized_end=379,
)
_sym_db.RegisterEnumDescriptor(_RECAPPLYLEAVEMATCH_LEAVESTATE)

_REQAPPLYENTERMATCH = _descriptor.Descriptor(
    name='ReqApplyEnterMatch',
    full_name='mahjong.ReqApplyEnterMatch',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='allocId', full_name='mahjong.ReqApplyEnterMatch.allocId', index=0,
            number=1, type=5, cpp_type=1, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None, file=DESCRIPTOR),
        _descriptor.FieldDescriptor(
            name='level', full_name='mahjong.ReqApplyEnterMatch.level', index=1,
            number=2, type=5, cpp_type=1, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None, file=DESCRIPTOR),
        _descriptor.FieldDescriptor(
            name='reject', full_name='mahjong.ReqApplyEnterMatch.reject', index=2,
            number=3, type=5, cpp_type=1, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None, file=DESCRIPTOR),
        _descriptor.FieldDescriptor(
            name='type', full_name='mahjong.ReqApplyEnterMatch.type', index=3,
            number=4, type=5, cpp_type=1, label=1,
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
    serialized_start=32,
    serialized_end=114,
)

_RECAPPLYENTERMATCH = _descriptor.Descriptor(
    name='RecApplyEnterMatch',
    full_name='mahjong.RecApplyEnterMatch',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='state', full_name='mahjong.RecApplyEnterMatch.state', index=0,
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
        _RECAPPLYENTERMATCH_ENTERSTATE,
    ],
    options=None,
    is_extendable=False,
    syntax='proto3',
    extension_ranges=[],
    oneofs=[
    ],
    serialized_start=116,
    serialized_end=242,
)

_REQAPPLYLEAVEMATCH = _descriptor.Descriptor(
    name='ReqApplyLeaveMatch',
    full_name='mahjong.ReqApplyLeaveMatch',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
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
    serialized_start=244,
    serialized_end=264,
)

_RECAPPLYLEAVEMATCH = _descriptor.Descriptor(
    name='RecApplyLeaveMatch',
    full_name='mahjong.RecApplyLeaveMatch',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='state', full_name='mahjong.RecApplyLeaveMatch.state', index=0,
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
        _RECAPPLYLEAVEMATCH_LEAVESTATE,
    ],
    options=None,
    is_extendable=False,
    syntax='proto3',
    extension_ranges=[],
    oneofs=[
    ],
    serialized_start=266,
    serialized_end=379,
)

_REQUPDATEMATCHINFO_MATCHINFO = _descriptor.Descriptor(
    name='MatchInfo',
    full_name='mahjong.ReqUpdateMatchInfo.MatchInfo',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='allocId', full_name='mahjong.ReqUpdateMatchInfo.MatchInfo.allocId', index=0,
            number=1, type=5, cpp_type=1, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None, file=DESCRIPTOR),
        _descriptor.FieldDescriptor(
            name='level', full_name='mahjong.ReqUpdateMatchInfo.MatchInfo.level', index=1,
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
    serialized_start=457,
    serialized_end=500,
)

_REQUPDATEMATCHINFO = _descriptor.Descriptor(
    name='ReqUpdateMatchInfo',
    full_name='mahjong.ReqUpdateMatchInfo',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='infos', full_name='mahjong.ReqUpdateMatchInfo.infos', index=0,
            number=1, type=11, cpp_type=10, label=3,
            has_default_value=False, default_value=[],
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None, file=DESCRIPTOR),
    ],
    extensions=[
    ],
    nested_types=[_REQUPDATEMATCHINFO_MATCHINFO, ],
    enum_types=[
    ],
    options=None,
    is_extendable=False,
    syntax='proto3',
    extension_ranges=[],
    oneofs=[
    ],
    serialized_start=381,
    serialized_end=500,
)

_RECUPDATEMATCHINFO_MATCHINFO = _descriptor.Descriptor(
    name='MatchInfo',
    full_name='mahjong.RecUpdateMatchInfo.MatchInfo',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='allocId', full_name='mahjong.RecUpdateMatchInfo.MatchInfo.allocId', index=0,
            number=1, type=5, cpp_type=1, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None, file=DESCRIPTOR),
        _descriptor.FieldDescriptor(
            name='level', full_name='mahjong.RecUpdateMatchInfo.MatchInfo.level', index=1,
            number=2, type=5, cpp_type=1, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None, file=DESCRIPTOR),
        _descriptor.FieldDescriptor(
            name='games', full_name='mahjong.RecUpdateMatchInfo.MatchInfo.games', index=2,
            number=3, type=5, cpp_type=1, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None, file=DESCRIPTOR),
        _descriptor.FieldDescriptor(
            name='players', full_name='mahjong.RecUpdateMatchInfo.MatchInfo.players', index=3,
            number=4, type=5, cpp_type=1, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None, file=DESCRIPTOR),
        _descriptor.FieldDescriptor(
            name='totalPlayers', full_name='mahjong.RecUpdateMatchInfo.MatchInfo.totalPlayers', index=4,
            number=5, type=5, cpp_type=1, label=1,
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
    serialized_start=579,
    serialized_end=676,
)

_RECUPDATEMATCHINFO = _descriptor.Descriptor(
    name='RecUpdateMatchInfo',
    full_name='mahjong.RecUpdateMatchInfo',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='infos', full_name='mahjong.RecUpdateMatchInfo.infos', index=0,
            number=6, type=11, cpp_type=10, label=3,
            has_default_value=False, default_value=[],
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None, file=DESCRIPTOR),
    ],
    extensions=[
    ],
    nested_types=[_RECUPDATEMATCHINFO_MATCHINFO, ],
    enum_types=[
    ],
    options=None,
    is_extendable=False,
    syntax='proto3',
    extension_ranges=[],
    oneofs=[
    ],
    serialized_start=503,
    serialized_end=676,
)

_REQMATCHRECORDINFO = _descriptor.Descriptor(
    name='ReqMatchRecordInfo',
    full_name='mahjong.ReqMatchRecordInfo',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='allocIds', full_name='mahjong.ReqMatchRecordInfo.allocIds', index=0,
            number=2, type=5, cpp_type=1, label=3,
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
    serialized_start=678,
    serialized_end=716,
)

_RECMATCHRECORDINFO = _descriptor.Descriptor(
    name='RecMatchRecordInfo',
    full_name='mahjong.RecMatchRecordInfo',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='state', full_name='mahjong.RecMatchRecordInfo.state', index=0,
            number=1, type=5, cpp_type=1, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None, file=DESCRIPTOR),
        _descriptor.FieldDescriptor(
            name='matchRecords', full_name='mahjong.RecMatchRecordInfo.matchRecords', index=1,
            number=2, type=11, cpp_type=10, label=3,
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
    serialized_start=718,
    serialized_end=801,
)

_UGAMERECORDINFO = _descriptor.Descriptor(
    name='UGameRecordInfo',
    full_name='mahjong.UGameRecordInfo',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='recordId', full_name='mahjong.UGameRecordInfo.recordId', index=0,
            number=1, type=9, cpp_type=9, label=1,
            has_default_value=False, default_value=_b("").decode('utf-8'),
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None, file=DESCRIPTOR),
        _descriptor.FieldDescriptor(
            name='allocId', full_name='mahjong.UGameRecordInfo.allocId', index=1,
            number=2, type=5, cpp_type=1, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None, file=DESCRIPTOR),
        _descriptor.FieldDescriptor(
            name='gameId', full_name='mahjong.UGameRecordInfo.gameId', index=2,
            number=3, type=5, cpp_type=1, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None, file=DESCRIPTOR),
        _descriptor.FieldDescriptor(
            name='teahouseId', full_name='mahjong.UGameRecordInfo.teahouseId', index=3,
            number=4, type=5, cpp_type=1, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None, file=DESCRIPTOR),
        _descriptor.FieldDescriptor(
            name='lookId', full_name='mahjong.UGameRecordInfo.lookId', index=4,
            number=5, type=5, cpp_type=1, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None, file=DESCRIPTOR),
        _descriptor.FieldDescriptor(
            name='playTime', full_name='mahjong.UGameRecordInfo.playTime', index=5,
            number=6, type=5, cpp_type=1, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None, file=DESCRIPTOR),
        _descriptor.FieldDescriptor(
            name='playerDatas', full_name='mahjong.UGameRecordInfo.playerDatas', index=6,
            number=7, type=11, cpp_type=10, label=3,
            has_default_value=False, default_value=[],
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None, file=DESCRIPTOR),
        _descriptor.FieldDescriptor(
            name='content', full_name='mahjong.UGameRecordInfo.content', index=7,
            number=8, type=12, cpp_type=9, label=1,
            has_default_value=False, default_value=_b(""),
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
    serialized_start=804,
    serialized_end=988,
)

_URECORDPLAYER = _descriptor.Descriptor(
    name='URecordPlayer',
    full_name='mahjong.URecordPlayer',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='playerId', full_name='mahjong.URecordPlayer.playerId', index=0,
            number=1, type=5, cpp_type=1, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None, file=DESCRIPTOR),
        _descriptor.FieldDescriptor(
            name='nick', full_name='mahjong.URecordPlayer.nick', index=1,
            number=2, type=9, cpp_type=9, label=1,
            has_default_value=False, default_value=_b("").decode('utf-8'),
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None, file=DESCRIPTOR),
        _descriptor.FieldDescriptor(
            name='score', full_name='mahjong.URecordPlayer.score', index=2,
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
    serialized_start=990,
    serialized_end=1052,
)

_RECAPPLYENTERMATCH.fields_by_name['state'].enum_type = _RECAPPLYENTERMATCH_ENTERSTATE
_RECAPPLYENTERMATCH_ENTERSTATE.containing_type = _RECAPPLYENTERMATCH
_RECAPPLYLEAVEMATCH.fields_by_name['state'].enum_type = _RECAPPLYLEAVEMATCH_LEAVESTATE
_RECAPPLYLEAVEMATCH_LEAVESTATE.containing_type = _RECAPPLYLEAVEMATCH
_REQUPDATEMATCHINFO_MATCHINFO.containing_type = _REQUPDATEMATCHINFO
_REQUPDATEMATCHINFO.fields_by_name['infos'].message_type = _REQUPDATEMATCHINFO_MATCHINFO
_RECUPDATEMATCHINFO_MATCHINFO.containing_type = _RECUPDATEMATCHINFO
_RECUPDATEMATCHINFO.fields_by_name['infos'].message_type = _RECUPDATEMATCHINFO_MATCHINFO
_RECMATCHRECORDINFO.fields_by_name['matchRecords'].message_type = _UGAMERECORDINFO
_UGAMERECORDINFO.fields_by_name['playerDatas'].message_type = _URECORDPLAYER
DESCRIPTOR.message_types_by_name['ReqApplyEnterMatch'] = _REQAPPLYENTERMATCH
DESCRIPTOR.message_types_by_name['RecApplyEnterMatch'] = _RECAPPLYENTERMATCH
DESCRIPTOR.message_types_by_name['ReqApplyLeaveMatch'] = _REQAPPLYLEAVEMATCH
DESCRIPTOR.message_types_by_name['RecApplyLeaveMatch'] = _RECAPPLYLEAVEMATCH
DESCRIPTOR.message_types_by_name['ReqUpdateMatchInfo'] = _REQUPDATEMATCHINFO
DESCRIPTOR.message_types_by_name['RecUpdateMatchInfo'] = _RECUPDATEMATCHINFO
DESCRIPTOR.message_types_by_name['ReqMatchRecordInfo'] = _REQMATCHRECORDINFO
DESCRIPTOR.message_types_by_name['RecMatchRecordInfo'] = _RECMATCHRECORDINFO
DESCRIPTOR.message_types_by_name['UGameRecordInfo'] = _UGAMERECORDINFO
DESCRIPTOR.message_types_by_name['URecordPlayer'] = _URECORDPLAYER
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ReqApplyEnterMatch = _reflection.GeneratedProtocolMessageType('ReqApplyEnterMatch', (_message.Message,), dict(
    DESCRIPTOR=_REQAPPLYENTERMATCH,
    __module__='service.match_pb2'
    # @@protoc_insertion_point(class_scope:mahjong.ReqApplyEnterMatch)
))
_sym_db.RegisterMessage(ReqApplyEnterMatch)

RecApplyEnterMatch = _reflection.GeneratedProtocolMessageType('RecApplyEnterMatch', (_message.Message,), dict(
    DESCRIPTOR=_RECAPPLYENTERMATCH,
    __module__='service.match_pb2'
    # @@protoc_insertion_point(class_scope:mahjong.RecApplyEnterMatch)
))
_sym_db.RegisterMessage(RecApplyEnterMatch)

ReqApplyLeaveMatch = _reflection.GeneratedProtocolMessageType('ReqApplyLeaveMatch', (_message.Message,), dict(
    DESCRIPTOR=_REQAPPLYLEAVEMATCH,
    __module__='service.match_pb2'
    # @@protoc_insertion_point(class_scope:mahjong.ReqApplyLeaveMatch)
))
_sym_db.RegisterMessage(ReqApplyLeaveMatch)

RecApplyLeaveMatch = _reflection.GeneratedProtocolMessageType('RecApplyLeaveMatch', (_message.Message,), dict(
    DESCRIPTOR=_RECAPPLYLEAVEMATCH,
    __module__='service.match_pb2'
    # @@protoc_insertion_point(class_scope:mahjong.RecApplyLeaveMatch)
))
_sym_db.RegisterMessage(RecApplyLeaveMatch)

ReqUpdateMatchInfo = _reflection.GeneratedProtocolMessageType('ReqUpdateMatchInfo', (_message.Message,), dict(

    MatchInfo=_reflection.GeneratedProtocolMessageType('MatchInfo', (_message.Message,), dict(
        DESCRIPTOR=_REQUPDATEMATCHINFO_MATCHINFO,
        __module__='service.match_pb2'
        # @@protoc_insertion_point(class_scope:mahjong.ReqUpdateMatchInfo.MatchInfo)
    ))
    ,
    DESCRIPTOR=_REQUPDATEMATCHINFO,
    __module__='service.match_pb2'
    # @@protoc_insertion_point(class_scope:mahjong.ReqUpdateMatchInfo)
))
_sym_db.RegisterMessage(ReqUpdateMatchInfo)
_sym_db.RegisterMessage(ReqUpdateMatchInfo.MatchInfo)

RecUpdateMatchInfo = _reflection.GeneratedProtocolMessageType('RecUpdateMatchInfo', (_message.Message,), dict(

    MatchInfo=_reflection.GeneratedProtocolMessageType('MatchInfo', (_message.Message,), dict(
        DESCRIPTOR=_RECUPDATEMATCHINFO_MATCHINFO,
        __module__='service.match_pb2'
        # @@protoc_insertion_point(class_scope:mahjong.RecUpdateMatchInfo.MatchInfo)
    ))
    ,
    DESCRIPTOR=_RECUPDATEMATCHINFO,
    __module__='service.match_pb2'
    # @@protoc_insertion_point(class_scope:mahjong.RecUpdateMatchInfo)
))
_sym_db.RegisterMessage(RecUpdateMatchInfo)
_sym_db.RegisterMessage(RecUpdateMatchInfo.MatchInfo)

ReqMatchRecordInfo = _reflection.GeneratedProtocolMessageType('ReqMatchRecordInfo', (_message.Message,), dict(
    DESCRIPTOR=_REQMATCHRECORDINFO,
    __module__='service.match_pb2'
    # @@protoc_insertion_point(class_scope:mahjong.ReqMatchRecordInfo)
))
_sym_db.RegisterMessage(ReqMatchRecordInfo)

RecMatchRecordInfo = _reflection.GeneratedProtocolMessageType('RecMatchRecordInfo', (_message.Message,), dict(
    DESCRIPTOR=_RECMATCHRECORDINFO,
    __module__='service.match_pb2'
    # @@protoc_insertion_point(class_scope:mahjong.RecMatchRecordInfo)
))
_sym_db.RegisterMessage(RecMatchRecordInfo)

UGameRecordInfo = _reflection.GeneratedProtocolMessageType('UGameRecordInfo', (_message.Message,), dict(
    DESCRIPTOR=_UGAMERECORDINFO,
    __module__='service.match_pb2'
    # @@protoc_insertion_point(class_scope:mahjong.UGameRecordInfo)
))
_sym_db.RegisterMessage(UGameRecordInfo)

URecordPlayer = _reflection.GeneratedProtocolMessageType('URecordPlayer', (_message.Message,), dict(
    DESCRIPTOR=_URECORDPLAYER,
    __module__='service.match_pb2'
    # @@protoc_insertion_point(class_scope:mahjong.URecordPlayer)
))
_sym_db.RegisterMessage(URecordPlayer)

DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('H\003'))
# @@protoc_insertion_point(module_scope)
