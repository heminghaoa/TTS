#!flask/bin/python
import argparse
import io
import json
import os
import sys
from pathlib import Path
from threading import Lock
from typing import Union
from urllib.parse import parse_qs

from flask import Flask, render_template, render_template_string, request, send_file

from TTS.config import load_config
from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer


def create_argparser():
    def convert_boolean(x):
        return x.lower() in ["true", "1", "yes"]

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=5002, help="port to listen on.")
    parser.add_argument("--use_cuda", type=convert_boolean, default=False, help="true to use CUDA.")
    return parser


# parse the args
args = create_argparser().parse_args()

path = Path(__file__).parent / "../.models.json"
manager = ModelManager(path)

# update in-use models to the specified released models.
model_path = None
config_path = None

model_name = "tts_models/multilingual/multi-dataset/your_tts"

# load pre-trained model paths
model_path, config_path, model_item = manager.download_model(model_name)


# load models
synthesizer = Synthesizer(
    tts_checkpoint=model_path,
    tts_config_path=config_path,
    tts_speakers_file=None,
    tts_languages_file=None,
    vocoder_checkpoint=None,
    vocoder_config=None,
    encoder_checkpoint="",
    encoder_config="",
    use_cuda=args.use_cuda,
)

#use_multi_speaker = hasattr(synthesizer.tts_model, "num_speakers") and (
#    synthesizer.tts_model.num_speakers > 1 or synthesizer.tts_speakers_file is not None
#)
#speaker_manager = getattr(synthesizer.tts_model, "speaker_manager", None)

#use_multi_language = hasattr(synthesizer.tts_model, "num_languages") and (
#    synthesizer.tts_model.num_languages > 1 or synthesizer.tts_languages_file is not None
#)
#language_manager = getattr(synthesizer.tts_model, "language_manager", None)

#use_gst = synthesizer.tts_config.get("use_gst", False)

app = Flask(__name__)

def style_wav_uri_to_dict(style_wav: str) -> Union[str, dict]:
    """Transform an uri style_wav, in either a string (path to wav file to be use for style transfer)
    or a dict (gst tokens/values to be use for styling)

    Args:
        style_wav (str): uri

    Returns:
        Union[str, dict]: path to file (str) or gst style (dict)
    """
    if style_wav:
        if os.path.isfile(style_wav) and style_wav.endswith(".wav"):
            return style_wav  # style_wav is a .wav file located on the server

        style_wav = json.loads(style_wav)
        return style_wav  # style_wav is a gst dictionary with {token1_id : token1_weigth, ...}
    return None


lock = Lock()

default_speaker_wav = style_wav_uri_to_dict("/opt/voices/SteveJobs.wav")

@app.after_request
def enable_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = \
            "Origin, Accept, Content-Type, Content-Disposition"
    return response


@app.route("/health", methods=["GET"])
def health_check1():
    return "OK", 200

@app.route("/", methods=["GET"])
def health_check2():
    return "OK", 200



@app.route("/api/tts", methods=["OPTIONS", "POST"])
def tts():

    if request.method == "OPTIONS":
        return {}

    with lock:
        params = request.json

        # text
        if (params.get("text") is None):
            text = ""
        else:
            text = params["text"]

        #language id
        if (params.get("language") is None):
            language_idx = "en"
        else:
            language_idx = params["language"]

        #speaker_wave
        if (params.get("speaker_wav") is None):
            speaker_wav = default_speaker_wav
        else:
            speaker_wav = style_wav_uri_to_dict(params["speaker_wav"])

        print(f" > Model input: {text}")
        print(f" > Language Idx: {language_idx}")
        print(f" > Speaker wave: { speaker_wav }")
        wavs = synthesizer.tts(text, speaker_name="", speaker_wav = speaker_wav, language_name=language_idx, style_wav="")
        out = io.BytesIO()
        synthesizer.save_wav(wavs, out)

    return send_file(out, mimetype="audio/wav")

def main():
    app.run(host="::", port=args.port)


if __name__ == "__main__":
    main()
