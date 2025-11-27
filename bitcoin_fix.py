import ctypes
import ctypes.util
import os

# Patch find_library to return the correct OpenSSL paths
_original_find_library = ctypes.util.find_library

def _find_library_patch(name):
    """Return full paths to OpenSSL 1.1.1 DLLs"""
    if name in ('ssl', 'crypto'):
        if name == 'ssl':
            path = r'C:\Program Files\OpenSSL-Win64\bin\libssl-1_1-x64.dll'
        else:  # crypto
            path = r'C:\Program Files\OpenSSL-Win64\bin\libcrypto-1_1-x64.dll'
        
        if os.path.exists(path):
            return path
    
    # Fall back to original for other libraries
    return _original_find_library(name)

# Apply the patch
ctypes.util.find_library = _find_library_patch

# Verify the patch works
test_ssl = ctypes.util.find_library('ssl')
test_crypto = ctypes.util.find_library('crypto')

if not test_ssl or not test_crypto:
    raise RuntimeError(f"Failed to locate OpenSSL DLLs. ssl={test_ssl}, crypto={test_crypto}")

print(f"OpenSSL DLLs located: ssl={test_ssl}, crypto={test_crypto}")