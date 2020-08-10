<<<<<<< Updated upstream:3d-converter/chunks/NODE.py
from utils.reader import Reader
from utils.writer import Writer
=======
from ..utils.reader import Reader
from ..utils.writer import Writer
from .chunk import Chunk
>>>>>>> Stashed changes:models_converter/chunks/NODE.py


class Decoder(Chunk, Reader):
    def __init__(self, header: dict):
        super().__init__(header)

<<<<<<< Updated upstream:3d-converter/chunks/NODE.py
        # Variables
        self.readed = []
        # Variables

        nodes_count = self.readUShort()
        for node in range(nodes_count):
            self.readed.append({})
            name = self.readString()
            parent = self.readString()
            self.readed[node] = {'name': name,
                                 'parent': parent}

            has_target = True if self.readUShort() else False
            self.readed[node]['has_target'] = has_target
            if has_target:
                target_type = self.readChar(4)
                target_name = self.readString()
                binds_count = self.readUShort()
                binds = []
                for bind in range(binds_count):
                    binds.append({})
                    symbol = self.readString()
                    target = self.readString()
                    binds[bind] = {'symbol': symbol,
                                   'target': target}
                self.readed[node]['target_type'] = target_type
                self.readed[node]['target'] = target_name
                self.readed[node]['binds'] = binds

            frames_count = self.readUShort()
            self.readed[node]['frames'] = []
            if frames_count > 0:
                settings = list(bin(self.readUByte())[2:].zfill(8))
                self.readed[node]['frames_settings'] = settings
                for frame in range(frames_count):
                    self.readed[node]['frames'].append({})
                    frame_id = self.readUShort()
                    if settings[7] or frame == 0:  # Rotation
                        rot_x = self.readUShort() / 32512
                        rot_y = self.readUShort() / 32512
                        rot_z = self.readUShort() / 32512
                        w = self.readUShort() / 32512

                    if settings[4] or frame == 0:  # Position X
                        pos_x = self.readFloat()
                    if settings[5] or frame == 0:  # Position Y
                        pos_y = self.readFloat()
                    if settings[6] or frame == 0:  # Position Z
                        pos_z = self.readFloat()

                    if settings[1] or frame == 0:  # Scale X
                        scale_x = self.readFloat()
                    if settings[2] or frame == 0:  # Scale Y
                        scale_y = self.readFloat()
                    if settings[3] or frame == 0:  # Scale Z
                        scale_z = self.readFloat()
                    self.readed[node]['frames'][frame] = {'frame_id': frame_id,
                                                          'rotation': {'x': rot_x,
                                                                       'y': rot_y,
                                                                       'z': rot_z,
                                                                       'w': w},
                                                          'position': {'x': pos_x,
                                                                       'y': pos_y,
                                                                       'z': pos_z},
                                                          'scale': {'x': scale_x,
                                                                    'y': scale_y,
                                                                    'z': scale_z}}


class Encoder(Writer):
    def __init__(self, data: dict):
=======
    def parse(self, initial_bytes: bytes):
        super().__init__(initial_bytes)

        nodes_count = self.readUShort()
        for node_index in range(nodes_count):
            self.parsed.append({})
            name = self.readString()
            parent = self.readString()
            self.parsed[node_index] = {'name': name,
                                       'parent': parent}

            self.parse_target(node_index)

            self.parse_frames(node_index)

    def parse_target(self, node_index):
        has_target = True if self.readUShort() else False
        self.parsed[node_index]['has_target'] = has_target
        if has_target:
            target_type = self.readChar(4)
            target_name = self.readString()
            binds_count = self.readUShort()
            binds = []
            for bind in range(binds_count):
                binds.append({})
                symbol = self.readString()
                target = self.readString()
                binds[bind] = {'symbol': symbol,
                               'target': target}
            self.parsed[node_index]['target_type'] = target_type
            self.parsed[node_index]['target'] = target_name
            self.parsed[node_index]['binds'] = binds

    def parse_frames(self, node_index):
        frames_count = self.readUShort()
        self.parsed[node_index]['frames'] = []
        if frames_count > 0:
            settings = list(bin(self.readUByte())[2:].zfill(8))
            settings = [bool(int(value)) for value in settings]
            self.parsed[node_index]['frames_settings'] = settings
            for frame in range(frames_count):
                self.parsed[node_index]['frames'].append({})
                frame_id = self.readUShort()
                if settings[7] or frame == 0:  # Rotation
                    rot_x = self.readNShort()
                    rot_y = self.readNShort()
                    rot_z = self.readNShort()
                    w = self.readNShort()

                if settings[4] or frame == 0:  # Position X
                    pos_x = self.readFloat()
                if settings[5] or frame == 0:  # Position Y
                    pos_y = self.readFloat()
                if settings[6] or frame == 0:  # Position Z
                    pos_z = self.readFloat()

                if settings[1] or frame == 0:  # Scale X
                    scale_x = self.readFloat()
                if settings[2] or frame == 0:  # Scale Y
                    scale_y = self.readFloat()
                if settings[3] or frame == 0:  # Scale Z
                    scale_z = self.readFloat()
                self.parsed[node_index]['frames'][frame] = {'frame_id': frame_id,
                                                            'rotation': {'x': rot_x,
                                                                         'y': rot_y,
                                                                         'z': rot_z,
                                                                         'w': w},
                                                            'position': {'x': pos_x,
                                                                         'y': pos_y,
                                                                         'z': pos_z},
                                                            'scale': {'x': scale_x,
                                                                      'y': scale_y,
                                                                      'z': scale_z}}


class Encoder(Chunk, Writer):
    def __init__(self):
>>>>>>> Stashed changes:models_converter/chunks/NODE.py
        super().__init__()
        self.name = 'NODE'

    def encode(self, data: list):
        self.data = data
        self.writeUShort(len(self.data))
        for node in self.data:
            self.writeString(node['name'])
            self.writeString(node['parent'])

            self.writeUShort(1 if node['has_target'] else 0)
            if node['has_target']:
                self.writeChar(node['target_type'])
                self.writeString(node['target'])
                self.writeUShort(len(node['binds']))
                for bind in node['binds']:
                    self.writeString(bind['symbol'])
                    self.writeString(bind['target'])

            if 'frames_settings' in node:
                frames_settings = node['frames_settings']
            else:
                frames_settings = None
            self.encode_frames(node['frames'], frames_settings)

        self.length = len(self.buffer)

    def encode_frames(self, frames, frames_settings):
        self.writeUShort(len(frames))
        if len(frames) > 0:
            self.writeUByte(int(''.join([str(item) for item in frames_settings])[::], 2))
            for frame in frames:
                self.writeUShort(frame['frame_id'])
                if frames_settings[7] or frames.index(frame) == 0:  # Rotation
                    self.writeNShort(frame['rotation']['x'])
                    self.writeNShort(frame['rotation']['y'])
                    self.writeNShort(frame['rotation']['z'])
                    self.writeNShort(frame['rotation']['w'])

                if frames_settings[4] or frames.index(frame) == 0:  # Position X
                    self.writeFloat(frame['position']['x'])
                if frames_settings[5] or frames.index(frame) == 0:  # Position Y
                    self.writeFloat(frame['position']['y'])
                if frames_settings[6] or frames.index(frame) == 0:  # Position Z
                    self.writeFloat(frame['position']['z'])

                if frames_settings[1] or frames.index(frame) == 0:  # Scale X
                    self.writeFloat(frame['scale']['x'])
                if frames_settings[2] or frames.index(frame) == 0:  # Scale Y
                    self.writeFloat(frame['scale']['y'])
                if frames_settings[3] or frames.index(frame) == 0:  # Scale Z
                    self.writeFloat(frame['scale']['z'])
