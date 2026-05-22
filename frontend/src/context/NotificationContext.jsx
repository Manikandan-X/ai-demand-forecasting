import { createContext, useState } from "react";

export const NotificationContext = createContext(null);

export const NotificationProvider = ({ children }) => {
  const [notifications, setNotifications] = useState([]);
  const [unread, setUnread] = useState(0);

  const addNotification = (data) => {
    const newNotification = {
      id: Date.now(),
      message: data.message,
      time: "Just now",
      read: false,
    };

    setNotifications((prev) => [newNotification, ...prev]);
    setUnread((prev) => prev + 1);
  };

  const markAsRead = (id) => {
    setNotifications((prev) =>
      prev.map((n) =>
        n.id === id ? { ...n, read: true } : n
      )
    );

    setUnread((prev) => Math.max(prev - 1, 0));
  };

  const markAllAsRead = () => {
    setNotifications((prev) =>
      prev.map((n) => ({ ...n, read: true }))
    );
    setUnread(0);
  };

  return (
    <NotificationContext.Provider
      value={{
        notifications,
        unread,
        addNotification,
        markAsRead,
        markAllAsRead,
      }}
    >
      {children}
    </NotificationContext.Provider>
  );
};