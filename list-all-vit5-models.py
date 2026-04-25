"""
List all ViT5 variants available on HuggingFace
================================================
Script này liệt kê TẤT CẢ các phiên bản ViT5 có sẵn trên HuggingFace Hub.
"""

try:
    from huggingface_hub import list_models
except ImportError:
    print("Please install huggingface_hub: pip install huggingface_hub")
    exit(1)

def list_vit5_models():
    """List all ViT5-related models from VietAI."""
    print("Fetching ViT5 models from HuggingFace Hub...")
    print("=" * 70)
    
    # Get all models from VietAI org containing 'vit5'
    models = list(list_models(author="VietAI", search="vit5"))
    
    print(f"\nTotal ViT5 models found: {len(models)}\n")
    
    # Categorize
    base_models = []
    large_models = []
    finetuned_base = []
    finetuned_large = []
    other = []
    
    for model in models:
        model_id = model.id
        if "vit5-base" in model_id and "vit5-base-vietnews" not in model_id:
            base_models.append(model_id)
        elif "vit5-large" in model_id and "vit5-large-vietnews" not in model_id:
            large_models.append(model_id)
        elif "vit5-base-vietnews" in model_id:
            finetuned_base.append(model_id)
        elif "vit5-large-vietnews" in model_id:
            finetuned_large.append(model_id)
        else:
            other.append(model_id)
    
    print("📦 PRETRAINED MODELS")
    print("-" * 70)
    for m in base_models:
        print(f"  ✓ {m}")
    for m in large_models:
        print(f"  ✓ {m}")
    
    print(f"\n📊 FINETUNED MODELS")
    print("-" * 70)
    print(f"\n  Based on vit5-base ({len(finetuned_base)} models):")
    for m in finetuned_base[:10]:  # Show first 10
        print(f"    • {m}")
    if len(finetuned_base) > 10:
        print(f"    ... and {len(finetuned_base) - 10} more")
    
    print(f"\n  Based on vit5-large ({len(finetuned_large)} models):")
    for m in finetuned_large[:10]:  # Show first 10
        print(f"    • {m}")
    if len(finetuned_large) > 10:
        print(f"    ... and {len(finetuned_large) - 10} more")
    
    if other:
        print(f"\n🔧 OTHER VARIANTS ({len(other)}):")
        for m in other[:5]:
            print(f"    • {m}")
    
    # Summary statistics
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Pretrained base models: {len(base_models)}")
    print(f"  Pretrained large models: {len(large_models)}")
    print(f"  Finetuned on base: {len(finetuned_base)}")
    print(f"  Finetuned on large: {len(finetuned_large)}")
    print(f"  Total: {len(models)}")
    
    # Show most popular
    print("\n" + "=" * 70)
    print("MOST POPULAR (by downloads)")
    print("=" * 70)
    popular = sorted(models, key=lambda x: x.downloads if hasattr(x, 'downloads') else 0, reverse=True)[:10]
    for i, model in enumerate(popular, 1):
        downloads = getattr(model, 'downloads', 'N/A')
        print(f"  {i}. {model.id} ({downloads} downloads)")

def search_finetuned_for_task(task_name="summarization"):
    """Search for finetuned models for specific task."""
    print(f"\nSearching for '{task_name}' models...")
    models = list(list_models(author="VietAI", search="vit5"))
    
    matching = [m for m in models if task_name.lower() in m.id.lower()]
    
    print(f"Found {len(matching)} models:")
    for m in matching:
        print(f"  - {m.id}")

if __name__ == "__main__":
    list_vit5_models()
    
    # Search for specific task models
    print("\n")
    search_finetuned_for_task("summarization")
    print()
    search_finetuned_for_task("translation")
    print()
    search_finetuned_for_task("ner")
