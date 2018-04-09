# Anomaly detection data transform tool


### Installation
```bash
$ conda create -n anomaly-transform python=3.5 numpy
$ source activate anomaly-transform
$ pip install -r requirements.txt
```


This repository contains a collection of tools to convert raw data into a common hd5 file format.
Each converter must create an hd5 file with the following structure:

3 root-level groups called `NORMAL`, `ABNORMAL` and `TEST`
* `NORMAL`: contains measurement (samples) where the event is considered normal (good flight, regular brain activity etc)
* `ABNORMAL`: contains measurement (samples) where the event is considered abnormal 
* `TEST`: contains measurement where the type is unknown

Each root-level group contains a list of subgroup labelled `SAMPLE_n`
Each `SAMPLE_n` subgroup contains a dict with the following keys

* `data`: the np.array containing the samples
* `sample_rate`: number of samples per seconds
* `sample_length_seconds`: the length of the sample in seconds (can be optional)


Convert Kaggle brainwaves data to hdf5
--------------------

```bash
$ python alphai_data_conversion/brainwaves_converter.py input_directory subject_name destination_file
```
where
* `input_directory`: is the directory where files are located
* `subject_name`: is the filename prefix (es: Dog_1)
* `destination_file`: is the fullpath of the hd5 output file


