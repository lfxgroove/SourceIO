import zlib

from ...utils.pylib import VTFLibV2
from ....library.utils import Buffer, MemoryBuffer
from ....logger import SLoggingManager

log_manager = SLoggingManager()
logger = log_manager.get_logger('Source1::VTF')


def load_texture(file_object, hdr=False):
    data = file_object.read()
    lib = VTFLibV2(data)
    try:
        rgba_data = lib.convert(True)
        return rgba_data, *rgba_data.shape[:2]
    except Exception as ex:
        logger.error('Caught exception "{}" '.format(ex))
    finally:
        lib.destroy()
        del lib

    return None, 0, 0


def load_texture_tth(header_file: Buffer, data_file: Buffer):
    vtf_data = bytearray()
    if header_file.read_ascii_string(3) != "TTH":
        return None
    header_file.seek(6)
    entry_count = header_file.read_uint8()
    header_file.skip(1)
    header_size = header_file.read_uint32()
    header_file.seek(16 + entry_count * 8 + 4)
    vtf_data += header_file.read(header_size)
    vtf_data += zlib.decompress(data_file.read())
    memory_buffer = MemoryBuffer(vtf_data)
    return load_texture(memory_buffer)
