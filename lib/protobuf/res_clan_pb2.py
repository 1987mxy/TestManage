# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)


DESCRIPTOR = descriptor.FileDescriptor(
  name='res_clan.proto',
  package='',
  serialized_pb='\n\x0eres_clan.proto\x1a\x12res_activity.proto\x1a\x12res_listbase.proto\"\x88\x01\n\x0f\x43lanGetResponse\x12\n\n\x02id\x18\x01 \x02(\r\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0c\n\x04logo\x18\x03 \x01(\t\x12\x11\n\tparent_id\x18\x04 \x01(\r\x12\x10\n\x08\x62ulletin\x18\x05 \x01(\t\x12(\n\nactivities\x18\x06 \x03(\x0b\x32\x14.ActivityGetResponse\"P\n\x10\x43lanListResponse\x12\x1f\n\x05\x63lans\x18\x01 \x03(\x0b\x32\x10.ClanGetResponse\x12\x1b\n\x06params\x18\x02 \x01(\x0b\x32\x0b.ListParamsB\x12\n\x0eproto.responseH\x02')




_CLANGETRESPONSE = descriptor.Descriptor(
  name='ClanGetResponse',
  full_name='ClanGetResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='id', full_name='ClanGetResponse.id', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='name', full_name='ClanGetResponse.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='logo', full_name='ClanGetResponse.logo', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='parent_id', full_name='ClanGetResponse.parent_id', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='bulletin', full_name='ClanGetResponse.bulletin', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='activities', full_name='ClanGetResponse.activities', index=5,
      number=6, type=11, cpp_type=10, label=3,
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
  serialized_start=59,
  serialized_end=195,
)


_CLANLISTRESPONSE = descriptor.Descriptor(
  name='ClanListResponse',
  full_name='ClanListResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='clans', full_name='ClanListResponse.clans', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='params', full_name='ClanListResponse.params', index=1,
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
  serialized_start=197,
  serialized_end=277,
)

import res_activity_pb2
import res_listbase_pb2

_CLANGETRESPONSE.fields_by_name['activities'].message_type = res_activity_pb2._ACTIVITYGETRESPONSE
_CLANLISTRESPONSE.fields_by_name['clans'].message_type = _CLANGETRESPONSE
_CLANLISTRESPONSE.fields_by_name['params'].message_type = res_listbase_pb2._LISTPARAMS

class ClanGetResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _CLANGETRESPONSE
  
  # @@protoc_insertion_point(class_scope:ClanGetResponse)

class ClanListResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _CLANLISTRESPONSE
  
  # @@protoc_insertion_point(class_scope:ClanListResponse)

# @@protoc_insertion_point(module_scope)