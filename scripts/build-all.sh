#!/bin/bash
#
# Build PDFs for all three books in the Software Supply Chain Security series
#

REBUILD_COVERS=0

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "=============================================="
echo "Building Software Supply Chain Security Series"
echo "=============================================="
echo ""

mkdir -p "$ROOT_DIR/dist"

# Build Book 1
echo "[1/3] Building Book 1: Understanding the Software Supply Chain"
if [ "$REBUILD_COVERS" -eq 1 ] || [ ! -f "$ROOT_DIR/contents/book1/cover.svg" ]; then
    echo "Generating cover for Book 1..."
    python $ROOT_DIR/scripts/cover-generator.py --book=1 --output="$ROOT_DIR/contents/book1/cover.svg"
    echo ""
fi
cd "$ROOT_DIR/contents/book1" && ./build-pdf.sh
mv "$ROOT_DIR/contents/book1/book-1-understanding-the-open-source-supply-chain.pdf" "$ROOT_DIR/dist/book-1-understanding-the-software-supply-chain.pdf"
mv "$ROOT_DIR/contents/book1/book-1-cover.pdf" "$ROOT_DIR/dist/book-1-cover.pdf"
echo ""

# Build Book 2
echo "[2/3] Building Book 2: Protecting the Software Supply Chain"
if [ "$REBUILD_COVERS" -eq 1 ] || [ ! -f "$ROOT_DIR/contents/book2/cover.svg" ]; then
    echo "Generating cover for Book 2..."
    python $ROOT_DIR/scripts/cover-generator.py --book=2 --output="$ROOT_DIR/contents/book2/cover.svg"
    echo ""
fi
cd "$ROOT_DIR/contents/book2" && ./build-pdf.sh
mv "$ROOT_DIR/contents/book2/book-2-protecting-the-open-source-supply-chain.pdf" "$ROOT_DIR/dist/book-2-protecting-the-software-supply-chain.pdf"
mv "$ROOT_DIR/contents/book2/book-2-cover.pdf" "$ROOT_DIR/dist/book-2-cover.pdf"
echo ""

# Build Book 3
echo "[3/3] Building Book 3: Governing the Software Supply Chain"
if [ "$REBUILD_COVERS" -eq 1 ] || [ ! -f "$ROOT_DIR/contents/book3/cover.svg" ]; then
    echo "Generating cover for Book 3..."
    python $ROOT_DIR/scripts/cover-generator.py --book=3 --output="$ROOT_DIR/contents/book3/cover.svg"
    echo ""
fi
cd "$ROOT_DIR/contents/book3" && ./build-pdf.sh
mv "$ROOT_DIR/contents/book3/book-3-governing-the-open-source-supply-chain.pdf" "$ROOT_DIR/dist/book-3-governing-the-software-supply-chain.pdf"
mv "$ROOT_DIR/contents/book3/book-3-cover.pdf" "$ROOT_DIR/dist/book-3-cover.pdf"
echo ""

cd "$SCRIPT_DIR"

echo "=============================================="
echo "Build Complete"
echo "=============================================="
echo ""
echo "Output files:"
echo "  - book-1-understanding-the-software-supply-chain.pdf"
echo "  - book-1-cover.pdf"
echo "  - book-2-protecting-the-software-supply-chain.pdf"
echo "  - book-2-cover.pdf"
echo "  - book-3-governing-the-software-supply-chain.pdf"
echo "  - book-3-cover.pdf"
