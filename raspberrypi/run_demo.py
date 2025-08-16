# 간단 데모: 계획 조회 → 급식 로그 업로드 → 잔량 보고 → 이상행동 보고
from datetime import datetime, timezone
from client import now_utc
from feed import upload_feeding_log
from state import report_left_amount
from behavior import report_behavior
from plan import fetch_plan

def main():
    plan = fetch_plan()
    print("Plan:", plan)

    res = upload_feeding_log(weight_g=4200, amt_g=30, left_g=980)
    print("FeedingLog created:", res)

    st = report_left_amount(950)
    print("State reported:", st)

    info = report_behavior("normal")  # 혹은 'vomit_suspect'
    print("Behavior reported:", info)

if __name__ == "__main__":
    main()
