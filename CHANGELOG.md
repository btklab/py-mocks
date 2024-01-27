# Changelog

All notable changes to "py-mocks" project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- Fixed [README.md] synopsis
- Fixed [Calc-LPpulp.py] synopsis

## [1.5.0] - 2024-01-21

- Added [Calc-LPpulp.py] script
- Added [requirements.txt] pymatgen

## [1.4.4] - 2024-01-17

- Fix: synopsis
- Updated [Calc-ChemMassPercent.py] output error massage when hyphen is used in molecular formula

## [1.4.3] - 2024-01-13

- Updated [Calc-ChemMassPercent.py] examples

## [1.4.2] - 2024-01-13

- Changed [Calc-ChemMassPercent.py] property name depending on unit
- Changed [Calc-ChemMassPercent.py] to print output at the end
- Fixed [Calc-ChemMassPercent.py] invalid variable name `Solid_@`
- Fixed [README.md] typo

## [1.4.1] - 2024-01-04

- Updated links
- Added [Calc-ChemMassPercent.py] `--molar` option

## [1.4.0] - 2024-01-04

- Added [Calc-ChemMassPercent.py] script
- Added [Get-PeriodicTable.py] `--molmass` option
- Added [pymatcalc.py], [pycalc.py], [pysym.py] `sys.exit(0)` end of script
- Added [pymatcalc.py], [pycalc.py] examples of solve simultaneous equations
- Fixed [README.md] indent

## [1.3.0] - 2024-01-01

- Added: [Get-PeriodicTable.py] script
- Added: [Get-MolecularMass.py] script
- Added: [Calc-ChemWeightRL.py] script
- Added: [Calc-ChemWeightLR.py] script

## [1.2.3] - 2024-01-01

- Changed: [pyplot-x-rs.py] graph title in English

## [1.2.2]

- Changed [pyplot.py], [pyplot-pandas.py], [pyplot-x-rs.py], [pyplot-timeline2.py] Specify Japanese font family in Linux environment.


## [1.2.1]

- Fixed [catcsv.py], [pycalc.py], [pymatcalc.py], [pyplot-pandas.py], [pyplot-timeline2.py], [pyplot-x-rs.py], [pyplot.py], [pysym.py] Fixed delimiter to use raw string
- Fixed examples [pymatcalc.py] 
- Updated [README.md]
- Added Pester tests and GitHub workflows


## [1.2.0]

- Added [pyplot-timeline2.py] function

## [1.1.0] - 2023-02-28

- Added [pysym.py] Output the expression and the result of assignment at the same time

## [1.0.0] - 2023-02-28

- Fix [README.md] section links
- Added [CHANGELOG.md]


## [0.1.0] - 2023-02-28

- Changed [README.md]
- Added [pycalc.py], [pymatcalc.py], [pysym.py], [pyplot.py], [pyplot-pandas.py], [pyplot-x-rs.py]


[pycalc.py]: src/pycalc.py
[pymatcalc.py]: src/pymatcalc.py
[pysym.py]: src/pysym.py
[pyplot.py]: src/pyplot.py
[pyplot-pandas.py]: src/pyplot-pandas.py
[pyplot-x-rs.py]: src/pyplot-x-rs.py
[pyplot-timeline2.py]: src/pyplot-timeline2.py

[README.md]: blob/main/README.md
[CHANGELOG.md]: blob/main/CHANGELOG.md
[requirements.txt]: blob/main/requirements.txt

[Get-PeriodicTable.py]: src/Get-PeriodicTable.py
[Get-MolecularMass.py]: src/Get-MolecularMass.py
[Calc-ChemWeightRL.py]: src/Calc-ChemWeightRL.py
[Calc-ChemWeightLR.py]: src/Calc-ChemWeightLR.py

[Calc-ChemMassPercent.py]: src/Calc-ChemMassPercent.py

[Calc-LPpulp.py]: src/Calc-LPpulp.py

[unreleased]: https://github.com/btklab/py-mocks/compare/1.5.0..HEAD
[1.5.0]: https://github.com/btklab/py-mocks/releases/tag/1.5.0
[1.4.4]: https://github.com/btklab/py-mocks/releases/tag/1.4.4
[1.4.3]: https://github.com/btklab/py-mocks/releases/tag/1.4.3
[1.4.2]: https://github.com/btklab/py-mocks/releases/tag/1.4.2
[1.4.1]: https://github.com/btklab/py-mocks/releases/tag/1.4.1
[1.4.0]: https://github.com/btklab/py-mocks/releases/tag/1.4.0
[1.3.0]: https://github.com/btklab/py-mocks/releases/tag/1.3.0
[1.2.3]: https://github.com/btklab/py-mocks/releases/tag/1.2.3
[1.2.2]: https://github.com/btklab/py-mocks/releases/tag/1.2.1
[1.2.1]: https://github.com/btklab/py-mocks/releases/tag/1.2.1
[1.2.0]: https://github.com/btklab/py-mocks/releases/tag/1.2.0
[1.1.0]: https://github.com/btklab/py-mocks/releases/tag/1.1.0
[1.0.0]: https://github.com/btklab/py-mocks/releases/tag/1.0.0
[0.1.0]: https://github.com/btklab/py-mocks/releases/tag/0.1.0

