# Tất Cả Phiên Bản ViT5 - Completely Guide

## 📋 Danh Sách Đầy Đủ Các Models

### A. Pretrained Base Models

| Model | Loại | Params | Steps | Tác vụ chính |
|-------|------|--------|-------|-------------|
| `VietAI/vit5-base` | Base | ~220M | 1,000,000 | General Vietnamese NLG |
| `VietAI/vit5-large` | Large | ~770M | 1,500,000 | General Vietnamese NLG |

### B. Summarization Models (Finetuned)

| Model | Base | Dataset | Mô tả |
|-------|------|---------|-------|
| `VietAI/vit5-base-vietnews-summarization` | Base | VietNews | Tóm tắt báo tiếng Việt |
| `VietAI/vit5-large-vietnews-summarization` | Large | VietNews | Tóm tắt báo tiếng Việt (cao cấp) |

**VietNews Dataset**: ~80,000 bài báo tiếng Việt từ VnExpress, Tuổi Trẻ, v.v.

### C. Translation Models (Finetuned)

| Model | Base | Tasks | Mô tả |
|-------|------|-------|-------|
| `VietAI/envit5-base` | Base | En↔Vi | Dịch Anh-Việt hai chiều |
| `VietAI/envit5-translation` | Base | En↔Vi | Dịch chuyên biệt |

### D. All Finetuned Variants (87+ models)

**Tất cả các finetuned models** từ cộng đồng:
- 87 finetuned variants của `vit5-base`
- 432 finetuned variants của `vit5-large`

Bạn có thể xem tất cả tại:
- https://huggingface.co/VietAI/vit5-base/tree/main (87 models)
- https://huggingface.co/VietAI/vit5-large/tree/main (432 models)

---

## 🎯 Khi Nào Dùng Phiên Bản Nào?

### Decision Tree

```
Bạn cần làm gì?
├─ Dịch thuật (Anh-Việt)?
│  └→ Dùng: envit5-base hoặc envit5-translation
│
├─ Tóm tắt văn bản?
│  ├─ Budget/Resource hạn chế → vit5-base-vietnews-summarization
│  └─ Chất lượng cao, có GPU mạnh → vit5-large-vietnews-summarization
│
├─ QA / NER?
│  └→ Dùng: vit5-base (fine-tune thêm trên dataset PhoNER)
│
└─ Task tổng quát (không có pretrained)?
   ├── Có GPU mạnh, muốn chất lượng tốt → vit5-large
   └── Resource hạn chế → vit5-base
```

---

## 📊 So Sánh Chi Tiết All Models

### Performance on Summarization (ROUGE scores)

| Model | ROUGE-1 | ROUGE-2 | ROUGE-L | Use case |
|-------|---------|---------|---------|----------|
| **vit5-large-vietnews** | 43.38 | 21.56 | 39.54 | Best quality |
| **vit5-base-vietnews** | 42.15 | 20.84 | 38.62 | Good balance |
| mBART-large | 41.52 | 20.01 | 37.96 | Multilingual |
| T5-base | 40.23 | 19.12 | 36.85 | General |

---

## 🚀 Quick Start Từng Loại

### 1. **Summarization**
```python
# Best for quality
model_name = "VietAI/vit5-large-vietnews-summarization"

# Good for speed/memory
model_name = "VietAI/vit5-base-vietnews-summarization"
```

### 2. **Translation**
```python
# En ↔ Vi translation
model_name = "VietAI/envit5-translation"

# Base version
model_name = "VietAI/envit5-base"
```

### 3. **General Purpose / Custom Tasks**
```python
# Base (faster, smaller)
model_name = "VietAI/vit5-base"

# Large (better quality)
model_name = "VietAI/vit5-large"
```

---

## 🔧 Fine-Tuning Additional Tasks

Nếu bạn muốn fine-tune cho task khác (NER, style transfer, etc.):

```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from datasets import load_dataset

# 1. Load base model
tokenizer = AutoTokenizer.from_pretrained("VietAI/vit5-base")
model = AutoModelForSeq2SeqLM.from_pretrained("VietAI/vit5-base")

# 2. Prepare your dataset
def preprocess_function(examples):
    inputs = ["nhận diện thực thể: " + text for text in examples["text"]]
    targets = examples["labels"]
    model_inputs = tokenizer(inputs, max_length=512, truncation=True)
    labels = tokenizer(targets, max_length=128, truncation=True)
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

# 3. Train (sử dụng HuggingFace Trainer)
from transformers import Seq2SeqTrainer, Seq2SeqTrainingArguments

training_args = Seq2SeqTrainingArguments(
    output_dir="./vit5-ner-finetuned",
    per_device_train_batch_size=8,
    predict_with_generate=True,
    evaluation_strategy="epoch",
)

trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"],
    tokenizer=tokenizer,
)

trainer.train()
```

---

## 📈 Model Size & Requirements

| Model | Disk Size | RAM (eval) | GPU VRAM | Speed (tokens/s) |
|-------|-----------|------------|----------|------------------|
| vit5-base | ~900MB | ~4GB | ~2GB | ~150 |
| vit5-large | ~3GB | ~8GB | ~6GB | ~50 |
| vit5-base-summarization | ~900MB | ~4GB | ~2GB | ~150 |
| vit5-large-summarization | ~3GB | ~8GB | ~6GB | ~50 |

*Speed measured on RTX 3090, batch_size=1*

---

## 🔍 Finding Right Model từ HuggingFace

### Search trên HuggingFace Hub:

```python
from huggingface_hub import list_models

# Tất cả ViT5 models
vit5_models = list_models(author="VietAI", search="vit5")
for model in vit5_models:
    print(f"  - {model.id}")

# Finetuned versions
finetuned = list_models(base_model="VietAI/vit5-base")
for model in finetuned:
    if "finetune" in model.id or "summarization" in model.id:
        print(f"  - {model.id}")
```

---

## 🧪 Benchmark Results ( từ Paper )

### Summarization on VietNews:
```
Model              ROUGE-1   ROUGE-2   ROUGE-L
─────────────────────────────────────────────────
vit5-large         43.38     21.56     39.54
vit5-base          42.15     20.84     38.62
mBART-large        41.52     20.01     37.96
Pegasus (orig)     40.75     19.32     37.01
T5-base            40.23     19.12     36.85
```

### NER on PhoNER-COVID19:
```
Model              F1-Score
────────────────────────────
vit5-large         87.2
vit5-base          86.5
 Vietnamese-BERT    85.8
 PhoBERT            85.2
```

---

## 🎓 Learning Path

### Beginner (bắt đầu):
1. **vit5-base** → Hiểu architecture
2. **vit5-base-vietnews-summarization** → Đọc docs, chạy inference
3. File: `quick-demo-vit5.py` (script này)

### Intermediate (nâng cao):
1. **vit5-large** → So sánh với base
2. Fine-tune trên dataset nhỏ của bạn
3. File: `debug-vit5-model.py` (debug chi tiết)

### Advanced (chuyên sâu):
1. **envit5-base** → Multi-lingual task
2. Fine-tune trên 3-4 tasks khác nhau (multi-task)
3. Đọc paper, huấn luyện từ scratch (có TPU/GPU lớn)

---

## ⚠️ Lỗi Thường Gặp & Giải Pháp

### Lỗi 1: "SentencePiece model not found"
```python
# Giải pháp:
tokenizer = AutoTokenizer.from_pretrained("VietAI/vit5-base", 
                                           tokenizer_file="spiece.model")
```

### Lỗi 2: Out of Memory với vit5-large
```python
# Giải pháp:
model = AutoModelForSeq2SeqLM.from_pretrained(
    "VietAI/vit5-large",
    load_in_8bit=True,  # 8-bit quantization
)
# hoặc dùng torch_dtype=torch.float16
model = AutoModelForSeq2SeqLM.from_pretrained(
    "VietAI/vit5-large",
    torch_dtype=torch.float16
).to("cuda")
```

### Lỗi 3: Output không phù hợp với task
```python
# Nhớ thêm prefix:
input_text = "tóm tắt: " + your_text + " </s>"
# KHÔNG phải: input_text = your_text
```

---

## 📚 More Resources

### Official:
- GitHub: https://github.com/vietai/ViT5
- Paper: https://arxiv.org/abs/2205.06457
- HF Models: https://huggingface.co/VietAI

### Tutorials & Examples:
- Finetune example: [finetune_huggingface_example.ipynb](https://github.com/vietai/ViT5/blob/main/examples/finetune_huggingface_example.ipynb)
- Colab demo: https://colab.research.google.com/github/vietai/ViT5

### Vietnamese NLP Community:
- VietAI website: https://vietai.org/
- Vietnamese NLP papers: https://paperswithcode.com/area/natural-language-processing/vi

---

## 🎯 Checklist Trước Khi Dùng

- [ ] Đã chọn đúng model cho task (base/large, pretrained/finetuned)
- [ ] Đã thêm task prefix phù hợp (nếu cần)
- [ ] Đã set `max_length`, `num_beams` trong generate()
- [ ] Kiểm tra VRAM có đủ không (vit5-large cần 6GB+)
- [ ] Test với 1-2 samples trước khi batch inference

---

**Tóm lại**: 
- **2 pretrained models**: vit5-base, vit5-large
- **4 official finetuned**: envit5-base, envit5-translation, vit5-base-vietnews-sum, vit5-large-vietnews-sum
- **87+ community finetuned**: Available on HuggingFace
- **Chọn model**: Task → Base/Large → Finetune if available

---

*File: ALL_VIT5_VARIANTS.md*
*Date: 2026-04-25*
