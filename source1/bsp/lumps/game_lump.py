from typing import List

from ..datatypes.gamelumps.detail_prop_lump import DetailPropLump
from ..datatypes.gamelumps.static_prop_lump import StaticPropLump
from ....utilities.byte_io_mdl import ByteIO
from .. import Lump, lump_tag
from ..datatypes.game_lump_header import GameLumpHeader


@lump_tag(35, 'LUMP_GAME_LUMP')
class GameLump(Lump):

    def __init__(self, bsp, lump_id):
        super().__init__(bsp, lump_id)
        self.lump_count = 0
        self.game_lumps_info: List[GameLumpHeader] = []
        self.game_lumps = {}

    def parse(self):
        reader = self.reader
        self.lump_count = reader.read_uint32()
        for _ in range(self.lump_count):
            self.game_lumps_info.append(GameLumpHeader(self, self._bsp).parse(reader))
        for lump in self.game_lumps_info:
            if lump.size == 0:
                continue
            relative_offset = lump.offset - self._lump.offset
            print(f'GLump "{lump.id}" offset: {relative_offset} size: {lump.size} ')
            with reader.save_current_pos():
                reader.seek(relative_offset)
                if lump.flags == 1:
                    curr_index = self.game_lumps_info.index(lump)
                    if curr_index + 1 != len(self.game_lumps_info):
                        next_offset = self.game_lumps_info[curr_index + 1].offset - self._lump.offset
                    else:
                        next_offset = self._lump.size - relative_offset
                    compressed_size = next_offset - relative_offset
                    buffer = reader.read(compressed_size)
                    game_lump_reader = Lump.decompress_lump(ByteIO(buffer))
                else:
                    game_lump_reader = ByteIO(reader.read(lump.size))

                pass  # TODO
            if lump.id == 'sprp':
                game_lump = StaticPropLump(lump)
                game_lump.parse(game_lump_reader)
                self.game_lumps[lump.id] = game_lump
            elif lump.id == 'dprp':
                detail_lump = DetailPropLump(lump)
                detail_lump.parse(game_lump_reader)
                self.game_lumps[lump.id] = detail_lump

        return self
