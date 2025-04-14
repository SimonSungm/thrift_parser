#!/usr/bin/python3
from thrift_parser import parse_file, thrift_definitions
import pprint

parse_file('example.thrift')

pprint.pprint(thrift_definitions)
