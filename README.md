# Tutorial: Train CIFAR10 with PyTorch on NERSC Cori-GPU

Here is a tutorial how to train deep learning models on the CIFAR10 dataset on Cori-GPU platform using [PyTorch](http://pytorch.org/).

## Submit an interactive job

First you'd need to request one or more GPU using the following script. See [this page](https://docs-dev.nersc.gov/cgpu/access/) for further details.

```sh
module load cgpu
salloc -C gpu -N 1 -t 60 -c 10 -G 1 -A m3691
```

Then run the following commands to kick off training.

```sh
module load pytorch/v1.5.0-gpu
srun python main.py
```

## Submit a batch job

Run the following commands for submitting a batch job.

```sh
sbatch train_cgpu.sh
```

The dashboard on `my.nersc.gov` sometimes cannot correctly display jobs running on the GPU cluster, so a better way is to run `jobstats` in the terminal to view the job status. When the job starts running, its status will change from `PENDING` to `RUNNING`.

In the batch mode, the results will be redirected to `<job_id>.out`, under your working directory by default.

## Continuously training on NERSC

Run the following command for continuously training on NERSC

```sh
python -u train_nersc.py --name cifar --interval 60 > cifar.log &
```

The interval is # minutes between two status checking for re-launch. `-u` to force no buffering.

To quickly test the script's validity, try setting time in `train_cgpu.sh` to be 3 minutes and run

```sh
python train_nersc.py --interval 1
```

You can build your own script based on this one.

---

## Prerequisites

- Python 3.6+
- PyTorch 1.0+

## Accuracy

| Model                                                | Acc.   |
| ---------------------------------------------------- | ------ |
| [VGG16](https://arxiv.org/abs/1409.1556)             | 92.64% |
| [ResNet18](https://arxiv.org/abs/1512.03385)         | 93.02% |
| [ResNet50](https://arxiv.org/abs/1512.03385)         | 93.62% |
| [ResNet101](https://arxiv.org/abs/1512.03385)        | 93.75% |
| [RegNetX_200MF](https://arxiv.org/abs/2003.13678)    | 94.24% |
| [RegNetY_400MF](https://arxiv.org/abs/2003.13678)    | 94.29% |
| [MobileNetV2](https://arxiv.org/abs/1801.04381)      | 94.43% |
| [ResNeXt29(32x4d)](https://arxiv.org/abs/1611.05431) | 94.73% |
| [ResNeXt29(2x64d)](https://arxiv.org/abs/1611.05431) | 94.82% |
| [DenseNet121](https://arxiv.org/abs/1608.06993)      | 95.04% |
| [PreActResNet18](https://arxiv.org/abs/1603.05027)   | 95.11% |
| [DPN92](https://arxiv.org/abs/1707.01629)            | 95.16% |

## Learning rate adjustment

I manually change the `lr` during training:

- `0.1` for epoch `[0,150)`
- `0.01` for epoch `[150,250)`
- `0.001` for epoch `[250,350)`

Resume the training with `python main.py --resume --lr=0.01`
