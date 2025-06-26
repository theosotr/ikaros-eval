FROM ubuntu:22.04

ENV TZ=Europe/Zurich
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt update -yq && apt upgrade -yq
RUN apt install -y vim software-properties-common git sudo wget locales curl \
  build-essential libffi-dev libffi8ubuntu1 libgmp-dev libgmp10 libncurses-dev\
  libncurses5 libtinfo5 zip unzip
RUN sudo locale-gen "en_US.UTF-8"
RUN update-locale LC_ALL="en_US.UTF-8"
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1
RUN apt install -yq python3-distutils python3-pip

# Create the ikaros user.
RUN useradd -ms /bin/bash ikaros && \
    echo ikaros:ikaros | chpasswd && \
    cp /etc/sudoers /etc/sudoers.bak && \
    echo 'ikaros ALL=(ALL:ALL) NOPASSWD:ALL' >> /etc/sudoers
USER ikaros
ENV HOME /home/ikaros
WORKDIR ${HOME}

# Install missing python packages
RUN pip3 install --upgrade setuptools distlib pip
RUN pip3 install seaborn pandas matplotlib numpy

USER ikaros

RUN touch ${HOME}/.bash_profile
RUN echo "source ${HOME}/.bash_profile" >> ${HOME}/.bashrc
RUN echo 'export LANG="en_US.UTF-8"' >> ${HOME}/.bashrc

# Install GHC
RUN curl --proto '=https' --tlsv1.2 -sSf https://get-ghcup.haskell.org | BOOTSTRAP_HASKELL_NONINTERACTIVE=1 BOOTSTRAP_HASKELL_GHC_VERSION=latest BOOTSTRAP_HASKELL_CABAL_VERSION=latest BOOTSTRAP_HASKELL_INSTALL_STACK=1 BOOTSTRAP_HASKELL_INSTALL_HLS=1 BOOTSTRAP_HASKELL_ADJUST_BASHRC=P sh
RUN echo "source ~/.ghcup/env" >> ${HOME}/.bashrc

# Install Rust
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y

# Create directory for helper installation scripts
RUN mkdir ${HOME}/installation_scripts
 
# Install sdkman
ADD ./installation_scripts/install_sdkman.sh ${HOME}/installation_scripts/install_sdkman.sh
RUN ${HOME}/installation_scripts/install_sdkman.sh
ENV SDKMAN_DIR "${HOME}/.sdkman"
 
# Install Java
ADD ./installation_scripts/install_java.sh ${HOME}/installation_scripts/install_java.sh
SHELL ["/bin/bash", "-c"]
RUN source .sdkman/bin/sdkman-init.sh && sdk update
RUN ${HOME}/installation_scripts/install_java.sh

# Install Scala
ADD ./installation_scripts/install_scala.sh ${HOME}/installation_scripts/install_scala.sh
RUN ${HOME}/installation_scripts/install_scala.sh
ENV SCALA_3.6.0 ${HOME}/scala3/dist/target/universal/scala3-3.6.0-RC1-bin-SNAPSHOT/bin

WORKDIR ${HOME}
# Now cleanup helper scripts
RUN sudo rm -rf ${HOME}/installation_scripts

# Install LLVM used by rustc and Z3 used by Ikaros
USER root
RUN apt install -y llvm clang z3

USER ikaros
ENV PATH "${PATH}:${HOME}/.cargo/bin"
# Add source code of ikaros
ADD ./Ikaros ${HOME}/Ikaros
RUN sudo chown -R ikaros:ikaros ${HOME}/Ikaros
RUN cd ${HOME}/Ikaros && cargo build --release

ENV PATH "${PATH}:${HOME}/Ikaros/target/release"

WORKDIR ${HOME}
