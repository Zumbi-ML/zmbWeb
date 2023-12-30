# Etapa 1: Construir as dependências em uma imagem separada
FROM python:3.9 as builder

# Instalar dependências de sistema necessárias para compilação
RUN apt-get update && apt-get install -y \
    libblas-dev \
    liblapack-dev \
    gfortran \
    libsystemd-dev

# Definir diretório de trabalho
WORKDIR /src

# Instalar as dependências do Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt

# Etapa 2: Construir a imagem final
FROM python:3.9-slim

# Copiar as wheels compiladas da etapa anterior
COPY --from=builder /wheels /wheels

# Instalar as dependências do Python a partir das wheels
RUN pip install --no-cache /wheels/*

# Copiar o código fonte para a imagem
WORKDIR /app
COPY . .

# Expor a porta necessária
EXPOSE 8080

# Definir comando de entrada
ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:8080", "main:server"]
