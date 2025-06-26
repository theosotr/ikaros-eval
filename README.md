# Artifact for "Validating Soundness and Completeness in Pattern-Match Coverage Analyzers" (OOPSLA'25)

This is the artifact for the conditionally accepted OOPSLA'25 paper titled
"Validating Soundness and Completeness in Pattern-Match Coverage Analyzers".

An archived version of the artifact is also available on Zenodo.
See TODO.

# Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Setup](#setup)
- [Getting Started](#getting-started)
  * [Usage](#usage)
  * [Example](#example)
- [Step by Step Instructions](#step-by-step-instructions)
  * [RQ1: Bug-Finding Results (Section 5.2)](#rq1-bug-finding-results-section-52)
  * [RQ2: Bug and Test Case Characteristics (Section 5.3)](#rq2-bug-and-test-case-characteristics-section-53)
  * [RQ3: Performance (Section 5.4)](#rq3-performance-section-54)

# Overview

The artifact contains the instructions and scripts to re-run the evaluation
described in our paper. The artifact has the following structure:

* `scripts/`: This directory contains the scripts needed to re-run the
experiments presented in our paper.
* `data/`: This is the directory that contains the precomputed results of our
evaluation.
* `Ikaros/`: Contains the source code of the tool
(provided as a git submodule) used for validating
pattern-match coverage analyzers.
The name of this tool is `Ikaros` and is written in Rust.
* `installation_scripts/`: Contains helper scripts used to install all
dependencies (e.g., compiler versions from SDKMAN).
* `figures/`: This directory will be used to save the reproduced
figures of our paper.
* `Dockerfile`: The Dockerfile used to create a Docker image of our artifact.
  This image contains all data and dependencies.

`Ikaros` is available as open-source software under the
GNU General Public License v3.0, and can also be reached through the following
repository: https://github.com/CyrilFMoser/Ikaros.


# Requirements

See [REQUIREMENTS.md](./REQUIREMENTS.md)

# Setup

See [INSTALL.md](./INSTALL.md)

# Getting Started

To get started with `Ikaros`,
we use the Docker image named `ikaros-eval`,
built according to the instructions
from the [Setup](#Setup) guide.
This image comes preconfigured with all the necessary environments
for testing the three compilers,
that is,
it includes the required compiler installations as well as
all supporting tools needed for result processing.

You can enter a new container by using the following command:

```
docker run -ti --rm ikaros-eval
```

## Usage

The `ikaros` executable provides a rich CLI with many available options.

```
ikaros@a1a0025981b8:~$ ikaros --help
Usage: ikaros [OPTIONS] --pattern-gen <PATTERN_GEN> --language <LANGUAGE>

Options:
  -p, --pattern-gen <PATTERN_GEN>  Name of the person to greet [possible values: z3, construction, mutation]
  -l, --language <LANGUAGE>        Activate debug mode [possible values: haskell, scala, java]
  -i, --iterations <ITERATIONS>    
  -b, --batch-size <BATCH_SIZE>    [default: 16]
  -r, --redundancy                 
  -r, --reduce                     
  -h, --help                       Print help
  -V, --version                    Print version
```

## Example: Validating the Pattern-Match Coverage Analyzer of Scala

**NOTE:** At each run, `ikaros` generates random programs.
Therefore, you should expect to get different results at each run:
some randomly generated programs might trigger unfixed bugs
in pattern-match coverage analyzers.

### Example 1

In this example,
we use `ikaros` to generate 50 programs
(as specified by `--iterations 50`) to validate
the soundness and completeness of the pattern-match coverage analyzer in Scala.
The patterns within the generated programs are produced
using the refinement-based pattern generation strategy (RefPG)
described in the paper.
This is enabled via the `--pattern-gen construction` option.

```
ikaros@a1a0025981b8:~$ ikaros --language scala \
  --pattern-gen construction \
  --iterations 50
```

When the above command is executed,
`ikaros` prints messages like the following to the standard output:

```
Compiling...
Finished Compiling
Compiling...
Finished Compiling
...
```

In addition, after each run,
`ikaros` creates an `out/` directory in the current working directory.
This directory contains all bug-triggering programs and results,
organized as follows:

```
out/
└── Programs/
    └── Construction/
        └── scalac/
            ├── batches/
            ├── redundancy/
            │   └── false_positive/
            ├── exhaustiveness/
            │   ├── false_positive/
            │   └── false_negative/
            └── more_stats.csv
```



Here's a breakdown of the key components:

* `out/Programs/Construction/scalac/batches/`:
Stores temporary files created during the program generation
 and compilation process.

* `out/Programs/Construction/scalac/exhaustiveness/false_negative/`:
Contains programs that expose _soundness_ bugs in the exhaustiveness checker
of the pattern-match coverage analyzer.
If this directory is empty,
no such bugs were found during the run.

* `out/Programs/Construction/scalac/exhaustiveness/false_positive/`:
Contains programs that expose _completeness_ bugs in the exhaustiveness checker
of the pattern-match coverage analyzer.
If this directory is empty,
no such bugs were found during the run.

* `out/Programs/Construction/scalac/redundancy/false_positive/`:
Contains programs that expose _completeness_ bugs in the redundancy checker
of the pattern-match coverage analyzer.
If this directory is empty,
no such bugs were found during the run.

* `out/Programs/Construction/scalac/more_stats.csv`:
A CSV file summarizing various statistics from the run,
including program characteristics,
generation and compilation times,
and more.


### Example 2


In our second example, we repeat the experiment.
This time using the random pattern generation strategy (RPG),
as described in Section 3.3.3 of our paper.
This strategy leverages Z3 to establish the correctness oracle.

```
ikaros@a1a0025981b8:~$ ikaros --language scala \
  --pattern-gen z3 \
  --iterations 50
```


This now generates an output like so:

```
out/
└── Programs/
    └── Z3/
        └── scalac/
            ├── batches/
            ├── redundancy/
            │   └── false_positive/
            ├── exhaustiveness/
            │   ├── false_positive/
            │   └── false_negative/
            │       ├── program_0.scala
            │       ├── program_1.scala
            │       ├── program_2.scala
            │       ├── program_3.scala
            │       └── program_4.scala
            └── more_stats.csv
```

Notably,
`ikaros` successfully identified five soundness bugs (false negatives)
in the exhaustiveness checks of the pattern-match coverage analyzer.
The bug-triggering programs can be found in:
`out/Programs/Z3/scalac/exhaustiveness/false_negative/`.

**NOTE**:
The number of discovered bugs may vary in your own run,
depending on the randomly generated inputs.

Now, you can exit the Docker container by running:

```
ikaros@a1a0025981b8: exit
```

# Step By Step Instructions
