import glob
import warnings
import os

import h5py
import click
import numpy as np
import scipy.io as spio

warnings.simplefilter(action='ignore', category=FutureWarning)

ABNORMAL = 'preictal'
NORMAL = 'interictal'
TEST = 'test'

FILEMASK = '{}_{}_*.mat'
KEY_TEMPLATE = '{}_segment_{}'
USE_CUSTOM_TEST = True
N_CUSTOM_TEST_SAMPLES = 20


def _read_and_parse_files(input_directory, subject_name, type_of_samples):
    filemask = FILEMASK.format(subject_name, type_of_samples)
    samples = []
    sample_rates = []
    file_list = glob.glob(os.path.join(input_directory, filemask))

    if not file_list:
        click.echo("No File found with mask {}".format(filemask))

    for full_file_path in glob.glob(os.path.join(input_directory, filemask)):

        click.echo("loading {} file {}".format(type_of_samples, full_file_path))

        datafile = spio.loadmat(full_file_path, squeeze_me=True)
        sample_number = os.path.splitext(os.path.basename(full_file_path))[0].split('_')[-1]

        key = KEY_TEMPLATE.format(type_of_samples, int(sample_number))

        sample_data = datafile[key].ravel()[0][0]
        sample_rate = datafile[key].ravel()[0][2]
        sample_rates.append(sample_rate)
        unique_sample_rate = set(sample_rates)
        if len(unique_sample_rate) > 1:
            raise ValueError("file {} samples has different samples rates [{}]".format(
                full_file_path,
                sample_rate,
                set(sample_rates)
            ))

        samples.insert(int(sample_number), sample_data)

    sample_rate = set(sample_rates).pop() if sample_rates else 0
    return samples, sample_rate


def _populate_store(store, group_name, data, sample_rate):

    group = store.create_group(group_name)
    group.create_dataset('SAMPLE_RATE', data=sample_rate)
    data_group = group.create_group('DATA')
    for i, sample in enumerate(data):
        k = 'SAMPLE_{}'.format(str(i).zfill(4))
        data_group.create_dataset(k, data=sample)

def get_data_mapping(use_custom_test):

    DATA_TYPE_STORE_KEY_MAPPING = {
        ABNORMAL: 'ABNORMAL',
        NORMAL: 'NORMAL',
    }

    if not use_custom_test:
        DATA_TYPE_STORE_KEY_MAPPING['TEST'] = 'TEST'

    return DATA_TYPE_STORE_KEY_MAPPING


@click.command()
@click.argument('input_directory', type=click.Path(exists=True))
@click.argument('subject_name', type=click.STRING)
@click.argument('destination_file', type=click.STRING)
def convert(input_directory, subject_name, destination_file, set_custom_test=USE_CUSTOM_TEST):

    if os.path.isfile(destination_file):
        if not click.confirm('Destination file {} exists. Do you want to continue?'.format(destination_file)):
            exit()

    store = h5py.File(destination_file, 'w')
    test_data = []
    data_type_key_mapping = get_data_mapping(set_custom_test)

    for type_of_samples, group_name in data_type_key_mapping.items():
        data, sample_rate = _read_and_parse_files(input_directory, subject_name, type_of_samples)

        if set_custom_test: # Leave some samples aside as tests
            n_train_samples = len(data) - N_CUSTOM_TEST_SAMPLES
            train_data = data[0:n_train_samples]
            test_data.append(data[n_train_samples:])

            _populate_store(store, group_name, train_data, sample_rate)
        else:
            _populate_store(store, group_name, data, sample_rate)

        click.echo("Saved data of type {}".format(type_of_samples))

    if set_custom_test:
        _populate_store(store, 'TEST', test_data, sample_rate)

    store.close()


if __name__ == '__main__':
    #    input = '/Users/fergus/Kaggle/EEG/Dog_1'
    convert()
    # convert(input_directory=input, subject_name='Dog_1', destination_file='doggy.hd5')
