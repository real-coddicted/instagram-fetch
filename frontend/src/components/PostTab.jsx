import { useState } from "react";
import { useApi } from "../hooks/useApi";
import { fetchPost } from "../api";
import { StatItem } from "./StatItem";

export function PostTab() {
  const [postUsername, setPostUsername] = useState("");
  const [postUrl, setPostUrl] = useState("");
  const { data: postData, loading, error, execute } = useApi(fetchPost);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!postUsername.trim() || !postUrl.trim()) return;
    execute(postUsername, postUrl);
  };

  return (
    <div className="tab-content">
      <form className="input-group double-input" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Target Username"
          aria-label="Target Username"
          value={postUsername}
          onChange={(e) => setPostUsername(e.target.value)}
        />
        <input
          type="text"
          placeholder="Instagram Post URL"
          aria-label="Instagram Post URL"
          value={postUrl}
          onChange={(e) => setPostUrl(e.target.value)}
        />
        <button type="submit" disabled={loading}>
          {loading ? "Fetching..." : "Fetch"}
        </button>
      </form>

      {loading && <div className="loader"></div>}
      {error && <div className="error-msg">{error}</div>}

      {postData && !loading && (
        <div className="post-card standalone">
          {postData.media_url &&
            (postData.media_type === "VIDEO" ? (
              <video className="post-media" src={postData.media_url} controls />
            ) : (
              <img
                className="post-media"
                src={postData.media_url}
                alt="Post media content"
              />
            ))}
          <div className="post-caption">{postData.caption || "No caption"}</div>
          <div className="post-stats-grid">
            <StatItem label="Likes" value={postData.like_count} />
            <StatItem label="Comments" value={postData.comments_count} />
          </div>
          <div className="post-date">
            Posted: {new Date(postData.timestamp).toLocaleDateString()}
          </div>
        </div>
      )}
    </div>
  );
}
