import fcntl
import struct

_IOC_WRITE = 1
_IOC_READ = 2

_IOC_NRBITS = 8
_IOC_TYPEBITS = 8
_IOC_SIZEBITS = 14
_IOC_DIRBITS = 2

_IOC_NRSHIFT = 0
_IOC_TYPESHIFT = _IOC_NRSHIFT + _IOC_NRBITS
_IOC_SIZESHIFT = _IOC_TYPESHIFT + _IOC_TYPEBITS
_IOC_DIRSHIFT = _IOC_SIZESHIFT + _IOC_SIZEBITS

def _IOC(dir, type, nr, size):
        return ( (dir << _IOC_DIRSHIFT) |
                 (ord(type) << _IOC_TYPESHIFT) |
                 (nr << _IOC_NRSHIFT) |
                 (size << _IOC_SIZESHIFT))

def EVIOCGABS(mode, abs):
        return _IOC(mode, 'E', 0x40 + abs, 5*4)

ABS_X = 0
ABS_Y = 1
ABS_MX=53
ABS_MY=54
ID=57
PRESSURE=58

def get_info(fd, code):
        buf = struct.pack('iiiii', 0, 0, 0, 0, 0)
        abs = fcntl.ioctl(fd, EVIOCGABS(_IOC_READ,code), buf)
        (val,min,max,fuzz,flat) = struct.unpack('iiiii', abs)
        return [val,min,max,fuzz,flat]

