#!/usr/bin/env bash

# Simple build helper: configure and build TestApp into TestApp/build
# Usage: ./run_build.sh [<BuildType>|clean]
#   ./TestApp/run_build.sh debug     # Debug build (default)
#   ./TestApp/run_build.sh release   # Release build
#   ./TestApp/run_build.sh clean     # Clean build directory

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="${PROJECT_DIR}"
BUILD_DIR="${APP_DIR}/build"

ARG="${1:-}"

case "${ARG,,}" in
  clean)
    echo "Cleaning ${BUILD_DIR}..."
    rm -rf "${BUILD_DIR}"
    echo "Cleaned."
    exit 0
    ;;
  release)
    BUILD_TYPE="Release"
    ;;
  debug|"")
    BUILD_TYPE="Debug"
    ;;
  *)
    BUILD_TYPE="${ARG}"
    ;;
esac

echo "Configuring project in ${BUILD_DIR} (BuildType=${BUILD_TYPE})"
mkdir -p "${BUILD_DIR}"
cmake -S "${APP_DIR}" -B "${BUILD_DIR}" -DCMAKE_BUILD_TYPE="${BUILD_TYPE}"

echo "Building..."
cmake --build "${BUILD_DIR}" --config "${BUILD_TYPE}" -- -j"$(nproc)"

echo "Build finished. Binary: ${BUILD_DIR}/TestApp"