#! /bin/bash

find $1 -type f -name "more_stats.csv" | while read -r file; do
  # Extract the last 3 components of the path
  pattern=$(basename "$(dirname "$(dirname "$file")")" | tr '[:upper:]' '[:lower:]')
  compiler=$(basename "$(dirname "$file")")

  # Construct target filename
  target="$2/${compiler}_${pattern}.stats"

  # Create destination directory if not exists
  mkdir -p data2

  # Copy the file
  cp "$file" "$target"
done

