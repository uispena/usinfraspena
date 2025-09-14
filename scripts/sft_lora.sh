#!/usr/bin/env bash
set -euo pipefail
MODEL="TinyLlama/TinyLlama-1.1B-Chat-v1.0"
OUT="models/lora/kubeaid-tinyllama"
accelerate launch -m trl.sft_trainer \
  --model_name $MODEL \
  --dataset_format chatml \
  --train_file data/sft/k8s_admin.jsonl \
  --output_dir $OUT \
  --per_device_train_batch_size 4 \
  --gradient_accumulation_steps 4 \
  --learning_rate 2e-4 \
  --logging_steps 20 \
  --save_steps 200 \
  --num_train_epochs 1 \
  --packing True \
  --use_peft True \
  --lora_r 16 --lora_alpha 32 --lora_dropout 0.05 \
  --load_in_4bit True --bnb_4bit_compute_dtype bfloat16
echo "LoRA saved to $OUT"
