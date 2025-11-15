# Documentation

## Coordinate system
BF1942 uses the Left-handed coordinate system (because Direct3d 8 also uses that):\
x: right, y: up, z: away\
In-game this will result to:\
x: East, y: higher altitude, z: North

## Skeleton File (.ske)
This file contains a list of bones.\
Each bone has a name and a transformation matrix.
```
.ske
├── uint32 | Header (Probably the version, always 1)
├── uint32 | Number of bones
└── <Bones, * Number of bones>
    ├── uint16 | Bone name length
    ├── char[] | Bone name (string)
    ├── uint16 | Parent Bone index (FFFF and FFFE indicate no parent. Seems like a signed short)
    └── <Transformation matrix>
        ├── float | m00
        ├── float | m01
        ├── float | m02
        ├── float | m03
        ├── float | m10
        ├── float | m11
        ├── float | m12
        ├── float | m13
        ├── float | m20
        ├── float | m21
        ├── float | m22
        └── float | m23
```
The Transformation matrix has this structure:
```
[ m00  m01  m02  m03 ]  
[ m10  m11  m12  m13 ]  
[ m20  m21  m22  m23 ]  
[ m30  m31  m32  m33 ]
```
Where m30, m31 and m32 are 0 and m33 is 1.\
The right column is the translation column (x, y, z, 1).\

## Skin File (.skn)
This file contains a list of vertices.
Each vertex has a position (vector) and a list of weights.
The weight belongs to a bone and have a relative position (vector).
Bones are indicated by index (probably internal to the file) and a name (string).
```
.skn
├── uint32   | Header (Probably the version, always 1)
├── uint32   | Number of vertices
├── <Vertices, * Number of vertices>
│   ├── float  | Vertex position x
│   ├── float  | Vertex position y
│   ├── float  | Vertex position z
│   ├── uint8  | Number of bone weights
│   └── <Bone weights, * Number of bone weights>
│       ├── uint16  | Bone index
│       ├── float   | Weight value
│       ├── float   | Relative position x
│       ├── float   | Relative position y
│       └── float   | Relative position z
├── uint16   | Number of used bones
└── <Bones, * Number of used bones
    ├── uint16  | Bone name length
    └── char[]  | Bone name (string)
```

## Bone Animation Frames File (.baf)
This file contains a list of Bones. A Bone has Frames and a Frame has a rotation and position vector.
```
.baf
├── uint32   | Header (Probably the version, always 3)
├── uint16   | Number of bones
├── <Bones, * Number of bones>
│   ├── uint16   | Bone name length
│   └── char[]   | Bone name (string)
├── uint32   | Number of frames
└── uint8    | Precision (number of bits in mantissa)
    <Bones, * Number of bones>
    ├── uint16   | Number of data (entries?, unknown what it is used for)
    └── <Data Entries, * 7>
        ├── uint16   | Data Entry Block Size
        └── <Data Entry Sub-Blocks, * for whole Data Entry Block Size>
            ├── uint7    | Number of Frames
            ├── uint1    | Is Run-length Encoded (MSB)
            ├── uint8    | Data Entry Sub-Block Size
            ├── <if not Is Run-length Encoded: Frames, * Number of Frames>
            │    └── float16    | Bone Data
            └── <if Is Run-length Encoded>
                 └── float16    | Bone Data (equal for all Number of Frames due to RLE)
```

The reason for the 7 is that there are 7 floats per frame:\
The first 4 have float Precision of 14 and make the rotation vector (Quaternion).\
The other 3 have a Precision as in the Precision entry in the file and make the position vector.
