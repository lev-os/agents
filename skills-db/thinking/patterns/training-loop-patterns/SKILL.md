---
name: training-loop-patterns
description: Ensure gradient zeroing happens before backward pass, not after. Verify forward pass returns tensors requiring gradients.
---

# Training Loop Patterns for Deep Learning

## What It Is
A collection of battle-tested architectural patterns and best practices for structuring the training loop in deep learning systems. The training loop is the core iterative process that feeds data through a model, computes loss, performs backpropagation, and updates weights. These patterns address common challenges: efficient data loading, proper gradient handling, model state management, checkpointing, and monitoring - going beyond the basic forward-backward-update cycle to production-grade implementations.

## When to Use It
- Building custom training pipelines beyond high-level frameworks
- Debugging training issues (exploding/vanishing gradients, slow convergence)
- Optimizing training throughput for large models or datasets
- Implementing custom training logic (curriculum learning, adversarial training)
- Transitioning from research prototype to production training system
- Need reproducibility and experiment tracking

## Execution Steps

### 1. Structure the Core Loop
Implement the canonical training loop structure with clear separation between data loading, forward pass, loss computation, backward pass, and optimization. This structure prevents common bugs and enables easy extension.

**Action**: Write skeleton code:
```
for epoch in range(num_epochs):
    for batch in dataloader:  # Iterate over mini-batches
        optimizer.zero_grad()  # Clear gradients from previous step
        outputs = model(batch.inputs)  # Forward pass
        loss = criterion(outputs, batch.targets)  # Compute loss
        loss.backward()  # Backward pass (compute gradients)
        optimizer.step()  # Update weights
```
Ensure gradient zeroing happens before backward pass, not after. Verify forward pass returns tensors requiring gradients.

### 2. Implement Efficient Data Loading
Use parallel data loading to prevent GPU starvation. The dataloader should prepare the next batch while the GPU processes the current one. Prefetching and worker processes dramatically improve throughput.

**Action**: Configure DataLoader with `num_workers=4-8` (CPU cores available), `pin_memory=True` (for CUDA), `prefetch_factor=2`. For very large datasets, use memory-mapped files or streaming from cloud storage. Monitor GPU utilization (should be >80%); low utilization indicates data loading bottleneck.

### 3. Handle Model and Optimizer State
Manage model training/evaluation modes correctly. Dropout and batch normalization behave differently during training vs inference. State management bugs cause silent performance degradation.

**Action**: Call `model.train()` at start of training loop, `model.eval()` before validation. Wrap validation code with `with torch.no_grad():` to prevent gradient computation (saves memory, speeds up evaluation). Save optimizer state in checkpoints, not just model weights, to resume training seamlessly.

### 4. Implement Gradient Clipping and Accumulation
Prevent exploding gradients with clipping; accumulate gradients to simulate larger batch sizes when GPU memory is limited. These patterns stabilize training and enable training large models on limited hardware.

**Action**: Add `torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)` after `loss.backward()` and before `optimizer.step()`. For gradient accumulation: skip `optimizer.zero_grad()` and `optimizer.step()` for N-1 steps, call them only every N steps. Scale loss by 1/N to maintain effective learning rate.

### 5. Add Checkpointing and Logging
Save model checkpoints periodically and log metrics for monitoring. Production systems need recovery from failures and visibility into training dynamics.

**Action**: Save checkpoint every K epochs or when validation loss improves: `torch.save({'epoch': epoch, 'model_state': model.state_dict(), 'optimizer_state': optimizer.state_dict(), 'loss': loss}, path)`. Log training loss, validation loss, learning rate, throughput (samples/sec) every N batches. Use TensorBoard, Weights & Biases, or MLflow for visualization.

### 6. Validate and Monitor
Implement validation loop mirroring training structure but without gradient computation. Monitor for overfitting (train loss << val loss) and other pathologies (NaN losses, dead neurons).

**Action**: After each epoch, run validation:
```
model.eval()
with torch.no_grad():
    for batch in val_dataloader:
        outputs = model(batch.inputs)
        val_loss = criterion(outputs, batch.targets)
```
Track: training loss (should decrease), validation loss (should decrease then plateau), train/val gap (should stay reasonable), gradient norms (detect exploding/vanishing), learning rate (if using scheduler).

## Real-World Applications

**Computer Vision Training**
- ImageNet training: Mixed precision (FP16) with gradient scaling to reduce memory and speed up training
- Object detection: Multi-scale training by varying input resolution across epochs
- Data augmentation in training loop: random crops, flips, color jitter applied on-the-fly

**Natural Language Processing**
- Transformer training: Gradient accumulation to simulate large batch sizes (effective batch size 512K+ for GPT-3)
- Dynamic padding: Batch together sequences of similar length to minimize padding overhead
- Learning rate warmup: Gradually increase LR for first few thousand steps to stabilize training

**Reinforcement Learning**
- Policy gradient methods: Custom training loop alternating between environment interaction and model updates
- Experience replay: Sample batches from replay buffer instead of sequential data
- Target network updates: Periodic copy of online network to target network (DQN pattern)

**Production Systems**
- Distributed training: Data parallel or model parallel patterns with gradient synchronization
- Mixed precision training: FP16 compute with FP32 master weights and loss scaling
- Checkpointing: Save every N hours (wall-clock time) to resume interrupted training

## Anti-Patterns

**Forgetting to zero gradients** → Gradients accumulate across iterations, causing incorrect weight updates and divergence.

**Using model.eval() during training** → Disables dropout and batch norm updating, model doesn't learn properly.

**Not using torch.no_grad() during validation** → Wastes memory storing gradients that are never used, may cause OOM errors.

**Gradient computation on every sample** → Use mini-batches (batch_size=32-256); single-sample updates are noisy and slow.

**Ignoring data loading bottlenecks** → GPU sits idle waiting for data; monitor GPU utilization, increase num_workers.

**Saving only model weights** → Can't resume training properly; always save optimizer state, epoch counter, RNG state for reproducibility.

## Success Metrics
- GPU utilization >85% during training (measured with nvidia-smi or profiler)
- Training loss decreases smoothly without spikes or plateaus
- Validation loss tracks training loss without severe overfitting (gap <20% of train loss)
- Throughput (samples/second) matches or exceeds baseline implementations
- Training completes within time budget (hours to days, not weeks)
- Checkpointing and resumption work correctly (loss continues from same value)

## Related Frameworks
- **Learning Rate Scheduling**: Techniques for adjusting LR during training (step decay, cosine annealing, warmup)
- **Data Augmentation Strategies**: On-the-fly transformations to increase effective dataset size
- **Mixed Precision Training**: Using FP16/BF16 for speed and memory efficiency
- **Distributed Training Patterns**: Data parallel, model parallel, pipeline parallel for multi-GPU training

## Common Pitfalls
- Not shuffling training data each epoch (model learns order artifacts)
- Using too large learning rate (loss explodes) or too small (converges slowly or gets stuck)
- Batch normalization with batch_size=1 (statistics computed on single sample are meaningless)
- Evaluating on training set instead of validation set (overfitting goes undetected)
- Not seeding RNG (results not reproducible across runs)
- Memory leaks from retaining graph references (detach tensors when storing metrics)
- Training on CPU when GPU is available (10-100x slower)

## Tools & Resources
- **Frameworks**: PyTorch, TensorFlow/Keras, JAX/Flax with built-in training loop utilities
- **Profiling**: PyTorch Profiler, NVIDIA Nsight, TensorBoard profiler for bottleneck identification
- **Experiment Tracking**: Weights & Biases, MLflow, Neptune.ai, TensorBoard for logging and visualization
- **Tutorials**: PyTorch official tutorials (pytorch.org/tutorials), Fast.ai course, Deep Learning Tuning Playbook (Google)
- **Monitoring**: wandb.watch() for gradient/weight histograms, torchinfo for model summary

## Code Pattern Template (PyTorch)

```python
# Setup
model.train()
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)

for epoch in range(num_epochs):
    # Training
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)

        optimizer.zero_grad()  # Clear gradients
        output = model(data)  # Forward pass
        loss = criterion(output, target)  # Compute loss
        loss.backward()  # Backward pass

        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)  # Gradient clipping
        optimizer.step()  # Update weights

        # Logging
        if batch_idx % log_interval == 0:
            print(f'Epoch: {epoch}, Batch: {batch_idx}, Loss: {loss.item():.4f}')

    scheduler.step()  # Update learning rate

    # Validation
    model.eval()
    val_loss = 0
    with torch.no_grad():
        for data, target in val_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            val_loss += criterion(output, target).item()

    val_loss /= len(val_loader)
    print(f'Validation Loss: {val_loss:.4f}')

    # Checkpointing
    if val_loss < best_val_loss:
        best_val_loss = val_loss
        torch.save({
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'loss': val_loss,
        }, 'checkpoint.pth')

    model.train()  # Back to training mode
```

---
*Framework Type*: Implementation Pattern
*Domain*: Deep Learning, Machine Learning Engineering
*Practitioner Score*: 9/10 - Essential for anyone training neural networks beyond toy examples
*Complexity*: Medium - Straightforward concept but many subtle details for production quality
*Prerequisites*: PyTorch or TensorFlow basics, backpropagation understanding, Python programming
