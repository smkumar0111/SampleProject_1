# test-data/

The files in this folder (`sample-data-*.bin`) are **random binary data**,
generated locally with `/dev/urandom`. They contain no code, no scripts,
no macros, and nothing executable — just raw bytes.

They exist solely to bring this sample project's size up to roughly the
200 MB requested, for testing how a Jenkins job performs when cloning,
checking out, and archiving a larger repository (network/storage/LFS
behavior, timeout tuning, artifact handling, etc.).

They are tracked with Git LFS (see `../.gitattributes`). Delete this
folder freely if you don't need the extra bulk — the rest of the
project (app, tests, Jenkinsfile) works fine without it.
