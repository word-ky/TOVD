#!/usr/bin/env bash
set -e
temporary=/home/wenchang/asdasdsad/wjq/TOVD/shared/t013_yoloworld/weights/.p3r5-s_stage2-4466ab94.partial
destination=/home/wenchang/asdasdsad/wjq/TOVD/shared/t013_yoloworld/weights/s_stage2-4466ab94.pth
date -Is
stat --printf='temporary_bytes=%s\n' "$temporary"
sha256sum "$temporary"
test "$(stat -c %s "$temporary")" = 305058902
test "$(sha256sum "$temporary" | cut -d ' ' -f 1)" = 4466ab940ab2d93ff436b4869961bb885d7faf176bd0c8511d3cf451af55f458
test ! -e "$destination"
mv -T "$temporary" "$destination"
stat --printf='final_bytes=%s\nfinal_inode=%i\nfinal_mtime=%y\n' "$destination"
sha256sum "$destination"
test "$(stat -c %s "$destination")" = 305058902
test "$(sha256sum "$destination" | cut -d ' ' -f 1)" = 4466ab940ab2d93ff436b4869961bb885d7faf176bd0c8511d3cf451af55f458
echo FINAL_CHECKPOINT_VERIFIED
date -Is
