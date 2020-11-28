#!/bin/bash
#SBATCH --qos=regular
#SBATCH --constraint=gpu
#SBATCH --nodes=1
#SBATCH --gpus=1
#SBATCH --time=00:03:00
#SBATCH --cpus-per-task=10
#SBATCH --ntasks=1

##SBATCH --mail-type=ALL
#SBATCH --output=%j-%x.%u.out
#SBATCH --job-name=cifar

module load pytorch/v1.5.0-gpu
## conda activate env_name

srun python main.py $1
