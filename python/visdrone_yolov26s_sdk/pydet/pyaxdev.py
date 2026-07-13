import ctypes
import os
import platform

_lib = None

def check_error(code: int) -> None:
    if code != 0:
        raise Exception(f"API error: {code}")

base_dir = os.path.dirname(__file__)
arch = platform.machine()

if arch == 'x86_64':
    arch_dir = 'x86_64'
elif arch in ('aarch64', 'arm64'):
    arch_dir = 'aarch64'
else:
    raise RuntimeError(f"Unsupported architecture: {arch}")
so_name = 'libdet.so'
lib_paths = [
    os.path.join(base_dir, arch_dir, so_name),
    os.path.join(base_dir, so_name)
]

def _get_lib():
    global _lib
    if _lib is not None:
        return _lib
    last_error = None
    for lib_path in lib_paths:
        try:
            _lib = ctypes.CDLL(lib_path)
            # Setup function signatures
            _lib.ax_dev_enum_devices.argtypes = [ctypes.POINTER(AxDevices)]
            _lib.ax_dev_enum_devices.restype = ctypes.c_int
            _lib.ax_dev_sys_init.argtypes = [AxDeviceType, ctypes.c_char]
            _lib.ax_dev_sys_init.restype = ctypes.c_int
            _lib.ax_dev_sys_deinit.argtypes = [AxDeviceType, ctypes.c_char]
            _lib.ax_dev_sys_deinit.restype = ctypes.c_int
            return _lib
        except OSError as e:
            last_error = e
    raise RuntimeError(f"Failed to load {so_name}. Build libdet.axera first. "
                       f"Last error: {last_error}")

class AxDeviceType(ctypes.c_int):
    unknown_device = 0
    host_device = 1
    axcl_device = 2

class AxMemInfo(ctypes.Structure):
    _fields_ = [
        ('remain', ctypes.c_int),
        ('total', ctypes.c_int)
    ]

class AxHostInfo(ctypes.Structure):
    _fields_ = [
        ('available', ctypes.c_char),
        ('version', ctypes.c_char * 32),
        ('mem_info', AxMemInfo)
    ]

class AxDeviceInfo(ctypes.Structure):
    _fields_ = [
        ('temp', ctypes.c_int),
        ('cpu_usage', ctypes.c_int),
        ('npu_usage', ctypes.c_int),
        ('mem_info', AxMemInfo)
    ]

class AxDevices(ctypes.Structure):
    _fields_ = [
        ('host', AxHostInfo),
        ('host_version', ctypes.c_char * 32),
        ('dev_version', ctypes.c_char * 32),
        ('count', ctypes.c_ubyte),
        ('devices_info', AxDeviceInfo * 16)
    ]

def enum_devices() -> dict:
    lib = _get_lib()
    devices = AxDevices()
    check_error(lib.ax_dev_enum_devices(ctypes.byref(devices)))
    return {
        'host': {
            'available': bool(devices.host.available[0]),
            'version': devices.host.version.decode('utf-8'),
            'mem_info': {
                'remain': devices.host.mem_info.remain,
                'total': devices.host.mem_info.total
            }
        },
        'devices': {
            'host_version': devices.host_version.decode('utf-8'),
            'dev_version': devices.dev_version.decode('utf-8'),
            'count': devices.count,
            'devices_info': [{
                'temp': dev.temp,
                'cpu_usage': dev.cpu_usage,
                'npu_usage': dev.npu_usage,
                'mem_info': {
                    'remain': dev.mem_info.remain,
                    'total': dev.mem_info.total
                }
            } for dev in devices.devices_info[:devices.count]]
        }
    }

def sys_init(dev_type: AxDeviceType = AxDeviceType.axcl_device, devid: int = 0) -> None:
    lib = _get_lib()
    check_error(lib.ax_dev_sys_init(dev_type, devid))

def sys_deinit(dev_type: AxDeviceType = AxDeviceType.axcl_device, devid: int = 0) -> None:
    lib = _get_lib()
    check_error(lib.ax_dev_sys_deinit(dev_type, devid))
