# Cat Feeder Stack (API Server + Raspberry Pi Client)

이 저장소는 **FastAPI 기반 API 서버**와 **라즈베리파이 클라이언트 코드**를 포함합니다.
요청하신 값으로 이미 환경설정이 채워져 있으니 바로 실행할 수 있습니다.

- DB: `mysql+pymysql://admin:hanium2025@my-hanium-db.ct8466ykusoj.ap-southeast-2.rds.amazonaws.com:3306/cat_feeder`
- API_KEY: `hanium2025`
- 서버 퍼블릭 IPv4: `3.27.174.25` → 기본 호스트 포트는 **8080** (컨테이너 8000)

> ⚠️ 실무에서는 **.env를 공개 저장소에 커밋하지 마세요.** 여기서는 빠른 테스트를 위해 포함했습니다.

## 빠른 시작 (EC2, Docker)

```bash
# 1) 서버에서
cd server
docker build -t cat-feeder-api .
docker run -d --name cat-feeder-api -p 8080:8000 --env-file .env cat-feeder-api

# 또는 저장소 루트에서 docker compose
cd ..
docker compose up -d --build
```

- 보안 그룹 인바운드에 `TCP 8080`(또는 443) 허용 필요
- 운영에서는 HTTPS(예 Nginx + Let’s Encrypt) 권장

### 서버 헬스 체크
```bash
curl http://3.27.174.25:8080/health
```

## 라즈베리파이 설정

```bash
cd raspberrypi
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # TAG_ID만 수정
python run_demo.py
```

## 엔드포인트 요약

- `POST /api/feeding-logs` : 급식 세션 로그 업로드
- `POST /api/feeder-state` : 장비 잔량 보고
- `POST /api/feeding-info` : 이상행동 이벤트
- `GET  /api/cats/{tag_id}/plan` : 급식 계획/제한 조회
- `GET  /health` : 상태 점검

요청 시 헤더에 `X-API-Key: hanium2025` 필수.
