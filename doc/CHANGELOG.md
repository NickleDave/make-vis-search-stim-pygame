# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- `make` function now saves Pascal VOC annotation file for each search display image 
  [#20](https://github.com/NickleDave/searchstims/pull/20)

### Fixed
- fix arguments that `main` passes to `make` so that command-line interface works
  [#19](https://github.com/NickleDave/searchstims/pull/19)

## [2.4.0] 2020-02-29
### Added
- `background_color` argument to `AbstractStimMaker`
  + makes it possible to specify background color of search stimuli
    (e.g., white instead of default black)

## [2.3.1] 2019-09-07
### Changed
- both `searchstims.make` and `searchstims.utils.json_to_csv` function
  save `root_output_dir` field in csv as absolute path

## [2.3.0] 2019-09-06
### Added
- other `StimMaker` classes
- `searchstims.util` module with `make_csv` and `json_to_csv` functions
  + the `searchstims.make` function now calls `make_csv` after making
    the images, see below
  + the `json_to_csv` function is for converting the `.json` files that
    used to be generated with metadata to the new `.csv` files
    + it also generates individual `.meta.json` files for each image as
      `searchstims.make` now does

### Changed
- `searchstims.make` now outputs a .csv file instead of a .json file
  + meaning metadata for each image is now in long-form that's easy to
    parse with a library like Pandas, instead of a confusing nested
    dictionaries-list structure
  + some metadata like item locations does not fit well in table format
    so that data is saved in individual `.meta.json` files, one for each
    `.png` image file.
    - specifically, the `.meta.json` files contain
      + `target_indices`: location of target, if present; i.e. the
        indices to access the center of the target in an array
        representing the image
      + `distractor_indices`: same as `target_indices` but for
        distractor items in the search stimulus
      + `grid_as_char`: when stimulus was generated using a grid of
        cells, this character representation of the grid and where the
        items are within it is added to the `.meta.json` file. This can
        be an easy way to filter by location at the level of the grid,
- change `Two_v_Five_StimMaker` to use ForcedSquare font instead of .png
  files
  + This makes it possible to easily change size of 2 and 5.

## [2.2.0] 2019-05-22
### Added
- ability to pass `list` for `num_target_present` and `num_target_absent` in `searchstims.make`
  + to make more of one set size v. another, since "combinatorially speaking" there are many more 
    ways of making stimuli with larger set sizes, and this seems to affect accuracy on those set 
    sizes. E.g. with grid of size (5x5) there are 25 pick 1, i.e. 25, ways of making a "target 
    present" stimulus with set size of 1, whereas with a set size of 8 there are 25 pick 8
    (~100k) ways of making a target present stimulus (and that's before adding jitter). 

## [2.1.0] 2019-05-22
### Added
- `RVvRHGVStimMaker` class that makes "conjunction" search stimuli

## Changed
- refactor `AbstractStimMaker`
  + move core logic for making a single visual search stimulus into helper function `_make_stim`
    which is called by `make_stim` in main loop after all the set-up code
  + that way child classes of `AbstractStimMaker` can override `_make_stim` if they need to do
    something more complicated than what it does

## [2.0.0] 2019-05-22
### Added
- ability to specify colors for targets and distractors as tuples corresponding to 
RGB color codes; currently this only works if you write your own script, not if you use `config.ini` files

### Changed
- names of built-in visual search stimuli are now `RVvGV` and `2_v_5`, hence the major version bump

### Fixed
- bug that prevented user from making search stimuli where items are placed randomly instead of
  on a grid

## [1.2.0] 2019-05-22
### Changed
- refactor `searchstims.make` so it is more general
  + now accepts a `stim_dict` that maps visual search stimulus names to instances of `StimMaker` classes
  + in this way the function can be used with a script that passes user-defined `StimMaker` sub-classes
    - instead of being limited to the two types of stimuli that can be specified in the `config.ini` files
      + the alternative would've been to keep adding new possible sections the `config.ini` but this would've
        been gross and painful

## [1.1.1] 2019-05-22
### Fixed
- fix how metadata is saved now that all sections in a single config.ini file are made
  + `searchstims.make` function adds a key for each section to the `dict` it uses to 
  track stimuli, so the `.json` file created from that `dict` has metadata for each section

## [1.1.0] 2019-04-12
### Added
- [GENERAL] section of config has `enforce_unique` option
  + makes sure all images are unique when a grid is used
  + option is True by default
- added `imageio` as a dependency
  + needed to open .png files for tests
  + will be needed for other tests that look at actual images generated whenever they get written anyway

## [1.0.0] 2019-04-10
### Added
- possible to specify options that are common to all stimuli in [GENERAL] section
of config.ini file
  + e.g., image_size, item_bbox_size, jitter, grid_size
  + if one of these options is also specified in a section for a specific stimulus,
  that value overrides the one specified in the general section

### Changed
- user specifies an item bounding box for items in stimulus, instead of 'rect'
  + the actual item is drawn within this "bounding box"
  + would make it possible to draw items with different sizes but same shape
- user specifies sizes in order of (height, width)
  + since people feeding images to neural networks are used to this order
  + even though PyGame expects (width, height)

## [0.3.0a1] 2019-03-29
### Added
- possible to make multiple types of stimuli with a single config file
  + any section that is defined gets made

### Changed
- clean up configuration handling
  + add `searchstims.config` sub-package, move config-related code in there
  + uses `attrs`-based classes instead of `NamedTuple`s

### Fixed
- continuous integration no longer fails, tests pass
  + set environment variable for library that PyGame depends on so that library runs with a dummy driver
  and that way the "no video card" error doesn't get thrown

## [0.2.0] 2019-03-07
### Added
- Acknowledgments with number for DARPA funding in README.md.
- Switch from pre-release to release to get a DOI for version 0.2.0

## [0.2.0a6] 2019-02-11
### Added
- colors available for 'rectangle' stimulus that move either from red or green towards yellow (because of how 
RGB color space works); this makes it possible to vary the discriminability of the target and distractor along a 
single feature dimension (color). Using this one can fit a psychometric curve to the classifications of a neural 
network and estimate its accuracy level for a known discriminability of targets from distractors. 

## [0.2.0a5] 2019-02-11
### Changed
- image filenames in .json file are saved as relative to `output_dir` that was specified in `.ini` file
when the images were generated by `searchstims`. This way it is possible to move the entire output directory 
without breaking anything, but it does require that any scripts using the `.json` file know the path to that 
output directory, and join the filenames to it (e.g. using `os.path.join`) 

## [0.2.0a4] 2019-02-11
### Added
- ability to have items located randomly (not on a grid), and specify a minimum center 
distance between all items when placing randomly

## [0.2.0a3] 2019-02-10
### Added
- ability to set "border" within window, so that items are not placed outside 
the border. This provides another way to test for edge effects, i.e. by seeing  
whether impaired accuracy is rescued when items are kept within the borders

## [0.2.0a2] 2019-02-05
### Fixed
- data files (such as .png images of numbers) are now installed correctly

## [0.2.0a1] 2019-02-04
### Added
- More detail about `config.ini` to README.md, explains what the options actually are for
- `.json` file saved by searchstims has more info about stimuli, such as location
  of targets and distractors (in case this is needed for analysis)
- unit tests

### Changed
- separate `main.py` into functions, to separate concerns; 
  * the `main` function deals with command-line args
  * `parse_config` loads and parses `config.ini` files 
  * `make` function accepts parsed config
  * This way you can call the `make` function with a `ConfigTuple` instance
   regardless of its origins (e.g. if you need to write tests for `make` )
- command-line interface now requires name of config file as first arg, instead of 
  specifying it with optional `-c` flag (vestige of when I didn't understand how 
  `argparse` is meant to work)

### Fixed
- indent error in `main.py` that caused crash when `stimulus = rectangle`

## [0.1] - 2018-10-24
### Added
- Original version