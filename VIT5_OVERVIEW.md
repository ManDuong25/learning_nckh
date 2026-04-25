# ViT5 (Vietnamese Text-to-Text Transfer Transformer) - Tổng Quan Đầy Đủ

## 1. Giới Thiệu Tổng Quát

**ViT5** là mô hình Transformer-based encoder-decoder được pretrain dành riêng cho tiếng Việt, dựa trên kiến trúc **T5 (Text-to-Text Transfer Transformer)** của Google. Được phát triển bởi **VietAI** (tổ chức phi lợi nhuận), ViT5 là state-of-the-art cho các tác vụ sinh văn bản tiếng Việt.

**Paper**: [ViT5: Pretrained Text-to-Text Transformer for Vietnamese Language Generation](https://arxiv.org/abs/2205.06457)

---

## 2. Các Phiên Bản ViT5

### 2.1 Pretrained Models (Chính)

#### **ViT5-Base**
- **HuggingFace**: [VietAI/vit5-base](https://huggingface.co/VietAI/vit5-base)
- **Checkpoint**: 1,000,000 steps
- **Dataset**: CC100 (Vietnamese portion)
- **Thông số kỹ thuật**:
  ```
  Embedding dimension (d_model): 768
  Encoder layers: 12
  Decoder layers: 12
  Attention heads: 12
  Head dimension: 64
  Feed-forward dimension: 3072
  Activation: ReLU
  Vocabulary size: 36,096 (SentencePiece)
  Total parameters: ~220M
  ```

#### **ViT5-Large**
- **HuggingFace**: [VietAI/vit5-large](https://huggingface.co/VietAI/vit5-large)
- **Checkpoint**: 1,500,000 steps
- **Dataset**: CC100 (Vietnamese portion)
- **Thông số kỹ thuật**:
  ```
  Embedding dimension (d_model): 1024
  Encoder layers: 24
  Decoder layers: 24
  Attention heads: 16
  Head dimension: 64
  Feed-forward dimension: 2816
  Activation: GELU + Linear
  Vocabulary size: 36,096 (SentencePiece)
  Total parameters: ~770M
  ```

### 2.2 Finetuned Models

#### Summarization Task
- **ViT5-base-vietnews-summarization** → Fine-tune trên bộ [VietNews](https://github.com/ThanhChinhBK/vietnews)
- **ViT5-large-vietnews-summarization** → Fine-tune trên VietNews

#### Translation Task
- **EnViT5-base** → [VietAI/envit5-base](https://huggingface.co/VietAI/envit5-base)
- **EnViT5-translation** → [VietAI/envit5-translation](https://huggingface.co/VietAI/envit5-translation)

## 3. So Sánh Chi Tiết Base vs Large

| Thông Số | ViT5-Base | ViT5-Large | Tỷ Lệ |
|---------|-----------|------------|-------|
| Hidden Size (d_model) | 768 | 1024 | 1.33x |
| Encoder Layers | 12 | 24 | 2x |
| Decoder Layers | 12 | 24 | 2x |
| Attention Heads | 12 | 16 | 1.33x |
| Encoder FFN Dim | 3072 | 2816 | 0.92x* |
| Decoder FFN Dim | 3072 | 2816 | 0.92x* |
| Total Params | ~220M | ~770M | 3.5x |
| Memory (FP32) | ~0.88GB | ~3.08GB | 3.5x |
| Training Steps | 1M | 1.5M | 1.5x |

*Lưu ý: Large model có FFN dimension nhỏ hơn một chút nhưng nhiều layers hơn nhiều.

---

## 4. Kiến Trúc Chi Tiết

### 4.1 SentencePiece Tokenizer

**Vocabulary**: `spiece.model` (36,096 tokens)
- Tokenization: SentencePiece (subword)
- Đặc điểm:
  - Shared vocabulary giữa encoder và decoder
  - Optimized cho tiếng Việt
  - Bao gồm special tokens: `<pad>`, `<unk>`, `<s>`, `</s>`

### 4.2 Encoder Stack

```
Input → Token Embedding + Positional Embedding → [12|24] × [Self-Attention → LayerNorm → FeedForward] → Output
```

**Mỗi encoder layer gồm**:
1. **Multi-Head Self-Attention** (12|16 heads, 64 dim mỗi head)
   - Query, Key, Value projections
   - Attention scores: `softmax(QK^T / sqrt(d_k))`
   - Output: weighted sum of Values
2. **Layer Normalization** (normalize sau mỗi sub-layer)
3. **Position-wise Feed-Forward Network** (2-layer network)
   - Up-projection → Activation (ReLU/GELU) → Down-projection

### 4.3 Decoder Stack

```
[decoder_start] + Target Tokens → Token Embedding + Positional Embedding → [12|24] × [Self-Attn + Cross-Attn + FFN] → Output
```

**Mỗi decoder layer gồm**:
1. **Masked Multi-Head Self-Attention** (chỉ nhìn các token trước đó)
2. **Multi-Head Cross-Attention** (query từ decoder, key/value từ encoder)
3. **Layer Normalization** sau mỗi sub-layer
4. **Position-wise Feed-Forward Network**

### 4.4 Output Layer

```
Decoder Output → LayerNorm → Linear Projection (d_model → vocab_size) → Logits → Softmax
```

---

## 5. Các Tác Vụ Hỗ Trợ

ViT5 sử dụng **text-to-text** framework, nghĩa là mọi tác vụ đều được biến đổi thành dạng sinh văn bản:

### 5.1 Text Summarization (Tóm tắt văn bản)
**Format**: `"tóm tắt: {văn bản dài} </s>"`
- Input: Article text
- Output: Summary text

### 5.2 Machine Translation (Dịch máy)
**Format**: `"dịch sang tiếng Anh: {tiếng Việt} </s>`" hoặc `"dịch sang tiếng Việt: {tiếng Anh} </s>"`
- En→Vi, Vi→En

### 5.3 Question Answering (Hỏi đáp)
**Format**: `"câu hỏi: {câu hỏi} câu trả lời:"`

### 5.4 Named Entity Recognition (NER)
**Format**: `"nhận diện thực thể: {văn bản}"`

---

## 6. Sử Dụng Trong Thực Tế

### 6.1 Code Cơ Bản

```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load base model
tokenizer = AutoTokenizer.from_pretrained("VietAI/vit5-base")
model = AutoModelForSeq2SeqLM.from_pretrained("VietAI/vit5-base")
model.cuda()  # hoặc model.to("cpu")

# Tokenize
text = "tóm tắt: Việt AI là một tổ chức phi lợi nhuận. </s>"
inputs = tokenizer(text, return_tensors="pt").to(model.device)

# Generate
outputs = model.generate(
    input_ids=inputs.input_ids,
    attention_mask=inputs.attention_mask,
    max_length=50,
    num_beams=4,
    early_stopping=True
)

# Decode
result = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(result)
```

### 6.2 Cho Summarization

```python
def summarize(text, model_name="VietAI/vit5-large-vietnews-summarization"):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    
    # Add prefix for summarization task
    input_text = f"vietnews: {text} </s>"
    inputs = tokenizer(input_text, return_tensors="pt", truncation=True)
    
    outputs = model.generate(
        inputs.input_ids,
        attention_mask=inputs.attention_mask,
        max_length=256,
        min_length=50,
        num_beams=4,
        length_penalty=2.0,
        early_stopping=True
    )
    
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Ví dụ
article = "VietAI là tổ chức phi lợi nhuận với sứ mệnh ươm mầm tài năng về trí tuệ nhân tạo..."
print(summarize(article))
```

### 6.3 Fine-tuning (HuggingFace)

Xem hướng dẫn chi tiết tại: [finetune_huggingface_example.ipynb](https://github.com/vietai/ViT5/blob/main/examples/finetune_huggingface_example.ipynb)

---

## 7. So Sánh Với Qwen

| Đặc Điểm | **ViT5** | **Qwen** |
|---------|---------|---------|
| **Kiến trúc** | Encoder-Decoder (T5-style) | Decoder-only (GPT-style) |
| **Task type** | Seq2Seq (translation, summarization) | Causal LM (text generation) |
| **Input format** | Source → Target (supervised) | Previous tokens → Next token |
| **Generation** | Non-autoregressive attention | Autoregressive (left-to-right) |
| **Vietnamese** | Pretrained entirely on Vietnamese | Multilingual (including Vietnamese) |
| **Best for** | Translation, Summarization, QA | Chat, Creative writing, Completion |
| **Context** | Encoder sees full input | Causal mask (can't see future) |

**Lưu ý quan trọng**:
- ViT5 là **sequence-to-sequence**, phù hợp cho tác vụ có input-output rõ ràng
- Qwen là **causal language model**, phù hợp cho chat và sinh văn bản tự nhiên
- Cách sử dụng hoàn toàn khác nhau về prompt engineering

---

## 8. Đánh Giá Hiệu Suất

### Bộ dữ liệu benchmark:
- **Summarization**: VietNews dataset (~80K articles)
- **NER**: PhoNER-COVID19 dataset
- **Translation**: Wikilingua (En↔Vi)

### Kết quả (từ paper):

| Model | ROUGE-1 | ROUGE-2 | ROUGE-L |
|-------|--------|--------|---------|
| ViT5-Base | **42.15** | **20.84** | **38.62** |
| ViT5-Large | **43.38** | **21.56** | **39.54** |
| mBART-large | 41.52 | 20.01 | 37.96 |
| T5-base | 40.23 | 19.12 | 36.85 |

ViT5 vượt trội so với các mô hình multilingual như mBART và T5 gốc.

---

## 9. Tính Năng Đặc Biệt

### 9.1 Text-to-Text Unification
- Mọi tác vụ đều được biến đổi thành dạng "input text → output text"
- Không cần thay đổi kiến trúc giữa các tác vụ

### 9.2 SentencePiece Tokenization
- Subword tokenization phù hợp với tiếng Việt (có dấu, các từ ghép)
- Shared vocabulary giảm thiểu OOV tokens

### 9.3 TPU-Optimized
- Kiến trúc được thiết kế cho TPU/GPU training
- `vocab_size` chia hết cho 128 để tối ưu TPU

---

## 10. Giới Hạn & Lưu Ý

### Giới hạn:
1. **ChỉEncoder-Decoder**: Không phù hợp với generation không có input rõ ràng
2. **Không Multilingual**: Chỉ tập trung vào tiếng Việt (không như mBART hoặc XLM-R)
3. **Vocabulary riêng**: Cần cùng tokenizer với pretrained model
4. **Memory**: Large model (~770M params) cần GPU 16GB+ VRAM

### Lưu ý khi sử dụng:
1. Luôn thêm **prefix** (ví dụ: "tóm tắt:", "dịch:") để định hướng task
2. Thêm `</s>` token ở cuối input
3. Tùy chỉnh `max_length`, `num_beams` cho từng task
4. Fine-tune trên bộ dữ liệu cụ thể để tối ưu performance

---

## 11. Tài Nguyên & Liên Kết

- **GitHub Repository**: https://github.com/vietai/ViT5
- **HuggingFace Models**: https://huggingface.co/VietAI
- **Paper**: https://arxiv.org/abs/2205.06457
- **Demo Spaces**: https://huggingface.co/VietAI/spaces
- **Vocabulary**: https://storage.googleapis.com/vietai_public/viT5/vocab/spiece.model

---

## 12. Kết Luận

ViT5 là **mô hình state-of-the-art đầu tiên và duy nhất** được pretrain hoàn toàn trên tiếng Việt với kiến trúc encoder-decoder. So sánh với Qwen:

- **ViT5** → Tốt cho **tác vụ có input cụ thể** (dịch, tóm tắt, trả lời câu hỏi)
- **Qwen** → Tốt cho **generation tự do** (chat, viết lách, code)

Cả hai đều là lựa chọn xuất sắc cho NLP tiếng Việt, tùy theo use-case cụ thể.

---

*Script debug chi tiết: `debug-vit5-model.py`*
*Last updated: 2026-04-25*
