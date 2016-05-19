import collections
import copy
import json
import struct


_DATA_TYPES = {}
_DATA_TYPES['float'] = 'f'
_DATA_TYPES['double'] = 'd'
_DATA_TYPES['int8'] = 'b'
_DATA_TYPES['uint8'] = 'B'
_DATA_TYPES['int16'] = 'h'
_DATA_TYPES['uint16'] = 'H'
_DATA_TYPES['int32'] = 'i'
_DATA_TYPES['uint32'] = 'I'
_DATA_TYPES['int64'] = 'q'
_DATA_TYPES['uin64'] = 'Q'
_DATA_TYPES['json'] = 'json'

_TABLES = {}
_TABLE_LIST = []


def to_bytes(table):
    tabledef = table._tabledef
    data = []
    json_data = []

    for key, value in table._data.items():
        d = value[0]
        v = value[1]

        if v is None:
            print("ERROR missing required data: {}".format(key))
            return None

        if d == 'json':
            json_data.append([key, v])
        else:
            data.append(v)

    buff = struct.pack(tabledef._formatstring, tabledef._id, *data)
    if len(json_data):
        buff += bytes(json.dumps(json_data), 'UTF-8')

    return buff


def to_table(buff):
    # Read the first 2 bytes to determine table ID
    table_id = struct.unpack('!H', buff[:2])[0]
    tabledef = _TABLE_LIST[table_id]

    size = struct.calcsize(tabledef._formatstring)
    data = struct.unpack(tabledef._formatstring, buff[:size])

    table = Table(tabledef)

    i = 1  # table ID is still in here, so we skip
    for key, value in tabledef._datatypes.items():
        d = value[0]

        if d == 'json':
            # Check for json at the end
            continue
        else:
            v = data[i]
            table.set(key, v)

        i += 1

    if len(buff) > size:
        # There is json
        json_data = json.loads(bytes.decode(buff[size:], 'UTF-8'))
        for key, value in json_data:
            table.set(key, value)

    return table


class TableDef:
    def __init__(self, name):
        if _TABLES.get(name, None) is not None:
            print("WARNING table already defined: {}".format(name))

        self._id = len(_TABLE_LIST)
        self._datatypes = collections.OrderedDict()
        self._formatstring = '!H'

        _TABLES[name] = self
        _TABLE_LIST.append(self)

    def define(self, datatype, key, default=None):
        d = self._datatypes

        if d.get(key, None) is not None:
            print("ERROR key already defined: {}".format(key))
            return

        if _DATA_TYPES.get(datatype, None) is None:
            print ("ERROR datatype not defined: {}".format(datatype))
            return

        d[key] = [_DATA_TYPES[datatype], default]
        self._datatypes = collections.OrderedDict(sorted(d.items(),
                key=lambda t: t[0]))

        # Rebuild the format string
        formatstring = '!H'

        for value in self._datatypes.values():
            d = value[0]
            if d != 'json':  # json is appened to the end of the buffer
                formatstring += d

        self._formatstring = formatstring


class Table:
    def __init__(self, tabledef):
        if type(tabledef) is str:
            if tabledef not in _TABLES:
                print("ERROR table not defined: {}".format(tabledef))
                return
            tabledef = _TABLES[tabledef]

        self._data = copy.deepcopy(tabledef._datatypes)
        self._tabledef = tabledef  # For referencing ID and format string

    def set(self, key, value):
        if key in self._data:
            self._data[key][1] = value
        else:
            print("WARNING key not defined: {}".format(key))

    def get(self, key):
        value = self._data.get(key, None)
        if value is not None:
            value = value[1]
        return value