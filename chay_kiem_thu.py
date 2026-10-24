"""Chạy test tự viết thật và lưu log; không tự tạo test_nhom.py cho sinh viên."""
import io
import unittest
from pathlib import Path
base = Path(__file__).resolve().parent
if not (base / "test_nhom.py").exists():
    raise SystemExit("Hãy tạo test_nhom.py với ít nhất 10 kiểm thử riêng trước.")
suite = unittest.defaultTestLoader.discover(str(base), pattern="test_nhom.py")
buf = io.StringIO()
r = unittest.TextTestRunner(stream=buf, verbosity=2).run(suite)
text = buf.getvalue()
print(text)
(base / "output").mkdir(exist_ok=True)
(base / "output/ket_qua_test.txt").write_text(text, encoding="utf-8")
raise SystemExit(0 if r.wasSuccessful() else 1)
