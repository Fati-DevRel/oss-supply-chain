#!/bin/bash
# Set up content for local Zensical development
# Note: Zensical doesn't follow symlinks outside project dir, so we copy

cd "$(dirname "$0")"

# Remove old symlinks/copies if they exist
rm -rf docs/book1 docs/book2 docs/book3 docs/frontmatter docs/appendices

mkdir -p docs

# Copy content (Zensical requires files to be within project directory)
cp -r ../contents/book1 docs/
cp -r ../contents/book2 docs/
cp -r ../contents/book3 docs/
cp -r ../contents/frontmatter docs/
cp -r ../contents/appendices docs/

cp -r ../dist/*.pdf docs/

# Replace the font in all SVG images to use a Zensical-compatible font
find docs/ -name "*.svg" | while read -r svgfile; do
    sed -i.bak 's/font-family="[^"]*"/font-family="Roboto, Arial, sans-serif"/g' "$svgfile"
    rm "${svgfile}.bak"
done

echo "Content copied to docs/. Run 'zensical serve' from the site/ directory."
echo "Note: After editing content in contents/, run this script again to update."
