# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)


DESCRIPTOR = descriptor.FileDescriptor(
  name='con_hotkeyconfig.proto',
  package='',
  serialized_pb='\n\x16\x63on_hotkeyconfig.proto\"\xf1\x01\n\x0cHotKeyConfig\x12%\n\x07IGM_Key\x18\x01 \x01(\x0b\x32\x14.HotKeyConfig.HotKey\x12%\n\x07hotkeys\x18\x02 \x03(\x0b\x32\x14.HotKeyConfig.HotKey\x12\x14\n\x0cshowLifeLine\x18\x03 \x01(\x05\x12\x15\n\rwinKeyEnabled\x18\x04 \x01(\x08\x1a\x66\n\x06HotKey\x12\x13\n\x0boriginalKey\x18\x01 \x02(\x05\x12\x11\n\tmodifyKey\x18\x02 \x01(\x05\x12\x11\n\tshiftDown\x18\x03 \x01(\x05\x12\x10\n\x08\x63trlDown\x18\x04 \x01(\x05\x12\x0f\n\x07\x61ltDown\x18\x05 \x01(\x05\x42\x10\n\x0cproto.configH\x02')




_HOTKEYCONFIG_HOTKEY = descriptor.Descriptor(
  name='HotKey',
  full_name='HotKeyConfig.HotKey',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='originalKey', full_name='HotKeyConfig.HotKey.originalKey', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='modifyKey', full_name='HotKeyConfig.HotKey.modifyKey', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='shiftDown', full_name='HotKeyConfig.HotKey.shiftDown', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='ctrlDown', full_name='HotKeyConfig.HotKey.ctrlDown', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='altDown', full_name='HotKeyConfig.HotKey.altDown', index=4,
      number=5, type=5, cpp_type=1, label=1,
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
  serialized_start=166,
  serialized_end=268,
)

_HOTKEYCONFIG = descriptor.Descriptor(
  name='HotKeyConfig',
  full_name='HotKeyConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='IGM_Key', full_name='HotKeyConfig.IGM_Key', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='hotkeys', full_name='HotKeyConfig.hotkeys', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='showLifeLine', full_name='HotKeyConfig.showLifeLine', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='winKeyEnabled', full_name='HotKeyConfig.winKeyEnabled', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_HOTKEYCONFIG_HOTKEY, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=27,
  serialized_end=268,
)


_HOTKEYCONFIG_HOTKEY.containing_type = _HOTKEYCONFIG;
_HOTKEYCONFIG.fields_by_name['IGM_Key'].message_type = _HOTKEYCONFIG_HOTKEY
_HOTKEYCONFIG.fields_by_name['hotkeys'].message_type = _HOTKEYCONFIG_HOTKEY

class HotKeyConfig(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  
  class HotKey(message.Message):
    __metaclass__ = reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _HOTKEYCONFIG_HOTKEY
    
    # @@protoc_insertion_point(class_scope:HotKeyConfig.HotKey)
  DESCRIPTOR = _HOTKEYCONFIG
  
  # @@protoc_insertion_point(class_scope:HotKeyConfig)

# @@protoc_insertion_point(module_scope)
