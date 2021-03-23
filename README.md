# Usage instruction

Please build a Docker container and then use `docker run` as shown below to call the script.

## Building the Docker container

```bash
docker build -t gethurricaneloss .
```

## Running the tool

For example:

```bash
docker run -ti --rm gethurricaneloss  -n 1000 1 1 0.5 1 0.65 0.23
```

## Running test cases

```bash
docker run -ti --rm --entrypoint /usr/src/gethurricaneloss_test.py gethurricaneloss
```

# Notes
## Model implementation
I have never done anything in the field of probabilistic statistics before, so I'm not sure if I interpreted the model correctly.
I tried to optimise it nevertheless. On my 12-core machine it runs at 776 ms ± 12 ms for 1E3 runs, 34.4 s ± 899 ms for 1E9 runs.

## Memory issue
If the script doesn't return a number it is most likely that you've hit a memory limit: 1E9 samples require approx. 6GB of memory.
This could be alleviated by sequencing the work in the script rather than just splitting the work by cores 