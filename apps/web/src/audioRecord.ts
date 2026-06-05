const AUDIO_MIME_TYPES = [
  "audio/webm;codecs=opus",
  "audio/webm",
  "audio/ogg;codecs=opus",
  "audio/ogg",
  "audio/mp4",
] as const;

export type AudioRecordingHandle = {
  mimeType: string;
  stop: () => Promise<Blob>;
};

export function isAudioRecordingSupported() {
  return (
    typeof navigator !== "undefined" &&
    typeof navigator.mediaDevices !== "undefined" &&
    typeof navigator.mediaDevices.getUserMedia === "function" &&
    typeof MediaRecorder !== "undefined"
  );
}

function supportedAudioMimeType() {
  if (typeof MediaRecorder === "undefined") return null;
  return AUDIO_MIME_TYPES.find((mimeType) => MediaRecorder.isTypeSupported(mimeType)) ?? null;
}

function stopTracks(stream: MediaStream) {
  stream.getTracks().forEach((track) => track.stop());
}

export async function startAudioRecording(): Promise<AudioRecordingHandle> {
  if (!isAudioRecordingSupported()) {
    throw new Error("Audio recording is not supported in this browser.");
  }

  const mimeType = supportedAudioMimeType();
  if (!mimeType) {
    throw new Error("No supported audio recording MIME type is available.");
  }

  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  const recorder = new MediaRecorder(stream, { mimeType });
  const chunks: Blob[] = [];

  recorder.addEventListener("dataavailable", (event) => {
    if (event.data.size > 0) chunks.push(event.data);
  });

  recorder.start();

  return {
    mimeType,
    stop: () =>
      new Promise<Blob>((resolve, reject) => {
        recorder.addEventListener(
          "stop",
          () => {
            stopTracks(stream);
            resolve(new Blob(chunks, { type: mimeType.split(";")[0] || mimeType }));
          },
          { once: true },
        );
        recorder.addEventListener(
          "error",
          (event) => {
            stopTracks(stream);
            reject(event);
          },
          { once: true },
        );
        if (recorder.state === "recording") recorder.stop();
      }),
  };
}
