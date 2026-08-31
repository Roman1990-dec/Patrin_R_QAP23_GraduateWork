FROM python:3.13-slim

# Устанавливаем системные зависимости (необходимы для Playwright)
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем uv
RUN pip install uv

WORKDIR /app

# Копируем файлы с зависимостями
COPY pyproject.toml uv.lock ./

# Устанавливаем зависимости проекта
RUN uv sync --frozen

# Устанавливаем браузер Playwright (Chromium) и все системные зависимости для него
RUN uv run playwright install chromium && \
    uv run playwright install-deps

# Копируем весь проект
COPY . .

# Команда по умолчанию
CMD ["uv", "run", "pytest", "tests/", "--alluredir=allure-results"]