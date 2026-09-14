import { useState } from "react";

function VoiceInterview() {
  const [recording, setRecording] = useState(false);

  const startRecording = () => {
    setRecording(true);
  };

  const stopRecording = () => {
    setRecording(false);
  };

  return (
    <div>
      <h1>Voice Assessment</h1>

      <p>
        Tell us about yourself.
      </p>

      {!recording ? (
        <button onClick={startRecording}>
          🎤 Start Speaking
        </button>
      ) : (
        <button onClick={stopRecording}>
          ⏹ Stop
        </button>
      )}

      {recording && (
        <p>🎙️ Listening...</p>
      )}
    </div>
  );
}

export default VoiceInterview;