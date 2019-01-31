import os

__all__ = [
    "debug",
    "preprocess_settings",
    "stft_info",
    "hyper_params",
    "training_settings",
]

debug = True

HOME = os.path.expanduser("~")

preprocess_settings = {
    "pre_dst": os.path.join(HOME, "storage", "separation"),
    "downloader": {
        "bucket": "vuesic-musdbd18",
        "dataset": "musdb18.zip",
        "downloading_dst": os.path.join(HOME, "storage", "separation"),
    },
}

stft_info = {
    "n_fft": 4096, 
    "win_length": 2049, 
    "hop_length": 384
}

hyper_params = {}

training_settings = {
    "epochs": 2 if debug else 100,
    "training_path": os.path.join(HOME, "storage", "separation", "pt_f_train"),
    "rnn_decoder_params": {"debug": debug, "in_dim": 12},
    "rnn_encoder_params": {
        "debug": debug,
        "in_dim": stft_info["win_length"],
        "context_lenth": 10,
    },
}
