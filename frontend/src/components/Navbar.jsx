import {
  Link,
  useNavigate,
} from "react-router-dom";

import {
  useState,
  useEffect,
  useRef,
} from "react";

import API from "../api/axios";

export default function Navbar() {

  const navigate =
    useNavigate();

  const user =
    JSON.parse(
      localStorage.getItem(
        "user"
      )
    );

  const isAdmin =
    user?.role === "admin";

  const [mobileOpen, setMobileOpen] =
    useState(false);

  const [open, setOpen] =
    useState(false);

  const [
    notifications,
    setNotifications,
  ] = useState([]);

  const [
    loadingNotifications,
    setLoadingNotifications,
  ] = useState(false);

  const socketRef =
    useRef(null);

  // =========================
  // FETCH NOTIFICATIONS
  // =========================
  const fetchNotifications =
    async () => {

      try {

        setLoadingNotifications(
          true
        );

        const response =
          await API.get(
            "/notifications/"
          );

        setNotifications(
          response.data
        );

      } catch (error) {

        console.error(
          error
        );

      } finally {

        setLoadingNotifications(
          false
        );
      }
    };

  // =========================
  // WEBSOCKET
  // =========================
  useEffect(() => {

    const initialize =
      async () => {

        await fetchNotifications();
      };

    initialize();

    const ws =
      new WebSocket(
        "ws://localhost:8000/ws/notifications"
      );

    socketRef.current =
      ws;

    ws.onopen = () => {
      console.log(
        "WebSocket Connected"
      );
    };

    ws.onmessage = (
      event
    ) => {

      const data =
        JSON.parse(
          event.data
        );

      const newNotification =
        {
          id:
            Date.now(),

          title:
            "Notification",

          message:
            data.message ||
            "New Notification",

          is_read:
            false,

          created_at:
            new Date().toISOString(),
        };

      setNotifications(
        (prev) => [
          newNotification,
          ...prev,
        ]
      );
    };

    ws.onclose = () => {
      console.log(
        "WebSocket Disconnected"
      );
    };

    return () => {
      ws.close();
    };

  }, []);

  // =========================
  // UNREAD COUNT
  // =========================
  const unreadCount =
    notifications.filter(
      (n) =>
        !n.is_read
    ).length;

  // =========================
  // MARK READ
  // =========================
  const markAsRead =
    async (id) => {

      try {

        await API.put(
          `/notifications/${id}/read`
        );

        setNotifications(
          (prev) =>
            prev.map((n) =>
              n.id === id
                ? {
                    ...n,
                    is_read: true,
                  }
                : n
            )
        );

      } catch (error) {

        console.error(
          error
        );
      }
    };

  const markAllAsRead =
    async () => {

      try {

        await API.put(
          "/notifications/mark-all/read"
        );

        setNotifications(
          (prev) =>
            prev.map(
              (n) => ({
                ...n,
                is_read: true,
              })
            )
        );

      } catch (error) {

        console.error(
          error
        );
      }
    };

  // =========================
  // LOGOUT
  // =========================
  const handleLogout =
    () => {

      localStorage.removeItem(
        "token"
      );

      localStorage.removeItem(
        "user"
      );

      navigate("/");
    };

  const userMenus = [
    {
      name: "Dashboard",
      path: "/dashboard",
    },
    {
      name: "Dataset",
      path: "/upload",
    },
    {
      name: "Forecast",
      path: "/forecast",
    },
    {
      name: "Forecast History",
      path:
        "/forecast-history",
    },
    {
      name: "Reports",
      path: "/reports",
    },
  ];

  return (
    <nav
      className="
      sticky
      top-0
      z-50
      bg-slate-950
      border-b
      border-slate-800
      shadow-lg
      "
    >
      <div
        className="
        px-4
        sm:px-6
        py-4
        flex
        justify-between
        items-center
        "
      >

        {/* LEFT */}
        <div
          className="
          flex
          items-center
          gap-3
          "
        >

          {/* MOBILE MENU */}
          <button
            onClick={() =>
              setMobileOpen(
                !mobileOpen
              )
            }
            className="
            md:hidden
            text-white
            text-2xl
            "
          >
            ☰
          </button>

          {/* LOGO */}
          <h1
            className="
            text-xl
            md:text-3xl
            font-bold
            text-white
            "
          >
            AI Forecasting
          </h1>
        </div>

        {/* DESKTOP MENU */}
        <div
          className="
          hidden
          md:flex
          items-center
          gap-6
          "
        >

          {!isAdmin &&
            userMenus.map(
              (item) => (
                <Link
                  key={
                    item.name
                  }
                  to={
                    item.path
                  }
                  className="
                  text-slate-300
                  hover:text-cyan-400
                  transition
                  "
                >
                  {
                    item.name
                  }
                </Link>
              )
            )}

          {isAdmin && (
            <Link
              to="/admin"
              className="
              text-cyan-400
              font-semibold
              "
            >
              Admin Dashboard
            </Link>
          )}

          {/* BELL */}
          <div className="relative">

            <button
              onClick={() =>
                setOpen(
                  !open
                )
              }
              className="
              relative
              text-3xl
              "
            >
              🔔

              {unreadCount >
                0 && (
                <span
                  className="
                  absolute
                  -top-1
                  -right-1
                  bg-red-600
                  text-white
                  text-[10px]
                  rounded-full
                  w-5
                  h-5
                  flex
                  items-center
                  justify-center
                  "
                >
                  {
                    unreadCount
                  }
                </span>
              )}
            </button>

            {open && (
              <div
                className="
                absolute
                right-0
                top-14
                w-[320px]
                bg-slate-900
                border
                border-slate-700
                rounded-3xl
                shadow-xl
                p-5
                z-[999]
                "
              >

                <div
                  className="
                  flex
                  justify-between
                  items-center
                  mb-4
                  "
                >
                  <h2
                    className="
                    text-white
                    font-bold
                    "
                  >
                    Notifications
                  </h2>

                  {unreadCount >
                    0 && (
                    <button
                      onClick={
                        markAllAsRead
                      }
                      className="
                      text-cyan-400
                      text-sm
                      "
                    >
                      Mark All
                    </button>
                  )}
                </div>

                <div
                  className="
                  max-h-72
                  overflow-y-auto
                  space-y-3
                  "
                >

                  {loadingNotifications && (
                    <p className="text-slate-400">
                      Loading...
                    </p>
                  )}

                  {!loadingNotifications &&
                    notifications.length ===
                      0 && (
                      <p
                        className="
                        text-slate-400
                        "
                      >
                        No notifications
                      </p>
                    )}

                  {notifications.map(
                    (
                      notification
                    ) => (
                      <div
                        key={
                          notification.id
                        }
                        className="
                        bg-slate-800
                        rounded-xl
                        p-3
                        "
                      >
                        <p className="text-white text-sm">
                          {
                            notification.message
                          }
                        </p>

                        <div
                          className="
                          flex
                          justify-between
                          mt-2
                          "
                        >
                          <span
                            className="
                            text-xs
                            text-gray-400
                            "
                          >
                            {new Date(
                              notification.created_at
                            ).toLocaleString()}
                          </span>

                          {!notification.is_read && (
                            <button
                              onClick={() =>
                                markAsRead(
                                  notification.id
                                )
                              }
                              className="
                              text-green-400
                              text-xs
                              "
                            >
                              Read
                            </button>
                          )}
                        </div>
                      </div>
                    )
                  )}

                </div>

              </div>
            )}
          </div>

          {/* LOGOUT */}
          <button
            onClick={
              handleLogout
            }
            className="
            bg-red-600
            hover:bg-red-700
            px-4
            py-2
            rounded-xl
            text-white
            "
          >
            Logout
          </button>

        </div>
      </div>

      {/* MOBILE MENU */}
      {mobileOpen && (
        <div
          className="
          md:hidden
          bg-slate-900
          border-t
          border-slate-800
          px-4
          py-4
          space-y-4
          "
        >

          {!isAdmin &&
            userMenus.map(
              (item) => (
                <Link
                  key={
                    item.name
                  }
                  to={
                    item.path
                  }
                  onClick={() =>
                    setMobileOpen(
                      false
                    )
                  }
                  className="
                  block
                  text-slate-300
                  hover:text-cyan-400
                  "
                >
                  {
                    item.name
                  }
                </Link>
              )
            )}

          {isAdmin && (
            <Link
              to="/admin"
              onClick={() =>
                setMobileOpen(
                  false
                )
              }
              className="
              block
              text-cyan-400
              font-semibold
              "
            >
              Admin Dashboard
            </Link>
          )}

          <button
            onClick={
              handleLogout
            }
            className="
            bg-red-600
            px-4
            py-2
            rounded-xl
            text-white
            w-full
            "
          >
            Logout
          </button>

        </div>
      )}
    </nav>
  );
}