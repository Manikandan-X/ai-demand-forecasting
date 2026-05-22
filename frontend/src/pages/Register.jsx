import { useState } from "react";
import { Link } from "react-router-dom";
import API from "../api/axios";

export default function Register() {

  const [name, setName] =
    useState("");

  const [email, setEmail] =
    useState("");

  const [password, setPassword] =
    useState("");

  const handleRegister =
    async (e) => {

      e.preventDefault();

      try {

        await API.post(
          "/auth/register",
          {
            name,
            email,
            password,
          }
        );

        alert(
          "Registration Successful"
        );

      } catch (error) {

        console.error(error);

        alert(
          "Registration Failed"
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
      via-indigo-950
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
            Create Account
          </h1>

          <p className="text-gray-300 mt-2">
            Register for AI Forecasting
          </p>

        </div>

        <form
          onSubmit={handleRegister}
          className="space-y-5"
        >

          <input
            type="text"
            placeholder="Full Name"
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
            focus:ring-indigo-500
            "
            value={name}
            onChange={(e) =>
              setName(e.target.value)
            }
          />

          <input
            type="email"
            placeholder="Email Address"
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
            focus:ring-indigo-500
            "
            value={email}
            onChange={(e) =>
              setEmail(e.target.value)
            }
          />

          <input
            type="password"
            placeholder="Password"
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
            focus:ring-indigo-500
            "
            value={password}
            onChange={(e) =>
              setPassword(e.target.value)
            }
          />

          <button
            type="submit"
            className="
            w-full
            bg-gradient-to-r
            from-indigo-600
            to-purple-600
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
            Register
          </button>

        </form>

        <p
          className="
          text-center
          text-gray-300
          mt-6
          "
        >
          Already have an account?

          <Link
            to="/"
            className="
            text-indigo-400
            font-semibold
            ml-1
            "
          >
            Login
          </Link>

        </p>

      </div>

    </div>
  );
}