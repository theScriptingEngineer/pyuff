#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import sys, os
my_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, my_path + '/../../')

import pyuff

def test_read_write_read_given_data():
    test_read_write_read_given_data_base('./data/beam.uff')

def test_read_write_read_given_data_base(file=''):
    if file=='':
        return
    #read from file
    uff_read = pyuff.UFF(file)

    a = uff_read.read_sets()
    if type(a)==list:
        types = np.array([_['type'] for _ in a])
        a = a[np.argwhere(types==151)[0][0]]

    #write to file
    save_to_file = './data/temp.uff'
    if os.path.exists(save_to_file):
        os.remove(save_to_file)
    _ = pyuff.UFF(save_to_file)
    _.write_sets(a, 'add')

    #read back
    uff_read = pyuff.UFF(save_to_file)
    b = uff_read.read_sets(0)

    if os.path.exists(save_to_file):
        os.remove(save_to_file)

    labels = [_ for _ in a.keys() if \
              any(_[-len(w):]==w for w in ['_lab', '_name', '_description',\
                                           '_created', '_saved', '_written',\
                                           'db_app', '_name'])]
    string_keys = ['program', 'description']
    exclude_keys = []

    string_keys = list(set(string_keys).union(set(labels)).difference(set(exclude_keys)))
    numeric_keys = list((set(a.keys()).difference(set(string_keys)).difference(set(exclude_keys))))


    for k in numeric_keys:
        print('Testing: ', k)
        np.testing.assert_array_almost_equal(a[k], b[k], decimal=3)
    for k in string_keys:
        print('Testing string: ', k, a[k])
        np.testing.assert_string_equal(a[k], b[k])


def test_write_read_151():
    save_to_file = './data/test.uff'
    a = pyuff.prepare_test_151(save_to_file=save_to_file)
    uff_read = pyuff.UFF(save_to_file)
    b = uff_read.read_sets()
    if os.path.exists(save_to_file):
        os.remove(save_to_file)


    labels = [_ for _ in a.keys() if \
              any(_[-len(w):]==w for w in ['_lab', '_name', '_description',\
                                           '_created', '_saved', '_written',\
                                           'db_app', '_name'])]
    string_keys = ['program', 'description']
    exclude_keys = ['date_db_written', 'time_db_written']

    string_keys = list(set(string_keys).union(set(labels)).difference(set(exclude_keys)))
    numeric_keys = list((set(a.keys()).difference(set(string_keys)).difference(set(exclude_keys))))


    for k in numeric_keys:
        print('Testing: ', k)
        np.testing.assert_array_almost_equal(a[k], b[k])
    for k in string_keys:
        np.testing.assert_string_equal(a[k], b[k])

if __name__ == '__main__':
    test_write_read_151()

if __name__ == '__mains__':
    np.testing.run_module_suite()