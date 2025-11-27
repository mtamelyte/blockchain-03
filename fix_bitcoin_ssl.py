import ctypes
import ctypes.util
import sys

# Block bitcoin modules from loading until we patch
_blocked = [k for k in sys.modules.keys() if k.startswith('bitcoin')]
for k in _blocked:
    del sys.modules[k]

# Patch find_library to return correct paths
_original_find_library = ctypes.util.find_library

def _find_library_patch(name):
    if name == 'ssl':
        return r'C:\Program Files\OpenSSL-Win64\bin\libssl-1_1-x64.dll'
    elif name == 'crypto':
        return r'C:\Program Files\OpenSSL-Win64\bin\libcrypto-1_1-x64.dll'
    return _original_find_library(name)

ctypes.util.find_library = _find_library_patch

# Pre-load the DLLs
crypto_dll = ctypes.CDLL(r'C:\Program Files\OpenSSL-Win64\bin\libcrypto-1_1-x64.dll')
ssl_dll = ctypes.CDLL(r'C:\Program Files\OpenSSL-Win64\bin\libssl-1_1-x64.dll')

# Patch ctypes.cdll.LoadLibrary to intercept bitcoin's loading
_original_LoadLibrary = ctypes.cdll.LoadLibrary

def _patched_LoadLibrary(name):
    """Intercept LoadLibrary calls and return crypto DLL for ssl"""
    if name and ('ssl' in str(name).lower() or 'crypto' in str(name).lower()):
        # Return crypto DLL since that's where BN functions are
        return crypto_dll
    return _original_LoadLibrary(name)

ctypes.cdll.LoadLibrary = _patched_LoadLibrary

print("Patched OpenSSL loading")