# ViT5 USAGE GUIDE - Hướng Dẫn Nhanh

## 🚀 Quick Start (3 bước)

### 1. Install
```bash
pip install torch transformers sentencepiece
```

### 2. Basic Usage
```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("VietAI/vit5-base")
model = AutoModelForSeq2SeqLM.from_pretrained("VietAI/vit5-base")

# Để model lên GPU nếu có
import torch
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
```

### 3. Inference
```python
text = "tóm tắt: Trí tuệ nhân tạo đang thay đổi thế giới. </s>"
inputs = tokenizer(text, return_tensors="pt").to(device)

outputs = model.generate(**inputs, max_length=50)
result = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(result)
```

---

## 📝 Task-Specific Templates

### Summarization (Tóm tắt)
```python
prompt = f"tóm tắt: {long_text} </s>"
```

**Best model**: `VietAI/vit5-large-vietnews-summarization`

**Parameters**:
```python
model.generate(
    max_length=256,
    min_length=50,
    num_beams=4,
    length_penalty=2.0,  # khuyến khích output dài
    early_stopping=True
)
```

---

### Translation (Dịch thuật)

** Vietnamese → English**:
```python
prompt = f"dịch sang tiếng Anh: {vi_text} </s>"
model_name = "VietAI/envit5-translation"  # or "VietAI/envit5-base"
```

** English → Vietnamese**:
```python
prompt = f"dịch sang tiếng Việt: {en_text} </s>"
model_name = "VietAI/envit5-translation"
```

**Parameters**:
```python
model.generate(
    max_length=100,
    num_beams=5,  # beams cao hơn cho translation
    early_stopping=True
)
```

---

### Question Answering (Hỏi đáp)
```python
prompt = f"câu hỏi: {question} câu trả lời:"
```

**Example**:
```python
context = "Việt AI là tổ chức phi lợi nhuận thành lập năm 2018."
question = "Việt AI thành lập năm nào?"
prompt = f"câu hỏi: {question} dựa trên: {context} câu trả lời:"
```

---

### Text Simplification (Làm đơn giản)
```python
prompt = f"đơn giản hóa: {complex_text} </s>"
```
*(Fine-tune thêm trên dataset simplification)*

---

### Style Transfer (Chuyển phong cách)
```python
# Formal → Informal
prompt = f"chuyển thành văn nói: {formal_text} </s>"
```

---

## 🔧 Generation Parameters

### Beam Search (chất lượng cao)
```python
outputs = model.generate(
    input_ids,
    attention_mask,
    max_length=100,
    num_beams=4,           # 4-8 cho quality
    early_stopping=True,
    no_repeat_ngram_size=2,  # Tránh lặp
    length_penalty=1.0,    # 1.0 = balanced, >1.0 khuyến khích dài
)
```

### Sampling (đa dạng)
```python
outputs = model.generate(
    input_ids,
    do_sample=True,
    max_length=100,
    temperature=0.7,       # 0.7-1.0, thấp hơn = less random
    top_k=50,              # Lấy top-k tokens
    top_p=0.95,           # Nucleus sampling
)
```

### Greedy (nhanh)
```python
outputs = model.generate(
    input_ids,
    max_length=100,
    num_beams=1,          # Greedy decode
)
```

---

## 🎯 Model Selection Table

| Task | Recommended Model | Batch Size | VRAM |
|------|------------------|------------|------|
| Summarization | `vit5-large-vietnews` | 4 | 6GB |
| Summarization (small) | `vit5-base-vietnews` | 8 | 2GB |
| Translation | `envit5-base` | 8 | 2GB |
| QA / NER | `vit5-base` (fine-tune) | 8 | 2GB |
| General tasks | `vit5-base` | 8 | 2GB |
| High quality | `vit5-large` | 2 | 6GB |

---

## 📊 Performance Tips

### Speed Optimization
```python
# 1. Use FP16 (2x faster on GPU)
model = AutoModelForSeq2SeqLM.from_pretrained(
    "VietAI/vit5-base",
    torch_dtype=torch.float16
).cuda()

# 2. Use smaller batch
# batch_size 1 có thể xử lý sequence dài hơn

# 3. Reduce beam count
num_beams=1  # Greedy - nhanh nhất
num_beams=4  # Balance
num_beams=8  # Chất lượng cao (chậm)

# 4. Use cache (default)
model.config.use_cache = True  # Tốt hơn 20% speed
```

### Memory Optimization (vit5-large)
```python
from transformers import AutoModelForSeq2SeqLM

# 8-bit quantization (chỉ 3GB VRAM)
model = AutoModelForSeq2SeqLM.from_pretrained(
    "VietAI/vit5-large",
    load_in_8bit=True,  # Cần: pip install bitsandbytes
    device_map="auto"
)

# Hoặc CPU offloading
model = AutoModelForSeq2SeqLM.from_pretrained(
    "VietAI/vit5-large",
    device_map="auto"  # Tự động split GPU/CPU
)
```

---

## 🔄 Fine-Tuning Quick Guide

```python
from transformers import (
    AutoTokenizer, 
    AutoModelForSeq2SeqLM,
    Seq2SeqTrainer, 
    Seq2SeqTrainingArguments
)
from datasets import load_dataset

# 1. Load
tokenizer = AutoTokenizer.from_pretrained("VietAI/vit5-base")
model = AutoModelForSeq2SeqLM.from_pretrained("VietAI/vit5-base")

# 2. Prepare dataset
def preprocess(examples):
    inputs = ["tóm tắt: " + doc for doc in examples["document"]]
    targets = examples["summary"]
    model_inputs = tokenizer(
        inputs, 
        max_length=512, 
        truncation=True, 
        padding="max_length"
    )
    labels = tokenizer(
        targets,
        max_length=128,
        truncation=True,
        padding="max_length"
    )
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

dataset = load_dataset("your_dataset")
tokenized = dataset.map(preprocess, batched=True)

# 3. Train
training_args = Seq2SeqTrainingArguments(
    output_dir="./results",
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    predict_with_generate=True,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    logging_dir="./logs",
    logging_steps=10,
    save_total_limit=2,
    load_best_model_at_end=True,
    num_train_epochs=3,
)

trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=tokenized["train"],
    eval_dataset=tokenized["validation"],
    tokenizer=tokenizer,
)

trainer.train()

# 4. Save
model.save_pretrained("./my-finetuned-vit5")
tokenizer.save_pretrained("./my-finetuned-vit5")
```

---

## 🧪 Testing Your Model

```python
# Load fine-tuned model
model = AutoModelForSeq2SeqLM.from_pretrained("./my-finetuned-vit5")
tokenizer = AutoTokenizer.from_pretrained("./my-finetuned-vit5")

# Test
test_input = "tóm tắt: Đây là văn bản cần tóm tắt. </s>"
inputs = tokenizer(test_input, return_tensors="pt")

outputs = model.generate(**inputs, max_length=50)
result = tokenizer.decode(outputs[0], skip_special_tokens=True)

print(f"Input: {test_input}")
print(f"Output: {result}")
```

---

## 📈 Evaluation Metrics

### For Summarization (ROUGE)
```python
from datasets import load_metric

rouge = load_metric("rouge")
predictions = [generated_summary_1, ...]
references = [ground_truth_1, ...]

results = rouge.compute(
    predictions=predictions,
    references=references,
    rouge_types=["rouge1", "rouge2", "rougeL"]
)
print(results)
```

### For Translation (BLEU)
```python
from datasets import load_metric

bleu = load_metric("bleu")
predictions = [[tokenizer.translate(text)]]  # tokenized
references = [[tokenizer.reference(text)]]

results = bleu.compute(predictions=predictions, references=references)
print(f"BLEU: {results['bleu']:.2f}")
```

### For QA (F1)
```python
from datasets import load_metric

f1 = load_metric("f1")
# predictions, references là span indices
```

---

## ⚡ Production Deployment

### 1. Export to ONNX
```python
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("VietAI/vit5-base")
model = AutoModelForSeq2SeqLM.from_pretrained("VietAI/vit5-base")

dummy_input = tokenizer("test", return_tensors="pt").input_ids
torch.onnx.export(
    model,
    dummy_input,
    "vit5-base.onnx",
    opset_version=12,
    do_constant_folding=True
)
```

### 2. Use with ONNX Runtime
```python
import onnxruntime as ort
import numpy as np

session = ort.InferenceSession("vit5-base.onnx")
inputs = tokenizer(text, return_tensors="np")
outputs = session.run(None, inputs)[0]
```

### 3. FastAPI REST API
```python
from fastapi import FastAPI
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

app = FastAPI()
tokenizer = AutoTokenizer.from_pretrained("VietAI/vit5-base")
model = AutoModelForSeq2SeqLM.from_pretrained("VietAI/vit5-base").to("cuda")

@app.post("/summarize")
def summarize(text: str):
    prompt = f"tóm tắt: {text} </s>"
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    outputs = model.generate(**inputs, max_length=100)
    summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return {"summary": summary}
```

---

## 🐛 Common Issues & Solutions

### Issue 1: Token count quá dài (>512)
```python
# Giải pháp: Truncate
inputs = tokenizer(
    text, 
    max_length=512, 
    truncation=True,  # Cắt bớt
    padding="max_length"
)
```

### Issue 2: Output quá ngắn
```python
outputs = model.generate(
    ...,
    min_length=30,        # Đảm bảo tối thiểu 30 tokens
    length_penalty=2.0,   # Khuyến khích output dài
)
```

### Issue 3: Memory error với large model
```python
# Giảm batch size, dùng FP16
model = AutoModelForSeq2SeqLM.from_pretrained(
    "VietAI/vit5-large",
    torch_dtype=torch.float16,  # 2x memory giảm
).cuda()

# Batch size 1
inputs = tokenizer(text, return_tensors="pt", padding=True)
```

### Issue 4: Output không đúng task
```python
# NHỚ: Thêm task prefix!
# SAI:
prompt = text

# ĐÚNG:
prompt = f"tóm tắt: {text} </s>"
```

---

## 📚 Advanced Topics

### Multi-task với prompt engineering
```python
def vit5_predict(text, task="summarize"):
    prefixes = {
        "summarize": "tóm tắt: ",
        "translate_en": "dịch sang tiếng Anh: ",
        "translate_vi": "dịch sang tiếng Việt: ",
        "qa": "câu hỏi: ",
    }
    prompt = prefixes[task] + text + " </s>"
    # ... generate
```

### Prompt chaining (multi-step)
```python
# Step 1: Summarize first
summary = vit5_predict(long_text, "summarize")

# Step 2: Translate summary
translated = vit5_predict(summary, "translate_en")
```

### Batch inference
```python
texts = ["tóm tắt: " + t + " </s>" for t in long_texts]
inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True).to(device)

# Batch generation
outputs = model.generate(**inputs, max_length=100)
summaries = [tokenizer.decode(o, skip_special_tokens=True) for o in outputs]
```

---

## ✅ Checklist Trước Khi Deploy

- [ ] Model đã được test trên 100+ samples
- [ ] Generation parameters đã được optimize (max_length, num_beams)
- [ ] Input đã có task prefix
- [ ] Output đã được post-process (remove special tokens, strip whitespace)
- [ ] Batch size phù hợp với GPU memory
- [ ] Error handling (long inputs, empty inputs)
- [ ] Rate limiting nếu là API
- [ ] Logging input/output để debug

---

## 🎓 Best Practices

1. **Always add task prefix** → Không có prefix model không biết task
2. **Set max_length** → Tránh infinite generation
3. **Use beam search** (4 beams) → Balance speed/quality
4. **Validate on holdout set** trước khi deploy
5. **Monitor generation** → Tránh toxic/inappropriate output
6. **Cache model** → Tránh reload mỗi request

---

## 🔗 Resources

- **Official Code**: https://github.com/vietai/ViT5
- **Models**: https://huggingface.co/VietAI
- **Paper**: https://arxiv.org/abs/2205.06457
- **Vietnamese NLP**: https://vietai.org/

---

**Last Updated**: 2026-04-25
