import os
from cffi import FFI

ffi = FFI()
ffi.cdef("""
    void Say_hello(char name[], char output[], int32_t output_len);
""")

# Get absolute path to DLL
base_dir = os.path.dirname(os.path.abspath(__file__))
dll_path = os.path.join(base_dir, "bin", "LVFunctions.dll")
module = ffi.dlopen(dll_path)

name = ffi.new("char[]", b"Jan")

OUTPUT_SIZE = 255
output = ffi.new("char[]", OUTPUT_SIZE)
module.Say_hello(name, output, OUTPUT_SIZE)

output_bytes = ffi.string(output)
print(output_bytes.decode("ascii"))