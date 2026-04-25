"""
Quick Demo Script for ViT5
============================
Script demo nhanh để test ViT5 với các tác vụ phổ biến.
"""

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

def load_model(model_name="VietAI/vit5-base"):
    """Load tokenizer and model."""
    print(f"Loading {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    model.eval()
    
    # Move to GPU if available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    print(f"Model loaded on {device}")
    
    return tokenizer, model, device

def generate(model, tokenizer, text, max_length=50, num_beams=4, device="cpu"):
    """Generate text from input."""
    inputs = tokenizer(text, return_tensors="pt").to(device)
    
    with torch.no_grad():
        outputs = model.generate(
            input_ids=inputs.input_ids,
            attention_mask=inputs.attention_mask,
            max_length=max_length,
            num_beams=num_beams,
            early_stopping=True,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )
    
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def main():
    print("=" * 60)
    print("ViT5 Quick Demo")
    print("=" * 60)
    
    # Load model
    tokenizer, model, device = load_model("VietAI/vit5-base")
    
    print(f"\nSpecial tokens:")
    print(f"  Pad: {tokenizer.pad_token} (id: {tokenizer.pad_token_id})")
    print(f"  EOS: {tokenizer.eos_token} (id: {tokenizer.eos_token_id})")
    print(f"  Decoder start: {tokenizer.decoder_start_token} (id: {tokenizer.decoder_start_token_id})")
    
    # Test cases
    test_cases = [
        {
            "task": "Summarization",
            "input": "tóm tắt: Trí tuệ nhân tạo (AI) là lĩnh vực nghiên cứu và phát triển các hệ thống máy tính có khả năng thực hiện các nhiệm vụ thường đòi hỏi trí thông minh của con người. Các ứng dụng AI hiện nay bao gồm nhận dạng giọng nói, dịch máy, xe tự lái và chẩn đoán y tế. </s>",
            "max_length": 60,
        },
        {
            "task": "Translation (Vi→En)",
            "input": "dịch sang tiếng Anh: Tôi yêu Việt Nam, một quốc gia đầy màu sắc và bình yên. </s>",
            "max_length": 40,
        },
        {
            "task": "Question Answering",
            "input": "câu hỏi: Thủ đô Việt Nam là gì? câu trả lời:",
            "max_length": 20,
        },
        {
            "task": "Text Generation (from title)",
            "input": "tiêu đề: Học sinh Việt Nam đạt giảiOlympic quốc tế nội dung:",
            "max_length": 50,
        }
    ]
    
    print("\n" + "=" * 60)
    print("GENERATION RESULTS")
    print("=" * 60)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{i}. Task: {test['task']}")
        print(f"   Input:  \"{test['input']}\"")
        
        output = generate(
            model, tokenizer, test['input'],
            max_length=test['max_length'],
            device=device
        )
        print(f"   Output: \"{output}\"")
    
    print("\n" + "=" * 60)
    print("Demo hoàn tất!")
    print("=" * 60)

if __name__ == "__main__":
    main()
