#!/bin/bash

which trang 2>&1 >/dev/null
if [ $? != 0 ]; then
    echo "trang binary not found"
    echo "Install trang (http://www.thaiopensource.com/relaxng/trang.html) or make sure it is in your PATH"
    exit 1
fi


function compile_one() {
    local src=$1
    local dst=$2
    if [ ! -f "$src" ]; then
        echo "Source file $src does not exist"
        exit 1
    fi
    if [ -z "$dst" ]; then
        echo "Please specify destination file"
        exit 1
    fi

    echo "Writing RelaxNG from $src to $dst"
    trang -Irnc -Orng $src $dst
}

# Loop over all rnc files in a directory compiling them to rnc with the same name with different ending
function compile_all_in_path() {
    local path=$1
    if [ ! -d "$path"  ]; then
        echo "Directory $path was not found"
        exit 1
    fi

    schemas=$(find $path -type f -name '*.rnc')

    for schema in $schemas; do
        compile_one $schema $(echo $schema | sed 's/\.rnc$/.rng/g')
    done
}

case $1 in
    *)
        echo "Usage:"
        echo "$0 all <path>: compiles rnc all schemas in <path> to rng"
        echo "$0 one <source> <destination>: compiles rnc <source> to rng <destination>"
    ;;
    all)
        path=${SCHEMAS_PATH:-$2}
        echo "Compiling all rnc schemas in $path"
        compile_all_in_path "$path"
    ;;
    one)
        compile_one $2 $3
    ;;
esac
