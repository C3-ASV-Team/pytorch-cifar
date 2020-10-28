#!/bin/bash
#SBATCH --qos=regular
#SBATCH --constraint=gpu
#SBATCH --nodes=1
#SBATCH --time=00:05:00
#SBATCH --mail-type=ALL
#SBATCH --cpus-per-task=10
#SBATCH --ntasks=1

module load pytorch/v1.5.0-gpu

srun python main.py

