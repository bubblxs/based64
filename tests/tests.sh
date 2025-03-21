#!/bin/bash

set -e

BASED64_PY="$(dirname $(pwd))/based64.py"

get_file_hash ()
{
      local md5=$(md5sum $1 | awk '{ split($0, md5); print md5[1]; }')

      echo $md5
}

encode_file ()
{
      local flags=""

      if [ "$2" == "--decode" ]; then
            flags="-d"
      fi

      local msg=$(python3 $BASED64_PY -f $1 $flags; echo $?)

      echo $msg
}

echo_and_exit_failed_test ()
{
      local msg=$1
      local file_path=$2
      local file_hash=$3

      echo "======================================="
      echo "============= TEST FAILED ============="
      echo "======================================="
      echo ""
      echo -e "> $msg"
      echo "> file: $file_path"
      echo "> file hash: $file_hash"

      exit 1
}

main ()
{
      # note: files named with white spaces will fuck this up, so i have to remember to change the said spaces with underscore or whatever.
      local FILES_DIR="$(pwd)/files"
      local TEST_FILES=$(ls $FILES_DIR) 
      
      if [ ! -f $BASED64_PY ]; then
            echo "based64.py was not found." >&2 
            exit 1
      fi

      if [ ! -d $FILES_DIR ]; then 
            echo "test files dir was not found." >&2
            exit 1
      fi

      local num_tests=0
      for file in $TEST_FILES; do
            local file_full_path=$FILES_DIR/$file
            local og_file_hash=$(get_file_hash $file_full_path)
            # assuming that everything went right, we should not get any message but the exit code: 0
            local msg=$(encode_file $file_full_path)

            if [ "$msg" != 0 ]; then
                  echo_and_exit_failed_test "message: '$msg'" $file_full_path $og_file_hash
            fi

            local msg=$(encode_file $file_full_path.based64 --decode)

            if [ "$msg" != 0 ]; then
                  echo_and_exit_failed_test "message:  '$msg'" $file_full_path $og_file_hash
            fi

            local file_hash=$(get_file_hash $file_full_path)
            
            if [ $og_file_hash != $file_hash ]; then
                  echo_and_exit_failed_test "message: file hashes dont match. calculated '$og_file_hash', got '$file_hash'" $file_full_path $og_file_hash
            fi

            ((num_tests += 1))
      done

      echo "all done! num of tests made $num_tests."
}

main $@