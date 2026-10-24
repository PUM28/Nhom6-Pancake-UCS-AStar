"""Kiểm độc lập kết quả C đã lưu, không thay test_nhom.py của Quân."""
import csv
import itertools
import json
import platform
import statistics
import sys
from pathlib import Path
from tao_du_lieu import generate
BASE=Path(__file__).resolve().parent
CONFIGS=(('ucs','zero'),('astar','largest'),('astar','combined'))
COMMON={'S0':(6,5,4,3,2,1),'H':(3,1,4,2,5,6),
        'P':(5,6,3,2,4,1),'Q':(4,1,6,2,5,3)}

def replay(start,actions):
    s=tuple(start);p=[list(s)]
    for k in actions:
        assert type(k) is int and 2<=k<=len(s)
        s=tuple(reversed(s[:k]))+s[k:];p.append(list(s))
    return s,p


def main():
    data=json.loads((BASE/'du_lieu_nhom.json').read_text())
    assert data==generate(62026)
    custom={c['name']:c for c in data['cases']}
    assert set(custom)=={'N1','N2'}
    assert custom['N1']['start']!=custom['N2']['start']
    assert custom['N1']['goal']==custom['N2']['goal']
    for c in custom.values():
        assert len(c['start'])==7 and sorted(c['start'])==list(range(1,8))
        assert sorted(c['goal'])==list(range(1,8)) and c['goal']!=list(range(1,8))
        assert c['start']!=c['goal']
        assert list(replay(c['goal'],c['scramble_actions'])[0])==c['start']
    allrows=[]
    for tag,cases in [('bat_buoc',{n:{'start':list(s),'goal':list(range(1,7))} for n,s in COMMON.items()}),('tu_tao',custom)]:
        rows=json.loads((BASE/f'output/{tag}.json').read_text())
        with (BASE/f'output/{tag}.csv').open(encoding='utf-8-sig',newline='') as f: csvrows=list(csv.DictReader(f))
        expected={(name,a,h,o) for name in cases for a,h in CONFIGS for o in ('asc','desc')}
        assert len(rows)==len(expected)==len(csvrows)
        assert {(r['case'],r['algorithm'],r['heuristic'],r['order']) for r in rows}==expected
        for r,csvr in zip(rows,csvrows):
            c=cases[r['case']]
            assert r['start']==c['start'] and r['goal']==c['goal']
            assert r['status']=='found' and r['repeat']==3 and r['trace']==[]
            goal,path=replay(r['start'],r['actions'])
            assert list(goal)==r['goal'] and path==r['path']
            assert r['cost']==sum(r['actions']) and r['moves']==len(r['actions'])
            assert r['valid_pops']==r['expanded']+1
            assert r['popped']==r['valid_pops']+r['stale_pops']
            assert r['generated']==(r['n']-1)*r['expanded']
            assert len(r['timing_samples_ms'])==3
            assert r['elapsed_ms']==statistics.median(r['timing_samples_ms'])
            assert all(str(r[k])==csvr[k] for k in csvr)
        for name in cases:assert len({r['cost'] for r in rows if r['case']==name})==1
        allrows+=rows
    report={'status':'PASS','checked_rows':len(allrows),'common_rows':24,'custom_rows':12,
            'seed':62026,'python':sys.version,'platform':platform.platform(),
            'checks':['Ma trận đủ và không trùng','CSV khớp JSON','Đường replay bằng phép đảo độc lập',
            'Cost/moves/path đúng','3 đẳng thức số đếm','3 lần chạy và trung vị đúng',
            'Cost bằng nhau giữa 6 cấu hình mỗi case','Seed/lịch sử/đích riêng hợp lệ'],
            'pending':['C3: chờ bản tính tay đã chốt trước khi xuất hai trace H và đối chiếu',
                       'C4: Sơn cần thực hành step/debugger trên máy mình',
                       'Log 3 test riêng không thay log >=10 test của cả nhóm']}
    (BASE/'output/kiem_chung_C.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
