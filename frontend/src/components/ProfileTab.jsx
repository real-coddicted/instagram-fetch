import { useState } from "react";
import { useApi } from "../hooks/useApi";
import { fetchProfile } from "../api";
import { StatItem } from "./StatItem";

export function ProfileTab() {
  const [username, setUsername] = useState("");
  const { data: profile, loading, error, execute } = useApi(fetchProfile);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!username.trim()) return;
    execute(username);
  };

  return (
    <div className="tab-content">
      <form className="input-group" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter Instagram username (e.g. nike)"
          aria-label="Instagram username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <button type="submit" disabled={loading}>
          {loading ? "Searching..." : "Search"}
        </button>
      </form>

      {loading && <div className="loader"></div>}
      {error && <div className="error-msg">{error}</div>}

      {profile && !loading && (
        <div className="profile-card">
          {profile.profile_picture_url && (
            <img
              className="profile-pic"
              src={profile.profile_picture_url}
              alt={`${profile.username} profile`}
            />
          )}
          <div className="profile-name">@{profile.username}</div>
          <div className="profile-bio">{profile.biography || ""}</div>

          <div className="stats-grid">
            <StatItem label="Followers" value={profile.followers_count} />
            <StatItem label="Posts" value={profile.media_count} />
            <StatItem label="Following" value={profile.follows_count} />
          </div>
        </div>
      )}
    </div>
  );
}
