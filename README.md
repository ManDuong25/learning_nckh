# ViT5 Debug & Learning Resource Pack

Ồ! Bạn đã tìm thấy kho tài nguyên này. Đây là bộ sưu tập **đầy đủ nhất** về ViT5 để bạn hiểu sâu từ kiến trúc đến fine-tuning.

## 📁 Nội Dung Gói Này

```
Vit5Learning/
├── README.md                          ← File này
├── VIT5_OVERVIEW.md                   ← Tổng quan đầy đủ về ViT5
├── VIT5_VS_QWEN_COMPARISON.md         ← So sánh chi tiết ViT5 vs Qwen
├── ALL_VIT5_VARIANTS.md              ← Catalog tất cả phiên bản
├── debug-vit5-model.py               ← Debug script CHI TIẾT (546 lines)
├── quick-demo-vit5.py                ← Demo Nhanh (100 lines)
└── USAGE_GUIDE.md                    ← Hướng dẫn sử dụng nhanh
```

---

## 🎯 Bắt Đầu Từ Đâu?

### Nếu bạn muốn **HIỂU SÂU KIẾN TRÚC**:
```
1. debug-vit5-model.py → Chạy script này
   - Xem output: configuration, layers, attention, params
   - Script sẽ in ra TẤT CẢ chi tiết của base & large models
   
2. VIT5_OVERVIEW.md → Đọc để tổng hợp kiến thức
   - Kiến trúc, configs, training details
   - Cách sử dụng cho từng task
```

### Nếu bạn muốn **DEMO NHANH**:
```
quick-demo-vit5.py → Chạy script này
   - Test summarization, translation, QA ngay lập tức
   - Output ví dụ thực tế
   - Chỉ ~100 lines code
```

### Nếu bạn muốn **SO SÁNH với Qwen** (model bạn đã biết):
```
VIT5_VS_QWEN_COMPARISON.md → Đọc file này
   - So sánh kiến trúc: Encoder-Decoder vs Decoder-only
   - Input/Output format khác nhau thế nào
   - Khi nào dùng ViT5, khi nào dùng Qwen
```

### Nếu bạn muốn **XEM TẤT CẢ VARIANTS**:
```
ALL_VIT5_VARIANTS.md → Danh sách đầy đủ
   - vit5-base, vit5-large
   - vit5-base-vietnews-summarization
   - vit5-large-vietnews-summarization
   - envit5-base, envit5-translation
   - 87+ community finetuned models
```

---

## 🚀 Quick Start (5 phút)

### Bước 1: Install dependencies
```bash
pip install torch transformers sentencepiece
```

### Bước 2: Chạy demo nhanh
```bash
python quick-demo-vit5.py
```
**Expected output**: 
```
Input:  "tóm tắt: Trí tuệ nhân tạo..."
Output: "AI là lĩnh vực nghiên cứu..."
```

### Bước 3: Debug sâu (tuỳ chọn)
```bash
python debug-vit5-model.py
```
**Expected output**:
```
SECTION 3: MODEL CONFIGURATION ANALYSIS
  ViT5-base Configuration:
    Encoder layers: 12
    Hidden size: 768
    Attention heads: 12
    FFN dim: 3072
    Total parameters: 220.45M
  ViT5-large Configuration:
    Encoder layers: 24
    Hidden size: 1024
    ...
```

---

## 📊 Cheat Sheet

### Model Selection Table

| Bạn cần... | Dùng model... | Parameters | VRAM |
|------------|--------------|------------|------|
| Tóm tắt nhanh | `vit5-base-vietnews-sum` | 220M | 2GB |
| Tóm tắt chất lượng cao | `vit5-large-vietnews-sum` | 770M | 6GB |
| Dịch Anh-Việt | `envit5-base` | 220M | 2GB |
| Task tổng quát | `vit5-base` | 220M | 2GB |
| Task tổng quát + chất lượng | `vit5-large` | 770M | 6GB |

### Task Prompt Format

```python
# Summarization
"tóm tắt: {text} </s>"

# Translation (Vi→En)
"dịch sang tiếng Anh: {text} </s>"

# Translation (En→Vi)
"dịch sang tiếng Việt: {text} </s>"

# QA
"câu hỏi: {question} câu trả lời:"

# NER
"nhận diện thực thể: {text}"
```

---

## 🔬 Understanding ViT5 Architecture

### Encoder-Decoder vs Decoder-Only

**ViT5 (T5-style)**:
- Encoder: Đọc input, tạo representation
- Decoder: Dùng representation để sinh output
- Có cross-attention giữa encoder và decoder
- Phù hợp: Translation, Summarization, QA

**Qwen (GPT-style)**:
- Chỉ có decoder (causal)
- Mỗi token chỉ nhìn tokens trước đó
- Phù hợp: Chat, Text Completion

Xem chi tiết: `VIT5_VS_QWEN_COMPARISON.md`

---

## 📖 Key Files Explained

### 1. `debug-vit5-model.py`
**Điều gì trong này?**
- Load both base & large models
- Print cấu trúc từng layer
- Show tokenization examples
- Run forward pass & generation
- Compare base vs large (params, speed)
- Visualize architecture

**Output**:
- Số layers, hidden size, attention heads
- Vocabulary info & special tokens
- Token breakdown cho tiếng Việt
- Generation results
- Parameter count & memory estimate

### 2. `quick-demo-vit5.py`
**Điều gì trong này?**
- Load model nhanh
- Test 4 tác vụ: summarization, translation, QA, generation
- Code ngắn gọn, dễ đọc
- Phù hợp để chạy thử ngay

**Output**:
- Input → Output cho mỗi task
- Device info
- Token examples

### 3. `VIT5_OVERVIEW.md`
**Điều gì trong này?**
- Giới thiệu tổng quan
- Chi tiết config base/large
- So sánh với Qwen
- Use cases & limitations
- Training details
- Bibtex citation

### 4. `VIT5_VS_QWEN_COMPARISON.md`
**Điều gì trong này?**
- So sánh kiến trúc (table)
- Input/output format khác nhau
- Training objective
- Performance & speed
- Prompt engineering differences
- Khi nào dùng cái nào

### 5. `ALL_VIT5_VARIANTS.md`
**Điều gì trong này?**
- Danh sách TẤT CẢ models
- Performance table (ROUGE, F1)
- Fine-tuning guide
- Error troubleshooting
- Learning path (beginner → advanced)

---

## 🎓 Study Plan Đề Xuất

### Day 1: Get Familiar
```
1. Read VIT5_OVERVIEW.md (30 phút)
2. Run quick-demo-vit5.py (10 phút)
3. Chạy thử 2-3 examples trong debug script
```

### Day 2: Architecture Deep Dive
```
1. Run debug-vit5-model.py (xem full output)
2. Ghi ra: số layers, attention heads, params của base vs large
3. Đọc config files trong script comments
4. Vẽ sơ đồ encoder-decoder
```

### Day 3: Compare with Qwen
```
1. Đọc VIT5_VS_QWEN_COMPARISON.md
2. Viết 1 trang: "Khi nào dùng ViT5, khi nào dùng Qwen"
3. Viết code ví dụ cho cả hai cho cùng 1 task (translation)
```

### Day 4: Fine-tuning Prep
```
1. Đọc ALL_VIT5_VARIANTS.md phần fine-tuning
2. Clone repo official: https://github.com/vietai/ViT5
3. Xem examples/ folder trong repo
4. Chuẩn bị dataset nhỏ (500 mẫu) để fine-tune
```

### Day 5: Fine-tune & Evaluate
```
1. Fine-tune vit5-base trên dataset nhỏ
2. Đo ROUGE/F1 scores
3. Compare với pretrained (không fine-tune)
4. Viết report kết quả
```

---

## 🛠 Tools & Commands

### Check model info (command line)
```bash
# Install huggingface_hub
pip install huggingface_hub

# List all ViT5 models
python -c "
from huggingface_hub import list_models
for m in list_models(author='VietAI', search='vit5'):
    print(m.id)
"
```

### Convert to ONNX (để deploy)
```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

tokenizer = AutoTokenizer.from_pretrained("VietAI/vit5-base")
model = AutoModelForSeq2SeqLM.from_pretrained("VietAI/vit5-base")

# Export to ONNX
dummy_input = tokenizer("test", return_tensors="pt")
torch.onnx.export(
    model, 
    dummy_input['input_ids'],
    "vit5-base.onnx",
    opset_version=11
)
```

### Quantize (giảm memory)
```python
# 8-bit quantization
model = AutoModelForSeq2SeqLM.from_pretrained(
    "VietAI/vit5-base",
    load_in_8bit=True  # Cần bitsandbytes
)
```

---

## ❓ Frequently Asked Questions

### Q1: ViT5 vs PhoBERT/BERT?
- **ViT5**: Encoder-Decoder → sinh văn bản (generation)
- **PhoBERT/BERT**: Encoder-only → classification, embedding

### Q2: Có fine-tune ViT5 được không?
✅ **Có**, dùng HuggingFace Trainer hoặc T5X (official)

### Q3: Chạy ViT5 trên CPU được không?
✅ **Được**, nhưng chậm. vit5-base vẫn chạy được trên CPU.

### Q4: Input length tối đa?
- Default: 512 tokens
- Có thể extend lên 1024 với positional embedding interpolation

### Q5: Tiếng Việt có dấu có ảnh hưởng không?
- ✅ ViT5 tokenizer xử lý tốt dấu
- SentencePiece chia subword thông minh
- Không cần preprocess bỏ dấu

---

## 🎯 Project Ideas Để Luyện Tập

### Beginner:
1. **Vietnamese Summarizer**: Tóm tắt 1000 bài báo VnExpress
2. **Simple Translator**: En→Vi translation cho câu đơn

### Intermediate:
3. **Title Generator**: Từ nội dung → tiêu đề báo
4. **Paraphraser**: Viết lại câu theo phong cách khác
5. **QA Bot**: Trả lời câu hỏi từ đoạn văn

### Advanced:
6. **Multi-task Model**: Fine-tune trên summarization + NER + translation
7. **Train from Scratch**: Collect 10GB Vietnamese text, train new ViT5
8. **Model Distillation**: Distill vit5-large → vit5-small (mới)

---

## 📚 Additional Reading

### Must-read:
1. [Original T5 Paper](https://arxiv.org/abs/1910.10683) → Hiểu base architecture
2. [ViT5 Paper](https://arxiv.org/abs/2205.06457) → Viết特殊性 cho tiếng Việt
3. [HuggingFace T5 Docs](https://huggingface.co/docs/transformers/model_doc/t5) → API

### Nice-to-read:
4. [SentencePiece Paper](https://arxiv.org/abs/1808.06226) → Tokenization
5. [Attention Is All You Need](https://arxiv.org/abs/1706.03762) → Transformer cơ bản
6. [TPU Training Guide](https://cloud.google.com/tpu/docs) → Nếu bạn muốn train lớn

---

## 🐛 Debugging Tips

### "My generated text is gibberish"
```python
# 1. Check tokenization
tokens = tokenizer(text)
print(f"Tokens: {tokens['input_ids']}")

# 2. Check special tokens
print(f"EOS: {tokenizer.eos_token_id}")
print(f"PAD: {tokenizer.pad_token_id}")

# 3. Add prefix & </s>
text = "tóm tắt: " + text + " </s>"
```

### "Memory error with large model"
```python
# Giảm batch size
model.generate(..., num_beams=1)  # beam=4 dùng 4x memory

# Hoặc dùng FP16
model = AutoModelForSeq2SeqLM.from_pretrained(
    "VietAI/vit5-large",
    torch_dtype=torch.float16
).cuda()
```

### "Output too short"
```python
# Tăng min_length
outputs = model.generate(
    ...,
    min_length=50,  # Thêm này
    max_length=200,
    length_penalty=2.0  # Khuyến khích dài hơn
)
```

---

## 🎉 Conclusion

ViT5 là **mô hình vàng** cho NLP tiếng Việt dạng Seq2Seq.

**Quick recommendation**:
- Dùng `vit5-base` để start
- Nếu cần quality hơn → `vit5-large`
- Summarization → dùng finetuned variant
- Translation → dùng `envit5-base`

**So với Qwen**:
- **ViT5**: Best for translation, summarization
- **Qwen**: Best for chat, creative writing

---

## 📞 Get Help

- **Issues**: https://github.com/vietai/ViT5/issues
- **Discord**: VietAI Discord server (search "VietAI")
- **Paper questions**: Open issue trên GitHub repo

---

## 🎁 Bonus: One-Liner Summary

> "ViT5 is to Vietnamese what T5 is to English — a unified text-to-text framework that excels at translation, summarization, and question answering, with specialized pretraining for Vietnamese morphology and syntax."

---

**Happy Learning! 🚀**

*Created: 2026-04-25*
*Last updated: Check modification date*
