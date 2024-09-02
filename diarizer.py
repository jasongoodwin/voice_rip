import torch
from speechbrain.pretrained import EncoderClassifier
import torchaudio

class Diarizer:
    def __init__(self):
        # Load the speaker embedding model
        self.embedding_model = EncoderClassifier.from_hparams(
            source="speechbrain/spkrec-ecapa-voxceleb",
            savedir="pretrained_models/spkrec-ecapa-voxceleb"
        )
        self.sample_rate = 16000

    def diarize(self, audio_file):
        # Load audio
        waveform, sample_rate = torchaudio.load(audio_file)
        
        # Resample if necessary
        if sample_rate != self.sample_rate:
            waveform = torchaudio.transforms.Resample(sample_rate, self.sample_rate)(waveform)

        # Convert to mono if stereo
        if waveform.shape[0] > 1:
            waveform = torch.mean(waveform, dim=0, keepdim=True)

        # Split audio into fixed-length segments (e.g., 3 seconds each)
        segment_length = 3 * self.sample_rate
        segments = waveform.split(segment_length, dim=1)

        # Get embeddings for each segment
        embeddings = []
        for segment in segments:
            if segment.shape[1] < segment_length / 2:  # Skip very short segments
                continue
            emb = self.embedding_model.encode_batch(segment)
            embeddings.append(emb.squeeze())

        # Perform clustering to identify speakers
        from sklearn.cluster import AgglomerativeClustering
        clustering = AgglomerativeClustering(n_clusters=None, distance_threshold=0.7)
        labels = clustering.fit_predict(torch.stack(embeddings).cpu().numpy())

        # Create segments with speaker labels
        segments = []
        for i, label in enumerate(labels):
            segments.append({
                "start": i * 3,  # 3 seconds per segment
                "end": (i + 1) * 3,
                "speaker": f"Speaker_{label}"
            })

        return segments

# Usage example
if __name__ == "__main__":
    diarizer = Diarizer()
    result = diarizer.diarize("output.wav")
    for segment in result:
        print(f"{segment['speaker']}: {segment['start']:.2f}s - {segment['end']:.2f}s")
