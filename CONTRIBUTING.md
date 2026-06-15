# Contributing to Iraq WDI Analysis
## المساهمة في مشروع تحليل مؤشرات العراق

Thank you for your interest in contributing! We welcome contributions from everyone.

## How to Contribute | كيف تساهم

### Reporting Bugs | الإبلاغ عن الأخطاء

If you find a bug, please open an issue on GitHub with:
- A clear description of the problem
- Steps to reproduce the bug
- Expected vs actual behavior
- Your environment (Python version, OS)

إذا وجدت خطأً، افتح issue على GitHub مع:
- وصف واضح للمشكلة
- خطوات لإعادة إنتاج الخطأ
- السلوك المتوقع مقابل الفعلي
- بيئتك (إصدار بايثون، نظام التشغيل)

### Suggesting Features | اقتراح الميزات

We welcome feature suggestions! Please describe:
- The feature you want to add
- Why it would be useful
- How you envision it working

نرحب باقتراحات الميزات! يرجى وصف:
- الميزة التي تريد إضافتها
- لماذا ستكون مفيدة
- كيف تتخيلها تعمل

### Submitting Pull Requests | إرسال طلبات السحب

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`python -m pytest tests/`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## Development Setup | إعداد التطوير

```bash
# Clone the repository
git clone https://github.com/h19kod/data_anlysis_.git
cd data_anlysis_

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .

# Run tests
python -m pytest tests/ -v
```

## Code Style | أسلوب الكود

- Follow PEP 8 guidelines
- Use type hints for function signatures
- Write docstrings for all public functions and classes
- Add comments in Arabic for key sections
- Keep functions focused and small

## Testing | الاختبار

All contributions should include tests:
- Unit tests for new functions
- Integration tests for new features
- Ensure all existing tests pass

## Documentation | التوثيق

- Update README.md if you change user-facing behavior
- Add docstrings to new functions
- Update docs/ if you add new modules

## License | الترخيص

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Questions?** Open an issue or contact @h19kod

**أسئلة؟** افتح issue أو تواصل مع @h19kod
