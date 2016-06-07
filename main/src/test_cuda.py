import numpy as np

import pycuda.gpuarray as gpuarray
from pycuda.compiler import SourceModule
import pycuda.driver as cuda
import pycuda.autoinit


def phase1_device(d_keys, d_offset, d_length, count, bucketCount):
    mod = SourceModule("""
    #include <stdio.h>
    typedef unsigned long long  KEY_T ;
    typedef KEY_T               *KEY_PTR;
    typedef unsigned int        VALUE_T;
    typedef VALUE_T             *VALUE_PTR;
    #define C0  0x01010101
    #define C1  0x12345678
    #define LARGE_PRIME 1900813
    #define MAX_INT  0xffffffff

    __forceinline__ __device__ unsigned int hash_h(KEY_T  key, unsigned int bucketCount)
    {
        return ((C0 + C1 * key) % LARGE_PRIME ) % bucketCount;
    }
    __global__ void phase1( KEY_PTR  keys,
                unsigned int * offset,
                unsigned int length,
                unsigned int* count,
                unsigned int bucketCount){

        unsigned int tid = (blockDim.x*blockDim.y * gridDim.x*blockIdx.y) + (blockDim.x*blockDim.y*blockIdx.x)+(blockDim.x*threadIdx.y)+threadIdx.x;
        if(tid<length){
            KEY_T key = keys[tid];
            unsigned int bucket = hash_h(key,bucketCount);
            offset[tid] = atomicInc (count+bucket,MAX_INT);
            printf(" offset = %u ", offset[tid]);

        }
        __syncthreads();
    }
    """, options=['--compiler-options', '-Wall'])

    np_d_keys = np.array(d_keys, dtype=np.uint64)
    keys_gpu = gpuarray.to_gpu(np_d_keys)
    np_d_offsets = np.array(d_offset, dtype=np.uint32)
    offset_gpu = gpuarray.to_gpu(np_d_offsets)
    count_gpu = gpuarray.to_gpu(count)
    block_dim = (512, 1, 1)
    if (d_length//512) == 0:
        grid_dim = (1, 1, 1)
    else:
        grid_dim = (d_length//512, 1, 1)

    phase1 = mod.get_function("phase1")
    phase1(keys_gpu, offset_gpu, np.uint(d_length), count_gpu,
           np.uint(bucketCount), grid=grid_dim, block=block_dim)

    d_offset = offset_gpu.get()
    count = count_gpu.get()
    print('Finished. Leaving.')
    print(d_offset)

if __name__ == '__main__':
    d_keys = range(0, 1024)
    d_offset = range(1024, 2048)
    d_length = 1024
    count = np.array(range(2048, 3072))
    bucketCount = 128
    phase1_device(d_keys, d_offset, d_length, count, bucketCount)
