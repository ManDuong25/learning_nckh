╔══════════════════════════════════════════════════════════════════════════╗
║                     ViT5 LEARNING CHECKLIST                              ║
║          Bạn đã hiểu đầy đủ về ViT5 chưa?                               ║
╚══════════════════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────────────────────┐
│ 📚 ĐỌC & HIỂU                                                             │
├──────────────────────────────────────────────────────────────────────────┤
│ ☐ QUICKSTART.txt              — Bắt đầu trong 5 phút                     │
│ ☐ VIT5_OVERVIEW.md            — Kiến trúc & use cases                    │
│ ☐ VIT5_VS_QWEN_COMPARISON.md  — So sánh với Qwen                          │
│ ☐ ALL_VIT5_VARIANTS.md        — Catalog tất cả models                     │
│ ☐ USAGE_GUIDE.md              — Patterns & best practices                 │
│ ☐ CHEAT_SHEET.txt             — Reference nhanh                           │
│ ☐ SUMMARY.md                  — Tổng hợp toàn bộ                          │
│ ☐ INDEX.md                    — File index & purposes                     │
└──────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│ 🐍 CHẠY SCRIPTS                                                           │
├──────────────────────────────────────────────────────────────────────────┤
│ ☐ quick-demo-vit5.py          — Demo 4 tasks (2 phút)                    │
│ ☐ debug-vit5-model.py         — Debug chi tiết (10 phút)                 │
│ ☐ list-all-vit5-models.py     — List 87+ variants từ HuggingFace         │
└──────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│ 🧠 KIẾN THỨC CƠ BẢN                                                        │
├──────────────────────────────────────────────────────────────────────────┤
│ ☐ Biết ViT5 là gì (encoder-decoder dựa trên T5)                          │
│ ☐ Hiểu Base vs Large: 220M vs 770M params                                │
│ ☐ Biết 2 pretrained models: vit5-base, vit5-large                        │
│ ☐ Biết các finetuned variants (summarization, translation)               │
│ ☐ Hiểu kiến trúc: 12L|24L encoder + 12L|24L decoder                     │
│ ☐ Hiểu multi-head attention: 12|16 heads, 64 dim                         │
│ ☐ Biết vocabulary: SentencePiece, 36,096 tokens                          │
│ ☐ Biết training objective: span corruption + downstream                  │
└──────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│ 🎯 TASK PROMPT TEMPLATES                                                   │
├──────────────────────────────────────────────────────────────────────────┤
│ ☐ Summarization:    "tóm tắt: {text} </s>"                               │
│ ☐ Translation Vi→En: "dịch sang tiếng Anh: {text} </s>"                 │
│ ☐ Translation En→Vi: "dịch sang tiếng Việt: {text} </s>"                │
│ ☐ Question Answer:   "câu hỏi: {q} câu trả lời:"                         │
│ ☐ NER:              "nhận diện thực thể: {text} </s>"                   │
└──────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│ ⚙️ CONFIG NUMBERS (Base)                                                  │
├──────────────────────────────────────────────────────────────────────────┤
│ ☐ d_model: 768                                                            │
│ ☐ Encoder layers: 12                                                      │
│ ☐ Decoder layers: 12                                                      │
│ ☐ Attention heads: 12                                                     │
│ ☐ FFN dim: 3072                                                           │
│ ☐ Total params: ~220M                                                     │
│ ☐ Memory (FP16): ~0.44GB                                                  │
└──────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│ ⚙️ CONFIG NUMBERS (Large)                                                 │
├──────────────────────────────────────────────────────────────────────────┤
│ ☐ d_model: 1024                                                           │
│ ☐ Encoder layers: 24                                                      │
│ ☐ Decoder layers: 24                                                      │
│ ☐ Attention heads: 16                                                     │
│ ☐ FFN dim: 2816                                                           │
│ ☐ Total params: ~770M                                                     │
│ ☐ Memory (FP16): ~1.54GB                                                  │
└──────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│ 🔄 SO SÁNH VIT5 vs QWEN                                                    │
├──────────────────────────────────────────────────────────────────────────┤
│ ☐ Hiểu ViT5 là Encoder-Decoder, Qwen là Decoder-Only                      │
│ ☐ Biết ViT5 dùng cho translation/summarization/QA                         │
│ ☐ Biết Qwen dùng cho chat/creative/code                                    │
│ ☐ Hiểu input format khác nhau (prefix vs chat template)                   │
│ ☐ Biết memory: ViT5-base 0.44GB vs Qwen-7B 15GB+                          │
│ ☐ Biết speed: ViT5 150 tok/s vs Qwen ~20 tok/s                            │
└──────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│ 🎯 CHỌN MODEL ĐÚNG                                                         │
├──────────────────────────────────────────────────────────────────────────┤
│ ☐ Summarization → vit5-large-vietnews (quality) hoặc base (speed)         │
│ ☐ Translation → envit5-base                                               │
│ ☐ General task → vit5-base                                                │
│ ☐ High resource → vit5-large                                              │
│ ☐ Low resource  → vit5-base (hoặc 8-bit quantization)                     │
└──────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│ 💻 CODE SKILLS                                                             │
├──────────────────────────────────────────────────────────────────────────┤
│ ☐ Load model từ HuggingFace: AutoTokenizer/AutoModel                      │
│ ☐ Tokenize với task prefix                                                │
│ ☐ Generate với: max_length, num_beams, temperature                        │
│ ☐ Decode output: skip_special_tokens=True                                 │
│ ☐ Move to GPU: model.to("cuda")                                           │
│ ☐ Use FP16: torch_dtype=torch.float16                                     │
│ ☐ Batch inference                                                          │
└──────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│ 🔧 GENERATION PARAMETERS                                                   │
├──────────────────────────────────────────────────────────────────────────┤
│ ☐ Quality: num_beams=4-8, length_penalty=2.0                             │
│ ☐ Speed: num_beams=1                                                       │
│ ☐ Diversity: temperature=0.7-1.0, top_k=50, top_p=0.95                   │
│ ☐ Control length: min_length, max_length                                  │
│ ☐ Avoid repeat: no_repeat_ngram_size=2                                    │
└──────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│ 🎓 FINE-TUNING                                                            │
├──────────────────────────────────────────────────────────────────────────┤
│ ☐ Biết dùng HuggingFace Seq2SeqTrainer                                    │
│ ☐ Biết prepare dataset cho text-to-text format                            │
│ ☐ Biết set hyperparams: lr=3e-4, epochs=3-5, batch=8                     │
│ ☐ Biết evaluate với ROUGE/BLEU/F1                                         │
│ ☐ Đã thử fine-tune trên dataset nhỏ (500+ mẫu)                            │
└──────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│ 🚀 PRODUCTION                                                              │
├──────────────────────────────────────────────────────────────────────────┤
│ ☐ Export to ONNX                                                           │
│ ☐ Optimize với FP16 / 8-bit quantization                                  │
│ ☐ Wrap trong FastAPI REST endpoint                                         │
│ ☐ Add logging & monitoring                                                │
│ ☐ Test với 100+ samples trước deploy                                       │
│ ☐ Batch inference implementation                                           │
└──────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│ 🐛 TROUBLESHOOTING                                                         │
├──────────────────────────────────────────────────────────────────────────┤
│ ☐ Out of memory → Use FP16, reduce batch/beams                            │
│ ☐ Gibberish output → Add task prefix, check max_length                    │
│ ☐ Output too short → length_penalty=2.0, min_length                      │
│ ☐ Slow inference → num_beams=1, use GPU, batch size>1                     │
│ ☐ Model not loading → upgrade transformers, clear cache                   │
└──────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│ 📊 BENCHMARKS                                                              │
├──────────────────────────────────────────────────────────────────────────┤
│ ☐ Biết ViT5-large đạt ROUGE-1: 43.38 (VietNews)                           │
│ ☐ Biết ViT5-base đạt ROUGE-1: 42.15                                      │
│ ☐ So sánh với mBART (41.52) và T5-base (40.23)                            │
│ ☐ Hiểu ViT5 vượt trội multilingual models                                 │
└──────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│ 📈 RESOURCE AWARENESS                                                      │
├──────────────────────────────────────────────────────────────────────────┤
│ ☐ Biết vit5-base chạy được trên CPU (chậm)                               │
│ ☐ Biết vit5-large cần GPU 6GB+ (RTX 3080/4090)                            │
│ ☐ Biết vit5-base có thể batch size 8 trên 16GB GPU                        │
│ ☐ Biết vit5-large batch size 2-4                                         │
│ ☐ Biết 8-bit quantization giảm 3x memory                                  │
└──────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│ 🔍 RESEARCH & DEVELOPMENT                                                  │
├──────────────────────────────────────────────────────────────────────────┤
│ ☐ Đã đọc paper: https://arxiv.org/abs/2205.06457                          │
│ ☐ Đã xem GitHub repo: https://github.com/vietai/ViT5                       │
│ ☐ Đã check HuggingFace models: https://huggingface.co/VietAI               │
│ ☐ Biết training data: CC100 Vietnamese + Wikipedia                        │
│ ☐ Biết pretraining steps: 1M (base), 1.5M (large)                         │
└──────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│ ✅ PROJECT COMPLETION                                                      │
├──────────────────────────────────────────────────────────────────────────┤
│ ☐ Đã chạy được inference với ít nhất 3 tasks khác nhau                    │
│ ☐ Đã fine-tune ViT5-base trên dataset nhỏ (>=500 mẫu)                     │
│ ☐ Đã so sánh output với ground truth (ROUGE/F1)                           │
│ ☐ Đã implements API wrapper (FastAPI/Flask) — optional                    │
│ ☐ Đã optimize inference (FP16, quantization) — optional                   │
└──────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│ 🎓 CERTIFICATION (Optional)                                                │
├──────────────────────────────────────────────────────────────────────────┤
│ Tự đánh giá:                                                               │
│                                                                             │
│ Score: ___ / 100                                                           │
│                                                                             │
│ ≥ 90: Expert — Bạn có thể fine-tune & deploy ViT5                         │
│ 70-89: Proficient — Bạn có thể sử dụng ViT5 production-ready              │
│ 50-69: Intermediate — Bạn hiểu kiến trúc & code cơ bản                   │
│ 30-49: Beginner — Bạn cần đọc lại docs                                     │
│ < 30: Newbie — Bắt đầu từ QUICKSTART.txt                                  │
└──────────────────────────────────────────────────────────────────────────┘

╔══════════════════════════════════════════════════════════════════════════╗
║  PROGRESS TRACKING                                                         ║
╠══════════════════════════════════════════════════════════════════════════╣
║  Reading:    ___ / 7 docs  (___%)                                          ║
║  Running:    ___ / 3 scripts (___%)                                        ║
║  Knowledge:  ___ / 30 items (___%)                                         ║
║  Skills:     ___ / 12 items (___%)                                         ║
║  Projects:   ___ / 5 milestones (___%)                                     ║
╚══════════════════════════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════════════════════╗
║  NEXT STEPS                                                                ║
╠══════════════════════════════════════════════════════════════════════════╣
║  1. Read QUICKSTART.txt (5 phút)                                          ║
║  2. Run python quick-demo-vit5.py (2 phút)                                ║
║  3. Read VIT5_OVERVIEW.md (15 phút)                                       ║
║  4. Run python debug-vit5-model.py (10 phút)                              ║
║  5. Check ALL_VIT5_VARIANTS.md, chọn model phù hợp (5 phút)               ║
║  6. Đọc USAGE_GUIDE.md, code theo ví dụ (20 phút)                         ║
║  7. Fine-tune trên dataset của bạn (1-2 giờ)                              ║
║  8. Deploy lên production (1-2 giờ)                                       ║
╚══════════════════════════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════════════════════╗
║  TIME INVESTMENT                                                           ║
╠══════════════════════════════════════════════════════════════════════════╣
║  Reading only:         ~1.5 hours                                         ║
║  Reading + running:    ~2 hours                                           ║
║  Fine-tuning practice: ~3-5 hours                                         ║
║  Production project:   ~1-2 days                                          ║
╚══════════════════════════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════════════════════╗
║  SUCCESS CRITERIA                                                          ║
╠══════════════════════════════════════════════════════════════════════════╣
║  ✅ Bạn có thể tóm tắt văn bản tiếng Việt với ViT5                        ║
║  ✅ Bạn có thể dịch Anh↔Việt với ViT5                                     ║
║  ✅ Bạn biết khi nào dùng ViT5, khi nào dùng Qwen                         ║
║  ✅ Bạn biết chọn đúng variant cho task                                    ║
║  ✅ Bạn có thể fine-tune ViT5 trên dataset riêng                          ║
║  ✅ Bạn có thể deploy ViT5 lên production                                  ║
╚══════════════════════════════════════════════════════════════════════════╝

────────────────────────────────────────────────────────────────────────────
"Knowledge is not acquired until it is used." — Start coding now!
────────────────────────────────────────────────────────────────────────────

*Checklist version: 1.0*
*Last updated: 2026-04-25*
*Package: ViT5 Learning Resource Pack*
