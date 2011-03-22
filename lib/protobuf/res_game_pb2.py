# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)


DESCRIPTOR = descriptor.FileDescriptor(
  name='res_game.proto',
  package='',
  serialized_pb='\n\x0eres_game.proto\x1a\x12res_listbase.proto\"6\n\x0bLogicalGame\x12\n\n\x02id\x18\x01 \x01(\r\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\r\n\x05modes\x18\x03 \x03(\t\"5\n\x0fLogicalGameList\x12\"\n\x0clogicalGames\x18\x01 \x03(\x0b\x32\x0c.LogicalGame\"w\n\x0cPhysicalGame\x12\n\n\x02id\x18\x01 \x01(\r\x12\x0c\n\x04name\x18\x02 \x01(\t\x12&\n\x08versions\x18\x03 \x03(\x0b\x32\x14.PhysicalGameVersion\x12%\n\x07version\x18\x04 \x01(\x0b\x32\x14.PhysicalGameVersion\"8\n\x10PhysicalGameList\x12$\n\rphysicalGames\x18\x01 \x03(\x0b\x32\r.PhysicalGame\"R\n\x13PhysicalGameVersion\x12\x0c\n\x04\x63ode\x18\x01 \x01(\t\x12\x0f\n\x07\x64isplay\x18\x02 \x01(\t\x12\x0c\n\x04\x66ile\x18\x03 \x01(\t\x12\x0e\n\x06\x64igest\x18\x04 \x01(\t\"\xb5\x01\n\x03Map\x12\n\n\x02id\x18\x01 \x01(\r\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0f\n\x07version\x18\x03 \x01(\t\x12\x16\n\x0ephysicalGameID\x18\x04 \x01(\r\x12 \n\x18physicalGameVersionLimit\x18\x05 \x01(\t\x12\x0e\n\x06\x64igest\x18\x06 \x01(\t\x12\x14\n\x0c\x64ownloadLink\x18\x07 \x01(\t\x12\x10\n\x08\x66ileSize\x18\x08 \x01(\r\x12\x11\n\tthumbnail\x18\t \x01(\t\":\n\x07MapList\x12\x12\n\x04maps\x18\x01 \x03(\x0b\x32\x04.Map\x12\x1b\n\x06params\x18\x02 \x01(\x0b\x32\x0b.ListParams\"\x84\x01\n\x08\x45ventGet\x12\n\n\x02id\x18\x01 \x01(\r\x12\x0c\n\x04name\x18\x02 \x01(\t\x12$\n\rphysical_game\x18\x03 \x01(\x0b\x32\r.PhysicalGame\x12\x1b\n\rrequired_maps\x18\x04 \x03(\x0b\x32\x04.Map\x12\x1b\n\roptional_maps\x18\x05 \x03(\x0b\x32\x04.MapB\x12\n\x0eproto.responseH\x02')




_LOGICALGAME = descriptor.Descriptor(
  name='LogicalGame',
  full_name='LogicalGame',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='id', full_name='LogicalGame.id', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='name', full_name='LogicalGame.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='modes', full_name='LogicalGame.modes', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=38,
  serialized_end=92,
)


_LOGICALGAMELIST = descriptor.Descriptor(
  name='LogicalGameList',
  full_name='LogicalGameList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='logicalGames', full_name='LogicalGameList.logicalGames', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=94,
  serialized_end=147,
)


_PHYSICALGAME = descriptor.Descriptor(
  name='PhysicalGame',
  full_name='PhysicalGame',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='id', full_name='PhysicalGame.id', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='name', full_name='PhysicalGame.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='versions', full_name='PhysicalGame.versions', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='version', full_name='PhysicalGame.version', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=149,
  serialized_end=268,
)


_PHYSICALGAMELIST = descriptor.Descriptor(
  name='PhysicalGameList',
  full_name='PhysicalGameList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='physicalGames', full_name='PhysicalGameList.physicalGames', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=270,
  serialized_end=326,
)


_PHYSICALGAMEVERSION = descriptor.Descriptor(
  name='PhysicalGameVersion',
  full_name='PhysicalGameVersion',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='code', full_name='PhysicalGameVersion.code', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='display', full_name='PhysicalGameVersion.display', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='file', full_name='PhysicalGameVersion.file', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='digest', full_name='PhysicalGameVersion.digest', index=3,
      number=4, type=9, cpp_type=9, label=1,
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
  serialized_start=328,
  serialized_end=410,
)


_MAP = descriptor.Descriptor(
  name='Map',
  full_name='Map',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='id', full_name='Map.id', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='name', full_name='Map.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='version', full_name='Map.version', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='physicalGameID', full_name='Map.physicalGameID', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='physicalGameVersionLimit', full_name='Map.physicalGameVersionLimit', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='digest', full_name='Map.digest', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='downloadLink', full_name='Map.downloadLink', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='fileSize', full_name='Map.fileSize', index=7,
      number=8, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='thumbnail', full_name='Map.thumbnail', index=8,
      number=9, type=9, cpp_type=9, label=1,
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
  serialized_start=413,
  serialized_end=594,
)


_MAPLIST = descriptor.Descriptor(
  name='MapList',
  full_name='MapList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='maps', full_name='MapList.maps', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='params', full_name='MapList.params', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=596,
  serialized_end=654,
)


_EVENTGET = descriptor.Descriptor(
  name='EventGet',
  full_name='EventGet',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='id', full_name='EventGet.id', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='name', full_name='EventGet.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='physical_game', full_name='EventGet.physical_game', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='required_maps', full_name='EventGet.required_maps', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='optional_maps', full_name='EventGet.optional_maps', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=657,
  serialized_end=789,
)

import res_listbase_pb2

_LOGICALGAMELIST.fields_by_name['logicalGames'].message_type = _LOGICALGAME
_PHYSICALGAME.fields_by_name['versions'].message_type = _PHYSICALGAMEVERSION
_PHYSICALGAME.fields_by_name['version'].message_type = _PHYSICALGAMEVERSION
_PHYSICALGAMELIST.fields_by_name['physicalGames'].message_type = _PHYSICALGAME
_MAPLIST.fields_by_name['maps'].message_type = _MAP
_MAPLIST.fields_by_name['params'].message_type = res_listbase_pb2._LISTPARAMS
_EVENTGET.fields_by_name['physical_game'].message_type = _PHYSICALGAME
_EVENTGET.fields_by_name['required_maps'].message_type = _MAP
_EVENTGET.fields_by_name['optional_maps'].message_type = _MAP

class LogicalGame(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _LOGICALGAME
  
  # @@protoc_insertion_point(class_scope:LogicalGame)

class LogicalGameList(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _LOGICALGAMELIST
  
  # @@protoc_insertion_point(class_scope:LogicalGameList)

class PhysicalGame(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _PHYSICALGAME
  
  # @@protoc_insertion_point(class_scope:PhysicalGame)

class PhysicalGameList(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _PHYSICALGAMELIST
  
  # @@protoc_insertion_point(class_scope:PhysicalGameList)

class PhysicalGameVersion(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _PHYSICALGAMEVERSION
  
  # @@protoc_insertion_point(class_scope:PhysicalGameVersion)

class Map(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _MAP
  
  # @@protoc_insertion_point(class_scope:Map)

class MapList(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _MAPLIST
  
  # @@protoc_insertion_point(class_scope:MapList)

class EventGet(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _EVENTGET
  
  # @@protoc_insertion_point(class_scope:EventGet)

# @@protoc_insertion_point(module_scope)
