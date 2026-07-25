# src/titan/utils/hardware.py
import os
import torch
import logging

logger = logging.getLogger(__name__)

def optimize_cpu_environment():
    """
    Configures PyTorch and environment variables for optimal CPU execution.
    Targeted for architectures with AVX2/AVX_VNNI.
    """
    # Number of physical cores is often better than logical threads for dense matmuls
    # Your i5-12450H has 8 physical cores (4 P-cores, 4 E-cores) and 12 threads.
    # We will default to 8 for computational tasks to avoid hyperthreading overhead on matmuls.
    optimal_threads = 8 
    
    # Set PyTorch thread counts
    torch.set_num_threads(optimal_threads)
    torch.set_num_interop_threads(optimal_threads)
    
    # Intel OpenMP environment variables for CPU optimization
    os.environ["OMP_NUM_THREADS"] = str(optimal_threads)
    os.environ["MKL_NUM_THREADS"] = str(optimal_threads)
    
    # Ensure memory allocations are optimized
    os.environ["LD_PRELOAD"] = "" # Can be set to jemalloc or tcmalloc in the future if memory fragments
    
    logger.info(f"Hardware initialization complete.")
    logger.info(f"Intra-op threads: {torch.get_num_threads()}")
    logger.info(f"Inter-op threads: {torch.get_num_interop_threads()}")
    logger.info(f"AVX_VNNI optimization: Native on PyTorch CPU backend")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    optimize_cpu_environment()