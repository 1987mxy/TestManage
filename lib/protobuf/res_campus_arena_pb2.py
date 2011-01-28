# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)


DESCRIPTOR = descriptor.FileDescriptor(
  name='res_campus_arena.proto',
  package='',
  serialized_pb='\n\x16res_campus_arena.proto\x1a\x12res_activity.proto\x1a\x0eres_clan.proto\x1a\x0eres_user.proto\x1a\x0eres_game.proto\x1a\x12res_listbase.proto\"\x8e\x01\n\x0e\x43\x61mpusArenaGet\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x1e\n\x04\x63lan\x18\x02 \x01(\x0b\x32\x10.ClanGetResponse\x12\n\n\x02id\x18\x03 \x01(\r\x12\x15\n\rlogicalGameID\x18\x04 \x01(\r\x12\x17\n\x0flogicalGameMode\x18\x05 \x01(\t\x12\x12\n\x04maps\x18\x07 \x03(\x0b\x32\x04.Map\"\\\n\x13\x43\x61mpusArenaGrouping\x12\x19\n\x05users\x18\x01 \x03(\x0b\x32\n.UserModel\x12\r\n\x05\x63ount\x18\x02 \x01(\r\x12\n\n\x02id\x18\x03 \x01(\t\x12\x0f\n\x07\x65ventID\x18\x04 \x01(\r\"S\n\x17\x43\x61mpusArenaGroupingList\x12#\n\x05items\x18\x01 \x03(\x0b\x32\x14.CampusArenaGrouping\x12\x13\n\x0bplaceholder\x18\x0f \x01(\r\":\n\x11\x43\x61mpusArena03List\x12%\n\x05items\x18\x01 \x03(\x0b\x32\x16.CampusArena03ListItem\"\xc9\x01\n\x15\x43\x61mpusArena03ListItem\x12\n\n\x02id\x18\x01 \x01(\r\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0c\n\x04mode\x18\x03 \x01(\t\x12\r\n\x05mapid\x18\x04 \x01(\r\x12\x0f\n\x07mapname\x18\x05 \x01(\t\x12\x0e\n\x06mcount\x18\x06 \x01(\t\x12\r\n\x05haspw\x18\x07 \x01(\x08\x12\x10\n\x08leaderid\x18\x08 \x01(\r\x12\x1d\n\x15\x65\x61rly_quit_constraint\x18\t \x01(\x02\x12\x18\n\x10level_constraint\x18\n \x01(\r\"\x91\x01\n\x12\x43\x61mpusArena03Stats\x12&\n\x05items\x18\x01 \x03(\x0b\x32\x17.CampusArena03StatsItem\x12\x1b\n\x06params\x18\x02 \x01(\x0b\x32\x0b.ListParams\x12\x0f\n\x07my_rank\x18\x03 \x01(\r\x12\x10\n\x08my_score\x18\x04 \x01(\r\x12\x13\n\x0bmy_position\x18\x05 \x01(\r\"\xdc\x01\n\x16\x43\x61mpusArena03StatsItem\x12\n\n\x02id\x18\x0b \x01(\r\x12\x0c\n\x04name\x18\n \x01(\t\x12\x0c\n\x04rank\x18\x01 \x01(\r\x12\r\n\x05score\x18\x02 \x01(\r\x12\r\n\x05level\x18\x03 \x01(\x05\x12\x0b\n\x03win\x18\x06 \x01(\r\x12\x12\n\nearly_quit\x18\x07 \x01(\r\x12\r\n\x05total\x18\x08 \x01(\r\x12\x10\n\x08win_rate\x18\t \x01(\x02\x12\x12\n\ndoublekill\x18\r \x01(\r\x12\x12\n\ntriplekill\x18\x0e \x01(\r\x12\x12\n\nassistance\x18\x0f \x01(\r\"\xa8\x01\n\x11\x43\x61mpusArena03Home\x12\x11\n\tbulletins\x18\x04 \x03(\t\x12(\n\x07scStats\x18\x05 \x03(\x0b\x32\x17.CampusArena03StatsItem\x12*\n\twar3Stats\x18\x06 \x03(\x0b\x32\x17.CampusArena03StatsItem\x12*\n\tdotaStats\x18\x07 \x03(\x0b\x32\x17.CampusArena03StatsItemB\x12\n\x0eproto.responseH\x02')




_CAMPUSARENAGET = descriptor.Descriptor(
  name='CampusArenaGet',
  full_name='CampusArenaGet',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='name', full_name='CampusArenaGet.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='clan', full_name='CampusArenaGet.clan', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='id', full_name='CampusArenaGet.id', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='logicalGameID', full_name='CampusArenaGet.logicalGameID', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='logicalGameMode', full_name='CampusArenaGet.logicalGameMode', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='maps', full_name='CampusArenaGet.maps', index=5,
      number=7, type=11, cpp_type=10, label=3,
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
  serialized_start=115,
  serialized_end=257,
)


_CAMPUSARENAGROUPING = descriptor.Descriptor(
  name='CampusArenaGrouping',
  full_name='CampusArenaGrouping',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='users', full_name='CampusArenaGrouping.users', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='count', full_name='CampusArenaGrouping.count', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='id', full_name='CampusArenaGrouping.id', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='eventID', full_name='CampusArenaGrouping.eventID', index=3,
      number=4, type=13, cpp_type=3, label=1,
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
  serialized_start=259,
  serialized_end=351,
)


_CAMPUSARENAGROUPINGLIST = descriptor.Descriptor(
  name='CampusArenaGroupingList',
  full_name='CampusArenaGroupingList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='items', full_name='CampusArenaGroupingList.items', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='placeholder', full_name='CampusArenaGroupingList.placeholder', index=1,
      number=15, type=13, cpp_type=3, label=1,
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
  serialized_start=353,
  serialized_end=436,
)


_CAMPUSARENA03LIST = descriptor.Descriptor(
  name='CampusArena03List',
  full_name='CampusArena03List',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='items', full_name='CampusArena03List.items', index=0,
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
  serialized_start=438,
  serialized_end=496,
)


_CAMPUSARENA03LISTITEM = descriptor.Descriptor(
  name='CampusArena03ListItem',
  full_name='CampusArena03ListItem',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='id', full_name='CampusArena03ListItem.id', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='name', full_name='CampusArena03ListItem.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='mode', full_name='CampusArena03ListItem.mode', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='mapid', full_name='CampusArena03ListItem.mapid', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='mapname', full_name='CampusArena03ListItem.mapname', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='mcount', full_name='CampusArena03ListItem.mcount', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='haspw', full_name='CampusArena03ListItem.haspw', index=6,
      number=7, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='leaderid', full_name='CampusArena03ListItem.leaderid', index=7,
      number=8, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='early_quit_constraint', full_name='CampusArena03ListItem.early_quit_constraint', index=8,
      number=9, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='level_constraint', full_name='CampusArena03ListItem.level_constraint', index=9,
      number=10, type=13, cpp_type=3, label=1,
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
  serialized_start=499,
  serialized_end=700,
)


_CAMPUSARENA03STATS = descriptor.Descriptor(
  name='CampusArena03Stats',
  full_name='CampusArena03Stats',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='items', full_name='CampusArena03Stats.items', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='params', full_name='CampusArena03Stats.params', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='my_rank', full_name='CampusArena03Stats.my_rank', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='my_score', full_name='CampusArena03Stats.my_score', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='my_position', full_name='CampusArena03Stats.my_position', index=4,
      number=5, type=13, cpp_type=3, label=1,
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
  serialized_start=703,
  serialized_end=848,
)


_CAMPUSARENA03STATSITEM = descriptor.Descriptor(
  name='CampusArena03StatsItem',
  full_name='CampusArena03StatsItem',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='id', full_name='CampusArena03StatsItem.id', index=0,
      number=11, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='name', full_name='CampusArena03StatsItem.name', index=1,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='rank', full_name='CampusArena03StatsItem.rank', index=2,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='score', full_name='CampusArena03StatsItem.score', index=3,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='level', full_name='CampusArena03StatsItem.level', index=4,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='win', full_name='CampusArena03StatsItem.win', index=5,
      number=6, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='early_quit', full_name='CampusArena03StatsItem.early_quit', index=6,
      number=7, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='total', full_name='CampusArena03StatsItem.total', index=7,
      number=8, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='win_rate', full_name='CampusArena03StatsItem.win_rate', index=8,
      number=9, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='doublekill', full_name='CampusArena03StatsItem.doublekill', index=9,
      number=13, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='triplekill', full_name='CampusArena03StatsItem.triplekill', index=10,
      number=14, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='assistance', full_name='CampusArena03StatsItem.assistance', index=11,
      number=15, type=13, cpp_type=3, label=1,
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
  serialized_start=851,
  serialized_end=1071,
)


_CAMPUSARENA03HOME = descriptor.Descriptor(
  name='CampusArena03Home',
  full_name='CampusArena03Home',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='bulletins', full_name='CampusArena03Home.bulletins', index=0,
      number=4, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='scStats', full_name='CampusArena03Home.scStats', index=1,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='war3Stats', full_name='CampusArena03Home.war3Stats', index=2,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='dotaStats', full_name='CampusArena03Home.dotaStats', index=3,
      number=7, type=11, cpp_type=10, label=3,
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
  serialized_start=1074,
  serialized_end=1242,
)

import res_activity_pb2
import res_clan_pb2
import res_user_pb2
import res_game_pb2
import res_listbase_pb2

_CAMPUSARENAGET.fields_by_name['clan'].message_type = res_clan_pb2._CLANGETRESPONSE
_CAMPUSARENAGET.fields_by_name['maps'].message_type = res_game_pb2._MAP
_CAMPUSARENAGROUPING.fields_by_name['users'].message_type = res_user_pb2._USERMODEL
_CAMPUSARENAGROUPINGLIST.fields_by_name['items'].message_type = _CAMPUSARENAGROUPING
_CAMPUSARENA03LIST.fields_by_name['items'].message_type = _CAMPUSARENA03LISTITEM
_CAMPUSARENA03STATS.fields_by_name['items'].message_type = _CAMPUSARENA03STATSITEM
_CAMPUSARENA03STATS.fields_by_name['params'].message_type = res_listbase_pb2._LISTPARAMS
_CAMPUSARENA03HOME.fields_by_name['scStats'].message_type = _CAMPUSARENA03STATSITEM
_CAMPUSARENA03HOME.fields_by_name['war3Stats'].message_type = _CAMPUSARENA03STATSITEM
_CAMPUSARENA03HOME.fields_by_name['dotaStats'].message_type = _CAMPUSARENA03STATSITEM

class CampusArenaGet(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _CAMPUSARENAGET
  
  # @@protoc_insertion_point(class_scope:CampusArenaGet)

class CampusArenaGrouping(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _CAMPUSARENAGROUPING
  
  # @@protoc_insertion_point(class_scope:CampusArenaGrouping)

class CampusArenaGroupingList(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _CAMPUSARENAGROUPINGLIST
  
  # @@protoc_insertion_point(class_scope:CampusArenaGroupingList)

class CampusArena03List(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _CAMPUSARENA03LIST
  
  # @@protoc_insertion_point(class_scope:CampusArena03List)

class CampusArena03ListItem(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _CAMPUSARENA03LISTITEM
  
  # @@protoc_insertion_point(class_scope:CampusArena03ListItem)

class CampusArena03Stats(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _CAMPUSARENA03STATS
  
  # @@protoc_insertion_point(class_scope:CampusArena03Stats)

class CampusArena03StatsItem(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _CAMPUSARENA03STATSITEM
  
  # @@protoc_insertion_point(class_scope:CampusArena03StatsItem)

class CampusArena03Home(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _CAMPUSARENA03HOME
  
  # @@protoc_insertion_point(class_scope:CampusArena03Home)

# @@protoc_insertion_point(module_scope)