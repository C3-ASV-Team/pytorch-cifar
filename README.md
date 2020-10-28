# Tutorial: Train CIFAR10 with PyTorch on NERSC Cori-GPU

Here is a tutorial how to train deep learning models on the CIFAR10 dataset on Cori-GPU platform using [PyTorch](http://pytorch.org/).

## Submit interactive job

First you'd need to request one or more GPU using the following script. See [this page](https://docs-dev.nersc.gov/cgpu/access/) for further details.
```
module load esslurm
salloc -C gpu -N 1 -t 60 -c 10 -G 1 -A m3691
```
Then run the following commands to kick off training.
```
module load pytorch-1.5.0/gpu
srun python main.py
```

## Submit batch job
Run the following commands for submitting a batch job.
```
sbatch train_cgpu.sh
```

---
## Prerequisites
- Python 3.6+
- PyTorch 1.0+

## Accuracy
| Model             | Acc.        |
| ----------------- | ----------- |
| [VGG16](https://arxiv.org/abs/1409.1556)              | 92.64%      |
| [ResNet18](https://arxiv.org/abs/1512.03385)          | 93.02%      |
| [ResNet50](https://arxiv.org/abs/1512.03385)          | 93.62%      |
| [ResNet101](https://arxiv.org/abs/1512.03385)         | 93.75%      |
| [RegNetX_200MF](https://arxiv.org/abs/2003.13678)     | 94.24%      |
| [RegNetY_400MF](https://arxiv.org/abs/2003.13678)     | 94.29%      |
| [MobileNetV2](https://arxiv.org/abs/1801.04381)       | 94.43%      |
| [ResNeXt29(32x4d)](https://arxiv.org/abs/1611.05431)  | 94.73%      |
| [ResNeXt29(2x64d)](https://arxiv.org/abs/1611.05431)  | 94.82%      |
| [DenseNet121](https://arxiv.org/abs/1608.06993)       | 95.04%      |
| [PreActResNet18](https://arxiv.org/abs/1603.05027)    | 95.11%      |
| [DPN92](https://arxiv.org/abs/1707.01629)             | 95.16%      |

## Learning rate adjustment
I manually change the `lr` during training:
- `0.1` for epoch `[0,150)`
- `0.01` for epoch `[150,250)`
- `0.001` for epoch `[250,350)`

Resume the training with `python main.py --resume --lr=0.01`
