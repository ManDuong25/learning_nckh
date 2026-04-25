# ViT5 vs Qwen: So Sánh Chi Tiết

## Tổng Quan Nhanh

| Đặc Điểm | **ViT5** | **Qwen** |
|---------|----------|----------|
| **Mã nguồn** | Encoder-Decoder (T5) | Decoder-only (GPT) |
| **Họ mô hình** | T5-family | GPT-family |
| **Chủ đề** | Tiếng Việt chuyên sâu | Đa ngôn ngữ (multilingual) |
| **Cấu trúc** | 2 phần: Encoder + Decoder | 1 phần: Decoder tự hồi quy |
| **Attention** | Full attention (encoder) + Causal + Cross | Causal attention only |
| **Training objective** | Denoising autoencoder + downstream tasks | Causal LM (next token prediction) |

---

## 1. Kiến Trúc Sự Khác Biệt

### ViT5 (Encoder-Decoder)
```
┌─────────┐     ┌──────────┐
│ Encoder │───── │  Decoder │
│  12L/24L│     │ 12L/24L  │
└─────────┘     └──────────┘
      │               │
      │ Cross-Attn    │ Self-Attn (causal)
      └───────────────┘
           Attention
```

**Encoder (12|24 layers)**:
- Full bidirectional self-attention (nhìn toàn bộ input)
- Tạo biểu diễn ngữ nghĩa phong phú của input

**Decoder (12|24 layers)**:
- **Masked self-attention**: Chỉ nhìn các token trước đó (causal)
- **Cross-attention**: Ghép thông tin từ encoder
- Tạo ra output token một cách tuần tự

### Qwen (Decoder-only)
```
┌─────────────┐
│   Decoder   │
│  (32L/48L)  │ ← Causal Self-Attention
└─────────────┘
```

- Chỉ có **causal masked self-attention** (không cross-attention)
- Mỗi token chỉ nhìn các token trước đó
- Tối ưu cho **next token prediction**

---

## 2. Input/Output Format

### ViT5 (Text-to-Text)

**Cách tiếp cận**: Biến mọi task thành `input_text → output_text`

| Task | Input Format | Output |
|------|-------------|--------|
| Summarization | `tóm tắt: {long_text} </s>` | `Summary ngắn` |
| Translation | `dịch sang tiếng Anh: {vn_text} </s>` | `English translation` |
| QA | `câu hỏi: {question} câu trả lời:` | `Answer` |

**Ưu điểm**:
- Thống nhất cho mọi task
- Dễ prompt engineering
- Có thể handle input-output khác độ dài

### Qwen (Causal Language Model)

**Cách tiếp cận**: Dự đoán token tiếp theo dựa trên context trước đó

| Task | Prompt Format | Output |
|------|--------------|--------|
| Chat | `User: Xin chào\nAssistant:` | `Chào bạn!` |
| Completion | `Trí tuệ nhân tạo là` | `...` |
| QA | `Câu hỏi: Thủ đô Việt Nam là gì?\nĐáp án:` | `Hà Nội` |

**Ưu điểm**:
- tự nhiên cho conversational AI
- Không cần special task prefix
- Multi-turn conversation dễ dàng

---

## 3. Training Objectives

### ViT5
1. **Span Corruption Pretraining** (như T5):
   - Mask 15% spans trong text
   - Predict các span bị mask
   - Task: `"mọc grass <X> over <Y> the hill" → "the grass grows over the hill"`
   
2. **Fine-tuning trên downstream tasks**:
   - Summarization
   - NER
   - Translation

### Qwen
1. **Causal Language Modeling**:
   - Dự đoán token tiếp theo từ context
   - Loss: `-log P(token_t | token_1...token_{t-1})`
   
2. **SFT (Supervised Fine-Tuning)**:
   - Human-generated conversations
   
3. **RLHF** (nếu có):
   - Reinforcement learning from human feedback

---

## 4. Performance & Use Cases

### ViT5 Best For:
✅ **Translation** (En↔Vi, viết bản dịch tự nhiên)  
✅ **Summarization** (tóm tắt văn bản dài)  
✅ **Question Answering** (trả lời từ ngữ cảnh)  
✅ **Text Simplification** (viết lại cho dễ hiểu)  
✅ **Style Transfer** (chuyển phong cách văn bản)  

**Điểm mạnh**: Input có cấu trúc rõ ràng → Output tương ứng

### Qwen Best For:
✅ **Chat & Conversation** (hội thoại tự nhiên)  
✅ **Creative Writing** (viết truyện, thơ, ý tưởng)  
✅ **Code Generation** (sinh code)  
✅ **Knowledge QA** (dựa trên knowledge đã học)  
✅ **Few-shot/Zero-shot** (hiểu instruction)  

**Điểm mạnh**: Task mở, cần sự sáng tạo và follow instruction

---

## 5. Code Comparison

### ViT5 Example (Translation)
```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("VietAI/vit5-base")
model = AutoModelForSeq2SeqLM.from_pretrained("VietAI/vit5-base")

# Task-specific prefix
input_text = "dịch sang tiếng Anh: Tôi học trí tuệ nhân tạo. </s>"

inputs = tokenizer(input_text, return_tensors="pt")
outputs = model.generate(**inputs, max_length=50)

result = tokenizer.decode(outputs[0], skip_special_tokens=True)
# Output: "I study artificial intelligence."
```

### Qwen Example (Translation via prompting)
```python
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen1.5-7B")
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen1.5-7B")

# Instruction prompt
prompt = """User: Dịch sang tiếng Anh: "Tôi học trí tuệ nhân tạo."
Assistant:"""

inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_length=50)

result = tokenizer.decode(outputs[0], skip_special_tokens=True)
# Output: "User: ... \nAssistant: I study artificial intelligence."
```

**Khác biệt chính**:
- ViT5: Cần **task prefix** rõ ràng
- Qwen: Dùng **instruction** trong conversation format

---

## 6. Memory & Speed

| Metric | ViT5-Base | ViT5-Large | Qwen-7B | Qwen-14B |
|--------|-----------|------------|---------|----------|
| Params | ~220M | ~770M | ~7.7B | ~14B |
| Memory (FP16) | ~0.44GB | ~1.54GB | ~15GB | ~28GB |
| Inference speed | ⚡⚡⚡⚡⚡ (fast) | ⚡⚡⚡ (medium) | ⚡⚡ (slow) | ⚡ (very slow) |
| Suitable for CPU? | ✅ Yes | ✅ Yes (slow) | ❌ No | ❌ No |

**Nhận xét**:
- ViT5 rất nhẹ, chạy tốt trên CPU/GPU nhỏ
- Qwen cần GPU mạnh (RTX 3090/4090 trở lên)
- ViT5 Base có thể chạy trên laptop

---

## 7. Prompt Engineering

### ViT5 Prompting (Task-specific prefix)

```
"<task_prefix>: <text> </s>"
```

**Các prefix phổ biến**:
- `"tóm tắt: {text}"` → Summarization
- `"dịch sang tiếng Anh: {text}"` → Translation
- `"câu hỏi: {q} câu trả lời:"` → QA
- `"chuyển thành câu tiếng Anh: {text}"` → Style transfer

**Nguyên tắc**:
- Prefix bắt buộc (để model biết task)
- Thêm `</s>` token cuối input
- Không cần format conversation

### Qwen Prompting (Chat/Instruction format)

```
System: You are a helpful assistant.
User: Dịch sang tiếng Anh: "Xin chào"
Assistant:
```

Hoặc Multi-turn:
```
User: Tên thành phố nào là thủ đô Việt Nam?
Assistant: Hà Nội.
User: Còn thành phố lớn nhất?
Assistant: TP. Hồ Chí Minh.
```

**Nguyên tắc**:
- Dùng chat template (System/User/Assistant)
- Có thể nhiều turn
- Model tự động nhận diện role

---

## 8. Training Data

### ViT5
- ** Ngôn ngữ**: Chỉ tiếng Việt
- **Nguồn**: CC100 Vietnamese corpus + Wikipedia + crawling
- **Kích thước**: ~50GB plain text
- **Cấu trúc**: Đa dạng (news, wiki, web crawl)

### Qwen
- **Ngôn ngữ**: Multilingual (trên 100 ngôn ngữ, có tiếng Việt)
- **Nguồn**: Web text, Wikipedia, books, code, multilingual corpus
- **Kích thước**: ~3TB tokenized
- **Cấu trúc**: Rất đa dạng (text + code + multilingual)

---

## 9. Khi Nào Nên Dùng Ai?

### Chọn **ViT5** nếu:
✅ Bạn cần **tác vụ Seq2Seq rõ ràng** (input → output)  
✅ Tập trung **chỉ tiếng Việt**  
✅ Cần **tóm tắt, dịch thuật chính xác**  
✅ Tài nguyên **hạn chế** (memory, compute)  
✅ Muốn **fine-tune nhanh** trên dữ liệu nhỏ  

### Chọn **Qwen** nếu:
✅ Cần **chatbot hội thoại tự nhiên**  
✅ Muốn **mô hình đa nhiệm vụ** (code + text + chat)  
✅ Có **GPU mạnh** (16GB+ VRAM)  
✅ Cần **zero-shot/few-shot** capability  
✅ Thực hiện **instruction-following** tasks  

---

## 10. Kết Hợp Cả Hai (Advanced)

Trong thực tế, bạn có thể kết hợp:

1. **ViT5** → Dịch/chuyển ngữ, tóm tắt
2. **Qwen** → Paraphrase, tạo nội dung mở rộng

**Ví dụ flow**:
```
Original Vietnamese text → ViT5 (summarize) → Short summary → Qwen (expand to English article)
```

---

## 11. Tóm Tắt Cuối Cùng

| Tiêu chí | **ViT5** | **Qwen** |
|---------|---------|---------|
| Loại model | Encoder-Decoder | Decoder-only |
| Task best | Translation, Summarization | Chat, Generation |
| Vietnamese | Specialized | Multilingual |
| Model size | 220M - 770M | 7B - 72B |
| Speed | ⚡⚡⚡⚡⚡ (Very fast) | ⚡⚡ (Slow) |
| Memory | < 2GB | 15GB+ |
| Prompt style | Task prefix | Chat template |
| Fine-tuning easy | ✅ Very easy | ✅ Easy (but needs more data) |

---

**Lời khuyên**:
- **Bắt đầu với ViT5** nếu bạn làm NLP tiếng Việt truyền thống (dịch, tóm tắt)
- **Chọn Qwen** nếu bạn cần assistant AI chat năng động, đa nhiệm
- Cả hai đều có thể fine-tune, nhưng ViT5 nhanh hơn nhiều

---

*File: VIT5_VS_QWEN_COMPARISON.md*
*Date: 2026-04-25*
