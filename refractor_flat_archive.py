import sys
import os
import struct
import lzo
from datetime import datetime


if sys.version_info < (3, 10):
    version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    sys.exit(f"Error: Python 3.10 or higher is required to use this module. You are using {version}")


def read_i(f, n: int = 1, force_list: bool = False) -> int | tuple[int, ...]:
    res = struct.unpack('I' * n, f.read(4 * n))
    if n == 1 and not force_list:
        return res[0]
    return res


def read_s(f, length: int = None) -> str:
    return f.read(read_i(f) if length is None else length).decode("utf-8", errors="ignore")


def read_bytes(f, n: int = 1) -> list[int]:
    return list(f.read(n))


def write_i(f, values: list[int] | int) -> bool:
    if not isinstance(values, (list, tuple)):
        values = [values]
    return f.write(struct.pack('I' * len(values), *values))


def write_s(f, value: str) -> bool:
    write_i(f, len(value))
    return f.write(bytearray(value.encode()))


def write_bytes(f, value: bytes) -> bool:
    return f.write(bytearray(value))


XpackHeaderIdNames = {
    0x48128321: "Default",
    0x52382184: "XPack1",
    0x71629419: "XPack2",
    0x81671213: "None",  # this somehow corresponds to not using a mod.dll
}


class RefractorFlatArchiveInfo:
    def __init__(self, f=None, compressed_size=None, uncompressed_size=None, data_offset=None):
        self.compressed_size = read_i(f) if f is not None else compressed_size
        self.uncompressed_size = read_i(f) if f is not None else uncompressed_size
        self.data_offset = read_i(f) if f is not None else data_offset

    def write(self, f):
        write_i(f, [self.compressed_size, self.uncompressed_size, self.data_offset])


class RefractorFlatArchiveEntry:
    def __init__(self, path: str, is_external=False, is_string=False, file_info=None, external_filepath=None,
                 file_contents=None):
        self.path = path
        self.is_external = is_external
        self.is_string = is_string
        self.file_info = file_info
        self.external_filepath = external_filepath
        self.file_contents = file_contents


class RefractorFlatArchive:
    def __init__(self, path: str, read=True):
        self.path = path
        self.compressed = False
        self.success = False
        self.file_list = []
        self.file_size = None
        self.xpack_header_id = None
        self.xpack_headerId_name = None
        if read:
            self.read()

    def read(self):
        with open(self.path, 'rb') as f:
            f.seek(0, 2)
            self.file_size = f.tell()
            f.seek(0)
            is_v1dot1 = False
            if self.file_size >= 28:
                # v 1.1 has an additional string of 28 bytes at the start
                is_v1dot1 = read_s(f, 28) in ["Refractor2 FlatArchive 1.1  "]
                if not is_v1dot1:
                    f.seek(0)
            offset = read_i(f)
            self.compressed = read_i(f) == 1

            if not is_v1dot1:
                random_bytes = read_bytes(f, 143)
                _ = read_bytes(f, 1)  # unknown
                xpack_header_id_encrypted = read_i(f)
                self.xpack_header_id = xpack_header_id_encrypted - sum(random_bytes)
                self.xpack_headerId_name = XpackHeaderIdNames.get(self.xpack_header_id, False)

            f.seek(offset)
            rfa_entries = read_i(f)
            for i in range(rfa_entries):
                entry_path = read_s(f)
                file_info = RefractorFlatArchiveInfo(f)
                _ = read_i(f, 3)  # unknown
                self.file_list.append(RefractorFlatArchiveEntry(entry_path, file_info=file_info))
                self.success = True

    def get_file_list(self):
        return [file.path for file in self.file_list]

    def get_correct_file_path(self, path: str):
        for file in self.file_list:
            if file.path.lower().replace('\\', '/') == path.lower().replace('\\', '/'):
                return file.path
        return None

    def extract_block(self, file_info: RefractorFlatArchiveInfo, destination_path: str | None = None,
                      as_bytes: bool = False) -> bool | bytes:
        self.success = False
        with open(self.path, 'rb') as f:
            data = []
            f.seek(file_info.data_offset)
            if not self.compressed:
                data = [f.read(file_info.uncompressed_size)]
            else:
                segment_num = read_i(f)
                for i in range(segment_num):
                    f.seek(file_info.data_offset + 4 + 3 * 4 * i)
                    segment_info = RefractorFlatArchiveInfo(f)
                    if segment_info.compressed_size == 0 or segment_info.uncompressed_size == 0:
                        data.append(b'')
                    else:
                        f.seek(file_info.data_offset + 4 + 3 * 4 * segment_num + segment_info.data_offset)
                        data_compressed = f.read(segment_info.compressed_size)
                        data.append(lzo.decompress(data_compressed, False, segment_info.uncompressed_size))
            if data:
                if destination_path is None:
                    self.success = True
                    ret_str = b"" if as_bytes else ""
                    for data_segment in data:
                        ret_str += data_segment if as_bytes else data_segment.decode("utf-8", errors="ignore")
                    return ret_str
                directory_path = os.path.dirname(destination_path)
                if not directory_path == "" and not os.path.isdir(directory_path):
                    os.makedirs(directory_path)
                with open(destination_path, 'wb') as fout:
                    fout.truncate()
                    self.success = True
                    for data_segment in data:
                        fout.write(data_segment)
        return False

    def extract_all(self, destination_dir=None):
        for file in self.file_list:
            # Remove leading slashes such that the files get extracted relative to the working directory when no destination dir is set
            relative_file_path = file.path.lstrip('/')
            destination_path = relative_file_path if destination_dir is None else os.path.join(destination_dir,
                                                                                               relative_file_path)
            self.extract_block(file.file_info, destination_path)

    def extract_file(self, path: str, destination_dir=None, as_string=False):
        path = self.get_correct_file_path(path)
        destination_path = path if destination_dir is None else os.path.join(destination_dir, path)
        for file in self.file_list:
            if file.path == path:
                return self.extract_block(file.file_info, None if as_string else destination_path)
        return False

    def add_file(self, file_path: str, base_directory: str):
        relative_path = os.path.relpath(file_path, base_directory).replace('\\', '/')
        self.remove_file(relative_path)
        self.file_list.append(RefractorFlatArchiveEntry(relative_path, is_external=True, external_filepath=file_path))

    def add_file_as_string(self, relative_path: str, contents: str):
        relative_path = relative_path.replace('\\', '/')
        self.remove_file(relative_path)
        self.file_list.append(
            RefractorFlatArchiveEntry(relative_path, is_external=True, is_string=True, file_contents=contents))

    def add_directory(self, directory: str, base_directory=None):
        if base_directory is None:
            base_directory = directory
        files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(directory) for f in filenames]
        for file in files:
            self.add_file(file, base_directory)

    def remove_file(self, file_path: str) -> bool:
        file_path_corrected = self.get_correct_file_path(file_path)
        if file_path_corrected is None:
            return False
        for file in self.file_list:
            if file.path == file_path_corrected:
                self.file_list.remove(file)
                break
        return True

    def delete_all_non_server_files(self):
        for i in reversed(range(len(self.file_list))):
            file_path = self.file_list[i].path
            if os.path.splitext(file_path)[1].lower() in ['.bik', '.dds', '.tga', 'wav'] or os.path.basename(
                    file_path).lower() in ['palette.pal', 'envmap_g_.rcm', 'lightmapshadowbits.lsb',
                                           'terrainpalette.pal', 'textureprecache.dat']:
                self.file_list.pop(i)

    def write(self, dest_path=None, compressed=True):
        overwrite_self = dest_path is None
        if dest_path is None:
            dest_path = self.path + "tmp"

        def file_key(file):
            return str.casefold(file.path)

        with open(dest_path, "wb") as f:
            # write header
            write_i(f, 0)  # size (4bytes), pre-fill
            write_i(f, 1 if compressed else 0)  # compressed (4bytes)
            random_bytes_string = "Refractor Flat Archive Packed with Arkylien's Python Module on " + datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S")
            random_bytes = bytes(random_bytes_string, 'utf-8') + b'\x00' * (143 - len(random_bytes_string))
            write_bytes(f, random_bytes)
            write_bytes(f, b'\x00')  # unusedByte
            xpack_header_id = self.xpack_header_id if self.xpack_header_id is not None else 0x48128321
            write_i(f, xpack_header_id + sum(random_bytes))

            self.file_list.sort(key=file_key)

            file_infos = []
            # write file_blocks
            for file in self.file_list:
                if file.is_external:
                    if file.is_string:
                        file_bytes = bytes(file.file_contents, "UTF-8")
                    else:
                        try:
                            with open(file.external_filepath, "rb") as f_source:
                                file_bytes = f_source.read()
                        except Exception as e:
                            raise Exception(f"Can't open: {file.external_filepath}", e)
                else:  # internal RFA file
                    file_bytes = self.extract_block(file.file_info, as_bytes=True)
                    if file_bytes is False:
                        raise Exception(f"Can't open: {file.path} in RFA")
                data_offset = f.tell()
                if not compressed:  # not compressed
                    f.write(file_bytes)
                    compressed_size = len(file_bytes)
                else:
                    max_segment_size = 32768  # 2 ** 15
                    file_bytes_blocks = [file_bytes[i:min(i + max_segment_size, len(file_bytes))] for i in
                                         range(0, len(file_bytes), max_segment_size)]
                    write_i(f, len(file_bytes_blocks))  # number of segments
                    write_i(f, [0] * len(file_bytes_blocks) * 3)  # segments header pre-fill
                    start_data_blocks = f.tell()
                    segment_infos = []
                    compressed_size = len(file_bytes_blocks) * 3 * 4 + 4
                    for fileBytesBlock in file_bytes_blocks:
                        file_bytes_compressed = lzo.compress(fileBytesBlock, 9,
                                                             False)  # compression level = 9, Include metadata header = False
                        segment_infos.append(
                            RefractorFlatArchiveInfo(None, len(file_bytes_compressed), len(fileBytesBlock),
                                                     f.tell() - start_data_blocks))
                        f.write(file_bytes_compressed)
                        compressed_size += len(file_bytes_compressed)
                    end_data_blocks = f.tell()
                    f.seek(data_offset + 4)
                    for segmentInfo in segment_infos:
                        segmentInfo.write(f)
                    f.seek(end_data_blocks)
                file_infos.append(
                    (file.path, RefractorFlatArchiveInfo(None, compressed_size, len(file_bytes), data_offset)))

            start_file_list = f.tell()

            # write file_name_info_list
            write_i(f, len(file_infos))  # number of files
            for file_info in file_infos:
                write_s(f, file_info[0])  # filePath
                file_info[1].write(f)
                write_i(f, [0, 0, 0])  # unknowns

            # write eof
            write_i(f, 0)

            # rewrite offset
            f.seek(0)
            write_i(f, start_file_list)

        if overwrite_self:
            os.replace(dest_path, self.path)


class RefractorFlatArchiveGroup:
    def __init__(self, rfa_paths=None):
        self.rfa_paths = [] if rfa_paths is None else [RefractorFlatArchive(path) for path in rfa_paths]

    def extract_file(self, path: str, destination_dir=None, as_string=False) -> bool:
        for rfa in self.rfa_paths:
            file_path_in_rfa = rfa.get_correct_file_path(path)
            if file_path_in_rfa is not None:
                return rfa.extract_file(file_path_in_rfa, destination_dir, as_string)
        return False

    def get_file_list(self) -> [str]:
        file_path_list = []
        for rfa in self.rfa_paths:
            for file in rfa.file_list:
                if not file.path.lower() in (path.lower() for path in file_path_list):
                    file_path_list.append(file.path)
        return file_path_list

    def file_exists(self, path: str) -> bool:
        for rfa in self.rfa_paths:
            file_path_in_rfa = rfa.get_correct_file_path(path)
            if file_path_in_rfa is not None:
                return True
        return False

    def get_correct_file_path(self, path: str) -> str | None:
        for rfa in self.rfa_paths:
            file_path_in_rfa = rfa.get_correct_file_path(path)
            if file_path_in_rfa is not None:
                return file_path_in_rfa
        return None
