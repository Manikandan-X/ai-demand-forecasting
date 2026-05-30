import { Navigate } from "react-router-dom";

export default function ProtectedRoute({
  children,
  adminOnly = false,
}) {

  const token =
    sessionStorage.getItem(
      "token"
    );

  const user =
    JSON.parse(
      sessionStorage.getItem(
        "user"
      )
    );

  // NOT LOGGED IN
  if (!token) {

    return (
      <Navigate to="/" />
    );
  }

  // SUPER ADMIN CHECK
  if (
    adminOnly &&
    user?.role !==
      "super_admin"
  ) {

    return (
      <Navigate
        to="/dashboard"
      />
    );
  }

  return children;
}