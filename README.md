# TorchSparse

TorchSparse is a high-performance neural network library for point cloud processing.

## Installation

TorchSparse depends on the [Google Sparse Hash](https://github.com/sparsehash/sparsehash) library.

- On Ubuntu, it can be installed by

  ```bash
  sudo apt-get install libsparsehash-dev
  ```

- On Mac OS, it can be installed by

  ```bash
  brew install google-sparsehash
  ```

- You can also compile the library locally (if you do not have the sudo permission) and add the library path to the environment variable `CPLUS_INCLUDE_PATH`.

The latest released TorchSparse (v1.4.0) can then be installed by

```bash
pip install --upgrade git+https://github.com/mit-han-lab/torchsparse.git@v1.4.0
```

If you use TorchSparse in your code, please remember to specify the exact version as your dependencies.

## Benchmark

We compare TorchSparse with [MinkowskiEngine](https://github.com/NVIDIA/MinkowskiEngine) (where the latency is measured on NVIDIA GTX 1080Ti):

|                          | MinkowskiEngine v0.4.3 | TorchSparse v1.0.0 |
| :----------------------- | :--------------------: | :----------------: |
| MinkUNet18C (MACs / 10)  |        224.7 ms        |      124.3 ms      |
| MinkUNet18C (MACs / 4)   |        244.3 ms        |      160.9 ms      |
| MinkUNet18C (MACs / 2.5) |        269.6 ms        |      214.3 ms      |
| MinkUNet18C              |        323.5 ms        |      294.0 ms      |

## Getting Started

### Sparse Tensor

Sparse tensor (`SparseTensor`) is the main data structure for point cloud, which has two data fields:

- Coordinates (`coords`): a 2D integer tensor with a shape of N x 4, where the first three dimensions correspond to quantized x, y, z coordinates, and the last dimension denotes the batch index.
- Features (`feats`): a 2D tensor with a shape of N x C, where C is the number of feature channels.

Most existing datasets provide raw point cloud data with float coordinates. We can use `sparse_quantize` (provided in `torchsparse.utils.quantize`) to voxelize x, y, z coordinates and remove duplicates:

```python
coords -= np.min(coords, axis=0, keepdims=True)
coords, indices = sparse_quantize(coords, voxel_size, return_index=True)
coords = torch.tensor(coords, dtype=torch.int)
feats = torch.tensor(feats[indices], dtype=torch.float)
tensor = SparseTensor(coords=coords, feats=feats)
```

We can then use `sparse_collate_fn` (provided in `torchsparse.utils.collate`) to assemble a batch of `SparseTensor`'s (and add the batch dimension to `coords`). Please refer to [this example](https://github.com/mit-han-lab/torchsparse/blob/dev/pre-commit/examples/example.py) for more details.

### Sparse Neural Network

The neural network interface in TorchSparse is very similar to PyTorch:

```python
from torch import nn
from torchsparse import nn as spnn

model = nn.Sequential(
    spnn.Conv3d(in_channels, out_channels, kernel_size),
    spnn.BatchNorm(out_channels),
    spnn.ReLU(True),
)
```

## Frequently Asked Questions
Before posting an issue, please go through the following troubleshooting steps:
- Check whether the issue is torchsparse specific or enviornment specific.
- Read the error logs closely - if it's a compilation error, the problem will be shown in the log. Often, compilation issues will come from incorrect enviornment (pytorch/nvcc) configuration, rather than incompatibility with this library.
- Try [completely uninstalling CUDA](https://askubuntu.com/q/530043) and make sure that there are no additional cuda installations:
  ```bash
  ls /usr/local/cuda* -d
  ```
- Then, follow **all** of the steps for toolkit installation in the [cuda installation guide](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html), especially the [post installation actions](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#post-installation-actions) to set your `LD_LIBRARY_PATH` and `PATH`.
- Ensure that pytorch and nvcc are using the same version of cuda: 

  ```bash
  nvcc --version
  python -c "import torch; print(torch.version.cuda);"
  ```
- If you're trying to cross compile the library (i.e. compiling for a different GPU than the one at build time, such as in a dockerfile), make use of the `TORCH_CUDA_ARCH_LIST` enviornmental variableYou can use [this chart](http://arnon.dk/matching-sm-architectures-arch-and-gencode-for-various-nvidia-cards/) to find your architecture/gencode. For example, if you want to compile for a Turing-architecture GPU, you would do:

  ```bash
  TORCH_CUDA_ARCH_LIST="7.0;7.5" pip install --upgrade git+https://github.com/mit-han-lab/torchsparse.git
  ```
- If you see `Killed` in the compilation log, it's likely the compilation failed due to out of memory as a result of parallel compilation. You can limit the number of CPUs the compiler will use by setting the `MAX_JOBS` enviornmental variable before installing:
  ```bash
  MAX_JOBS=2 pip install --upgrade git+https://github.com/mit-han-lab/torchsparse.git
  ```

## Citation

If you use TorchSparse in your research, please use the following BibTeX entry:

```bibtex
@inproceedings{tang2020searching,
  title = {{Searching Efficient 3D Architectures with Sparse Point-Voxel Convolution}},
  author = {Tang, Haotian and Liu, Zhijian and Zhao, Shengyu and Lin, Yujun and Lin, Ji and Wang, Hanrui and Han, Song},
  booktitle = {European Conference on Computer Vision (ECCV)},
  year = {2020}
}
```

## Acknowledgements

TorchSparse is inspired by many existing open-source libraries, including (but not limited to) [MinkowskiEngine](https://github.com/NVIDIA/MinkowskiEngine), [SECOND](https://github.com/traveller59/second.pytorch) and [SparseConvNet](https://github.com/facebookresearch/SparseConvNet).
