import torch

print("✅ Torch version:", torch.__version__)
print("⚙️ CUDA version:", torch.version.cuda)
print("📦 GPU available:", torch.cuda.is_available())
print("💻 Device:", torch.cuda.get_device_name(0))
