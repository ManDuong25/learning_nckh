# ABSA: ViT5 vs PhoBERT vs Qwen — Quick Reference

## 🎯 Problem: Aspect-Based Sentiment Analysis

**Input:** Review tiếng Việt
**Output:** Các khía cạnh (aspect) và cảm xúc (sentiment)

### Example
```
Input:  "Sản phẩm dùng tốt, giá hợp lý, bao bì đẹp."

Output: [
  {"aspect": "công dụng", "sentiment": "positive", "text": "dùng tốt"},
  {"aspect": "giá cả",     "sentiment": "positive", "text": "giá hợp lý"},
  {"aspect": "bao bì",     "sentiment": "positive", "text": "bao bì đẹp"}
]
```

**Aspect categories:** công dụng, giá cả, bao bì, mùi (có thể thêm khác)

---

## 🆚 Model Comparison Table

| Feature | **PhoBERT** | **ViT5** | **Qwen** |
|---------|-------------|----------|----------|
| **Type** | Encoder-only (BERT) | Encoder-Decoder (T5) | Decoder-only (GPT) |
| **Task approach** | Token classification | Text generation | Few-shot prompting |
| **Vietnamese** | ✅ Specialized | ✅ Specialized | ⚠️ Multilingual |
| **Parameters** | ~110M | ~220M-770M | ~7B-72B |
| **Memory (FP16)** | ~0.5GB | ~1-2GB | ~15-140GB |
| **Speed** | ~200 tok/s ✅ | ~150 tok/s | ~20 tok/s ❌ |
| **Training data** | Token-level BIO | Review→JSON pairs | None (zero-shot) |
| **Accuracy (F1)** | **~90%** ✅ | ~85% | ~80% |
| **Aspects** | Fixed set | Flexible/generative | Flexible/instruction |
| **Implementation** | Medium | Medium | Hard (prompting) |
| **Production-ready** | ✅ **YES** | ⚠️ Possible | ❌ No |

---

## 🏆 Winner Analysis

### 🥇 PhoBERT — Best for Production
**Use when:**
- Aspects are pre-defined (công dụng, giá, bao bì, mùi)
- Have 500+ labeled reviews (BIO format)
- Need high accuracy & fast inference
- Limited GPU memory

**Pros:**
- ✅ Highest accuracy (token-level)
- ✅ Fastest inference
- ✅ Smallest memory
- ✅ Mature ecosystem

**Cons:**
- ❌ Requires expensive token-level annotation
- ❌ Fixed aspect list
- ❌ Needs CRF for best span extraction

---

### 🥈 ViT5 — Best for Flexibility
**Use when:**
- Aspects may vary/open vocabulary
- Only 200-500 examples available
- Want structured JSON output
- Research/prototyping

**Pros:**
- ✅ Flexible output format
- ✅ Can generate new aspects
- ✅ Easier data prep (span-level vs token-level)
- ✅ Multi-task capable

**Cons:**
- ❌ Inconsistent generation
- ❌ Harder to extract exact spans
- ❌ Larger model

---

### 🥉 Qwen — Best for Zero-Shot
**Use when:**
- Zero training data (<100 examples)
- Have powerful GPU (16GB+)
- Quick prototyping needed
- Multi-lingual reviews

**Pros:**
- ✅ No training needed
- ✅ Handles complex instructions
- ✅ Very flexible

**Cons:**
- ❌ Very slow & memory-heavy
- ❌ Inconsistent output format
- ❌ Expensive at scale
- ❌ Prompt engineering required

---

## 📋 Decision Flowchart

```
Need Vietnamese ABSA?
        ↓
  Have training data?
    / \\         \\
   Yes  No        \\
    ↓    ↓         ↓
  Aspects  Use Qwen  Use ViT5
  fixed?   (zero-   (few-shot,
    ↓      shot)    generative)
  Yes      ↓         ↓
    ↓   Need GPU?   Need
  PhoBERT  / \\    flexibility?
  (Best)   Y  N      ↓
           ↓  ↓     ViT5
         Qwen PhoBERT  (Good)
         (Large GPU)
```

---

## 💡 Recommended Choice

| Scenario | Model | Why |
|----------|-------|-----|
| Production, fixed aspects | **PhoBERT** | Best accuracy & speed |
| Research, flexible aspects | **ViT5** | Generative, easy data prep |
| Zero-shot, quick test | **Qwen** | No training data needed |
| Limited GPU (<8GB) | **PhoBERT** | Only 0.5GB memory |
| Batch processing 1000s | **PhoBERT** | Fastest throughput |
| Multi-lingual reviews | **Qwen** | Handles many languages |
| 200-500 examples only | **ViT5** | Less data needed than PhoBERT |

---

## 🎯 Implementation Tips

### PhoBERT (Token Classification)
```python
# Use for: Exact span extraction
model = AutoModelForTokenClassification.from_pretrained(
    "vinai/phobert-base",
    num_labels=9  # 4 aspects × 2 sentiments + O
)
# Label format: B-CONG_DUNG, I-CONG_DUNG, B-GIA_NEG, etc.
```

### ViT5 (Text Generation)
```python
# Use for: Flexible output, generative
prompt = f"phân tích: {review} </s>"
output = model.generate(prompt)  # → "công dụng: positive; giá: negative"
```

### Qwen (Prompting)
```python
# Use for: Zero-shot
prompt = """User: Phân tích review: "{review}"
Assistant: {json}"""
# No training, just inference
```

---

## 📊 Performance Summary

| Metric | PhoBERT | ViT5 | Qwen-7B |
|--------|---------|------|---------|
| F1 Score | **90%** | 85% | 80% |
| Sentiment Acc | **92%** | 88% | 86% |
| Sent/Sec (batch=1) | **200** | 150 | 20 |
| VRAM | **0.5GB** | 1GB | 15GB |
| Training time | 30 min | 2 hours | 4 hours |
| Data needed | 500+ | 200+ | 0 |

---

## 🎓 Quick Answer

**"Nên dùng model nào cho ABSA tiếng Việt?"**

```text
Có data (500+ mẫu) → PhoBERT (token classification) — CHẤT LƯỢNG CAO NHẤT
Ít data (200-500 mẫu) → ViT5 (text generation) — LINH HOẠT
Không có data → Qwen (prompting) — NHANH NHƯNG CHẬM
```

---

## 📁 Files in This Package

- `06-vit5-vs-phobert-absa.ipynb` — Full comparison notebook
- `VIT5_VS_PHOBERT_ABSA.md` — This quick reference
- `USAGE_GUIDE.md` — Token classification patterns
- `05-fine-tuning-guide.ipynb` — How to fine-tune

---

**Last updated:** 2026-04-25
**Task:** Aspect-Based Sentiment Analysis (ABSA)
**Domain:** Vietnamese product reviews
**Conclusion:** PhoBERT wins for production, ViT5 for flexibility, Qwen for zero-shot
