"""
Debug Script for ViT5 (Vision Transformer) - Encoder-Decoder Model for Vietnamese

This script provides a detailed analysis of the ViT5 architecture, comparing
base and large variants, and demonstrating tokenization, forward pass, and
generation capabilities.

Author: Generated for ViT5 Learning
Date: 2026-04-25
"""

import torch
import transformers
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import sys

# =============================================================================
# SECTION 1: IMPORT AND VERIFICATION
# =============================================================================

print("=" * 80)
print("SECTION 1: IMPORT AND ENVIRONMENT VERIFICATION")
print("=" * 80)

# Print library versions
print(f"Python version: {sys.version}")
print(f"PyTorch version: {torch.__version__}")
print(f"Transformers version: {transformers.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"CUDA device: {torch.cuda.get_device_name(0)}")
print()

# =============================================================================
# SECTION 2: LOAD MODELS AND TOKENIZERS
# =============================================================================

print("=" * 80)
print("SECTION 2: LOADING MODELS AND TOKENIZERS")
print("=" * 80)

# Define model paths
MODEL_BASE = "VietAI/vit5-base"
MODEL_LARGE = "VietAI/vit5-large"

print(f"Loading tokenizer from {MODEL_BASE}...")
try:
    tokenizer_base = AutoTokenizer.from_pretrained(MODEL_BASE)
    print(f"✓ Tokenizer loaded successfully")
except Exception as e:
    print(f"✗ Error loading tokenizer: {e}")
    sys.exit(1)

print(f"\nLoading model from {MODEL_BASE}...")
try:
    model_base = AutoModelForSeq2SeqLM.from_pretrained(MODEL_BASE)
    print(f"✓ Model loaded successfully")
except Exception as e:
    print(f"✗ Error loading model: {e}")
    sys.exit(1)

# Try loading large model (may require more memory)
print(f"\nAttempting to load tokenizer from {MODEL_LARGE}...")
try:
    tokenizer_large = AutoTokenizer.from_pretrained(MODEL_LARGE)
    print(f"✓ Large tokenizer loaded successfully")
    print(f"Loading model from {MODEL_LARGE}...")
    model_large = AutoModelForSeq2SeqLM.from_pretrained(MODEL_LARGE)
    print(f"✓ Large model loaded successfully")
    large_available = True
except Exception as e:
    print(f"⚠ Large model not available: {e}")
    large_available = False
    tokenizer_large = None
    model_large = None

print()

# =============================================================================
# SECTION 3: MODEL CONFIGURATION DETAILS
# =============================================================================

print("=" * 80)
print("SECTION 3: MODEL CONFIGURATION ANALYSIS")
print("=" * 80)

def print_model_config(model, model_name, config_source):
    """Print detailed configuration of a ViT5 model."""
    config = model.config
    print(f"\n{model_name} Configuration (from {config_source}):")
    print("-" * 40)
    
    # Encoder configuration
    print("  Encoder:")
    print(f"    - Number of layers: {config.encoder_layers}")
    print(f"    - Hidden size (d_model): {config.d_model}")
    print(f"    - Number of attention heads: {config.encoder_attention_heads}")
    print(f"    - Feedforward dimension: {config.encoder_ffn_dim}")
    print(f"    - Dropout: {config.encoder_dropout if hasattr(config, 'encoder_dropout') else config.dropout_rate}")
    
    # Decoder configuration
    print("  Decoder:")
    print(f"    - Number of layers: {config.decoder_layers}")
    print(f"    - Hidden size (d_model): {config.d_model}")
    print(f"    - Number of attention heads: {config.decoder_attention_heads}")
    print(f"    - Feedforward dimension: {config.decoder_ffn_dim}")
    print(f"    - Dropout: {config.decoder_dropout if hasattr(config, 'decoder_dropout') else config.dropout_rate}")
    
    # Shared configuration
    print("  Shared:")
    print(f"    - Vocabulary size: {config.vocab_size}")
    print(f"    - Maximum position embeddings: {config.max_position_embeddings if hasattr(config, 'max_position_embeddings') else 'N/A'}")
    print(f"    - Attention type: {config.attention_type if hasattr(config, 'attention_type') else 'standard'}")
    print(f"    - Activation function: {config.activation_function if hasattr(config, 'activation_function') else 'relu/gelu'}")
    print(f"    - Layer normalization epsilon: {config.layer_norm_eps if hasattr(config, 'layer_norm_eps') else 1e-6}")
    print(f"    - Use cache: {config.use_cache if hasattr(config, 'use_cache') else True}")
    
    # Architecture details
    print("  Architecture Type:")
    print(f"    - Model type: {config.model_type}")
    print(f"    - Is encoder-decoder: {config.is_encoder_decoder}")
    print(f"    - Tie word embeddings: {config.tie_word_embeddings}")

def calculate_total_params(model):
    """Calculate total number of parameters in the model."""
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    return total_params, trainable_params

# Print base model configuration
print_model_config(model_base, "ViT5-base")
total_base, trainable_base = calculate_total_params(model_base)
print(f"\n  Parameters:")
print(f"    - Total parameters: {total_base:,} ({total_base/1e6:.2f}M)")
print(f"    - Trainable parameters: {trainable_base:,} ({trainable_base/1e6:.2f}M)")

# Print large model configuration if available
if large_available and model_large:
    print_model_config(model_large, "ViT5-large")
    total_large, trainable_large = calculate_total_params(model_large)
    print(f"\n  Parameters:")
    print(f"    - Total parameters: {total_large:,} ({total_large/1e6:.2f}M)")
    print(f"    - Trainable parameters: {trainable_large:,} ({trainable_large/1e6:.2f}M)")
    
    # Comparison
    print(f"\n  Comparison (Large vs Base):")
    print(f"    - Parameter ratio: {total_large/total_base:.2f}x")
    print(f"    - Layer ratio: {model_large.config.encoder_layers + model_large.config.decoder_layers}/{model_base.config.encoder_layers + model_base.config.decoder_layers} = {(model_large.config.encoder_layers + model_large.config.decoder_layers)/(model_base.config.encoder_layers + model_base.config.decoder_layers):.1f}x")
    print(f"    - Hidden size ratio: {model_large.config.d_model/model_base.config.d_model:.1f}x")

print()

# =============================================================================
# SECTION 4: SPECIAL TOKENS
# =============================================================================

print("=" * 80)
print("SECTION 4: SPECIAL TOKENS")
print("=" * 80)

def print_special_tokens(tokenizer, model_name):
    """Display special tokens used by the tokenizer."""
    print(f"\n{model_name} Special Tokens:")
    print("-" * 40)
    print(f"  Pad token: '{tokenizer.pad_token}' (ID: {tokenizer.pad_token_id})")
    print(f"  Unknown token: '{tokenizer.unk_token}' (ID: {tokenizer.unk_token_id})")
    print(f"  BOS token: '{tokenizer.bos_token}' (ID: {tokenizer.bos_token_id if hasattr(tokenizer, 'bos_token_id') else 'N/A'})")
    print(f"  EOS token: '{tokenizer.eos_token}' (ID: {tokenizer.eos_token_id if hasattr(tokenizer, 'eos_token_id') else 'N/A'})")
    print(f"  Decoder start token: '{tokenizer.decoder_start_token}' (ID: {tokenizer.decoder_start_token_id})")
    
    # Additional special tokens
    additional_tokens = set(tokenizer.additional_special_tokens)
    if additional_tokens:
        print(f"  Additional special tokens:")
        for token in additional_tokens:
            print(f"    - '{token}' (ID: {tokenizer.convert_tokens_to_ids(token)})")
    
    print(f"\n  Vocabulary sample (first 20 tokens):")
    vocab = tokenizer.get_vocab()
    for i, (token, idx) in enumerate(sorted(vocab.items(), key=lambda x: x[1])[:20]):
        print(f"    {idx:5d}: '{token}'")

print_special_tokens(tokenizer_base, "ViT5-base")
if large_available and tokenizer_large:
    print_special_tokens(tokenizer_large, "ViT5-large")

print()

# =============================================================================
# SECTION 5: TOKENIZATION DEMO
# =============================================================================

print("=" * 80)
print("SECTION 5: TOKENIZATION DEMO")
print("=" * 80)

# Vietnamese test sentences
vn_sentences = [
    "Chào bạn, tôi là một người Việt Nam.",
    "Trí tuệ nhân tạo đang phát triển rất nhanh.",
    "Mô hình ViT5 là một biến thể của T5 dành cho tiếng Việt.",
    "Hôm nay thời tiết đẹp quá, chúng ta đi dạo nhé!",
]

print("\nTokenization examples:")
print("-" * 40)

for sentence in vn_sentences:
    print(f"\n  Original text: \"{sentence}\"")
    
    # Tokenize with base model
    tokens_base = tokenizer_base(sentence, return_tensors="pt", padding=False)
    print(f"  Base tokenizer:")
    print(f"    - Input IDs: {tokens_base['input_ids'].tolist()[0]}")
    print(f"    - Attention mask: {tokens_base['attention_mask'].tolist()[0]}")
    print(f"    - Number of tokens: {len(tokens_base['input_ids'][0])}")
    
    # Decode back
    decoded_base = tokenizer_base.decode(tokens_base['input_ids'][0], skip_special_tokens=False)
    print(f"    - Decoded: \"{decoded_base}\"")
    
    # Show token strings
    token_ids = tokens_base['input_ids'][0].tolist()
    token_strings = [tokenizer_base.decode([tid]) for tid in token_ids]
    print(f"    - Token breakdown: {' | '.join(token_strings)}")
    
    if large_available:
        tokens_large = tokenizer_large(sentence, return_tensors="pt", padding=False)
        print(f"  Large tokenizer:")
        print(f"    - Number of tokens: {len(tokens_large['input_ids'][0])}")

print()

# =============================================================================
# SECTION 6: MODEL ARCHITECTURE VISUALIZATION
# =============================================================================

print("=" * 80)
print("SECTION 6: MODEL ARCHITECTURE VISUALIZATION")
print("=" * 80)

def print_model_architecture(model, model_name):
    """Print detailed architecture of the model."""
    print(f"\n{model_name} Architecture:")
    print("-" * 40)
    print("[Input]")
    print("  ↓")
    print("  [Embeddings]")
    print(f"    - Token Embeddings: {model.shared.num_embeddings} tokens × {model.config.d_model} dims")
    print(f"    - Positional Embeddings: {model.encoder.embed_positions.num_embeddings} positions")
    
    # Encoder layers
    print(f"  ↓")
    print(f"  [Encoder: {config.encoder_layers} layers]")
    for i, layer in enumerate(model.encoder.layers[:2]):  # Show first 2 layers
        print(f"    - Layer {i}: Self-Attention + FeedForward")
        print(f"      • Self-attn heads: {layer.self_attn.num_heads}")
        print(f"      • Attention dim: {layer.self_attn.embed_dim}")
        print(f"      • FeedForward in: {layer.fc1.in_features} → out: {layer.fc1.out_features}")
    if len(model.encoder.layers) > 2:
        print(f"    ... ({len(model.encoder.layers) - 2} more layers)")
        last_layer = model.encoder.layers[-1]
        print(f"    - Layer {len(model.encoder.layers)-1}: Self-Attention + FeedForward")
        print(f"      • Self-attn heads: {last_layer.self_attn.num_heads}")
        print(f"      • FeedForward in: {last_layer.fc1.in_features} → out: {last_layer.fc1.out_features}")
    
    print(f"  ↓")
    print(f"  [Decoder: {config.decoder_layers} layers]")
    for i, layer in enumerate(model.decoder.layers[:2]):  # Show first 2 layers
        print(f"    - Layer {i}: Self-Attn + Cross-Attn + FeedForward")
        print(f"      • Self-attn heads: {layer.self_attn.num_heads}")
        print(f"      • Cross-attn heads: {layer.encoder_attn.num_heads}")
    if len(model.decoder.layers) > 2:
        print(f"    ... ({len(model.decoder.layers) - 2} more layers)")
    
    print(f"  ↓")
    print(f"  [Output Projection]")
    print(f"    - Linear layer: {config.d_model} → {config.vocab_size}")
    print(f"  ↓")
    print(f"  [Output Logits]")

# Print base architecture
print_model_architecture(model_base, "ViT5-base")

if large_available and model_large:
    print_model_architecture(model_large, "ViT5-large")

print()

# =============================================================================
# SECTION 7: FORWARD PASS DEMO
# =============================================================================

print("=" * 80)
print("SECTION 7: FORWARD PASS DEMO")
print("=" * 80)

# Set model to eval mode
model_base.eval()

# Prepare input
input_text = "Mô hình ViT5 rất thú vị."
inputs = tokenizer_base(input_text, return_tensors="pt")

print(f"\nInput text: \"{input_text}\"")
print(f"Input IDs shape: {inputs['input_ids'].shape}")
print(f"Attention mask shape: {inputs['attention_mask'].shape}")

# Forward pass
with torch.no_grad():
    outputs = model_base(
        input_ids=inputs['input_ids'],
        attention_mask=inputs['attention_mask'],
        decoder_input_ids=inputs['input_ids'],  # Use same for simplicity
        output_attentions=True,
        output_hidden_states=False
    )

print(f"\nOutputs:")
print(f"  - Logits shape: {outputs.logits.shape}")
print(f"    (batch_size=1, sequence_length={outputs.logits.shape[1]}, vocab_size={outputs.logits.shape[2]})")
print(f"  - Number of encoder attentions: {len(outputs.encoder_attentions)}")
print(f"  - Number of decoder attentions: {len(outputs.decoder_attentions)}")
print(f"  - Number of cross attentions: {len(outputs.cross_attentions)}")

# Get predictions
predictions = torch.argmax(outputs.logits, dim=-1)
print(f"\nPredicted token IDs: {predictions[0].tolist()}")
print(f"Number of predicted tokens: {len(predictions[0])}")

try:
    predicted_text = tokenizer_base.decode(predictions[0], skip_special_tokens=True)
    print(f"Predicted text: \"{predicted_text}\"")
except:
    print("Could not decode predicted text")

print()

# =============================================================================
# SECTION 8: GENERATION DEMO
# =============================================================================

print("=" * 80)
print("SECTION 8: TEXT GENERATION DEMO")
print("=" * 80)

generation_tasks = [
    {
        "task": "Summarization",
        "prompt": "Tóm tắt: Việt Nam là một quốc gia đẹp với nhiều danh lam thắng cảnh nổi tiếng. Từ vịnh Hạ Long hùng vĩ đến phố cổ Hội An yên bình, từ ruộng bậc thang Sa Pa đến bãi biển Đà Nẵng, Việt Nam có rất nhiều điểm đến hấp dẫn dành cho du khách trong và ngoài nước.",
        "max_length": 50,
        "min_length": 20,
    },
    {
        "task": "Translation (Vietnamese to English)",
        "prompt": "Dịch sang tiếng Anh: Tôi thích học công nghệ thông tin và trí tuệ nhân tạo.",
        "max_length": 50,
        "min_length": 10,
    },
    {
        "task": "Question Answering",
        "prompt": "Câu hỏi: Thủ đô của Việt Nam là đâu? Câu trả lời:",
        "max_length": 30,
        "min_length": 5,
    },
]

print("\nGeneration examples using ViT5-base:")
print("-" * 40)

model_base.eval()

for i, task in enumerate(generation_tasks, 1):
    print(f"\n{i}. {task['task']}")
    print(f"   Input: \"{task['prompt']}\"")
    
    # Tokenize input
    inputs = tokenizer_base(task['prompt'], return_tensors="pt", padding=True)
    
    # Generate output
    with torch.no_grad():
        generated_ids = model_base.generate(
            input_ids=inputs['input_ids'],
            attention_mask=inputs['attention_mask'],
            max_length=task['max_length'],
            min_length=task['min_length'],
            num_beams=4,
            early_stopping=True,
            do_sample=False,
            pad_token_id=tokenizer_base.pad_token_id,
            eos_token_id=tokenizer_base.eos_token_id,
        )
    
    # Decode output
    output_text = tokenizer_base.decode(generated_ids[0], skip_special_tokens=True)
    print(f"   Output: \"{output_text}\"")

print()

# =============================================================================
# SECTION 9: BASE VS LARGE COMPARISON
# =============================================================================

print("=" * 80)
print("SECTION 9: BASE VS LARGE MODEL COMPARISON")
print("=" * 80)

if large_available and model_large:
    print("\nDetailed Comparison:")
    print("-" * 40)
    
    # Configuration comparison
    config_base = model_base.config
    config_large = model_large.config
    
    print(f"{'Parameter':<30} {'Base':<15} {'Large':<15} {'Ratio'}")
    print("-" * 65)
    print(f"{'d_model (hidden size)':<30} {config_base.d_model:<15} {config_large.d_model:<15} {config_large.d_model/config_base.d_model:.1f}x")
    print(f"{'Encoder layers':<30} {config_base.encoder_layers:<15} {config_large.encoder_layers:<15} {config_large.encoder_layers/config_base.encoder_layers:.1f}x")
    print(f"{'Decoder layers':<30} {config_base.decoder_layers:<15} {config_large.decoder_layers:<15} {config_large.decoder_layers/config_base.decoder_layers:.1f}x")
    print(f"{'Encoder attention heads':<30} {config_base.encoder_attention_heads:<15} {config_large.encoder_attention_heads:<15} {config_large.encoder_attention_heads/config_base.encoder_attention_heads:.1f}x")
    print(f"{'Decoder attention heads':<30} {config_base.decoder_attention_heads:<15} {config_large.decoder_attention_heads:<15} {config_large.decoder_attention_heads/config_base.decoder_attention_heads:.1f}x")
    print(f"{'Encoder FFN dim':<30} {config_base.encoder_ffn_dim:<15} {config_large.encoder_ffn_dim:<15} {config_large.encoder_ffn_dim/config_base.encoder_ffn_dim:.1f}x")
    print(f"{'Decoder FFN dim':<30} {config_base.decoder_ffn_dim:<15} {config_large.decoder_ffn_dim:<15} {config_large.decoder_ffn_dim/config_base.decoder_ffn_dim:.1f}x")
    
    print(f"\n{'Total Parameters':<30} {total_base/1e6:<15.1f}M {total_large/1e6:<15.1f}M {total_large/total_base:.2f}x")
    print(f"{'Trainable Parameters':<30} {trainable_base/1e6:<15.1f}M {trainable_large/1e6:<15.1f}M {trainable_large/trainable_base:.2f}x")
    
    # Memory usage estimate
    memory_base = total_base * 4 / (1024**3)  # FP32
    memory_large = total_large * 4 / (1024**3)  # FP32
    print(f"\n{'Estimated Memory (FP32)':<30} {memory_base:<15.2f}GB {memory_large:<15.2f}GB {memory_large/memory_base:.2f}x")
    
    # Generation comparison on a sample task
    print(f"\nGeneration Speed Comparison:")
    print("-" * 40)
    
    test_prompt = "Tóm tắt: Việt Nam có văn hóa ẩm thực phong phú và đa dạng."
    
    import time
    
    # Base model generation
    inputs = tokenizer_base(test_prompt, return_tensors="pt")
    
    # Warm up
    _ = model_base.generate(**inputs, max_length=20)
    
    # Measure base
    start = time.time()
    output_base = model_base.generate(
        **inputs, 
        max_length=30,
        num_beams=4,
        early_stopping=True
    )
    time_base = time.time() - start
    
    output_text_base = tokenizer_base.decode(output_base[0], skip_special_tokens=True)
    
    print(f"  Base model time: {time_base:.3f}s")
    print(f"  Base output: \"{output_text_base}\"")
    
    # Large model generation
    inputs_large = tokenizer_large(test_prompt, return_tensors="pt")
    model_large.eval()
    
    # Warm up
    _ = model_large.generate(**inputs_large, max_length=20)
    
    # Measure large
    start = time.time()
    output_large = model_large.generate(
        **inputs_large, 
        max_length=30,
        num_beams=4,
        early_stopping=True
    )
    time_large = time.time() - start
    
    output_text_large = tokenizer_large.decode(output_large[0], skip_special_tokens=True)
    
    print(f"  Large model time: {time_large:.3f}s")
    print(f"  Large output: \"{output_text_large}\"")
    print(f"  Time ratio: {time_large/time_base:.2f}x")
    
else:
    print("\nLarge model not available for comparison.")
    print("Note: Large model requires more memory (typically 16GB+ GPU VRAM).")

print()

# =============================================================================
# SECTION 10: CONCLUSION
# =============================================================================

print("=" * 80)
print("SECTION 10: KEY OBSERVATIONS")
print("=" * 80)

print("""
ViT5 Architecture Summary:
--------------------------
1. Encoder-Decoder Structure: ViT5 follows the T5 architecture with separate
   encoder and decoder stacks, making it suitable for various NLP tasks.

2. Self-Attention Mechanism: Each layer uses multi-head self-attention to
   capture complex dependencies in input sequences.

3. Cross-Attention: Decoder layers include cross-attention to encoder outputs,
   allowing the model to attend to input information during generation.

4. Feed-Forward Networks: Position-wise feed-forward networks transform
   attention outputs with non-linear activations (typically gated-GELU).

5. Parameter Scaling: ViT5-large has ~4x more parameters than ViT5-base,
   with larger hidden size (1024 vs 768), more layers (24 vs 12), and
   more attention heads (16 vs 12).

6. Vocabulary: Both models share the same vocabulary size (32000) based on
   SentencePiece tokenizer, optimized for Vietnamese text.

7. Generation Capabilities: The models support beam search, sampling, and
   various decoding strategies for tasks like summarization, translation,
   and text generation.

8. Special Tokens: Include pad, unk, bos, eos, and decoder_start tokens
   essential for sequence-to-sequence modeling.

Use Cases:
----------
- Text Summarization
- Machine Translation
- Question Answering
- Text Generation
- Text Classification (with appropriate prompts)

Performance Considerations:
---------------------------
- Base model: Suitable for most applications with limited resources
- Large model: Better quality but requires significantly more memory
- Both models can run on CPU for inference but benefit from GPU acceleration
""")

print("\n" + "=" * 80)
print("DEBUG SCRIPT COMPLETE")
print("=" * 80)