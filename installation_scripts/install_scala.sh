#!/usr/bin/env bash
#
# Install the Scala compiler

export SDKMAN_DIR="$HOME/.sdkman"
[[ -s "$HOME/.sdkman/bin/sdkman-init.sh" ]] && source "$HOME/.sdkman/bin/sdkman-init.sh"
sdk install scala 3.4.1 < /dev/null
sdk install scala 3.6.2 < /dev/null
sdk install scala 3.7.1 < /dev/null
sdk install sbt < /dev/null

git clone https://github.com/scala/scala3 && cd scala3
git checkout 3.6.0-RC1
sbt dist/Universal/packageBin
