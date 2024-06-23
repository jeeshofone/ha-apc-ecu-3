#!/bin/bash

EXCLUDE_FILES=("configuration.yaml")
INCLUDE_EXTENSIONS=("*.py" "*.yaml" "*.md" "*.html")
DIRECTORIES=("." "./html-examples/")

wrap_content() {
    local filepath="$1"
    local content="$2"
    local tagname="${filepath}"
    echo -e "<${tagname}>\n${content}\n</${tagname}>"
}

is_excluded() {
    local filename="$1"
    for exclude in "${EXCLUDE_FILES[@]}"; do
        if [[ "$filename" == "$exclude" ]]; then
            return 0
        fi
    done
    return 1
}

process_directory() {
    local directory="$1"
    for ext in "${INCLUDE_EXTENSIONS[@]}"; do
        for filepath in "$directory"/$ext; do
            # Remove extra slash only if it exists
            local formatted_path=$(echo "$filepath" | sed 's/\/\//\//g')
            if [[ -f "$formatted_path" ]]; then
                if ! is_excluded "$(basename "$formatted_path")"; then
                    content=$(cat "$formatted_path")
                    wrap_content "${formatted_path}" "$content"
                fi
            fi
        done
    done
}

main() {
    for dir in "${DIRECTORIES[@]}"; do
        process_directory "$dir"
    done
}

main
