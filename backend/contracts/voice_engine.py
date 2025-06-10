
import numpy as np
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import librosa
from realtime import PyAudioStream

class VoiceInterface:
    SAMPLE_RATE = 16000
    CHUNK_SIZE = 2048
   
    def __init__(self):
        self.processor = WhisperProcessor.from_pretrained("openai/whisper-medium")
        self.model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-medium")
        self.model.config.forced_decoder_ids = None
        self.stream = PyAudioStream(
            rate=self.SAMPLE_RATE,
            channels=1,
            chunk_size=self.CHUNK_SIZE
        )
       
    def transcribe_stream(self, callback):
        def audio_callback(in_data, frame_count, time_info, status):
            features = self._preprocess_audio(in_data)
            tokens = self.model.generate(features)
            text = self.processor.batch_decode(tokens, skip_special_tokens=True)[0]
            callback(text)
            return (in_data, pyaudio.paContinue)
       
        self.stream.start_stream(audio_callback)
       
    def _preprocess_audio(self, data):
        audio = np.frombuffer(data, dtype=np.float32)
        return self.processor(
            audio,
            sampling_rate=self.SAMPLE_RATE,
            return_tensors="pt"
        ).input_features 
