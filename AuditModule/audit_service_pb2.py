# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: audit_service.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13\x61udit_service.proto\x12\napi_getway\"\x81\x01\n\x0c\x41uditRequest\x12\x0c\n\x04uuid\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\x0c\n\x04mode\x18\x04 \x01(\t\x12\x0f\n\x07success\x18\x05 \x01(\t\x12!\n\x06params\x18\x06 \x03(\x0b\x32\x11.api_getway.Param\"*\n\x05Param\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\"5\n\rAuditResponse\x12\x0c\n\x04uuid\x18\x01 \x01(\t\x12\x16\n\x0estatusResponse\x18\x02 \x01(\t2Q\n\tMyService\x12\x44\n\x0b\x43reateAudit\x12\x18.api_getway.AuditRequest\x1a\x19.api_getway.AuditResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'audit_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_AUDITREQUEST']._serialized_start=36
  _globals['_AUDITREQUEST']._serialized_end=165
  _globals['_PARAM']._serialized_start=167
  _globals['_PARAM']._serialized_end=209
  _globals['_AUDITRESPONSE']._serialized_start=211
  _globals['_AUDITRESPONSE']._serialized_end=264
  _globals['_MYSERVICE']._serialized_start=266
  _globals['_MYSERVICE']._serialized_end=347
# @@protoc_insertion_point(module_scope)