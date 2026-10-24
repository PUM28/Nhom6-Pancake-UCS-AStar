"""Kiểm tra thành phần cơ bản rồi tạo ZIP. Không chứng nhận chất lượng bài làm."""
import argparse
import itertools
import json
import re
import zipfile
from pathlib import Path
from data_cases import CASES, GOAL, CONFIGS, ORDERS
from pancake import check_path, validate_problem, flip
BASE=Path(__file__).resolve().parent


def inspect_results(path,cases):
    rows=json.loads(path.read_text(encoding="utf-8-sig"))
    byname={c["name"]:c for c in cases}
    expected={(c["name"],alg,h,o) for c in cases for o in ORDERS for alg,h in CONFIGS}
    got=[]
    for r in rows:
        key=(r["case"],r["algorithm"],r["heuristic"],r["order"]);got.append(key)
        c=byname[r["case"]]
        if tuple(r["start"])!=tuple(c["start"]) or tuple(r["goal"])!=tuple(c["goal"]):
            raise ValueError("JSON khác dữ liệu đã khai báo")
        p=check_path(c["start"],c["goal"],r["actions"],r["path"])
        if r["status"]!="found" or (p["cost"],p["moves"])!=(r["cost"],r["moves"]):
            raise ValueError("Dòng kết quả không khớp path/actions/cost")
    if len(got)!=len(expected) or set(got)!=expected:
        raise ValueError(f"{path.name}: cần đủ {len(expected)} cấu hình khác nhau")


def main():
    p=argparse.ArgumentParser();p.add_argument("--nhom",required=True);a=p.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9_-]+",a.nhom):p.error("Tên nhóm chỉ dùng chữ/số/_/-")
    required=["BaoCao.pdf","TinhTay.pdf","ThuyetTrinh.pptx","test_nhom.py","README_NHOM.md","DongGop.md",
              "du_lieu_nhom.json","output/bat_buoc.json","output/bat_buoc.csv","output/tu_tao.json",
              "output/tu_tao.csv","output/H_ucs.json","output/H_ucs_trace.csv","output/H_astar.json",
              "output/H_astar_trace.csv","output/ket_qua_test.txt"]
    missing=[x for x in required if not (BASE/x).is_file() or (BASE/x).stat().st_size==0]
    if missing:raise SystemExit("Chưa đủ tệp:\n"+"\n".join(missing))
    cases=json.loads((BASE/"du_lieu_nhom.json").read_text(encoding="utf-8-sig"))["cases"]
    if len(cases)!=2 or {c["name"] for c in cases}!={"N1","N2"}:raise ValueError("Cần N1,N2")
    common_goal=tuple(cases[0]["goal"])
    for c in cases:
        s,g=validate_problem(c["start"],c["goal"])
        if len(s)!=7 or g==tuple(range(1,8)) or g!=common_goal or s==g:
            raise ValueError("Hai case cần 7 bánh, cùng goal mới, start khác goal")
        trial=g
        for k in c["scramble_actions"]:trial=flip(trial,k)
        if trial!=s:raise ValueError("Lịch sử xáo trộn không khớp start")
    if cases[0]["start"]==cases[1]["start"]:raise ValueError("N1 và N2 phải khác nhau")
    common=[dict(name=n,start=list(s),goal=list(GOAL)) for n,s in CASES.items()]
    inspect_results(BASE/"output/bat_buoc.json",common)
    inspect_results(BASE/"output/tu_tao.json",cases)
    names=set(required)
    names.update(p.name for p in BASE.glob("*.py"))
    dest=BASE/f"{a.nhom}_Pancake_GiuaKy.zip"
    with zipfile.ZipFile(dest,"w",zipfile.ZIP_DEFLATED) as z:
        for n in sorted(names):z.write(BASE/n,f"{a.nhom}_Pancake_GiuaKy/{n}")
    print("Đã tạo",dest.name)
    print("Chỉ kiểm tra tệp và cấu trúc; nhóm vẫn phải tự rà báo cáo, test, PDF và nội dung slide.")

if __name__=="__main__":
    try:main()
    except (OSError,ValueError,KeyError,TypeError) as e:raise SystemExit("Chưa đóng gói: "+str(e))
