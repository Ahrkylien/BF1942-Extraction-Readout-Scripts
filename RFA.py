import os
import struct
import lzo
from datetime import datetime

def read_i(f, n = 1, forceList = False):
    res = struct.unpack('I'*n, f.read(4*n))
    if n==1 and not forceList:
        return(res[0])
    return res

def read_s(f, length = None):
    return f.read(read_i(f) if length == None else length).decode("utf-8", errors="ignore")

def read_bytes(f, n = 1):
    return list(f.read(n))

def write_i(f, values):
    if not isinstance(values, (list, tuple)): values = [values]
    return f.write(struct.pack('I'*len(values), *values))

def write_s(f, value):
    write_i(f, len(value))
    return f.write(bytearray(value.encode()))

def write_bytes(f, value):
    return f.write(bytearray(value))

XpackHeaderIdNames = {
    0x48128321 : "Default",
    0x52382184 : "XPack1",
    0x71629419 : "XPack2",
    0x81671213 : "None", # this somehow corresponds to not using a mod.dll
}

class RefractorFlatArchive_Info:
    def __init__(self, f = None, csize = None, ucsize = None, doffset = None):
        self.csize = read_i(f) if f != None else csize
        self.ucsize = read_i(f) if f != None else ucsize
        self.doffset = read_i(f) if f != None else doffset
        
    def write(self, f):
        write_i(f, [self.csize, self.ucsize, self.doffset])

class RefractorFlatArchiveEntry:
    def __init__(self, path, is_external = False, is_string = False, file_info = None, external_filepath = None, file_contents = None):
        self.path = path
        self.is_external = is_external
        self.is_string = is_string
        self.file_info = file_info
        self.external_filepath = external_filepath
        self.file_contents = file_contents

class RefractorFlatArchive:
    def __init__(self, path, read = True):
        self.path = path
        self.compressed = False
        self.success = False
        self.fileList = []
        self.fileSize = None
        self.xpackHeaderId = None
        self.xpackHeaderIdName = None
        if read:
            self.read()
    
    def read(self):
        try:
            with open(self.path, 'rb') as f:
                f.seek(0,2)
                self.fileSize = f.tell()
                f.seek(0)
                isV1dot1 = False
                if self.fileSize >= 28:
                    isV1dot1 = read_s(f, 28) in ["Refractor2 FlatArchive 1.1  "] # v 1.1 has an additional string of 28 bytes at the start
                    if not isV1dot1:
                        f.seek(0)
                offset = read_i(f)
                self.compressed = read_i(f) == 1
                
                if not isV1dot1:
                    randomBytes = read_bytes(f, 143)
                    unknown = read_bytes(f, 1)
                    XpackHeaderIdEncrypted = read_i(f)
                    self.xpackHeaderId = XpackHeaderIdEncrypted - sum(randomBytes)
                    self.xpackHeaderIdName = XpackHeaderIdNames.get(self.xpackHeaderId, False)
                
                f.seek(offset)
                rfaEntries = read_i(f)
                for i in range(rfaEntries):
                    entryPath = read_s(f)
                    file_info = RefractorFlatArchive_Info(f)
                    unknowns = read_i(f,3)
                    self.fileList.append(RefractorFlatArchiveEntry(entryPath, file_info=file_info))
                    self.success = True
        except: pass
    
    def getFileList(self):
        return [file.path for file in self.fileList]
    
    def getCorrectFilePath(self, path):
        for file in self.fileList:
            if file.path.lower().replace('\\', '/') == path.lower().replace('\\', '/'):
                return file.path
        return None
    
    def extractBlock(self, file_info, destinationPath = None, asBytes = False):
        self.success = False
        try:
            with open(self.path, 'rb') as f:
                data = []
                f.seek(file_info.doffset)
                if not self.compressed:
                    data = [f.read(file_info.ucsize)]
                else:
                    segment_num = read_i(f)
                    for i in range(segment_num):
                        f.seek(file_info.doffset+4+3*4*i)
                        segment_info = RefractorFlatArchive_Info(f)
                        if segment_info.csize == 0 or segment_info.ucsize == 0:
                            data.append(b'')
                        else:
                            f.seek(file_info.doffset+4+3*4*segment_num + segment_info.doffset)
                            data_compressed = f.read(segment_info.csize)
                            data.append(lzo.decompress(data_compressed, False, segment_info.ucsize))
                if data != []:
                    if destinationPath == None:
                        self.success = True
                        ret_str = b"" if asBytes else ""
                        for data_segment in data: ret_str += data_segment if asBytes else data_segment.decode("utf-8", errors="ignore")
                        return ret_str
                    dir = os.path.dirname(destinationPath)
                    if not os.path.exists(dir):
                        os.makedirs(dir)
                    with open(destinationPath, 'wb') as fout:
                        fout.truncate()
                        self.success = True
                        for data_segment in data:
                            fout.write(data_segment)
        except: pass
        return False
    
    def extractAll(self, destinationDir = None):
        for file in self.fileList:
            destinationPath = file.path if destinationDir == None else os.path.join(destinationDir, file.path)
            self.extractBlock(file.file_info, destinationPath)

    def extractFile(self, path, destinationDir = None, asString = False):
        path = self.getCorrectFilePath(path)
        destinationPath = path if destinationDir == None else os.path.join(destinationDir, path)
        for file in self.fileList:
            if file.path == path:
                return self.extractBlock(file.file_info, None if asString else destinationPath)
        return False
    
    def addFile(self, filePath, base_directory):
        relativePath = os.path.relpath(filePath, base_directory).replace('\\', '/')
        self.removeFile(relativePath)
        self.fileList.append(RefractorFlatArchiveEntry(relativePath, is_external=True, external_filepath=filePath))
        
    def addFileAsSring(self, relativePath, contents):
        relativePath = relativePath.replace('\\', '/')
        self.removeFile(relativePath)
        self.fileList.append(RefractorFlatArchiveEntry(relativePath, is_external=True, is_string=True, file_contents=contents))
    
    def addDirectory(self, directory, base_directory = None):
        if base_directory == None: base_directory = directory
        files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(directory) for f in filenames]
        for file in files:
            self.addFile(file, base_directory)
        
    def removeFile(self, filePath):
        filePathCorrected = self.getCorrectFilePath(filePath)
        if filePathCorrected is None:
            return False
        for file in self.fileList:
            if file.path == filePathCorrected:
                self.fileList.remove(file)
                break
        return True
    
    def deleteAllNonServerFiles(self):
        for i in reversed(range(len(self.fileList))):
            filePath = self.fileList[i].path
            if os.path.splitext(filePath)[1].lower() in ['.bik', '.dds', '.tga', 'wav'] or os.path.basename(filePath).lower() in ['palette.pal', 'envmap_g_.rcm', 'lightmapshadowbits.lsb', 'terrainpalette.pal', 'textureprecache.dat']:
                self.fileList.pop(i)
    
    def write(self, destPath = None, compressed = True):
        overWriteSelf = destPath == None
        if destPath == None: destPath = self.path+"tmp"
        
        def file_key(file):
            return str.casefold(file.path)
        
        with open(destPath, "wb") as f:
            # write header
            write_i(f, 0) # size (4bytes), pre-fill
            write_i(f, 1 if compressed else 0) # compressed (4bytes)
            randomBytesSring = "Refractor Flat Archive Packed with Arkylien's Python Module on "+datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            randomBytes = bytes(randomBytesSring, 'utf-8') + b'\x00'*(143-len(randomBytesSring))
            write_bytes(f, randomBytes)
            write_bytes(f, b'\x00') # unusedByte
            write_i(f, (self.xpackHeaderId if self.xpackHeaderId != None else 0x48128321) + sum(randomBytes)) # xpackHeaderId
            
            self.fileList.sort(key=file_key)
            
            file_infos = []
            # write file_blocks
            for file in self.fileList:
                if file.is_external:
                    if file.is_string:
                        fileBytes = bytes(file.file_contents, "UTF-8")
                    else:
                        try:
                            with open(file.external_filepath, "rb") as f_source:
                                fileBytes = f_source.read()
                        except:
                            print("cant open: "+file.external_filepath)
                            break
                else: # internal RFA file
                    fileBytes = self.extractBlock(file.file_info, asBytes = True)
                    if fileBytes == False:
                        print("cant open: "+file.path+" in RFA")
                        break
                dataOffset = f.tell()
                if not compressed: # not compressed
                    f.write(fileBytes)
                    csize = len(fileBytes)
                else:
                    maxSegmentSize = 32768
                    fileBytesBlocks = [fileBytes[i:min(i + maxSegmentSize, len(fileBytes))] for i in range(0, len(fileBytes), maxSegmentSize)]
                    write_i(f, len(fileBytesBlocks)) # number of segments
                    write_i(f, [0]*len(fileBytesBlocks)*3) # segments header pre-fill
                    startDataBlocks = f.tell()
                    segmentInfos = []
                    csize = len(fileBytesBlocks)*3*4+4
                    for fileBytesBlock in fileBytesBlocks:
                        fileBytesCompressed = lzo.compress(fileBytesBlock, 9, False) # compression level = 9, Include metadata header = False
                        segmentInfos.append(RefractorFlatArchive_Info(None, len(fileBytesCompressed), len(fileBytesBlock), f.tell()-startDataBlocks))
                        f.write(fileBytesCompressed)
                        csize += len(fileBytesCompressed)
                    endDataBlocks = f.tell()
                    f.seek(dataOffset+4)
                    for segmentInfo in segmentInfos:
                        segmentInfo.write(f)
                    f.seek(endDataBlocks)
                file_infos.append((file.path, RefractorFlatArchive_Info(None, csize, len(fileBytes), dataOffset)))
            
            startFileList = f.tell()
            
            # write file_name_info_list
            write_i(f, len(file_infos)) # number of files
            for file_info in file_infos:
                write_s(f, file_info[0]) # filePath
                file_info[1].write(f)
                write_i(f, [0, 0, 0]) # unknowns
            
            # write eof
            write_i(f, 0)
            
            # rewrite offset
            f.seek(0)
            write_i(f, startFileList)
        
        if overWriteSelf:
            os.replace(destPath, self.path)
            
class RefractorFlatArchiveGroup:
    def __init__(self, rfas = None):
        self.rfas = [] if rfas == None else [RefractorFlatArchive(path) for path in rfas]
        
    def extractFile(self, path, destinationDir = None, asString = False):
        for rfa in self.rfas:
            filePathInRFA = rfa.getCorrectFilePath(path)
            if filePathInRFA != None:
                return(rfa.extractFile(filePathInRFA, destinationDir, asString))
        return False
    
    def getFileList(self):
        filePathList = []
        for rfa in self.rfas:
            for file in rfa.fileList:
                if not file.path.lower() in (path.lower() for path in filePathList):
                    filePathList.append(file.path)
        return filePathList
        
    def fileExists(self, path):
        for rfa in self.rfas:
            filePathInRFA = rfa.getCorrectFilePath(path)
            if filePathInRFA != None:
                return True
        return False
    
    def getCorrectFilePath(self, path):
        for rfa in self.rfas:
            filePathInRFA = rfa.getCorrectFilePath(path)
            if filePathInRFA != None:
                return filePathInRFA
        return None
