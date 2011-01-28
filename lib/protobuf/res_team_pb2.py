# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)


DESCRIPTOR = descriptor.FileDescriptor(
  name='res_team.proto',
  package='',
  serialized_pb='\n\x0eres_team.proto\x1a\x0eres_clan.proto\x1a\x0eres_user.proto\x1a\x12res_listbase.proto\x1a\rres_tag.proto\"\xed\x02\n\x0fTeamGetResponse\x12\x0c\n\x04uuid\x18\x01 \x02(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0e\n\x06prefix\x18\x03 \x01(\t\x12\x0c\n\x04logo\x18\x04 \x01(\t\x12\x0e\n\x06slogan\x18\x05 \x01(\t\x12\x1b\n\x07members\x18\x07 \x03(\x0b\x32\n.UserModel\x12\x10\n\x08leaderID\x18\x08 \x01(\r\x12\x12\n\nassistants\x18\t \x03(\r\x12 \n\tbulletins\x18\n \x03(\x0b\x32\r.TeamBulletin\x12\x1c\n\x14\x63urrent_member_count\x18\x0b \x01(\r\x12\x18\n\x10max_member_count\x18\x0c \x01(\r\x12\r\n\x05lg_id\x18\r \x01(\r\x12\x0f\n\x07lg_name\x18\x0e \x01(\t\x12\r\n\x05order\x18\x0f \x01(\r\x12\r\n\x05score\x18\x10 \x01(\r\x12\x0c\n\x04rank\x18\x11 \x01(\r\x12\x12\n\x04tags\x18\x12 \x03(\x0b\x32\x04.Tag\x12\x13\n\x0bhas_applied\x18\x13 \x01(\x08\"P\n\x10TeamListResponse\x12\x1f\n\x05teams\x18\x01 \x03(\x0b\x32\x10.TeamGetResponse\x12\x1b\n\x06params\x18\x02 \x01(\x0b\x32\x0b.ListParams\"2\n\x0cTeamBulletin\x12\x0f\n\x07\x63ontent\x18\x02 \x02(\t\x12\x11\n\ttimestamp\x18\x03 \x02(\r\"@\n\x12MyTeamApplications\x12*\n\x10teamApplications\x18\x01 \x03(\x0b\x32\x10.TeamApplication\"A\n\x0fTeamApplication\x12\x1e\n\x04team\x18\x01 \x02(\x0b\x32\x10.TeamGetResponse\x12\x0e\n\x06\x61nswer\x18\x02 \x02(\tB\x12\n\x0eproto.responseH\x02')




_TEAMGETRESPONSE = descriptor.Descriptor(
  name='TeamGetResponse',
  full_name='TeamGetResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='uuid', full_name='TeamGetResponse.uuid', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='name', full_name='TeamGetResponse.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='prefix', full_name='TeamGetResponse.prefix', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='logo', full_name='TeamGetResponse.logo', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='slogan', full_name='TeamGetResponse.slogan', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='members', full_name='TeamGetResponse.members', index=5,
      number=7, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='leaderID', full_name='TeamGetResponse.leaderID', index=6,
      number=8, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='assistants', full_name='TeamGetResponse.assistants', index=7,
      number=9, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='bulletins', full_name='TeamGetResponse.bulletins', index=8,
      number=10, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='current_member_count', full_name='TeamGetResponse.current_member_count', index=9,
      number=11, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='max_member_count', full_name='TeamGetResponse.max_member_count', index=10,
      number=12, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='lg_id', full_name='TeamGetResponse.lg_id', index=11,
      number=13, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='lg_name', full_name='TeamGetResponse.lg_name', index=12,
      number=14, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='order', full_name='TeamGetResponse.order', index=13,
      number=15, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='score', full_name='TeamGetResponse.score', index=14,
      number=16, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='rank', full_name='TeamGetResponse.rank', index=15,
      number=17, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='tags', full_name='TeamGetResponse.tags', index=16,
      number=18, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='has_applied', full_name='TeamGetResponse.has_applied', index=17,
      number=19, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  serialized_start=86,
  serialized_end=451,
)


_TEAMLISTRESPONSE = descriptor.Descriptor(
  name='TeamListResponse',
  full_name='TeamListResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='teams', full_name='TeamListResponse.teams', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='params', full_name='TeamListResponse.params', index=1,
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
  serialized_start=453,
  serialized_end=533,
)


_TEAMBULLETIN = descriptor.Descriptor(
  name='TeamBulletin',
  full_name='TeamBulletin',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='content', full_name='TeamBulletin.content', index=0,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='timestamp', full_name='TeamBulletin.timestamp', index=1,
      number=3, type=13, cpp_type=3, label=2,
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
  serialized_start=535,
  serialized_end=585,
)


_MYTEAMAPPLICATIONS = descriptor.Descriptor(
  name='MyTeamApplications',
  full_name='MyTeamApplications',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='teamApplications', full_name='MyTeamApplications.teamApplications', index=0,
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
  serialized_start=587,
  serialized_end=651,
)


_TEAMAPPLICATION = descriptor.Descriptor(
  name='TeamApplication',
  full_name='TeamApplication',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='team', full_name='TeamApplication.team', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='answer', full_name='TeamApplication.answer', index=1,
      number=2, type=9, cpp_type=9, label=2,
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
  serialized_start=653,
  serialized_end=718,
)

import res_clan_pb2
import res_user_pb2
import res_listbase_pb2
import res_tag_pb2

_TEAMGETRESPONSE.fields_by_name['members'].message_type = res_user_pb2._USERMODEL
_TEAMGETRESPONSE.fields_by_name['bulletins'].message_type = _TEAMBULLETIN
_TEAMGETRESPONSE.fields_by_name['tags'].message_type = res_tag_pb2._TAG
_TEAMLISTRESPONSE.fields_by_name['teams'].message_type = _TEAMGETRESPONSE
_TEAMLISTRESPONSE.fields_by_name['params'].message_type = res_listbase_pb2._LISTPARAMS
_MYTEAMAPPLICATIONS.fields_by_name['teamApplications'].message_type = _TEAMAPPLICATION
_TEAMAPPLICATION.fields_by_name['team'].message_type = _TEAMGETRESPONSE

class TeamGetResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _TEAMGETRESPONSE
  
  # @@protoc_insertion_point(class_scope:TeamGetResponse)

class TeamListResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _TEAMLISTRESPONSE
  
  # @@protoc_insertion_point(class_scope:TeamListResponse)

class TeamBulletin(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _TEAMBULLETIN
  
  # @@protoc_insertion_point(class_scope:TeamBulletin)

class MyTeamApplications(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _MYTEAMAPPLICATIONS
  
  # @@protoc_insertion_point(class_scope:MyTeamApplications)

class TeamApplication(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _TEAMAPPLICATION
  
  # @@protoc_insertion_point(class_scope:TeamApplication)

# @@protoc_insertion_point(module_scope)