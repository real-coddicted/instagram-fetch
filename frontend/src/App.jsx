import { useState } from "react";
import { ProfileTab } from "./components/ProfileTab";
import { PostTab } from "./components/PostTab";

function App() {
  const [activeTab, setActiveTab] = useState("profile");

  return (
    <>
      <header>
        <h1>Instagram Metrics</h1>
        <p className="subtitle">
          Quickly access business data and post insights
        </p>
      </header>

      <div className="tabs">
        <button
          className={`tab-btn ${activeTab === "profile" ? "active" : ""}`}
          onClick={() => setActiveTab("profile")}
        >
          Profile Metrics
        </button>
        <button
          className={`tab-btn ${activeTab === "post" ? "active" : ""}`}
          onClick={() => setActiveTab("post")}
        >
          Post Metrics
        </button>
      </div>

      <div className="container">
        <div style={{ display: activeTab === "profile" ? "block" : "none" }}>
          <ProfileTab />
        </div>
        <div style={{ display: activeTab === "post" ? "block" : "none" }}>
          <PostTab />
        </div>
      </div>
    </>
  );
}

export default App;
