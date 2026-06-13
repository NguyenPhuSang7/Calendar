const SESSION_KEY = 'appointment_auth'

function getSession() {
  try {
    return JSON.parse(localStorage.getItem(SESSION_KEY))
  } catch {
    return null
  }
}

async function request(path, options = {}) {
  const session = getSession()
  const response = await fetch(path, {
    headers: {
      'Content-Type': 'application/json',
      ...(session?.token ? { Authorization: `Bearer ${session.token}` } : {}),
      ...options.headers,
    },
    ...options,
  })

  if (!response.ok) {
    const error = await response.json().catch(() => null)
    if (response.status === 401 && path !== '/api/auth/login') {
      localStorage.removeItem(SESSION_KEY)
      window.dispatchEvent(new Event('auth-expired'))
    }
    throw new Error(error?.message || 'Không thể kết nối đến máy chủ')
  }

  return response.status === 204 ? null : response.json()
}

export const api = {
  session: getSession,
  login: async (credentials) => {
    const session = await request('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    })
    localStorage.setItem(SESSION_KEY, JSON.stringify(session))
    return session
  },
  register: async (data) => {
    const session = await request('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify(data),
    })
    localStorage.setItem(SESSION_KEY, JSON.stringify(session))
    return session
  },
  logout: () => localStorage.removeItem(SESSION_KEY),
  contacts: () => request('/api/contacts'),
  createGuest: (data) =>
    request('/api/guests', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
  searchUsers: (query) => request(`/api/users/search?q=${encodeURIComponent(query)}`),
  friendRequests: () => request('/api/friend-requests'),
  sendFriendRequest: (userId) =>
    request(`/api/friend-requests/${userId}`, { method: 'POST' }),
  respondFriendRequest: (requestId, response) =>
    request(`/api/friend-requests/${requestId}`, {
      method: 'PATCH',
      body: JSON.stringify({ response }),
    }),
  appointments: (from, to, status) => {
    const params = new URLSearchParams({ from, to })
    if (status) params.set('status', status)
    return request(`/api/appointments?${params}`)
  },
  invitations: () => request('/api/appointments/invitations'),
  createAppointment: (data) =>
    request('/api/appointments', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
  updateAppointment: (id, data) =>
    request(`/api/appointments/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),
  deleteAppointment: (id) =>
    request(`/api/appointments/${id}`, { method: 'DELETE' }),
  updateStatus: (id, status) =>
    request(`/api/appointments/${id}/status`, {
      method: 'PATCH',
      body: JSON.stringify({ status }),
    }),
  respondInvitation: (id, response) =>
    request(`/api/appointments/${id}/invitation`, {
      method: 'PATCH',
      body: JSON.stringify({ response }),
    }),
  notes: (from, to) => request(`/api/notes?from=${from}&to=${to}`),
  createNote: (data) =>
    request('/api/notes', { method: 'POST', body: JSON.stringify(data) }),
  updateNote: (id, data) =>
    request(`/api/notes/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  deleteNote: (id) =>
    request(`/api/notes/${id}`, { method: 'DELETE' }),
}
