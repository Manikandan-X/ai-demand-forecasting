import { Navigate } from "react-router-dom";

export default function ProtectedRoute({
  children,
  adminOnly = false,
}) {

  const token =
    localStorage.getItem(
      "token"
    );

  const user =
    JSON.parse(
      localStorage.getItem(
        "user"
      )
    );

  // NOT LOGGED IN
  if (!token) {

    return (
      <Navigate to="/" />
    );
  }

  // ADMIN ROUTE CHECK
  if (
    adminOnly &&
    user?.role !== "admin"
  ) {

    return (
      <Navigate
        to="/dashboard"
      />
    );
  }

  return children;
}