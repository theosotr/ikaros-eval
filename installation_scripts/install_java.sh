#!/usr/bin/env bash
#
# Install the Java compiler

export SDKMAN_DIR="$HOME/.sdkman"
[[ -s "$HOME/.sdkman/bin/sdkman-init.sh" ]] && source "$HOME/.sdkman/bin/sdkman-init.sh"
sdk install java 24-open < /dev/null
sdk install java 22.0.2-oracle < /dev/null
sdk default java 22.0.2-oracle
