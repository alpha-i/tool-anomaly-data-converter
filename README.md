# Anomaly detection data transform tool


### Installation
```bash
$ conda create -n anomaly-transform python=3.5 numpy
$ source activate anomaly-transform
$ pip install -U setuptools --ignore-installed
$ pip install -r requirements.txt
```


This repository contains a collection of tools to convert raw data into a common hd5 file format.
Each converter must create an hd5 file with the following structure:

3 root-level groups called `NORMAL`, `ABNORMAL` and `TEST`
* `NORMAL`: contains measurement (samples) where the event is considered normal (good flight, regular brain activity etc)
* `ABNORMAL`: contains measurement (samples) where the event is considered abnormal
* `TEST`: contains measurement where the type is unknown

Each root-level group contains two keys:
 SAMPLE_RATE: is the unique sample rate valid for all the samples
 DATA: list of subgroup labelled `SAMPLE_n` containing the np.array

Convert Kaggle brainwaves data to hdf5
--------------------

```bash
$ python converters/brainwaves.py --use_custom_test input_directory subject_name destination_file
```
where
* `input_directory`: is the directory where files are located
* `subject_name`: is the filename prefix (es: Dog_1)
* `destination_file`: is the fullpath of the hd5 output file
