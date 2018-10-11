import json
import os
from typing import Dict

import logme
import tqdm
from scipy.io import wavfile
import numpy as np
import tensorflow as tf


class Data:
    def __init__(self, dtype, shape):
        self.dtype = dtype
        self.shape = shape

    def encode(self, value):
        """
        Encodes the shape as a tf.train.Feature using the correct type. Checks the shape if possible.
        :param value: The value to encode
        :return: The encoded value.
        """
        if self.dtype == tf.string:
            if isinstance(value, str):
                return self._bytes_feature(value.encode())
            elif isinstance(value, list):
                return self._bytes_feature_list(value)
            else:
                return self._bytes_feature(value)

        value = np.asarray(value)
        self.verify_shape(value)

        value = np.array(value).flatten().tolist()
        if self.dtype == tf.float32:
            return self._float32_feature_list(value)
        elif self.dtype == tf.int64:
            return self._int64_feature_list(value)
        else:
            raise NotImplementedError(
                "Encoding for {} not supported.".format(self.dtype)
            )

    def verify_shape(self, value):
        if np.prod(value.shape) != np.prod(self.shape):
            msg = "Shape mismatch for class {}. Given {} expected {}".format(
                self.__class__, value.shape, self.shape
            )
            raise ValueError(msg)

    def decode(self):
        """
        Creates a tf.FixedLenFeature decoder.
        :return: The decoder.
        """
        return tf.FixedLenFeature(self.shape, self.dtype)

    @staticmethod
    def _float32_feature_list(value):
        return tf.train.Feature(float_list=tf.train.FloatList(value=value))

    @staticmethod
    def _int64_feature_list(value):
        return tf.train.Feature(int64_list=tf.train.Int64List(value=value))

    @staticmethod
    def _bytes_feature(value):
        return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

    @staticmethod
    def _bytes_feature_list(value):
        return tf.train.Feature(bytes_list=tf.train.BytesList(value=value))


class String(Data):
    def __init__(self):
        super().__init__(tf.string, None)


class Floats(Data):
    def __init__(self, shape):
        super().__init__(tf.float32, shape)


class Ints(Data):
    def __init__(self, shape):
        super().__init__(tf.int64, shape)


def write_record(
    data: dict, writer: tf.python_io.TFRecordWriter, dataset: Dict[str, Data]
):
    features = {}
    for key in dataset:
        features[key] = dataset[key].encode(data[key])

    example = tf.train.Example(features=tf.train.Features(feature=features))

    writer.write(example.SerializeToString())


@logme.log
def write(src: str, dst: str, logger=None):
    if not dst.endswith(".tfrecord"):
        raise ValueError("{} must end with .tfrecord".format(dst))

    if not os.path.isfile(src):
        raise FileNotFoundError("{} is not a file!".format(src))

    if os.path.isfile(dst):
        raise FileExistsError("{} already exists!".format(dst))

    logger.info("Creating {}".format(dst))
    writer = tf.python_io.TFRecordWriter(dst)
    try:
        logger.info("Reading examples from {}".format(src))
        with open(src) as fp:
            samples = json.load(fp)  # type: dict

        logger.info("{} examples will be created".format(len(samples)))
        directory = os.path.join(os.path.dirname(src), "audio")
        for fname, data in tqdm.tqdm(samples.items(), unit="Ex"):
            wname = os.path.join(directory, f"{fname}.wav")

            if not os.path.exists(wname):
                raise FileNotFoundError(f"{wname} not found")

            _, audio = wavfile.read(wname)
            data["audio"] = audio

            dataset = {
                "note_str": String(),
                "pitch": Ints([1]),
                "velocity": Ints([1]),
                "audio": Floats([64000]),
                "qualities": Ints([10]),
                "instrument_source": Ints([1]),
                "instrument_family": Ints([1]),
            }

            data["pitch"] = [data["pitch"]]
            data["velocity"] = [data["velocity"]]

            write_record(data, writer, dataset)
    except Exception:
        logger.info(f"Removing {dst}")
        if os.path.exists(dst):
            os.remove(dst)
        raise
    finally:
        writer.close()