#!/bin/bash -l        
#SBATCH --time=15:00:00
#SBATCH --mem=10g
#SBATCH --tmp=10g
#SBATCH --mail-type=ALL  
#SBATCH --mail-user=lmoore@umn.edu
#SBATCH -o logs/audit_%A_%a.out
#SBATCH -e logs/audit_%A_%a.err
#SBATCH -J miran-disk-audit

python3 disk_audit_LM.py /home/miran045/shared