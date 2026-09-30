const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8001";

export const fetchProfile = async (username) => {
  const formattedUsername = username.trim().replace(/^@/, "");
  const url = `${API_BASE_URL}/profile/${encodeURIComponent(formattedUsername)}`;
  const response = await fetch(url);
  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || "Failed to fetch data from the backend.");
  }
  return data;
};

export const fetchPost = async (username, postUrl) => {
  const formattedUsername = username.trim().replace(/^@/, "");
  const url = `${API_BASE_URL}/post?username=${encodeURIComponent(formattedUsername)}&url=${encodeURIComponent(postUrl.trim())}`;
  const response = await fetch(url);
  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.error || "Failed to fetch post data from the backend.",
    );
  }
  return data;
};
