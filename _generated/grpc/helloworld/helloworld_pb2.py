# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: helloworld/helloworld.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1bhelloworld/helloworld.proto\x12\nhelloworld\"\x1c\n\x0cHelloRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\" \n\rHelloResponse\x12\x0f\n\x07message\x18\x01 \x01(\t2L\n\x07Greeter\x12\x41\n\x08SayHello\x12\x18.helloworld.HelloRequest\x1a\x19.helloworld.HelloResponse\"\x00\x42\x15Z\x13idl/grpc/helloworldb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'helloworld.helloworld_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z\023idl/grpc/helloworld'
  _HELLOREQUEST._serialized_start=43
  _HELLOREQUEST._serialized_end=71
  _HELLORESPONSE._serialized_start=73
  _HELLORESPONSE._serialized_end=105
  _GREETER._serialized_start=107
  _GREETER._serialized_end=183
# @@protoc_insertion_point(module_scope)