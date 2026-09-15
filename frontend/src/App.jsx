import { Routes, Route, Link } from "react-router-dom";
import VoiceInterview from "./pages/VoiceInterview";
import Profile from "./pages/Profile";
import Recommendations from "./pages/Recommendations";
import Roadmap from "./pages/Roadmap";

function Home() {
  return (
    <div>
      <h1>VoxMinds</h1>

      <p>
        Your Voice. Your Skills. Your Livelihood Prachi.
      </p>

      <Link to="/assessment">
        <button>
          🎤 Start Voice Assessment
        </button>
      </Link>
    </div>
  );
}

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />

      <Route
        path="/assessment"
        element={<VoiceInterview />}
      />
      <Route path="/profile" element={<Profile />}/>
      <Route path="/recommendations" element={<Recommendations />}/>
      <Route path="/roadmap" element={<Roadmap />}/>
    </Routes>
  );
}

export default App;