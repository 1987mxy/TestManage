# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)


DESCRIPTOR = descriptor.FileDescriptor(
  name='res_sc.proto',
  package='',
  serialized_pb='\n\x0cres_sc.proto\x1a\x0eres_user.proto\"\x90\x07\n\rStarCraftData\x12%\n\x06header\x18\x01 \x02(\x0b\x32\x15.StarCraftData.Header\x12&\n\x07players\x18\x02 \x03(\x0b\x32\x15.StarCraftData.Player\x12,\n\x0cleavePlayers\x18\x03 \x03(\x0b\x32\x16.StarCraftData.SCLeave\x1ah\n\x06Header\x12\x0f\n\x07version\x18\x01 \x02(\t\x12\x13\n\x0bmessageType\x18\x02 \x02(\t\x12\x12\n\nbattleType\x18\x03 \x01(\t\x12\x0c\n\x04time\x18\x04 \x02(\r\x12\x16\n\x0euserIDOfSender\x18\x05 \x02(\r\x1a\x86\x01\n\x08UnitInfo\x12\x10\n\x08stringID\x18\x01 \x02(\t\x12\x15\n\ntotalBuilt\x18\x02 \x01(\x05:\x01\x30\x12\x13\n\x08nowExist\x18\x03 \x01(\x05:\x01\x30\x12\x1a\n\x0fwaitForBuilding\x18\x04 \x01(\x05:\x01\x30\x12\x12\n\nisBuilding\x18\x05 \x01(\x05\x12\x0c\n\x04name\x18\x06 \x01(\t\x1a\xde\x03\n\x06Player\x12\x0e\n\x06userID\x18\x01 \x02(\r\x12\x0e\n\x06result\x18\x02 \x01(\t\x12\x12\n\ntotalScore\x18\x03 \x01(\r\x12\x11\n\tunitScore\x18\x04 \x01(\r\x12\x12\n\nbuildScore\x18\x05 \x01(\r\x12\x13\n\x0bsourceScore\x18\x06 \x01(\r\x12\x12\n\nnowMineral\x18\x07 \x01(\r\x12\x0e\n\x06nowGas\x18\x08 \x01(\r\x12\x12\n\nallMineral\x18\t \x01(\r\x12\x0e\n\x06\x61llGas\x18\n \x01(\r\x12\x15\n\rnumAllProduce\x18\x0b \x01(\r\x12\x16\n\x0enumAllUnitLost\x18\x0c \x01(\r\x12\x12\n\nnumAllKill\x18\r \x01(\r\x12\x13\n\x0bnumAllBuild\x18\x0e \x01(\r\x12\x15\n\rnumAllDestroy\x18\x0f \x01(\r\x12\x1a\n\x12numAllBuildingLost\x18\x10 \x01(\r\x12\x0e\n\x03\x41PM\x18\x11 \x01(\x02:\x01\x30\x12\x0c\n\x04race\x18\x12 \x01(\t\x12\x11\n\tleaveTime\x18\x13 \x01(\x05\x12\x0f\n\x07isLeave\x18\x14 \x01(\t\x12&\n\x05units\x18\x15 \x03(\x0b\x32\x17.StarCraftData.UnitInfo\x12\x18\n\x04user\x18\x16 \x01(\x0b\x32\n.UserModel\x12\r\n\x05\x66orce\x18\x17 \x01(\x05\x1a.\n\x07SCLeave\x12\x0e\n\x06userID\x18\x01 \x02(\r\x12\x13\n\x0bleaveReason\x18\x02 \x01(\tB\x12\n\x0eproto.responseH\x02')




_STARCRAFTDATA_HEADER = descriptor.Descriptor(
  name='Header',
  full_name='StarCraftData.Header',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='version', full_name='StarCraftData.Header.version', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='messageType', full_name='StarCraftData.Header.messageType', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='battleType', full_name='StarCraftData.Header.battleType', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='time', full_name='StarCraftData.Header.time', index=3,
      number=4, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='userIDOfSender', full_name='StarCraftData.Header.userIDOfSender', index=4,
      number=5, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=175,
  serialized_end=279,
)

_STARCRAFTDATA_UNITINFO = descriptor.Descriptor(
  name='UnitInfo',
  full_name='StarCraftData.UnitInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='stringID', full_name='StarCraftData.UnitInfo.stringID', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='totalBuilt', full_name='StarCraftData.UnitInfo.totalBuilt', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='nowExist', full_name='StarCraftData.UnitInfo.nowExist', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='waitForBuilding', full_name='StarCraftData.UnitInfo.waitForBuilding', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='isBuilding', full_name='StarCraftData.UnitInfo.isBuilding', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='name', full_name='StarCraftData.UnitInfo.name', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=282,
  serialized_end=416,
)

_STARCRAFTDATA_PLAYER = descriptor.Descriptor(
  name='Player',
  full_name='StarCraftData.Player',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='userID', full_name='StarCraftData.Player.userID', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='result', full_name='StarCraftData.Player.result', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='totalScore', full_name='StarCraftData.Player.totalScore', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='unitScore', full_name='StarCraftData.Player.unitScore', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='buildScore', full_name='StarCraftData.Player.buildScore', index=4,
      number=5, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='sourceScore', full_name='StarCraftData.Player.sourceScore', index=5,
      number=6, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='nowMineral', full_name='StarCraftData.Player.nowMineral', index=6,
      number=7, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='nowGas', full_name='StarCraftData.Player.nowGas', index=7,
      number=8, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='allMineral', full_name='StarCraftData.Player.allMineral', index=8,
      number=9, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='allGas', full_name='StarCraftData.Player.allGas', index=9,
      number=10, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='numAllProduce', full_name='StarCraftData.Player.numAllProduce', index=10,
      number=11, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='numAllUnitLost', full_name='StarCraftData.Player.numAllUnitLost', index=11,
      number=12, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='numAllKill', full_name='StarCraftData.Player.numAllKill', index=12,
      number=13, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='numAllBuild', full_name='StarCraftData.Player.numAllBuild', index=13,
      number=14, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='numAllDestroy', full_name='StarCraftData.Player.numAllDestroy', index=14,
      number=15, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='numAllBuildingLost', full_name='StarCraftData.Player.numAllBuildingLost', index=15,
      number=16, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='APM', full_name='StarCraftData.Player.APM', index=16,
      number=17, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='race', full_name='StarCraftData.Player.race', index=17,
      number=18, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='leaveTime', full_name='StarCraftData.Player.leaveTime', index=18,
      number=19, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='isLeave', full_name='StarCraftData.Player.isLeave', index=19,
      number=20, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='units', full_name='StarCraftData.Player.units', index=20,
      number=21, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='user', full_name='StarCraftData.Player.user', index=21,
      number=22, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='force', full_name='StarCraftData.Player.force', index=22,
      number=23, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=419,
  serialized_end=897,
)

_STARCRAFTDATA_SCLEAVE = descriptor.Descriptor(
  name='SCLeave',
  full_name='StarCraftData.SCLeave',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='userID', full_name='StarCraftData.SCLeave.userID', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='leaveReason', full_name='StarCraftData.SCLeave.leaveReason', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=899,
  serialized_end=945,
)

_STARCRAFTDATA = descriptor.Descriptor(
  name='StarCraftData',
  full_name='StarCraftData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='header', full_name='StarCraftData.header', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='players', full_name='StarCraftData.players', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='leavePlayers', full_name='StarCraftData.leavePlayers', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_STARCRAFTDATA_HEADER, _STARCRAFTDATA_UNITINFO, _STARCRAFTDATA_PLAYER, _STARCRAFTDATA_SCLEAVE, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=33,
  serialized_end=945,
)

import res_user_pb2

_STARCRAFTDATA_HEADER.containing_type = _STARCRAFTDATA;
_STARCRAFTDATA_UNITINFO.containing_type = _STARCRAFTDATA;
_STARCRAFTDATA_PLAYER.fields_by_name['units'].message_type = _STARCRAFTDATA_UNITINFO
_STARCRAFTDATA_PLAYER.fields_by_name['user'].message_type = res_user_pb2._USERMODEL
_STARCRAFTDATA_PLAYER.containing_type = _STARCRAFTDATA;
_STARCRAFTDATA_SCLEAVE.containing_type = _STARCRAFTDATA;
_STARCRAFTDATA.fields_by_name['header'].message_type = _STARCRAFTDATA_HEADER
_STARCRAFTDATA.fields_by_name['players'].message_type = _STARCRAFTDATA_PLAYER
_STARCRAFTDATA.fields_by_name['leavePlayers'].message_type = _STARCRAFTDATA_SCLEAVE

class StarCraftData(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  
  class Header(message.Message):
    __metaclass__ = reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _STARCRAFTDATA_HEADER
    
    # @@protoc_insertion_point(class_scope:StarCraftData.Header)
  
  class UnitInfo(message.Message):
    __metaclass__ = reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _STARCRAFTDATA_UNITINFO
    
    # @@protoc_insertion_point(class_scope:StarCraftData.UnitInfo)
  
  class Player(message.Message):
    __metaclass__ = reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _STARCRAFTDATA_PLAYER
    
    # @@protoc_insertion_point(class_scope:StarCraftData.Player)
  
  class SCLeave(message.Message):
    __metaclass__ = reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _STARCRAFTDATA_SCLEAVE
    
    # @@protoc_insertion_point(class_scope:StarCraftData.SCLeave)
  DESCRIPTOR = _STARCRAFTDATA
  
  # @@protoc_insertion_point(class_scope:StarCraftData)

# @@protoc_insertion_point(module_scope)