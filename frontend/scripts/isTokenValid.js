import jwtDecode from 'jwt-decode'; // You'll need this package

export const isTokenValid = (token_name) => {
  if (!token) return false;

  try {
    const decoded = jwtDecode(token);
    const currentTime = Date.now() / 1000; // Convert to seconds

    // Check if token is expired
    if (decoded.exp < currentTime) {
      return false;
    }

    return true;
  } catch (error) {
    return false;
  }
};
