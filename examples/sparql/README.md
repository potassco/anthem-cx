# SPARQL Benchmarks

This folder contains translations of the
[sparqlqc](http://sparql-qc-bench.inrialpes.fr/) query containment benchmarks.
The translation were obtained using a modified version of the
[SparqLog](https://github.com/joint-kg-labs/SparqLog) translator. While the
SparqLog translates the query containment problems into an extension of
Datalog, the modified version produces ASP programs.

There are two versions of the translation to ASP: the first produces a quite
direct translation of the problems (`*.lp`), while the second produces a more
ASP idiomatic representation (`*.reify.lp`).

## Directory Structure

The obtained equivalence problems are divided into three classes corresponding
to the classes of the original query containment problems: `noprojection`,
`projection`, `rdfs`. The respective folder for each class includes the
individual problems as sub-folder as well as a `*.csv` file detailing the
expected results for each problem.

Each individual problem contains two programs (given in two versions: `*.lp`
and `*.reify.lp`) as well as the user guide (`*.ug` and `*.reify.ug`).

## Running the Benchmarks

The two runscripts (`run_simple.sh` and `run_reify.sh`) can be used to run
`anthem-cx` on all the benchmarks problems. A timeout can be given to the
scripts in seconds (by default 60 seconds are used as the timeout). The scripts
produce a result table for each class listing each problem with the expected
result, actual result and runtime.

## Notes

- For some of the problems no `*.refiy.lp` version exists as the used
  translation does not work for them. Specifically these problems contain atom
  `triple(X,Y,Z)` in one of the programs which can not be translated to the
  reified format.

- Each program contains a fact (`v/1`) stating the (maximum) number of
  variables used in a rule. This number represent a sufficient maximum domain
  size to check due to the simple structure of the programs.

- The original benchmark set does not consider equivalences but containments
  instead. However, the notion of containment does not match the direction
  notion of equivalences as used by `anthem-cx`. That is each program has a
  unique model so that containment of the SPARQL problems asks whether the
  model of one program is contained in the model of the other. The notion used
  by `anthem-cx` asks whether the set of models of one program is contained in
  the set of models of the other program instead. While these notion do not
  match for a single direction only, they match when considering the full
  equivalence.
