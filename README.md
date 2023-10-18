<h1 align="center">
  <img src="https://raw.githubusercontent.com/datastreamapp/api-docs/main/docs/images/datastream.svg?sanitize=true" alt="DataStream Logo" width="400">
  <br/>
  DataStream API Python Wrapper
  <br/>
  <br/>
</h1>
<p align="center">
  DataStream.org API helper. See <a href="https://github.com/datastreamapp/api-docs/tree/main/docs">API documentation</a> for query string values and structure.
</p>

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

### Locations

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

### Records

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

```python
from datastream_py import set_api_key, metadata

set_api_key('xxxxxxxxxx')

results = list(metadata({
    '$select': 'DOI,Version,DatasetName',
    '$filter': "DOI eq '10.25976/xxxx-xx00'"
}))

print(results)
```
