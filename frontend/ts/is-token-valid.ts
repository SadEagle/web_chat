import { jwtDecode } from "jwt-decode";

export async function isTokenValid(token: string) {
  if (!token) return false;

  try {
    const decoded = jwtDecode(token);
    const currentTime = Date.now() / 1000;

    if (!decoded.exp || decoded.exp < currentTime) {
      return false;
    }
  } catch (error) {
    return false;
  }
  return true;
};
