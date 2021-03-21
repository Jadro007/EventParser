# EventParser

Tool used parsing and finding events in HTML files.


## How to use it


Run `run.py` with url you want to parse.
Example:

`run.py https://goout.net/cs/billy-talent/szrcvvo/`


Script accepts other parameters, run
`run.py -h`
for more details.


`--allow-poi` - allows using POI and NER categorization.

`--verbose int` - used for debugging purposes.

## Running tests
There are unit / integration tests for most of classes, just run all tests in `src` folder with proper pathing.

To run full integration testing with test dataset, run `test.py`


## What is in the project

- config - configuration options 
- data - dev and test datasets, list of POIs, list of cities
- nlp - NER project is copied here for better stability
- src - source code of this tool


##Other notes 
 
 Project can use Selenium on Windows (could be updated to support Linux), however it is quite slow, so it is not used in production.
 
 