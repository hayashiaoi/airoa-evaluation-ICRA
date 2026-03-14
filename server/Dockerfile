FROM nvidia/cuda:12.2.2-cudnn8-runtime-ubuntu22.04
COPY --from=ghcr.io/astral-sh/uv:0.5.1 /uv /uvx /bin/

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /workspace

# ① PPAを使わず、自力でコンパイルするための基本ツールをインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
    git git-lfs build-essential clang ca-certificates curl \
    yasm nasm pkg-config bzip2 && \
    rm -rf /var/lib/apt/lists/*

# ② FFmpeg 7.0 のソースコードをダウンロードし、全CPUコアを使って爆速でコンパイル＆インストール
RUN curl -O https://ffmpeg.org/releases/ffmpeg-7.0.tar.bz2 && \
    tar xjvf ffmpeg-7.0.tar.bz2 && \
    cd ffmpeg-7.0 && \
    ./configure --enable-shared --disable-static && \
    make -j$(nproc) && \
    make install && \
    ldconfig && \
    cd .. && \
    rm -rf ffmpeg-7.0 ffmpeg-7.0.tar.bz2

# avパッケージのビルド時にFFmpegを見つけやすくするための環境変数
ENV PKG_CONFIG_PATH="/usr/local/lib/pkgconfig"

# ==========================================================
# ▼ 解決策：ファイルのコピーより「前」に一番重い処理を終わらせる
# ==========================================================
RUN uv venv --python 3.11 /workspace/.venv
# FFmpegを使った av のコンパイル（10分）をここで単独実行し、キャッシュ化します
RUN uv pip install --python /workspace/.venv/bin/python av==14.4.0

# ==========================================================
# ▼ プログラムのコピー（ここを変更しても、上の処理はスキップされる）
# ==========================================================
COPY pyproject.toml uv.lock LICENSE README.md ./
COPY packages/policy-client ./packages/policy-client
COPY src/openpi ./src/openpi
COPY server ./server
COPY runtime_core ./runtime_core
COPY dataset/norm_stats.json ./dataset/norm_stats.json 

# すでに一番重い av はインストール済みのため、この sync は他の軽量パッケージの
# ダウンロードとローカルコードの同期のみになり、数秒で終わります。
RUN GIT_LFS_SKIP_SMUDGE=1 uv sync --frozen --no-dev
# ==========================================================

RUN uv pip install --python /workspace/.venv/bin/python pytest

# Support PyTorch checkpoints (same behavior as upstream serve_policy image).
RUN /workspace/.venv/bin/python -c "import transformers; print(transformers.__file__)" | xargs dirname | xargs -I{} cp -r /workspace/src/openpi/models_pytorch/transformers_replace/* {}

ENV PATH="/workspace/.venv/bin:${PATH}"
ENV PYTHONPATH="/workspace:/workspace/src:/workspace/packages/policy-client/src"
ENV OPENPI_DATA_HOME="/policy_assets"

ENTRYPOINT ["/workspace/server/entrypoint.sh"]