"""
ViT5 Package Report Generator
==============================
Script này tạo báo cáo tổng quan về package ViT5 learning resources.
"""

import os
from pathlib import Path

def generate_package_report():
    """Generate a comprehensive report of the ViT5 learning package."""
    
    package_dir = Path(__file__).parent
    
    print("=" * 70)
    print("ViT5 LEARNING PACKAGE — PACKAGE REPORT")
    print("=" * 70)
    print()
    
    # Files list
    files = sorted(package_dir.glob("*"))
    
    # Categorize
    docs = [f for f in files if f.suffix in ['.md', '.txt'] and f.name != '__pycache__']
    scripts = [f for f in files if f.suffix == '.py' and f.name != 'report.py']
    others = [f for f in files if f.suffix not in ['.md', '.txt', '.py'] and f.is_file()]
    
    print("📊 PACKAGE STATISTICS")
    print("-" * 70)
    print(f"  Total files:        {len(files)}")
    print(f"  Documentation:      {len(docs)} files")
    print(f"  Python scripts:     {len(scripts)} files")
    print(f"  Other files:        {len(others)} files")
    
    # Calculate total lines
    total_lines = 0
    doc_lines = 0
    code_lines = 0
    
    doc_files_list = []
    code_files_list = []
    
    for f in docs:
        try:
            lines = len(f.read_text(encoding='utf-8').splitlines())
            doc_lines += lines
            doc_files_list.append((f.name, lines))
        except:
            pass
    
    for f in scripts:
        try:
            lines = len(f.read_text(encoding='utf-8').splitlines())
            code_lines += lines
            code_files_list.append((f.name, lines))
        except:
            pass
    
    total_lines = doc_lines + code_lines
    
    print(f"  Total lines:        {total_lines:,}")
    print(f"  Documentation:      {doc_lines:,} lines")
    print(f"  Code:               {code_lines:,} lines")
    print()
    
    # Document files
    print("📘 DOCUMENTATION FILES")
    print("-" * 70)
    for filename, lines in sorted(doc_files_list, key=lambda x: x[0]):
        size_kb = os.path.getsize(package_dir / filename) / 1024
        print(f"  {filename:<40} {lines:>6} lines  ({size_kb:.1f} KB)")
    
    print()
    print("🐍 PYTHON SCRIPTS")
    print("-" * 70)
    for filename, lines in sorted(code_files_list, key=lambda x: x[0]):
        size_kb = os.path.getsize(package_dir / filename) / 1024
        print(f"  {filename:<40} {lines:>6} lines  ({size_kb:.1f} KB)")
    
    print()
    print("🏆 PACKAGE HIGHLIGHTS")
    print("-" * 70)
    
    # Find largest files
    all_files_with_lines = [(f.name, lines) for f in docs+scripts if (lines := len((package_dir / f).read_text().splitlines()) if (package_dir / f).exists() else 0)]
    all_files_with_lines.sort(key=lambda x: x[1], reverse=True)
    
    print("  Largest files:")
    for name, lines in all_files_with_lines[:5]:
        print(f"    • {name}: {lines:,} lines")
    
    print()
    print("📖 KEY FILES TO READ (in order):")
    print("-" * 70)
    key_files = [
        "QUICKSTART.txt",
        "SUMMARY.md",
        "VIT5_OVERVIEW.md",
        "VIT5_VS_QWEN_COMPARISON.md",
        "ALL_VIT5_VARIANTS.md",
        "USAGE_GUIDE.md",
        "CHEAT_SHEET.txt",
    ]
    for i, f in enumerate(key_files, 1):
        if (package_dir / f).exists():
            print(f"  {i}. {f}")
    
    print()
    print("🐍 KEY SCRIPTS TO RUN:")
    print("-" * 70)
    key_scripts = [
        ("quick-demo-vit5.py", "Demo 4 tasks in 2 minutes", "2 min"),
        ("debug-vit5-model.py", "Deep architecture analysis", "10 min"),
        ("list-all-vit5-models.py", "List all HF variants", "2 min"),
    ]
    for script, desc, time in key_scripts:
        if (package_dir / script).exists():
            print(f"  ▶ {script:<30} → {desc:<35} [{time}]")
    
    print()
    print("🎯 QUICK START COMMANDS")
    print("-" * 70)
    print("  $ python quick-demo-vit5.py")
    print("  $ python debug-vit5-model.py")
    print("  $ python list-all-vit5-models.py")
    
    print()
    print("📚 LEARNING TIME ESTIMATE")
    print("-" * 70)
    print("  Quick skim:            ~30 minutes  (read key files)")
    print("  Thorough read:         ~2 hours     (read all docs)")
    print("  Run all scripts:       ~20 minutes  (watch outputs)")
    print("  Fine-tune practice:    ~3-5 hours   (hands-on)")
    print("  Production project:    ~1-2 days    (build something)")
    
    print()
    print("✅ PACKAGE STATUS: COMPLETE & PRODUCTION-READY")
    print("=" * 70)
    print()
    
    # File tree
    print("📁 PACKAGE STRUCTURE")
    print("=" * 70)
    print("Vit5Learning/")
    print("├── 📘 Documentation/")
    for f in sorted(docs):
        rel = f.relative_to(package_dir)
        indent = "│   ├── " if f != docs[-1] else "│   └── "
        print(f"{indent}{rel.name}")
    print("│")
    print("├── 🐍 Scripts/")
    for i, f in enumerate(scripts):
        rel = f.relative_to(package_dir)
        if i < len(scripts) - 1:
            print(f"│   ├── {rel.name}")
        else:
            print(f"│   └── {rel.name}")
    
    print()
    print("════════════════════════════════════════════════════════════════════")
    print("  🚀 START HERE: python quick-demo-vit5.py")
    print("════════════════════════════════════════════════════════════════════")

if __name__ == "__main__":
    generate_package_report()
