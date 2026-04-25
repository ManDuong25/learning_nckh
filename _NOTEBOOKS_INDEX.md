# ViT5 Jupyter Notebooks — COMPLETE SET

## 📦 Notebooks Package

Đã chuyển đổi **tất cả scripts Python thành Jupyter notebooks** để bạn dễ chạy và đọc.

---

## 📓 Notebooks (5 files)

### 01-debug-vit5-model.ipynb
**Mục đích:** Debug chi tiết kiến trúc ViT5

**Nội dung:**
1. Environment verification (Python, PyTorch, CUDA)
2. Load vit5-base & vit5-large
3. Configuration analysis (layers, heads, FFN, params)
4. Special tokens & vocabulary display
5. Tokenization examples (Vietnamese sentences)
6. Architecture visualization (text diagram)
7. Forward pass (show shapes)
8. Generation demo (3 tasks)
9. Base vs Large comparison (speed, memory)
10. Summary & observations

**Độ dài:** ~30 cells
**Thời gian chạy:** 10-15 phút
**Output:** Hiểu sâu từng layer, parameters, attention

---

### 02-quick-demo-vit5.ipynb
**Mục đích:** Demo nhanh 4 tasks

**Nội dung:**
1. Setup & load model
2. Task 1: Summarization (tóm tắt)
3. Task 2: Translation (Anh-Việt)
4. Task 3: Question Answering
5. Task 4: Text generation (tiêu đề → nội dung)
6. Parameter comparison (greedy vs beam vs sampling)

**Độ dài:** ~15 cells
**Thời gian chạy:** 2-3 phút
**Output:** Thấy ViT5 generate text thực tế

---

### 03-explore-vit5-variants.ipynb
**Mục đích:** Khám phá tất cả variants từ HuggingFace

**Nội dung:**
1. Fetch all ViT5 models from HF Hub
2. Categorize: pretrained, finetuned, other
3. Display all 87+ models in table
4. Performance benchmark table (ROUGE)
5. Model selection helper function
6. Search by task keyword
7. Statistics summary

**Độ dài:** ~12 cells
**Thời gian chạy:** 2-3 phút
**Output:** Bảng đầy đủ tất cả models, recommendations

---

### 04-vit5-vs-qwen.ipynb
**Mục đích:** So sánh chi tiết ViT5 vs Qwen

**Nội dung:**
1. Architecture deep dive (encoder-decoder vs decoder-only diagrams)
2. Input/output format differences (task prefix vs chat template)
3. Training objectives (span corruption vs causal LM)
4. Performance & speed comparison table
5. Use case decision matrix
6. Code comparison (side-by-side)
7. Interactive comparison table (10 aspects)

**Độ dài:** ~20 cells (mostly markdown)
**Thời gian đọc:** 10-15 phút
**Output:** Biết chắc khi nào dùng ViT5, khi nào dùng Qwen

---

### 05-fine-tuning-guide.ipynb
**Mục đích:** Hướng dẫn fine-tune từ A-Z

**Nội dung:**
1. When to fine-tune (vs use pretrained)
2. Dataset preparation (text-to-text format)
3. Preprocessing function
4. Training arguments (hyperparameters)
5. Seq2SeqTrainer setup
6. Training loop (demo với sample data)
7. Evaluation (ROUGE metric)
8. Deployment checklist
9. Save & load model

**Độ dài:** ~25 cells
**Thời gian chạy:** Demo ~5 phút, training thực tế 1-5 hours
**Output:** Fine-tune được ViT5 cho task của bạn

---

## 🎯 Suggested Order

### Path 1: Người mới bắt đầu (1 ngày)
```
01 → 02 → 03 → Read docs → Done!
```

### Path 2: Người biết Qwen, muốn so sánh (2 ngày)
```
01 → 02 → 04 → 03 → Fine-tune practice
```

### Path 3: Production ready (1 tuần)
```
01 → 02 → 03 → 05 (fine-tune) → Deploy → Optimize
```

---

## 📊 Notebook Features

### All notebooks have:
- ✅ Clear markdown explanations
- ✅ Runnable code cells
- ✅ Real outputs (not placeholders)
- ✅ Error handling
- ✅ Tips & best practices
- ✅ Next steps section
- ✅ Beautiful formatting

### Interactive elements:
- Tables (pandas DataFrame)
- Progress indicators
- Timing measurements
- Comparison matrices
- Decision trees

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install torch transformers datasets accelerate sentencepiece
pip install huggingface_hub rouge_score

# 2. Open Jupyter
jupyter notebook

# 3. Start with Notebook 01
# Press Shift+Enter để chạy từng cell
```

---

## 💡 Notebook Tips

### Running:
- `Shift+Enter` — Run cell và chuyển sang cell tiếp
- `Ctrl+Enter` — Run cell, đứng tại cell hiện tại
- `Alt+Enter` — Run cell, insert cell below

### Editing:
- Double-click cell để edit
- Toolbar có: save, add cell, delete cell, move cells
- `Kernel → Restart` nếu cần reset

### Outputs:
- Some cells cần GPU (fine-tuning)
- Số liệu có thể khác nhau tùy environment
- Nếu CUDA out of memory → giảm batch size

---

## 🎓 What You'll Master

Sau 5 notebooks:

| Skill | Notebook |
|-------|----------|
| Understand ViT5 architecture | 01 ✅ |
| Run inference & generation | 02 ✅ |
| Choose right model variant | 03 ✅ |
| Compare ViT5 vs Qwen | 04 ✅ |
| Fine-tune on custom data | 05 ✅ |

---

## 📈 Content Stats

| Notebook | Cells | Lines of code | Read time | Run time |
|----------|-------|---------------|-----------|----------|
| 01 | ~30 | ~200 | 15 min | 10-15 min |
| 02 | ~15 | ~100 | 5 min | 2-3 min |
| 03 | ~12 | ~150 | 10 min | 2-3 min |
| 04 | ~20 | ~100 | 15 min | <1 min |
| 05 | ~25 | ~180 | 20 min | 5 min (demo) |
| **Total** | **~102** | **~730** | **~1 hour** | **~25 min** |

---

## 🔄 How to Use

### Daily practice:
```python
# Morning: Read notebook theory (markdown cells)
# Afternoon: Run code cells, experiment
# Evening: Take notes, summarize learning
```

### For reference:
- Keep notebooks open khi làm project
- Copy code cells vào project của bạn
- Sửa parameters để thử nghiệm

### For teaching:
- Show notebooks cho teammates
- Walk through cells together
- Do live coding theo notebook

---

## 🎁 Bonus: Notebook Shortcuts

| Action | Shortcut (Jupyter) |
|--------|-------------------|
| Run cell | Shift+Enter |
| Run & insert below | Alt+Enter |
| Run & stay | Ctrl+Enter |
| Save | Ctrl+S |
| Undo | Ctrl+Z |
| Find | Ctrl+F |
| Toggle line numbers | L |

---

## ✅ Completion Checklist

- [ ] Opened `01-debug-vit5-model.ipynb`
- [ ] Ran all cells in Notebook 01
- [ ] Understood output (config, params, shapes)
- [ ] Ran `02-quick-demo-vit5.ipynb`
- [ ] Saw generation on 4 tasks
- [ ] Ran `03-explore-vit5-variants.ipynb`
- [ ] Chose model for your use case
- [ ] Read `04-vit5-vs-qwen.ipynb`
- [ ] Understood when to use which model
- [ ] Went through `05-fine-tuning-guide.ipynb`
- [ ] (Optional) Fine-tuned on your dataset

---

## 🏆 Final Result

✅ **5 Jupyter notebooks — Complete ViT5 learning path**

**Từ zero đến expert:**
1. Debug → Hiểu architecture
2. Demo → Thấy nó hoạt động
3. Explore → Chọn model đúng
4. Compare → Biết khi nào dùng ViT5 vs Qwen
5. Fine-tune → Tự train model riêng

**Plus 11 documentation files** để reference.

---

## 🎯 Start Now!

```
jupyter notebook
→ Open 01-debug-vit5-model.ipynb
→ Press Shift+Enter
→ Learn!
```

---

**Version:** 1.0\n",
   "**Created:** 2026-04-25\n",
   "**Format:** Jupyter Notebook 4.0\n",
   "**Total cells:** ~102\n",
   "**Status:** ✅ Production-ready\n",
   "\n",
   "---\n",
   "\n",
   "**Happy learning! 🚀**"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
