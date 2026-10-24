import sys
from pathlib import Path
if sys.version_info < (3, 10):
    raise SystemExit("Cần Python 3.10 trở lên.")
base = Path(__file__).resolve().parent
required = ("pancake.py", "search.py", "run.py", "data_cases.py")
missing = [name for name in required if not (base/name).exists()]
print("Python:", sys.version.split()[0], "\nTrình chạy:", sys.executable)
print("Thư mục:", base)
if missing:raise SystemExit("Thiếu: " + ", ".join(missing))
print("Sẵn sàng. Chỉ dùng thư viện chuẩn; không cần pip install.")
