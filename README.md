<h1 align="center">
  <img src="https://raw.githubusercontent.com/datastreamapp/api-docs/main/docs/images/datastream.svg?sanitize=true" alt="DataStream Logo" width="400">
  <br/>
  DataStream API Python Wrapper
  <br/>
  <br/>
</h1>

This package is useful for those who want to extract large volumes of data from
DataStream's [Public API](https://github.com/datastreamapp/api-docs/tree/main/docs).

See [Usage](#usage) to learn how to use this package.

> Note: DataStream's Custom Download tool is another option that allows users to download csv data from across datasets
> in a particular DataStream hub using basic filters. This tool has fewer filtering options than the API, but works well
> for basic searches. You can find it via 'Explore Data' in the header menu from any DataStream regional hub.

## Requirements

- Python 3.9+

## Install

### Using CLI

```sh
pip install git+https://github.com/datastreamapp/datastream-py
```

### Using requirements.txt

Add the following to your `requirements.txt` file:

```
datastream-py @ git+https://github.com/datastreamapp/datastream-py@main
```

Then, run `pip install -r requirements.txt`

## Usage

Available methods:

- `set_api_key`
- `metadata`
- `locations`
- `observations`
- `records`

See [API documentation](https://github.com/datastreamapp/api-docs/tree/main/docs) for query string values and structure.

### Locations

Returns a [generator object that is iterable](https://docs.python.org/3/glossary.html#term-generator-iterator).

#### Get Locations from a dataset

```python
from datastream_py import set_api_key, locations

set_api_key('xxxxxxxxxx')

results = locations({
    '$select': 'Id,DOI,Name,Latitude,Longitude',
    '$filter': "DOI eq '10.25976/xxxx-xx00'",
    '$top': 10000
})

for location in results:
    print(location)
```

#### Get Locations from multiple datasets

```python
from datastream_py import set_api_key, locations

set_api_key('xxxxxxxxxx')

results = locations({
    '$select': 'Id,DOI,Name,Latitude,Longitude',
    '$filter': "DOI in ('10.25976/xxxx-xx00', '10.25976/xxxx-xx11', '10.25976/xxxx-xx22')",
    '$top': 10000
})

for location in results:
    print(location)
```

### Observations

Returns a [generator object that is iterable](https://docs.python.org/3/glossary.html#term-generator-iterator).

#### Get `Temperature` and `pH` observations from multiple datasets

```python
from datastream_py import set_api_key, observations

set_api_key('xxxxxxxxxx')

results = observations({
    '$select': 'DOI,ActivityType,ActivityMediaName,ActivityStartDate,ActivityStartTime,SampleCollectionEquipmentName,CharacteristicName,MethodSpeciation,ResultSampleFraction,ResultValue,ResultUnit,ResultValueType',
    '$filter': "DOI in ('10.25976/xxxx-xx00', '10.25976/xxxx-xx11', '10.25976/xxxx-xx22') and CharacteristicName in ('Temperature, water', 'pH')",
    '$top': 10000
})

for observation in results:
    print(observation)
```

### Records

Returns a [generator object that is iterable](https://docs.python.org/3/glossary.html#term-generator-iterator).

```python
from datastream_py import set_api_key, records

set_api_key('xxxxxxxxxx')

results = records({
    '$select': 'DOI,ActivityType,ActivityMediaName,ActivityStartDate,ActivityStartTime,SampleCollectionEquipmentName,CharacteristicName,MethodSpeciation,ResultSampleFraction,ResultValue,ResultUnit,ResultValueType',
    '$filter': "DOI eq '10.25976/xxxx-xx00'",
    '$top': 10000
})

for record in results:
    print(record)
```

### Metadata

Returns a [generator object that is iterable](https://docs.python.org/3/glossary.html#term-generator-iterator).

```python
from datastream_py import set_api_key, metadata

set_api_key('xxxxxxxxxx')

results = list(metadata({
    '$select': 'DOI,Version,DatasetName',
    '$filter': "DOI eq '10.25976/xxxx-xx00'"
}))

print(results)
```

### Get Result Count

Pass `$count` as `true` to get the count of results.
See [URL parameters](https://github.com/datastreamapp/api-docs#url-parameters) for more details.

```python
from datastream_py import set_api_key, observations

set_api_key('xxxxxxxxxx')

count = observations({
    '$filter': "DOI eq '10.25976/xxxx-xx00'",
    '$count': 'true'
})

print(count)
```