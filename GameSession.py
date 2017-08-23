import struct
import gzip
import datetime


class GameSession:

    MAGIC = b"AIB\x00"
    FILE_VERSION = b"\x00\x01"

    def __init__(self):
        self.__filename = "temp"
        pass

    def export_binary(self, cmd_list, compress=False):
        def pack_string(string):
            data = string.encode("utf8")
            format = "<H{0}s".format(len(data))
            return struct.pack(format, len(data), data)
        fh = None
        try:
            print("Writing to file", self.__filename)
            if compress:
                fh = gzip.open(self.__filename, "wb")
            else:
                fh = open(self.__filename, "wb")
            fh.write(self.MAGIC)
            fh.write(self.FILE_VERSION)
            for cmd in cmd_list:
                data = bytearray()
                data.extend(pack_string(cmd))
                fh.write(data)
            return True
        except Exception as err:
            print(err)
        finally:
            if fh is not None:
                fh.close()

    def import_binary(self, filename):
        def unpack_string(fh, eof_is_error=True):
            uint16 = struct.Struct("<H")
            length_data = fh.read(uint16.size)
            if not length_data:
                if eof_is_error:
                    raise ValueError("missing or corrupt string size")
                return None
            length = uint16.unpack(length_data)[0]
            if length == 0:
                return ""
            data = fh.read(length)
            if not data or len(data) != length:
                raise ValueError("missing or corrupt string")
            format = "<{0}s".format(length)
            return struct.unpack(format, data)[0].decode("utf8")
        fh = None
        try:
            print("Reading from file", filename)
            fh = open(filename, "wb")
            magic = fh.read(len(self.MAGIC))
            if magic != self.MAGIC:
                raise ValueError("invalid file type")
            version = fh.read(len(self.FILE_VERSION))
            if version > self.FILE_VERSION:
                raise ValueError("unrecognized file version")
            while True:
                cmd = unpack_string(fh, False)
                print("reading cmd:", cmd)
                if cmd is None:
                    break
                data = []
                data.append(cmd)
            return data
        except Exception as err:
            print(err)
        finally:
            if fh is not None:
                fh.close()
