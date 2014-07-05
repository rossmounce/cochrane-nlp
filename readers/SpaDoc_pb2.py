# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: SpaDoc.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)




DESCRIPTOR = _descriptor.FileDescriptor(
  name='SpaDoc.proto',
  package='ebm.spa',
  serialized_pb='\n\x0cSpaDoc.proto\x12\x07\x65\x62m.spa\"\xdc\x06\n\x08\x44ocument\x12\x0c\n\x04text\x18\x01 \x02(\t\x12\x0b\n\x03uri\x18\x02 \x01(\t\x12%\n\x05nodes\x18\x03 \x03(\x0b\x32\x16.ebm.spa.Document.Node\x12%\n\x05pages\x18\x04 \x03(\x0b\x32\x16.ebm.spa.Document.Page\x12(\n\x05words\x18\x05 \x03(\x0b\x32\x19.ebm.spa.Document.Mapping\x12,\n\tsentences\x18\x06 \x03(\x0b\x32\x19.ebm.spa.Document.Mapping\x12\x30\n\nmarginalia\x18\x07 \x03(\x0b\x32\x1c.ebm.spa.Document.Marginalis\x1a(\n\x08Interval\x12\r\n\x05upper\x18\x01 \x02(\r\x12\r\n\x05lower\x18\x02 \x02(\r\x1a\\\n\x04Node\x12\x12\n\npage_index\x18\x01 \x02(\r\x12\x12\n\nnode_index\x18\x02 \x02(\r\x12,\n\x08interval\x18\x03 \x02(\x0b\x32\x1a.ebm.spa.Document.Interval\x1a&\n\x04Page\x12\x0e\n\x06length\x18\x01 \x02(\r\x12\x0e\n\x06offset\x18\x02 \x02(\r\x1a\x88\x01\n\x07Mapping\x12\x33\n\x08\x65lements\x18\x01 \x03(\x0b\x32!.ebm.spa.Document.Mapping.Element\x1aH\n\x07\x45lement\x12\x12\n\nnode_index\x18\x01 \x02(\r\x12)\n\x05range\x18\x02 \x02(\x0b\x32\x1a.ebm.spa.Document.Interval\x1a\xa1\x02\n\nMarginalis\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\r\n\x05title\x18\x02 \x02(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12<\n\x0b\x61nnotations\x18\x04 \x03(\x0b\x32\'.ebm.spa.Document.Marginalis.Annotation\x1a\xa2\x01\n\nAnnotation\x12\x0b\n\x03uri\x18\x01 \x01(\t\x12\r\n\x05label\x18\x02 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\t\x12@\n\x07mapping\x18\x04 \x01(\x0b\x32/.ebm.spa.Document.Marginalis.Annotation.Mapping\x1a%\n\x07Mapping\x12\x0b\n\x03key\x18\x01 \x02(\t\x12\r\n\x05index\x18\x02 \x02(\r')




_DOCUMENT_INTERVAL = _descriptor.Descriptor(
  name='Interval',
  full_name='ebm.spa.Document.Interval',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='upper', full_name='ebm.spa.Document.Interval.upper', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='lower', full_name='ebm.spa.Document.Interval.lower', index=1,
      number=2, type=13, cpp_type=3, label=2,
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
  serialized_start=281,
  serialized_end=321,
)

_DOCUMENT_NODE = _descriptor.Descriptor(
  name='Node',
  full_name='ebm.spa.Document.Node',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='page_index', full_name='ebm.spa.Document.Node.page_index', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='node_index', full_name='ebm.spa.Document.Node.node_index', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='interval', full_name='ebm.spa.Document.Node.interval', index=2,
      number=3, type=11, cpp_type=10, label=2,
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
  serialized_start=323,
  serialized_end=415,
)

_DOCUMENT_PAGE = _descriptor.Descriptor(
  name='Page',
  full_name='ebm.spa.Document.Page',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='length', full_name='ebm.spa.Document.Page.length', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='offset', full_name='ebm.spa.Document.Page.offset', index=1,
      number=2, type=13, cpp_type=3, label=2,
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
  serialized_start=417,
  serialized_end=455,
)

_DOCUMENT_MAPPING_ELEMENT = _descriptor.Descriptor(
  name='Element',
  full_name='ebm.spa.Document.Mapping.Element',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='node_index', full_name='ebm.spa.Document.Mapping.Element.node_index', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='range', full_name='ebm.spa.Document.Mapping.Element.range', index=1,
      number=2, type=11, cpp_type=10, label=2,
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
  serialized_start=522,
  serialized_end=594,
)

_DOCUMENT_MAPPING = _descriptor.Descriptor(
  name='Mapping',
  full_name='ebm.spa.Document.Mapping',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='elements', full_name='ebm.spa.Document.Mapping.elements', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_DOCUMENT_MAPPING_ELEMENT, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=458,
  serialized_end=594,
)

_DOCUMENT_MARGINALIS_ANNOTATION_MAPPING = _descriptor.Descriptor(
  name='Mapping',
  full_name='ebm.spa.Document.Marginalis.Annotation.Mapping',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='ebm.spa.Document.Marginalis.Annotation.Mapping.key', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='index', full_name='ebm.spa.Document.Marginalis.Annotation.Mapping.index', index=1,
      number=2, type=13, cpp_type=3, label=2,
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
  serialized_start=849,
  serialized_end=886,
)

_DOCUMENT_MARGINALIS_ANNOTATION = _descriptor.Descriptor(
  name='Annotation',
  full_name='ebm.spa.Document.Marginalis.Annotation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='uri', full_name='ebm.spa.Document.Marginalis.Annotation.uri', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='label', full_name='ebm.spa.Document.Marginalis.Annotation.label', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='content', full_name='ebm.spa.Document.Marginalis.Annotation.content', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='mapping', full_name='ebm.spa.Document.Marginalis.Annotation.mapping', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_DOCUMENT_MARGINALIS_ANNOTATION_MAPPING, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=724,
  serialized_end=886,
)

_DOCUMENT_MARGINALIS = _descriptor.Descriptor(
  name='Marginalis',
  full_name='ebm.spa.Document.Marginalis',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='ebm.spa.Document.Marginalis.type', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='title', full_name='ebm.spa.Document.Marginalis.title', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='description', full_name='ebm.spa.Document.Marginalis.description', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='annotations', full_name='ebm.spa.Document.Marginalis.annotations', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_DOCUMENT_MARGINALIS_ANNOTATION, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=597,
  serialized_end=886,
)

_DOCUMENT = _descriptor.Descriptor(
  name='Document',
  full_name='ebm.spa.Document',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='text', full_name='ebm.spa.Document.text', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='uri', full_name='ebm.spa.Document.uri', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='nodes', full_name='ebm.spa.Document.nodes', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='pages', full_name='ebm.spa.Document.pages', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='words', full_name='ebm.spa.Document.words', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sentences', full_name='ebm.spa.Document.sentences', index=5,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='marginalia', full_name='ebm.spa.Document.marginalia', index=6,
      number=7, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_DOCUMENT_INTERVAL, _DOCUMENT_NODE, _DOCUMENT_PAGE, _DOCUMENT_MAPPING, _DOCUMENT_MARGINALIS, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=26,
  serialized_end=886,
)

_DOCUMENT_INTERVAL.containing_type = _DOCUMENT;
_DOCUMENT_NODE.fields_by_name['interval'].message_type = _DOCUMENT_INTERVAL
_DOCUMENT_NODE.containing_type = _DOCUMENT;
_DOCUMENT_PAGE.containing_type = _DOCUMENT;
_DOCUMENT_MAPPING_ELEMENT.fields_by_name['range'].message_type = _DOCUMENT_INTERVAL
_DOCUMENT_MAPPING_ELEMENT.containing_type = _DOCUMENT_MAPPING;
_DOCUMENT_MAPPING.fields_by_name['elements'].message_type = _DOCUMENT_MAPPING_ELEMENT
_DOCUMENT_MAPPING.containing_type = _DOCUMENT;
_DOCUMENT_MARGINALIS_ANNOTATION_MAPPING.containing_type = _DOCUMENT_MARGINALIS_ANNOTATION;
_DOCUMENT_MARGINALIS_ANNOTATION.fields_by_name['mapping'].message_type = _DOCUMENT_MARGINALIS_ANNOTATION_MAPPING
_DOCUMENT_MARGINALIS_ANNOTATION.containing_type = _DOCUMENT_MARGINALIS;
_DOCUMENT_MARGINALIS.fields_by_name['annotations'].message_type = _DOCUMENT_MARGINALIS_ANNOTATION
_DOCUMENT_MARGINALIS.containing_type = _DOCUMENT;
_DOCUMENT.fields_by_name['nodes'].message_type = _DOCUMENT_NODE
_DOCUMENT.fields_by_name['pages'].message_type = _DOCUMENT_PAGE
_DOCUMENT.fields_by_name['words'].message_type = _DOCUMENT_MAPPING
_DOCUMENT.fields_by_name['sentences'].message_type = _DOCUMENT_MAPPING
_DOCUMENT.fields_by_name['marginalia'].message_type = _DOCUMENT_MARGINALIS
DESCRIPTOR.message_types_by_name['Document'] = _DOCUMENT

class Document(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType

  class Interval(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _DOCUMENT_INTERVAL

    # @@protoc_insertion_point(class_scope:ebm.spa.Document.Interval)

  class Node(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _DOCUMENT_NODE

    # @@protoc_insertion_point(class_scope:ebm.spa.Document.Node)

  class Page(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _DOCUMENT_PAGE

    # @@protoc_insertion_point(class_scope:ebm.spa.Document.Page)

  class Mapping(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType

    class Element(_message.Message):
      __metaclass__ = _reflection.GeneratedProtocolMessageType
      DESCRIPTOR = _DOCUMENT_MAPPING_ELEMENT

      # @@protoc_insertion_point(class_scope:ebm.spa.Document.Mapping.Element)
    DESCRIPTOR = _DOCUMENT_MAPPING

    # @@protoc_insertion_point(class_scope:ebm.spa.Document.Mapping)

  class Marginalis(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType

    class Annotation(_message.Message):
      __metaclass__ = _reflection.GeneratedProtocolMessageType

      class Mapping(_message.Message):
        __metaclass__ = _reflection.GeneratedProtocolMessageType
        DESCRIPTOR = _DOCUMENT_MARGINALIS_ANNOTATION_MAPPING

        # @@protoc_insertion_point(class_scope:ebm.spa.Document.Marginalis.Annotation.Mapping)
      DESCRIPTOR = _DOCUMENT_MARGINALIS_ANNOTATION

      # @@protoc_insertion_point(class_scope:ebm.spa.Document.Marginalis.Annotation)
    DESCRIPTOR = _DOCUMENT_MARGINALIS

    # @@protoc_insertion_point(class_scope:ebm.spa.Document.Marginalis)
  DESCRIPTOR = _DOCUMENT

  # @@protoc_insertion_point(class_scope:ebm.spa.Document)


# @@protoc_insertion_point(module_scope)
