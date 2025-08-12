# Python 3.12 베이스 이미지 사용
FROM python:3.12-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 업데이트 및 필수 도구 설치
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    gnupg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Node.js 18.x 설치 (Mock Server용)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Playwright 브라우저 의존성 설치
RUN apt-get update && apt-get install -y \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libdbus-1-3 \
    libatspi2.0-0 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libxcb1 \
    libxkbcommon0 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# Allure 설치
RUN curl -o allure-2.27.0.tgz -L https://github.com/allure-framework/allure2/releases/download/2.27.0/allure-2.27.0.tgz \
    && tar -xzf allure-2.27.0.tgz \
    && mv allure-2.27.0 /opt/allure \
    && ln -s /opt/allure/bin/allure /usr/bin/allure \
    && rm allure-2.27.0.tgz

# Java 설치 (Allure 실행에 필요)
RUN apt-get update && apt-get install -y \
    default-jre-headless \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Playwright 브라우저 설치
RUN playwright install chromium firefox webkit

# Mock Server 의존성 파일 복사 및 설치
COPY mock_server/package*.json ./mock_server/
WORKDIR /app/mock_server
RUN npm ci --only=production
WORKDIR /app

# 프로젝트 파일 복사
COPY . .

# 실행 권한 부여
RUN chmod +x run_tests.sh run_with_allure.sh

# Mock Server 포트
EXPOSE 3000

# Allure Report 포트
EXPOSE 5050

# 환경 변수 설정
ENV PYTHONUNBUFFERED=1
ENV API_BASE_URL=http://localhost:3000

# 헬스체크
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/config || exit 1

# Docker 테스트 스크립트 복사 및 실행 권한
COPY docker_test.sh /docker_test.sh
RUN chmod +x /docker_test.sh

# 기본 실행 명령
CMD ["/docker_test.sh"]