# Artifact for "Validating Soundness and Completeness in Pattern-Match Coverage Analyzers" (OOPSLA'25)

This is the artifact for the conditionally accepted OOPSLA'25 paper titled
"Validating Soundness and Completeness in Pattern-Match Coverage Analyzers".

# Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Setup](#setup)
- [Getting Started](#getting-started)
  * [Usage](#usage)
  * [Example: Validating the Pattern-Match Coverage Analyzer of Scala](#example-validating-the-pattern-match-coverage-analyzer-of-scala)
  * [Discovered Bugs](#discovered-bugs)
- [Step by Step Instructions](#step-by-step-instructions)
  * [RQ1: Bug-Finding Results (Section 5.2)](#rq1-bug-finding-results-section-52)
  * [RQ2: Bug and Test Case Characteristics (Section 5.3)](#rq2-bug-and-test-case-characteristics-section-53)
  * [RQ3: Performance (Section 5.4)](#rq3-performance-section-54)
  * [Re-running Experiments and Reproducing Tables and Figures with New Data (Optional)](#re-running-experiments-and-reproducing-tables-and-figures-with-new-data-optional)

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

__Note: This artifact has been tested on a 64-bits Ubuntu machine.
Nevertheless, our Docker image works on any given operating system
that supports Docker.__

* A [Docker](https://docs.docker.com/get-docker/) installation.
* At least 16GB of available disk space.

# Setup

To get the artifact, run:

```
git clone --recursive https://github.com/theosotr/ikaros-eval
```

The easiest way to get `Ikaros` and all dependencies needed for evaluating 
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
  -p, --pattern-gen <PATTERN_GEN>
          trategy used to generate pattern-matching expressions and establish the test oracle.
          
          * construction: Refers to refinement-based pattern generation.
          
          * z3: Refers to random pattern generation using Z3 as the test oracle.
          
          * mutation: Uses semantic mutations to derive new programs from existing ones.
          
          [possible values: z3, construction, mutation]

  -l, --language <LANGUAGE>
          Target programming language for the generated programs
          
          [possible values: haskell, scala, java]

  -i, --iterations <ITERATIONS>
          Total number of programs to generate.
          
          If not specified, Ikaros will continue generating programs indefinitely.

  -b, --batch-size <BATCH_SIZE>
          Number of programs per batch sent to the compiler under test
          
          [default: 10]

  -r, --redundancy
          If provided, Ikaros also checks for false positives in redundancy diagnostics

      --reduce
          If provided, Ikaros attempts to minimize bug-triggering programs via reduction

  -h, --help
          Print help (see a summary with '-h')

  -V, --version
          Print version
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


This now generates files like so:

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


## Discovered bugs

We provide a JSON file (`data/bugs.json` in the root directory of the artifact)
that contains detailed information about
the bugs identified by `Ikaros` during our testing efforts.
Each entry in the file corresponds to a distinct bug
and includes the following fields:

```json
"DOTTY-1": {
    "language": "scala",
    "version": "3.6.3",
    "symptom": "fn-exhaustiveness",
    "status": "fixed",
    "characteristics": [
        "Poly. ADT",
        "constant"
    ],
    "url": "https://github.com/scala/scala3/issues/22590",
    "test-case": [
        "sealed trait T_A",
        "case class CC_B[T](a: T) extends T_A",
        "@main def test() = {",
        "  val v_a: CC_B[Int] = CC_B(10)",
        "  val v_b: Int = v_a match{",
        "    case CC_B(12) => 0",
        "  }",
        "}"
    ]
}
```

* `language`: The programming language of the test case.
* `version`: The compiler version in which the bug was found.
* `symptom`: The observed symptom of the bug. One of the following:
  - `fn-exhaustiveness`: False negative in exhaustiveness checks
  - `fp-exhaustiveness`: False positive in exhaustiveness checks
  - `fp-redundancy`: False positive in redundancy checks
  - `performance`: Compilation performance issue

* `status`: Indicates whether the bug has been fixed.
* `characteristics`: A list of notable language features
   used in the test case (e.g., polymorphic ADTs, constants).
* `url`: Link to the corresponding bug report (if one was submitted).
* `test-case`: The test case that triggers the bug, represented as an array
   of source code lines.

Now, you can exit the Docker container by running:

```
ikaros@a1a0025981b8: exit
```

# Step By Step Instructions

**NOTE**: Remember to run all the subsequent `docker run` commands
from the root directory of the artifact (i.e., `ikaros-eval/`).

To validate the main results presented in the paper,
first create a new Docker
container by running:

```
docker run -ti --rm \
  -v $(pwd)/data:/home/ikaros/data \
  -v $(pwd)/scripts:/home/ikaros/eval-scripts \
  -v $(pwd)/figures:/home/ikaros/eval-figures \
  -v $(pwd)/new-results:/home/ikaros/new-results \
  ikaros-eval
```

Note that we mount four _local volumes_ inside the newly created container.
The first volume (`data/`) contains the data collected during our evaluation,
including the bugs discovered by `Ikaros`.
The second volume (`eval-scripts/`) includes
all necessary scripts to reproduce
and validate the results of the paper.
The third volume (`eval-figures/`) is used to save the figures of our paper.
Finally,
the last volume (`new-results/`) mounts an empty directory where
you can store the results if you decide to re-run our experiments.


**NOTE**: Recomputing all the results presented in our paper takes
approximately three days.


## RQ1: Bug-Finding Results (Section 5.2)

For RQ1,
we first examine the `data/bugs.json` file
(see [Discovered bugs](#discovered-bugs)
to reproduce Table 1a regarding the status of
the discovered bugs.

```
ikaros@2a72c8b56b74:~$ python eval-scripts/process_bugs.py data/bugs.json rq1
                          Table 1a                          
============================================================
Status              scalac    javac     ghc       Total     
------------------------------------------------------------
Unconfirmed         0         1         0         1         
Confirmed           2         0         0         2         
Fixed               10        2         0         12        
Wont fix            0         1         0         1         
------------------------------------------------------------
Total               12        4         0         16   
```

### Comparison of bug-finding capability

To reproduce Table 1c and Figure 7, which compare the bug-finding effectiveness
of the two pattern generation strategies (namely RefPG and RPG),
execute the following command:

```
ikaros@2a72c8b56b74:~$ python eval-scripts/bug-evolution.py data eval-figures/
```

This will produce the following summary corresponding to Table 1c:

```
                     Table 1c                     
==================================================
Pat Gen   scalac    javac     ghc       Total     
--------------------------------------------------
RPG       3642      86        0         3728      
RefPG     36        0         0         36 
```


In addition, this script generates a figure that replicates Figure 7
from the paper.
The resulting plot is saved to the
_host machine_ under `figures/evolution.pdf`.


## RQ2: Bug and Test Case Characteristics (Section 5.3)

To address the second research question,
we analyze the `data/bugs.json` file to reproduce Table 1b,
which categorizes the symptoms of the discovered bugs,
as well as Table 2a,
which highlights the language features present in
 the corresponding bug-triggering test cases.

You can generate both tables by running the following command:


```
ikaros@2a72c8b56b74:~$ python eval-scripts/process_bugs.py data/bugs.json rq2
```

This produces the following output:

```
                          Table 1b                          
============================================================
Symptoms            scalac    javac     ghc       Total     
------------------------------------------------------------
Exhaustiveness FP   0         4         0         4         
Exhaustiveness FN   7         0         0         7         
Redundancy FP       4         0         0         4         
Performance         1         0         0         1         


                               Table 2a                               
======================================================================
ID        Language  ADT       GADT      Poly. ADT constant  null      
----------------------------------------------------------------------
1         scala     No        No        Yes       Yes       No        
2         scala     No        Yes       No        No        No        
3         scala     No        Yes       No        No        No        
4         scala     No        Yes       No        No        No        
5         scala     No        Yes       No        No        No        
6         scala     No        Yes       No        No        Yes       
7         scala     No        Yes       No        Yes       Yes       
8         scala     No        Yes       No        No        Yes       
9         scala     No        Yes       No        No        Yes       
10        scala     No        Yes       No        No        Yes       
11        scala     No        No        Yes       No        No        
12        scala     No        Yes       No        No        Yes       
13        java      Yes       No        No        No        No        
14        java      Yes       No        No        No        No        
15        java      Yes       No        No        No        No        
16        java      Yes       No        No        No        No 
```

### Addtional statistics about the generated programs


We now reproduce Table 2b, which presents various statistics about
the programs generated by `Ikaros`.
These statistics are based on a corpus of 20,000
programs generated during our experiments.
The raw data collected from our evaluation are inside the `data/` directory
(see files with the `.stats` suffix).

To generate the table and corresponding visualizations, run:


```
ikaros@2a72c8b56b74:~$ python eval-scripts/study-characteristics.py data eval-figures/
```


This replicates Table 2b as shown below:

```
                                         Table 2b                                         
==========================================================================================
Description         5%        Mean      Median    95%       Histogram                     
------------------------------------------------------------------------------------------
Type declarations   2.0       4         4.0       8.0       eval-figures//histograms/types.pdf
Constructors        1.0       3         3.0       6.0       eval-figures//histograms/constructors.pdf
GADTs               0.0       2         2.0       5.0       eval-figures//histograms/gadts.pdf
Constructor params  0.0       2         2.0       3.0       eval-figures//histograms/params.pdf
Polymorphic types   0.0       2         2.0       6.0       eval-figures//histograms/generics.pdf
Patterns            1.0       8         2.0       16.0      eval-figures//histograms/patterns.pdf

```

In addition to the table, the command generates histograms for each statistic, which are saved under the directory `figures/histograms` in your _host machine_.


### Comparison of the complexity

To reproduce Figure 8, which compares the complexity of the generated patterns
between our two pattern generation strategies,
run:

```
ikaros@2a72c8b56b74:~$ python eval-scripts/study-characteristics.py data/ eval-figures/ --patterns
```

This command generates Figure 8, which is stored under `figures/patterns.pdf`
inside the _host machine_.

**NOTE:** The figure is slightly different from the one presented in the paper.
We will update the Figure in the camera ready accordingly.


## RQ3: Performance (Section 5.4)


Reproducing Table 3 exactly as presented in the paper may not be feasible,
as the results depend on the capabilities of your machine.
However, we can approximate the results and extract the key takeaways.

### Step 1: Generate programs

Run the following commands to generate a total of 100 programs
per target language; 50 using RefPG and 50 using RPG

Estimated running time: 30 minutes.
Note that runs involving Scala may take longer,
as `scalac` is significantly slower than the other compilers.


```
ikaros@2a72c8b56b74:~$ ikaros --language scala --pattern-gen construction --iterations 50 --batch-size 1
ikaros@2a72c8b56b74:~$ ikaros --language scala --pattern-gen z3 --iterations 50 --batch-size 1
ikaros@2a72c8b56b74:~$ ikaros --language java --pattern-gen construction --iterations 50 --batch-size 1
ikaros@2a72c8b56b74:~$ ikaros --language java --pattern-gen z3 --iterations 50 --batch-size 1
ikaros@2a72c8b56b74:~$ ikaros --language haskell --pattern-gen construction --iterations 50 --batch-size 1
ikaros@2a72c8b56b74:~$ ikaros --language haskell --pattern-gen z3 --iterations 50 --batch-size 1
```

### Step 2: Collect statistics

After all runs have completed, copy the corresponding `.stats` files
(located under `out/Programs`,
as described in the [Example](#example-validating-the-pattern-match-coverage-analyzer-of-scala) guide)
into a new directory named `new-results`.

```
ikaros@2a72c8b56b74:~$ ./eval-scripts/copy-stats.sh out new-results
```

### Step 3: Reproduce Table 3

Run the following script to compute performance metrics:

```
ikaros@2a72c8b56b74:~$ python eval-scripts/study-performance.py new-results
```

This produces something like the following:

```
                 Generation time (Table 3)                  
============================================================
                    RefPG               RPG                 
------------------------------------------------------------
javac               495μs               324μs               
scalac              747μs               243μs               
ghc                 395μs               174μs               

                 Compilation time (Table 3)                 
============================================================
                    RefPG               RPG                 
------------------------------------------------------------
javac               598.9ms             1027.9ms            
scalac              3167.0ms            3078.9ms            
ghc                 111.5ms             97.2ms              

                 Smt solving time (Table 3)                 
============================================================
                    w/ timeout          w/o timeout         
------------------------------------------------------------
javac               9.4ms               47.5ms              
scalac              9.6ms               43.5ms              
ghc                 8.0ms               40.4ms  
```

Key Takeaways:

* Program generation time is negligible for both pattern generation methods
  (measured in microseconds).

* Compilation time constitutes the dominant overhead,
  ranging from hundreds to thousands of milliseconds.

* SMT solving time increases 3--5x without a timeout, but remains relatively
  minor overall.


## Re-running Experiments and Reproducing Tables and Figures with New Data (Optional)

Up to this point,
we have reproduced the tables and figures from our paper
using the pre-generated evaluation data.
However,
you also have the option to re-run selected experiments yourself 
in order to regenerate these results using fresh data.

### RQ1: Comparing Pattern Generation Strategies

To re-run the comparison between the two pattern generation strategies
in terms of bug-finding effectiveness (Section 5.2),
you can execute both approaches to test the correctness of
the pattern-match coverage analyzers in `scalac` and `javac`.
We exclude `ghc` from this comparison
as no bugs were found in our previous evaluations.

Use the following command to run each strategy on each target compiler
for 600 seconds (i.e., 10 minutes).
Notably,
in our full evaluation,
each configuration was run for 12 hours.

```
ikaros@2a72c8b56b74:~$ ./eval-scripts/run-ikaros.sh 600 new-results
```

The command above will take approximately 40 minutes to complete in total
(10 minutes per strategy × 2 strategies × 2 compilers).

You can shorten the runtime by adjusting the timeout.
For example, to run each method for 5 minutes,
simply change the first argument to 300.


Once `ikaros` completes all runs,
execute the following command to prepare the
 data needed for plotting Figure 7.

**IMPORTANT NOTE**:
ensure that the value of the `--duration` option (e.g., 600)
matches the value used in the previous step
(`./eval-scripts/run-ikaros.sh 600`),
so the data aligns correctly with the intended experiment duration.

```
ikaros@2a72c8b56b74:~$ python eval-scripts/pickle-bug-evolution.py \
  --ikaros-run out/Programs \
  --time-dir new-results \
  --duration 600 \
  --output-dir new-results
```

Finally, run the following command to
reproduce Table 1c and Figure 7 with the new data:

```
ikaros@2a72c8b56b74:~$ python eval-scripts/bug-evolution.py \
  new-results/ \
  eval-figures/ \
  --avoid-log-scale
```

The above command outputs Table 1c in the standard output,
while Figure 7 is found under `figures/evolution.pdf`.


### RQ2: Collecting Statistics About the Generated Programs

We now re-run the experiment for reproducing Figure 8 and Table 2b
by generating a total of 1,000 programs
per target language; 500 using RefPG and 500 using RPG
(estimated running time: 30 minutes):

```
ikaros@2a72c8b56b74:~$ ikaros --language scala --pattern-gen construction --iterations 500
ikaros@2a72c8b56b74:~$ ikaros --language scala --pattern-gen z3 --iterations 500
ikaros@2a72c8b56b74:~$ ikaros --language java --pattern-gen construction --iterations 500
ikaros@2a72c8b56b74:~$ ikaros --language java --pattern-gen z3 --iterations 500
ikaros@2a72c8b56b74:~$ ikaros --language haskell --pattern-gen construction --iterations 500
ikaros@2a72c8b56b74:~$ ikaros --language haskell --pattern-gen z3 --iterations 500
```

Then, we copy the statistics (see `.stats` files) from each `ikaros` run
to the `new-results/`

```
ikaros@2a72c8b56b74:~$ ./eval-scripts/copy-stats.sh out new-results
```

Finally,
it is time to reproduce Table 2b (along with the corresponding histograms
in `figures/histograms`)
and Figure 8 (located at `figures/patterns.pdf` inside the _host machine_)
by running:

``` bash
# For Table 2b
ikaros@2a72c8b56b74:~$ python eval-scripts/study-characteristics.py \
  new-results eval-figures/

# For Figure 8
ikaros@2a72c8b56b74:~$ python eval-scripts/study-characteristics.py \
  new-results eval-figures/ --patterns
```


Congratulations on completing the instructions of the artifact! :-)
