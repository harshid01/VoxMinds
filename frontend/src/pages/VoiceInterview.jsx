import { useRef, useState } from "react";
import api from "../services/api";

const LANGUAGES = {
  en: {
    name: "English",
    code: "en-IN",
    welcome:
      "Hello! I am VoxMinds. I will ask you a few questions to understand your skills and livelihood goals.",
  },

  hi: {
    name: "हिंदी",
    code: "hi-IN",
    welcome:
      "नमस्ते! मैं VoxMinds हूँ। आपकी कौशल और आजीविका की जरूरत समझने के लिए मैं आपसे कुछ सवाल पूछूंगा।",
  },

  gu: {
    name: "ગુજરાતી",
    code: "gu-IN",
    welcome:
      "નમસ્તે! હું VoxMinds છું. તમારી કુશળતા અને આજીવિકાની જરૂરિયાત સમજવા માટે હું તમને થોડા પ્રશ્નો પૂછીશ.",
  },
};

function VoiceInterview() {
  const [language, setLanguage] = useState("en");

  const [recording, setRecording] = useState(false);

  const [transcript, setTranscript] = useState("");

  const [currentQuestion, setCurrentQuestion] = useState(
    LANGUAGES.en.welcome
  );

  const [profile, setProfile] = useState({
    education: null,
    family_occupation: null,
    current_livelihood: null,
    skills: [],
    interests: [],
    mobility_constraints: [],
    employment_preference: null,
    district: null,
    state: null,
  });

  const [currentField, setCurrentField] = useState(null);

  const [completed, setCompleted] = useState(false);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");

  const recognitionRef = useRef(null);

  const startListening = () => {
    setError("");
    setTranscript("");

    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      setError(
        "Speech recognition is not supported. Please use Google Chrome."
      );
      return;
    }

    const recognition = new SpeechRecognition();

    recognition.lang = LANGUAGES[language].code;

    recognition.continuous = true;

    recognition.interimResults = true;

    recognition.onstart = () => {
      setRecording(true);
    };

    recognition.onresult = (event) => {
      let finalText = "";

      for (let i = event.resultIndex; i < event.results.length; i++) {
        if (event.results[i].isFinal) {
          finalText += event.results[i][0].transcript + " ";
        }
      }

      if (finalText) {
        setTranscript((previous) => previous + finalText);
      }
    };

    recognition.onerror = (event) => {
      console.error("Speech recognition error:", event.error);

      setError(`Speech recognition error: ${event.error}`);

      setRecording(false);
    };

    recognition.onend = () => {
      setRecording(false);
    };

    recognitionRef.current = recognition;

    recognition.start();
  };

  const stopListening = () => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
      recognitionRef.current = null;
    }

    setRecording(false);
  };

  const analyzeAnswer = async () => {
    if (!transcript.trim()) {
      setError("Please speak an answer before continuing.");
      return;
    }

    try {
      setLoading(true);
      setError("");

      const extractionResponse = await api.post(
        "/api/profile/extract",
        {
          transcript: transcript,
          language: language,
        }
      );

      const extractedProfile = extractionResponse.data.profile;

      const updatedProfile = {
        ...profile,
        ...extractedProfile,
      };

      setProfile(updatedProfile);

      const questionResponse = await api.post(
        `/api/interview/next?language=${language}`,
        updatedProfile
      );

      const nextQuestion = questionResponse.data;

      if (nextQuestion.completed) {
        setCompleted(true);
        setCurrentQuestion("");
        setCurrentField(null);
      } else {
        setCurrentQuestion(nextQuestion.question);
        setCurrentField(nextQuestion.field);
      }

      setTranscript("");
    } catch (err) {
      console.error("Interview error:", err);

      setError(
        "Unable to process your answer. Please make sure the VoxMinds backend is running."
      );
    } finally {
      setLoading(false);
    }
  };

  const changeLanguage = (newLanguage) => {
    if (recording || loading) {
      return;
    }

    setLanguage(newLanguage);

    setCurrentQuestion(LANGUAGES[newLanguage].welcome);

    setTranscript("");

    setError("");
  };

  return (
    <div>
      <h1>🎤 VoxMinds Voice Assessment</h1>

      <p>
        Your Voice. Your Skills. Your Livelihood.
      </p>

      <hr />

      <h3>Select Language</h3>

      <div>
        {Object.entries(LANGUAGES).map(([key, value]) => (
          <button
            key={key}
            onClick={() => changeLanguage(key)}
            disabled={recording || loading}
          >
            {value.name}
          </button>
        ))}
      </div>

      <hr />

      {!completed && (
        <div>
          <h2>🤖 VoxMinds</h2>

          <p>{currentQuestion}</p>

          {currentField && (
            <small>
              Collecting information about: <b>{currentField}</b>
            </small>
          )}
        </div>
      )}

      {completed && (
        <div>
          <h2>🎉 Assessment Complete</h2>

          <p>
            Thank you. VoxMinds has collected enough information to create
            your personalized livelihood profile.
          </p>
        </div>
      )}

      {!completed && (
        <div>
          <br />

          {!recording ? (
            <button
              onClick={startListening}
              disabled={loading}
            >
              🎤 Start Speaking
            </button>
          ) : (
            <button onClick={stopListening}>
              ⏹ Stop Speaking
            </button>
          )}

          {recording && (
            <div>
              <p>🔴 Listening...</p>
              <p>Speak naturally. You don't need to type anything.</p>
            </div>
          )}

          {transcript && !recording && (
            <div>
              <h3>📝 Your Answer</h3>

              <p>{transcript}</p>

              <button
                onClick={analyzeAnswer}
                disabled={loading}
              >
                {loading
                  ? "🧠 Analyzing..."
                  : "🧠 Continue"}
              </button>
            </div>
          )}
        </div>
      )}

      {error && (
        <div>
          <p>⚠️ {error}</p>
        </div>
      )}

      <hr />

      <h2>👤 Current Profile</h2>

      <pre>
        {JSON.stringify(profile, null, 2)}
      </pre>
    </div>
  );
}

export default VoiceInterview;