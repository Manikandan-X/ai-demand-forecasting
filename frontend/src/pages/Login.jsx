import {
  useState,
  useEffect
} from "react";

import {
  useNavigate,
  Link
} from "react-router-dom";

import API from "../api/axios";

export default function Login() {

  const [email, setEmail] =
    useState("");

  const [password, setPassword] =
    useState("");

  const navigate =
    useNavigate();

  useEffect(() => {

    const token =
      localStorage.getItem(
        "token"
      );

    if (token) {

      const user =
        JSON.parse(
          localStorage.getItem(
            "user"
          )
        );

      if (
        user?.role ===
        "admin"
      ) {

        navigate("/admin");

      } else {

        navigate(
          "/dashboard"
        );
      }
    }

  }, [navigate]);

  const handleLogin =
    async (e) => {

      e.preventDefault();

      try {

        const response =
          await API.post(
            "/auth/login",
            {
              email,
              password,
            }
          );

        const user =
          response.data.user;

        localStorage.setItem(
          "token",
          response.data
            .access_token
        );

        localStorage.setItem(
          "user",
          JSON.stringify(
            user
          )
        );

        if (
          user.role ===
          "admin"
        ) {

          navigate(
            "/admin"
          );

        } else {

          navigate(
            "/dashboard"
          );
        }

      } catch (error) {

        console.error(
          error
        );

        alert(
          "Login Failed"
        );
      }
    };

  return (

    <div
      className="
      min-h-screen
      flex
      items-center
      justify-center
      bg-gradient-to-br
      from-slate-950
      via-purple-950
      to-slate-900
      p-6
      "
    >

      <div
        className="
        w-full
        max-w-md
        backdrop-blur-xl
        bg-white/10
        border
        border-white/20
        rounded-[30px]
        p-8
        shadow-2xl
        animate-fade-in
        "
      >

        <div className="text-center mb-8">

          <h1
            className="
            text-4xl
            font-bold
            text-white
            "
          >
            Welcome Back
          </h1>

          <p className="text-gray-300 mt-2">
            Login to AI Forecasting
          </p>

        </div>

        <form
          onSubmit={
            handleLogin
          }
          className="
          space-y-5
          "
        >

          <input
            type="email"
            placeholder="
            Email Address
            "
            className="
            w-full
            bg-white/10
            border
            border-gray-500
            text-white
            placeholder-gray-300
            p-4
            rounded-2xl
            outline-none
            focus:ring-2
            focus:ring-purple-500
            "
            value={email}
            onChange={(e) =>
              setEmail(
                e.target.value
              )
            }
          />

          <input
            type="password"
            placeholder="
            Password
            "
            className="
            w-full
            bg-white/10
            border
            border-gray-500
            text-white
            placeholder-gray-300
            p-4
            rounded-2xl
            outline-none
            focus:ring-2
            focus:ring-purple-500
            "
            value={password}
            onChange={(e) =>
              setPassword(
                e.target.value
              )
            }
          />

          <button
            type="submit"
            className="
            w-full
            bg-gradient-to-r
            from-purple-600
            to-blue-600
            hover:scale-105
            transition
            duration-300
            text-white
            p-4
            rounded-2xl
            font-semibold
            shadow-lg
            "
          >
            Login
          </button>

        </form>

        <p
          className="
          text-center
          text-gray-300
          mt-6
          "
        >
          Don’t have an account?

          <Link
            to="/register"
            className="
            text-purple-400
            font-semibold
            ml-1
            "
          >
            Register
          </Link>

        </p>

      </div>

    </div>
  );
}