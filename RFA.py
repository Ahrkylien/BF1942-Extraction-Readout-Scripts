import os
import struct
import lzo

def read_i(f, n = 1, forceList = False):
    res = struct.unpack('I'*n, f.read(4*n))
    if n==1 and not forceList:
        return(res[0])
    return(res)

def read_s(f, length = None):
    return(f.read(read_i(f) if length == None else length).decode("utf-8", errors="ignore"))

def write_i(f, values):
    if not isinstance(values, (list, tuple)): values = [values]
    return(f.write(struct.pack('I'*len(values), *values)))

def write_s(f, value):
    write_i(f, len(value))
    return(f.write(bytearray(value.encode())))

def write_bytes(f, value):
    return(f.write(bytearray(value)))

class RefractorFlatArchive_Info:
    def __init__(self, f = None, csize = None, ucsize = None, doffset = None):
        self.csize = read_i(f) if f != None else csize
        self.ucsize = read_i(f) if f != None else ucsize
        self.doffset = read_i(f) if f != None else doffset
        
    def write(self, f):
        write_i(f, [self.csize, self.ucsize, self.doffset])
        
class RefractorFlatArchive:
    def __init__(self, path, read = True):
        self.path = path
        self.compressed = False
        self.success = False
        self.fileList = []
        self.fileListExternal = []
        self.fileSize = None
        if read:
            self.read()
    
    def read(self):
        try:
            with open(self.path, 'rb') as f:
                f.seek(0,2)
                self.fileSize = f.tell()
                f.seek(0)
                if self.fileSize >= 28:
                    if not read_s(f, 28) in ["Refractor2 FlatArchive 1.1  "]: # v 1.1 has an additional string of 28 bytes at the start
                        f.seek(0)
                offset = read_i(f)
                self.compressed = read_i(f) == 1
                f.seek(offset)
                rfaEntries = read_i(f)
                for i in range(rfaEntries):
                    entryPath = read_s(f)
                    file_info = RefractorFlatArchive_Info(f)
                    unknowns = read_i(f,3)
                    self.fileList.append((entryPath, file_info))
                    self.success = True
        except: pass
    
    def getFileList(self):
        filePathList = [fileInfo[0] for fileInfo in self.fileList]
        return(filePathList)
    
    def getCorrectFilePath(self, path):
        for fileInfo in self.fileList:
            if fileInfo[0].lower() == path.lower():
                return(fileInfo[0])
        return(None)
    
    def extractBlock(self, fileInfo, destinationPath = None, asBytes = False):
        self.success = False
        try:
            with open(self.path, 'rb') as f:
                data = []
                f.seek(fileInfo[1].doffset)
                if not self.compressed:
                    data = [f.read(fileInfo[1].ucsize)]
                else:
                    segment_num = read_i(f)
                    for i in range(segment_num):
                        f.seek(fileInfo[1].doffset+4+3*4*i)
                        segment_info = RefractorFlatArchive_Info(f)
                        if segment_info.csize == 0:
                            data.append(b'')
                        else:
                            f.seek(fileInfo[1].doffset+4+3*4*segment_num + segment_info.doffset)
                            data_compressed = f.read(segment_info.csize)
                            data.append(lzo.decompress(data_compressed, False, segment_info.ucsize))
                if data != []:
                    if destinationPath == None:
                        self.success = True
                        ret_str = b"" if asBytes else ""
                        for data_segment in data: ret_str += data_segment if asBytes else data_segment.decode("utf-8", errors="ignore")
                        return(ret_str)
                    dir = os.path.dirname(destinationPath)
                    if not os.path.exists(dir):
                        os.makedirs(dir)
                    with open(destinationPath, 'wb') as fout:
                        fout.truncate()
                        self.success = True
                        for data_segment in data:
                            fout.write(data_segment)
        except: pass
        return(False)
    
    def extractAll(self, destinationDir = None):
        for fileInfo in self.fileList:
            destinationPath = fileInfo[0] if destinationDir == None else os.path.join(destinationDir, fileInfo[0])
            self.extractBlock(fileInfo, destinationPath)

    def extractFile(self, path, destinationDir = None, asString = False):
        destinationPath = path if destinationDir == None else os.path.join(destinationDir, path)
        for fileInfo in self.fileList:
            if fileInfo[0] == path:
                return(self.extractBlock(fileInfo, None if asString else destinationPath))
        return(False)
    
    def addFile(self, filePath, base_directory):
        relativePath = os.path.relpath(filePath, base_directory)
        for file in self.fileList:
            if file[0].lower() == relativePath.lower():
                self.fileList.remove(file)
        self.fileListExternal.append([relativePath, False, filePath])
        
    def addFileAsSring(self, relativePath, contents):
        for file in self.fileList:
            if file[0].lower() == relativePath.lower():
                self.fileList.remove(file)
        self.fileListExternal.append([relativePath, True, contents])
    
    def addDirectory(self, directory, base_directory = None):
        if base_directory == None: base_directory = directory
        files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(directory) for f in filenames]
        for file in files:
            self.addFile(file, base_directory)
    
    def write(self, destPath = None, compressed = True):
        overWriteSelf = destPath == None
        if destPath == None: destPath = self.path+"tmp"
        
        def file_key(file):
            return(str.casefold(file[0]))
        
        with open(destPath, "wb") as f:
            # write header
            write_i(f, 0) #size (4bytes), pre-fill
            write_i(f, 1 if compressed else 0) #compressed (4bytes)
            # unknown part of header:
            header_unknown = [                              0x63, 0xEC, 0x95, 0xBF, 0xFE, 0x7B, 0x09, 0x3C,
            0x3A, 0xF0, 0x72, 0xEE, 0xA4, 0x72, 0xE7, 0xD9, 0x3F, 0xCC, 0x99, 0xC0, 0xD3, 0x71, 0xC1, 0x46,
            0x89, 0xBD, 0xD7, 0x53, 0xB5, 0x7E, 0x05, 0xB9, 0xF3, 0xB3, 0xDB, 0x18, 0x75, 0x94, 0x44, 0xFF,
            0x9B, 0xD2, 0xB9, 0x53, 0xC4, 0x1F, 0xB4, 0xF5, 0x65, 0xF1, 0x68, 0x9F, 0x58, 0x83, 0xAF, 0x0F,
            0x76, 0x1D, 0x44, 0x68, 0x67, 0x96, 0x32, 0xD5, 0xB9, 0x17, 0x8C, 0x6F, 0x30, 0x21, 0x5F, 0x61,
            0x5D, 0xD2, 0xE5, 0x49, 0x72, 0x64, 0xFB, 0xE2, 0x55, 0xF6, 0xD5, 0xE1, 0xF3, 0x8F, 0xF1, 0x1C,
            0xD7, 0x60, 0x49, 0xF1, 0xFB, 0x49, 0xCD, 0xE6, 0xDE, 0x9F, 0x10, 0x8D, 0xD6, 0x2D, 0x42, 0xAB,
            0xA8, 0x78, 0x5E, 0x98, 0x56, 0x48, 0xA4, 0xE9, 0x38, 0x63, 0x4A, 0x4D, 0x4E, 0x9C, 0x6F, 0xB5,
            0xD5, 0x0C, 0x50, 0xB8, 0x18, 0xA0, 0xBE, 0x35, 0x89, 0xD4, 0xD0, 0x3A, 0x10, 0xBD, 0xD5, 0x24,
            0xA3, 0x4D, 0x8C, 0x08, 0x17, 0xD3, 0x98, 0x00, 0x4B, 0xD0, 0x12, 0x48]
            write_bytes(f, header_unknown)
            
            fileListTotal = self.fileList + self.fileListExternal
            fileListTotal.sort(key=file_key)
            
            file_infos = []
            # write file_blocks
            for file in fileListTotal:
                if len(file) == 3: #external file
                    if file[1]: #content as string
                        fileBytes = bytes(file[2], "UTF-8")
                    else:
                        try:
                            with open(file[1], "rb") as f_source:
                                fileBytes = f_source.read()
                        except:
                            print("cant open: "+file[1])
                            break
                else: #internal RFA file
                    fileBytes = self.extractBlock(file, asBytes = True)
                    if fileBytes == False:
                        print("cant open: "+file[0]+" in RFA")
                        break
                dataOffset = f.tell()
                if not compressed: #not compressed
                    f.write(fileBytes)
                    csize = len(fileBytes)
                else:
                    maxSegmentSize = 32768
                    fileBytesBlocks = [fileBytes[i:min(i + maxSegmentSize, len(fileBytes))] for i in range(0, len(fileBytes), maxSegmentSize)]
                    write_i(f, len(fileBytesBlocks)) #number of segments
                    write_i(f, [0]*len(fileBytesBlocks)*3) #segments header pre-fill
                    startDataBlocks = f.tell()
                    segmentInfos = []
                    csize = len(fileBytesBlocks)*3*4+4
                    for fileBytesBlock in fileBytesBlocks:
                        fileBytesCompressed = lzo.compress(fileBytesBlock, 9, False) #compression level = 9, Include metadata header = False
                        segmentInfos.append(RefractorFlatArchive_Info(None, len(fileBytesCompressed), len(fileBytesBlock), f.tell()-startDataBlocks))
                        f.write(fileBytesCompressed)
                        csize += len(fileBytesCompressed)
                    endDataBlocks = f.tell()
                    f.seek(dataOffset+4)
                    for segmentInfo in segmentInfos:
                        segmentInfo.write(f)
                    f.seek(endDataBlocks)
                file_infos.append((file[0], RefractorFlatArchive_Info(None, csize, len(fileBytes), dataOffset)))
            
            startFileList = f.tell()
            
            # write file_name_info_list
            write_i(f, len(file_infos)) #number of files
            for file_info in file_infos:
                write_s(f, file_info[0]) #filePath
                file_info[1].write(f)
                write_i(f, [0, 0, 0]) #unknowns
            
            #write eof
            write_i(f, 0)
            
            #rewrite offset
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
        return(False)
    
    def getFileList(self):
        filePathList = []
        for rfa in self.rfas:
            for fileInfo in rfa.fileList:
                if not fileInfo[0].lower() in (path.lower() for path in filePathList):
                    filePathList.append(fileInfo[0])
        return(filePathList)
        
    def fileExists(self, path):
        for rfa in self.rfas:
            filePathInRFA = rfa.getCorrectFilePath(path)
            if filePathInRFA != None: return(True)
        return(False)
    
    def getCorrectFilePath(self, path):
        for rfa in self.rfas:
            filePathInRFA = rfa.getCorrectFilePath(path)
            if filePathInRFA != None: return(filePathInRFA)
        return(None)