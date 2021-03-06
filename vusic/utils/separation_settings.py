import os

__all__ = [
    "debug",
    "preprocess_settings",
    "stft_info",
    "hyper_params",
    "training_settings",
    "testing_settings",
    "model_paths",
]

debug = False

# XXX
HOME = os.path.expanduser("~")

preprocess_settings = {
    "pre_dst": os.path.join(HOME, "storage", "separation"),
    "downloader": {
        "bucket": "vuesic-musdbd18",
        "dataset": "musdb18.zip",
        "downloading_dst": os.path.join(HOME, "storage", "separation"),
    },
}

stft_info = {"n_fft": 4096, "win_length": 2049, "hop_length": 384}

hyper_params = {
    "learning_rate": 1e-4,
    "max_grad_norm": 0.5,
    "l_reg_m": 1e-2,
    "l_reg_twin": 0.5,
    "l_reg_denoiser": 1e-4,
}

# amount of bins we want to preserve for generating the mask
preserved_bins = 744

# context length for RNNs
context_length = 10
output_folder = "output" if debug else os.path.join(HOME, "storage")

output_paths = {
    "output_folder": output_folder,
    "rnn_encoder": os.path.join(output_folder, "rnn_encoder.pth"),
    "rnn_decoder": os.path.join(output_folder, "rnn_decoder.pth"),
    "fnn_masker": os.path.join(output_folder, "fnn_masker.pth"),
    "fnn_denoiser": os.path.join(output_folder, "fnn_denoiser.pth"),
    "loss": os.path.join(output_folder, "loss.pth"),
    "optimizer": os.path.join(output_folder, "separation_optimizer.pth"),
    "twin_loss": os.path.join(output_folder, "twin_loss.pth"),
    "fnn_denoiser": os.path.join(output_folder, "fnn_denoiser.pth"),
}

model_folder = os.path.join(HOME, "Desktop")

model_paths = {
    "model_folder": model_folder,
    "rnn_encoder": os.path.join(model_folder, "rnn_encoder.pth"),
    "rnn_decoder": os.path.join(model_folder, "rnn_decoder.pth"),
    "fnn_masker": os.path.join(model_folder, "fnn_masker.pth"),
    "fnn_denoiser": os.path.join(model_folder, "fnn_denoiser.pth"),
}

training_settings = {
    "epochs": 1 if debug else 100,
    "training_path": os.path.join(HOME, "storage", "pt_f_train"),
    "context_length": context_length,
    "sequence_length": 60,
    "rnn_encoder_params": {
        "debug": debug,
        "input_size": preserved_bins,
        "context_length": context_length,
    },
    "rnn_decoder_params": {"debug": debug, "input_size": preserved_bins * 2},
    "twin_decoder_params": {"debug": debug, "input_size": preserved_bins * 2},
    "fnn_masker_params": {
        "debug": debug,
        "input_size": preserved_bins * 2,
        "output_size": stft_info["win_length"],
        "context_length": context_length,
    },
    "fnn_denoiser_params": {"input_size": stft_info["win_length"], "debug": debug},
    "affine_transform_params": {"debug": debug, "input_size": preserved_bins * 2},
    "batch_size": 16,
}

testing_settings = {
    "testing_path": os.path.join(HOME, "storage", "separation", "pt_f_test")
}
