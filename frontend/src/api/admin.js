import API from "./api";

//
// =========================
// DASHBOARD
// =========================
//
export const getAdminDashboard = () =>
  API.get("/admin/dashboard");

export const getAnalytics = () =>
  API.get("/admin/analytics");

//
// =========================
// USERS (ENTERPRISE READY)
// =========================
//
export const getAllUsers = (params = {}) => {
  const { page = 1, limit = 10, search = "" } = params;

  return API.get(
    `/admin/users?page=${page}&limit=${limit}&search=${search}`
  );
};

export const deleteUser = (id) =>
  API.delete(`/admin/users/${id}`);

export const updateUserRole = (id, role) =>
  API.put(`/admin/users/${id}/role`, { role });

//
// =========================
// DATASETS
// =========================
//
export const getAllDatasets = (params = {}) => {
  const { page = 1, limit = 10, search = "" } = params;

  return API.get(
    `/admin/datasets?page=${page}&limit=${limit}&search=${search}`
  );
};

export const deleteDataset = (id) =>
  API.delete(`/admin/datasets/${id}`);

//
// =========================
// FORECASTS
// =========================
//
export const getAllForecasts = (params = {}) => {
  const { page = 1, limit = 10 } = params;

  return API.get(
    `/admin/forecasts?page=${page}&limit=${limit}`
  );
};