# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)


DESCRIPTOR = descriptor.FileDescriptor(
  name='msg_party.proto',
  package='',
  serialized_pb='\n\x0fmsg_party.proto\x1a\x0fres_party.proto\"@\n\x0bPartyJoined\x12\x0f\n\x07partyID\x18\x01 \x01(\r\x12 \n\x05party\x18\x02 \x01(\x0b\x32\x11.PartyGetResponse\"\x1e\n\x0bPartyLeaved\x12\x0f\n\x07partyID\x18\x01 \x01(\r\"n\n\x0fUserJoinedParty\x12\x0f\n\x07partyID\x18\x01 \x01(\r\x12\x0e\n\x06userID\x18\x02 \x01(\r\x12\x10\n\x08userName\x18\x03 \x01(\t\x12\x14\n\x0cuserPortrait\x18\x04 \x01(\t\x12\x12\n\nuserStatus\x18\x05 \x01(\t\"2\n\x0fUserLeavedParty\x12\x0f\n\x07partyID\x18\x01 \x01(\r\x12\x0e\n\x06userID\x18\x02 \x01(\r\"O\n\x18PartyMemberStatusUpdated\x12\x0f\n\x07partyID\x18\x01 \x01(\r\x12\x0e\n\x06userID\x18\x02 \x01(\r\x12\x12\n\nuserStatus\x18\x03 \x01(\t\"v\n\x0fPartyInvitation\x12\x10\n\x08leaderID\x18\x01 \x01(\r\x12\x12\n\nleaderName\x18\x02 \x01(\t\x12\x16\n\x0eleaderPortrait\x18\x03 \x01(\t\x12\x0f\n\x07partyID\x18\x04 \x01(\r\x12\x14\n\x0ctargetUserID\x18\x05 \x01(\r\";\n\x17PartyInvitationDeclined\x12\x0e\n\x06userID\x18\x01 \x01(\r\x12\x10\n\x08userName\x18\x02 \x01(\t\"7\n\x12PartyLeaderChanged\x12\x0f\n\x07partyID\x18\x01 \x01(\r\x12\x10\n\x08leaderID\x18\x02 \x01(\rB\r\n\tproto.msgH\x02')




_PARTYJOINED = descriptor.Descriptor(
  name='PartyJoined',
  full_name='PartyJoined',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='partyID', full_name='PartyJoined.partyID', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='party', full_name='PartyJoined.party', index=1,
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
  serialized_start=36,
  serialized_end=100,
)


_PARTYLEAVED = descriptor.Descriptor(
  name='PartyLeaved',
  full_name='PartyLeaved',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='partyID', full_name='PartyLeaved.partyID', index=0,
      number=1, type=13, cpp_type=3, label=1,
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
  serialized_start=102,
  serialized_end=132,
)


_USERJOINEDPARTY = descriptor.Descriptor(
  name='UserJoinedParty',
  full_name='UserJoinedParty',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='partyID', full_name='UserJoinedParty.partyID', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='userID', full_name='UserJoinedParty.userID', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='userName', full_name='UserJoinedParty.userName', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='userPortrait', full_name='UserJoinedParty.userPortrait', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='userStatus', full_name='UserJoinedParty.userStatus', index=4,
      number=5, type=9, cpp_type=9, label=1,
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
  serialized_start=134,
  serialized_end=244,
)


_USERLEAVEDPARTY = descriptor.Descriptor(
  name='UserLeavedParty',
  full_name='UserLeavedParty',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='partyID', full_name='UserLeavedParty.partyID', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='userID', full_name='UserLeavedParty.userID', index=1,
      number=2, type=13, cpp_type=3, label=1,
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
  serialized_start=246,
  serialized_end=296,
)


_PARTYMEMBERSTATUSUPDATED = descriptor.Descriptor(
  name='PartyMemberStatusUpdated',
  full_name='PartyMemberStatusUpdated',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='partyID', full_name='PartyMemberStatusUpdated.partyID', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='userID', full_name='PartyMemberStatusUpdated.userID', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='userStatus', full_name='PartyMemberStatusUpdated.userStatus', index=2,
      number=3, type=9, cpp_type=9, label=1,
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
  serialized_start=298,
  serialized_end=377,
)


_PARTYINVITATION = descriptor.Descriptor(
  name='PartyInvitation',
  full_name='PartyInvitation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='leaderID', full_name='PartyInvitation.leaderID', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='leaderName', full_name='PartyInvitation.leaderName', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='leaderPortrait', full_name='PartyInvitation.leaderPortrait', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='partyID', full_name='PartyInvitation.partyID', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='targetUserID', full_name='PartyInvitation.targetUserID', index=4,
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
  serialized_start=379,
  serialized_end=497,
)


_PARTYINVITATIONDECLINED = descriptor.Descriptor(
  name='PartyInvitationDeclined',
  full_name='PartyInvitationDeclined',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='userID', full_name='PartyInvitationDeclined.userID', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='userName', full_name='PartyInvitationDeclined.userName', index=1,
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
  serialized_start=499,
  serialized_end=558,
)


_PARTYLEADERCHANGED = descriptor.Descriptor(
  name='PartyLeaderChanged',
  full_name='PartyLeaderChanged',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='partyID', full_name='PartyLeaderChanged.partyID', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='leaderID', full_name='PartyLeaderChanged.leaderID', index=1,
      number=2, type=13, cpp_type=3, label=1,
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
  serialized_start=560,
  serialized_end=615,
)

import res_party_pb2

_PARTYJOINED.fields_by_name['party'].message_type = res_party_pb2._PARTYGETRESPONSE

class PartyJoined(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _PARTYJOINED
  
  # @@protoc_insertion_point(class_scope:PartyJoined)

class PartyLeaved(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _PARTYLEAVED
  
  # @@protoc_insertion_point(class_scope:PartyLeaved)

class UserJoinedParty(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _USERJOINEDPARTY
  
  # @@protoc_insertion_point(class_scope:UserJoinedParty)

class UserLeavedParty(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _USERLEAVEDPARTY
  
  # @@protoc_insertion_point(class_scope:UserLeavedParty)

class PartyMemberStatusUpdated(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _PARTYMEMBERSTATUSUPDATED
  
  # @@protoc_insertion_point(class_scope:PartyMemberStatusUpdated)

class PartyInvitation(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _PARTYINVITATION
  
  # @@protoc_insertion_point(class_scope:PartyInvitation)

class PartyInvitationDeclined(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _PARTYINVITATIONDECLINED
  
  # @@protoc_insertion_point(class_scope:PartyInvitationDeclined)

class PartyLeaderChanged(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _PARTYLEADERCHANGED
  
  # @@protoc_insertion_point(class_scope:PartyLeaderChanged)

# @@protoc_insertion_point(module_scope)