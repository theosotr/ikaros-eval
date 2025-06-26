To get the artifact, run:

```
git clone --recursive https://github.com/CyrilFMoser/Ikaros
```

The easiest way to get Hephaestus and all dependencies needed for evaluating 
the artifact is to download a _pre-built_ Docker 
image from DockerHub. Another option is to build the Docker 
image locally.

Docker Image
============

We provide a `Dockerfile` to build an image that contain:

* An installation of Python (version 3.10.12).
* An installation of [SDKMAN](https://sdkman.io/).
* An installation of JDK.
* An installation of Scala.
* An installation of GHC (Glaskow Haskell Compiler).
* An installation of Rust (used to compile `Ikaros`).
* An installation of `Ikaros`.
* A user named `ikaros` with sudo privileges.
* Python packages for plotting figures
  and analyzing data (i.e., `seaborn`, `pandas`, 
  `matplotlib` and `numpy`).

Pull Docker Image from DockerHub
--------------------------------

You can download the Docker image from DockerHub by using the following 
commands:

```
docker pull theosotr/ikaros-eval
# Rename the image to be consistent with our scripts
docker tag theosotr/ikaros-eval ikaros-eval
```

After downloading the Docker image successfully, 
please navigate to the root directory of the artifact:

```
cd ikaros-eval
```

Build Docker Image Locally
--------------------------

First enter the `ikaros-eval/` directory:

```
cd ikaros-eval
```

To build the image (named `ikaros-eval`), run the following command 
(estimated running time: 30 minutes, depending on your internet 
connection):

```
docker build -t ikaros-eval --no-cache .
```

**NOTE:** The image is built upon `ubuntu:22.04`.
