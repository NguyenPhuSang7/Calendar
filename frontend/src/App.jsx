import { useCallback, useEffect, useMemo, useState } from 'react'
import {
  CalendarDays, ChevronLeft, ChevronRight, Clock3, Eye, EyeOff, FileText,
  LayoutDashboard, LockKeyhole, LogOut, Menu, Pencil, Plus, Search,
  RefreshCw, Sparkles, Trash2, UserPlus, UserRound, UsersRound, X,
} from 'lucide-react'
import { api } from './api'

const INVITATION = {
  PENDING: { label: 'Chờ người liên hệ xác nhận', className: 'pending' },
  ACCEPTED: { label: 'Đã chấp nhận', className: 'confirmed' },
  DECLINED: { label: 'Đã từ chối', className: 'cancelled' },
}
const WEEKDAYS = ['T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'CN']

const toLocalDate = (date = new Date()) => {
  const offset = date.getTimezoneOffset()
  return new Date(date.getTime() - offset * 60_000).toISOString().slice(0, 10)
}
const formatTime = (value) => value?.slice(11, 16)
const monthTitle = (date) => new Intl.DateTimeFormat('vi-VN', {
  month: 'long', year: 'numeric',
}).format(date)
const longDate = (date) => new Intl.DateTimeFormat('vi-VN', {
  weekday: 'long', day: '2-digit', month: 'long', year: 'numeric',
}).format(new Date(`${date}T00:00:00`))

function App() {
  const [session, setSession] = useState(() => api.session())
  useEffect(() => {
    const expired = () => setSession(null)
    window.addEventListener('auth-expired', expired)
    return () => window.removeEventListener('auth-expired', expired)
  }, [])
  if (!session) return <LoginPage onLogin={setSession} />
  return <CalendarDashboard session={session} onLogout={() => {
    api.logout()
    setSession(null)
  }} />
}

function CalendarDashboard({ session, onLogout }) {
  const [activeView, setActiveView] = useState(() => viewFromHash())
  const [cursor, setCursor] = useState(() => new Date(new Date().getFullYear(), new Date().getMonth(), 1))
  const [selectedDate, setSelectedDate] = useState(toLocalDate())
  const [appointments, setAppointments] = useState([])
  const [notes, setNotes] = useState([])
  const [users, setUsers] = useState([])
  const [invitations, setInvitations] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [toast, setToast] = useState('')
  const [editor, setEditor] = useState(null)
  const [userEditorOpen, setUserEditorOpen] = useState(false)
  const [mobileMenu, setMobileMenu] = useState(false)
  const [query, setQuery] = useState('')

  const grid = useMemo(() => calendarGrid(cursor), [cursor])
  const rangeStart = grid[0].date
  const rangeEnd = grid.at(-1).date

  const loadCalendar = useCallback(async () => {
    setLoading(true)
    setError('')
    try {
      const [appointmentData, noteData, invitationData] = await Promise.all([
        api.appointments(rangeStart, rangeEnd),
        api.notes(rangeStart, rangeEnd),
        api.invitations(),
      ])
      setAppointments(appointmentData)
      setNotes(noteData)
      setInvitations(invitationData)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }, [rangeStart, rangeEnd])

  const loadUsers = useCallback(async () => {
    try {
      setUsers(await api.contacts())
    } catch (err) {
      setError(err.message)
    }
  }, [])

  useEffect(() => {
    loadUsers()
  }, [loadUsers])
  useEffect(() => {
    const handleHashChange = () => setActiveView(viewFromHash())
    window.addEventListener('hashchange', handleHashChange)
    if (!window.location.hash) window.history.replaceState(null, '', '#calendar')
    return () => window.removeEventListener('hashchange', handleHashChange)
  }, [])
  useEffect(() => { loadCalendar() }, [loadCalendar])
  useEffect(() => {
    if (!toast) return
    const timer = setTimeout(() => setToast(''), 2600)
    return () => clearTimeout(timer)
  }, [toast])

  const itemsByDate = useMemo(() => {
    const result = {}
    appointments.forEach((item) => {
      const date = item.startTime.slice(0, 10)
      ;(result[date] ||= []).push({ ...item, type: 'appointment' })
    })
    notes.forEach((item) => {
      ;(result[item.noteDate] ||= []).push({ ...item, type: 'note' })
    })
    return result
  }, [appointments, notes])

  const selectedItems = (itemsByDate[selectedDate] || []).filter((item) => {
    if (!query.trim()) return true
    return `${item.contactName || ''} ${item.title || ''} ${item.content || ''}`
      .toLocaleLowerCase('vi').includes(query.trim().toLocaleLowerCase('vi'))
  })

  const changeMonth = (amount) => {
    const next = new Date(cursor.getFullYear(), cursor.getMonth() + amount, 1)
    setCursor(next)
    setSelectedDate(toLocalDate(next))
  }
  const goToday = () => {
    const today = new Date()
    setCursor(new Date(today.getFullYear(), today.getMonth(), 1))
    setSelectedDate(toLocalDate(today))
  }
  const openCreate = (type, date = selectedDate) => setEditor({ type, date, item: null })
  const openEdit = (item) => setEditor({ type: item.type, date: selectedDate, item })
  const saved = async (message) => {
    setEditor(null)
    setToast(message)
    await loadCalendar()
  }
  const remove = async (item) => {
    if (!window.confirm(`Xóa ${item.type === 'note' ? 'ghi chú' : 'cuộc hẹn'} này?`)) return
    try {
      item.type === 'note' ? await api.deleteNote(item.id) : await api.deleteAppointment(item.id)
      await saved('Đã xóa khỏi lịch')
    } catch (err) { setError(err.message) }
  }
  const respondInvitation = async (id, response) => {
    try {
      await api.respondInvitation(id, response)
      setToast(response === 'ACCEPTED' ? 'Đã chấp nhận lời mời' : 'Đã từ chối lời mời')
      await loadCalendar()
    } catch (err) { setError(err.message) }
  }
  const navigate = (view) => {
    window.location.hash = view
    setActiveView(view)
    setMobileMenu(false)
  }

  return (
    <div className="app-shell">
      <Sidebar activeView={activeView} onNavigate={navigate} mobileOpen={mobileMenu}
        onClose={() => setMobileMenu(false)} onLogout={onLogout} />
      <main className="main-content calendar-main">
        <header className="topbar">
          <button className="icon-button menu-button" onClick={() => setMobileMenu(true)}><Menu size={22} /></button>
          <div><p className="eyebrow">{viewMeta(activeView).eyebrow}</p><h1>{viewMeta(activeView).title}</h1></div>
          <div className="topbar-actions">
            <div className="search-box"><Search size={18} /><input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Tìm trong ngày..." /></div>
            <div className="avatar">{initials(session.fullName)}</div>
          </div>
        </header>

        {error && <div className="error-banner">{error}<button onClick={() => setError('')}><X size={16} /></button></div>}
        {invitations.length > 0 && <InvitationBox invitations={invitations} onRespond={respondInvitation} />}

        {activeView === 'calendar' ? (
          <>
            <CalendarToolbar cursor={cursor} changeMonth={changeMonth} goToday={goToday}
              onCreate={() => openCreate('appointment')} />
            <CalendarView grid={grid} itemsByDate={itemsByDate} selectedDate={selectedDate}
              setSelectedDate={setSelectedDate} openCreate={openCreate} loading={loading}
              selectedItems={selectedItems} openEdit={openEdit} remove={remove} />
          </>
        ) : (
          <ManagementView view={activeView} cursor={cursor} changeMonth={changeMonth} goToday={goToday}
            appointments={appointments} notes={notes} users={users} query={query}
            openCreate={openCreate} openEdit={openEdit} remove={remove} loading={loading}
            onAddUser={() => setUserEditorOpen(true)} onRefreshUsers={loadUsers} />
        )}
      </main>

      {editor?.type === 'appointment' && (
        <AppointmentEditor contacts={users} date={editor.date} item={editor.item}
          onClose={() => setEditor(null)} onSaved={() => saved(editor.item ? 'Đã cập nhật cuộc hẹn' : 'Đã tạo cuộc hẹn')} />
      )}
      {editor?.type === 'note' && (
        <NoteEditor date={editor.date} item={editor.item}
          onClose={() => setEditor(null)} onSaved={() => saved(editor.item ? 'Đã cập nhật ghi chú' : 'Đã tạo ghi chú')} />
      )}
      {userEditorOpen && (
        <UserEditor onClose={() => setUserEditorOpen(false)} onSaved={async () => {
          setUserEditorOpen(false)
          setToast('Đã thêm guest vào danh bạ riêng')
          await loadUsers()
        }} />
      )}
      {toast && <div className="toast">{toast}</div>}
    </div>
  )
}

function CalendarToolbar({ cursor, changeMonth, goToday, onCreate }) {
  return <section className="calendar-toolbar">
    <div><p className="section-kicker">Kế hoạch của bạn</p><h2>{monthTitle(cursor)}</h2></div>
    <div className="calendar-toolbar-actions">
      <MonthNavigation changeMonth={changeMonth} goToday={goToday} />
      <button className="solid-button" onClick={onCreate}><Plus size={18} /> Thêm mới</button>
    </div>
  </section>
}

function MonthNavigation({ changeMonth, goToday }) {
  return <div className="date-navigation">
    <button onClick={() => changeMonth(-1)}><ChevronLeft size={18} /></button>
    <button className="today-button" onClick={goToday}>Hôm nay</button>
    <button onClick={() => changeMonth(1)}><ChevronRight size={18} /></button>
  </div>
}

function CalendarView({ grid, itemsByDate, selectedDate, setSelectedDate, openCreate, loading,
  selectedItems, openEdit, remove }) {
  return <div className="calendar-layout">
    <section className="month-calendar">
      <div className="weekday-row">{WEEKDAYS.map((day) => <div key={day}>{day}</div>)}</div>
      <div className="calendar-grid">
        {grid.map((day) => {
          const dayItems = itemsByDate[day.date] || []
          return <button key={day.date}
            className={`calendar-day ${day.inMonth ? '' : 'outside'} ${day.date === selectedDate ? 'selected' : ''} ${day.date === toLocalDate() ? 'today' : ''}`}
            onClick={() => setSelectedDate(day.date)}
            onDoubleClick={() => openCreate('appointment', day.date)}>
            <span className="day-number">{Number(day.date.slice(-2))}</span>
            <div className="day-items">
              {dayItems.slice(0, 3).map((item) => <span key={`${item.type}-${item.id}`}
                className={`mini-event ${item.type === 'note' ? `note-${item.color}` : invitationClass(item)}`}>
                {item.type === 'note' ? <FileText size={10} /> : <Clock3 size={10} />}
                {item.type === 'note' ? item.title : `${formatTime(item.startTime)} ${item.title}`}
              </span>)}
              {dayItems.length > 3 && <span className="more-items">+{dayItems.length - 3} mục khác</span>}
            </div>
          </button>
        })}
      </div>
      {loading && <div className="calendar-loading">Đang tải lịch...</div>}
    </section>
    <aside className="day-panel">
      <div className="day-panel-header">
        <div><p className="section-kicker">Chi tiết ngày</p><h3>{longDate(selectedDate)}</h3></div>
        <div className="quick-add">
          <button onClick={() => openCreate('appointment')} title="Thêm cuộc hẹn"><CalendarDays size={17} /></button>
          <button onClick={() => openCreate('note')} title="Thêm ghi chú"><FileText size={17} /></button>
        </div>
      </div>
      <div className="day-agenda">
        {selectedItems.length ? selectedItems.map((item) => <AgendaItem key={`${item.type}-${item.id}`}
          item={item} onEdit={() => openEdit(item)} onDelete={() => remove(item)} />) : (
          <div className="calendar-empty"><CalendarDays size={24} /><strong>Ngày này đang trống</strong>
            <p>Thêm cuộc hẹn hoặc một ghi chú nhỏ.</p><div>
              <button onClick={() => openCreate('appointment')}>Cuộc hẹn</button>
              <button onClick={() => openCreate('note')}>Ghi chú</button>
            </div></div>
        )}
      </div>
    </aside>
  </div>
}

function ManagementView({ view, cursor, changeMonth, goToday, appointments, notes, users,
  query, openCreate, openEdit, remove, loading, onAddUser, onRefreshUsers }) {
  const normalized = query.trim().toLocaleLowerCase('vi')
  const source = view === 'appointments' ? appointments.map((item) => ({ ...item, type: 'appointment' }))
    : view === 'notes' ? notes.map((item) => ({ ...item, type: 'note' })) : users
  const filtered = source.filter((item) => !normalized
    || JSON.stringify(item).toLocaleLowerCase('vi').includes(normalized))
  return <>
    <section className="calendar-toolbar management-toolbar">
      <div><p className="section-kicker">{view === 'customers' ? 'Người liên hệ' : 'Dữ liệu trong tháng'}</p>
        <h2>{view === 'customers' ? `${users.length} liên hệ` : monthTitle(cursor)}</h2></div>
      <div className="calendar-toolbar-actions">
        {view !== 'customers' && <MonthNavigation changeMonth={changeMonth} goToday={goToday} />}
        {view === 'appointments' && <button className="solid-button" onClick={() => openCreate('appointment')}><Plus size={18} /> Cuộc hẹn</button>}
        {view === 'notes' && <button className="solid-button" onClick={() => openCreate('note')}><Plus size={18} /> Ghi chú</button>}
        {view === 'customers' && <button className="secondary-button refresh-button" onClick={onRefreshUsers}><RefreshCw size={16} /> Làm mới</button>}
        {view === 'customers' && <button className="solid-button" onClick={onAddUser}><UserPlus size={18} /> Thêm guest</button>}
      </div>
    </section>
    {view === 'customers' ? <ContactsPanel contacts={filtered} onChanged={onRefreshUsers} />
      : <section className="management-card">
        {loading ? <div className="management-empty">Đang tải dữ liệu...</div>
          : filtered.length ? <div className="management-list">
            {filtered.map((item) => <AgendaItem key={`${item.type}-${item.id}`} item={item}
              onEdit={() => openEdit(item)} onDelete={() => remove(item)} />)}
          </div> : <div className="management-empty">Không có dữ liệu phù hợp.</div>}
      </section>}
  </>
}

function ContactsPanel({ contacts, onChanged }) {
  const [search, setSearch] = useState('')
  const [results, setResults] = useState([])
  const [requests, setRequests] = useState([])
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')

  const loadRequests = useCallback(async () => {
    try { setRequests(await api.friendRequests()) } catch (err) { setError(err.message) }
  }, [])
  useEffect(() => { loadRequests() }, [loadRequests])

  const findUsers = async (event) => {
    event.preventDefault()
    if (search.trim().length < 2) {
      setError('Nhập ít nhất 2 ký tự để tìm kiếm')
      return
    }
    setBusy(true); setError('')
    try { setResults(await api.searchUsers(search.trim())) }
    catch (err) { setError(err.message) }
    finally { setBusy(false) }
  }
  const sendRequest = async (userId) => {
    setError('')
    try {
      await api.sendFriendRequest(userId)
      setResults(results.map((item) => item.id === userId
        ? {...item, relationshipStatus: 'REQUEST_SENT'} : item))
    } catch (err) { setError(err.message) }
  }
  const respond = async (requestId, response) => {
    setError('')
    try {
      await api.respondFriendRequest(requestId, response)
      await loadRequests()
      if (response === 'ACCEPTED') await onChanged()
    } catch (err) { setError(err.message) }
  }

  return <div className="contacts-layout">
    {requests.length > 0 && <section className="friend-request-box">
      <div><p className="section-kicker">Lời mời kết bạn</p><h3>{requests.length} người đang chờ phản hồi</h3></div>
      {requests.map((request) => <article key={request.id} className="friend-request-item">
        <div><strong>{request.requesterName}</strong><span>@{request.requesterUsername}</span></div>
        <div className="invitation-actions">
          <button className="decline" onClick={() => respond(request.id, 'DECLINED')}>Từ chối</button>
          <button className="accept" onClick={() => respond(request.id, 'ACCEPTED')}>Chấp nhận</button>
        </div>
      </article>)}
    </section>}
    <section className="management-card contact-search-card">
      <div className="contact-search-heading"><p className="section-kicker">Tìm người dùng hệ thống</p>
        <h3>Kết nối bằng tên, số điện thoại hoặc email</h3></div>
      <form className="contact-search-form" onSubmit={findUsers}>
        <div className="search-box"><Search size={18} /><input value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Ví dụ: Minh Anh, 090..., email@gmail.com" /></div>
        <button className="solid-button" disabled={busy}>{busy ? 'Đang tìm...' : 'Tìm kiếm'}</button>
      </form>
      {error && <div className="form-error">{error}</div>}
      {results.length > 0 && <div className="user-search-results">
        {results.map((user) => <article className="customer-card" key={user.id}>
          <div className="customer-avatar">{initials(user.fullName)}</div>
          <div className="customer-info"><h3>{user.fullName}</h3><p>{user.email}</p>
            <span>{user.phone || `@${user.username}`}</span></div>
          <FriendAction user={user} onSend={() => sendRequest(user.id)} />
        </article>)}
      </div>}
    </section>
    <section className="management-card">
      <div className="contact-list-heading"><p className="section-kicker">Danh bạ của bạn</p>
        <h3>{contacts.length} liên hệ</h3></div>
      {contacts.length ? <div className="customer-grid">
        {contacts.map((contact) => <CustomerCard key={`${contact.type}-${contact.id}`} user={contact} />)}
      </div> : <div className="management-empty compact">Chưa có bạn bè hoặc guest nào.</div>}
    </section>
  </div>
}

function FriendAction({ user, onSend }) {
  const labels = {
    FRIEND: 'Đã là bạn bè',
    REQUEST_SENT: 'Đã gửi lời mời',
    REQUEST_RECEIVED: 'Đang chờ bạn phản hồi',
  }
  if (user.relationshipStatus !== 'NONE') {
    return <span className="relationship-label">{labels[user.relationshipStatus]}</span>
  }
  return <button className="friend-button" onClick={onSend}><UserPlus size={15} /> Kết bạn</button>
}

function UserEditor({ onClose, onSaved }) {
  const [form, setForm] = useState({
    fullName: '', email: '', phone: '',
  })
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const submit = async (event) => {
    event.preventDefault()
    setSaving(true)
    setError('')
    try {
      await api.createGuest({
        ...form,
        fullName: form.fullName.trim(),
        email: form.email.trim(),
        phone: form.phone.trim() || null,
      })
      await onSaved()
    } catch (err) {
      setError(err.message)
    } finally {
      setSaving(false)
    }
  }
  return (
    <EditorShell title="Thêm guest" kicker="Liên hệ riêng của bạn" onClose={onClose}>
      <form onSubmit={submit}>
        <label><span>Họ và tên</span><input autoFocus value={form.fullName}
          onChange={(e) => setForm({...form, fullName: e.target.value})} maxLength={120} required /></label>
        <div className="form-row">
          <label><span>Email</span><input type="email" value={form.email}
            onChange={(e) => setForm({...form, email: e.target.value})} required /></label>
          <label><span>Số điện thoại</span><input value={form.phone}
            onChange={(e) => setForm({...form, phone: e.target.value})} maxLength={30} /></label>
        </div>
        <div className="service-summary"><UserRound size={17} />
          Guest không có tài khoản đăng nhập, chỉ xuất hiện trong Danh bạ của bạn và lịch với guest tự động được chấp nhận.
        </div>
        {error && <div className="form-error">{error}</div>}
        <EditorActions onClose={onClose} saving={saving} label="Thêm guest" />
      </form>
    </EditorShell>
  )
}

function InvitationBox({ invitations, onRespond }) {
  return <section className="invitation-box">
    <div className="invitation-heading">
      <div className="invitation-icon"><UserRound size={19} /></div>
      <div><p className="section-kicker">Cần bạn phản hồi</p><h3>{invitations.length} lời mời cuộc hẹn</h3></div>
    </div>
    <div className="invitation-list">
      {invitations.map((item) => <article className="invitation-item" key={item.id}>
        <div><strong>{item.title}</strong>
          <span>{item.organizerName} · {longDate(item.startTime.slice(0, 10))} · {formatTime(item.startTime)}–{formatTime(item.endTime)}</span>
        </div>
        <div className="invitation-actions">
          <button className="decline" onClick={() => onRespond(item.id, 'DECLINED')}>Từ chối</button>
          <button className="accept" onClick={() => onRespond(item.id, 'ACCEPTED')}>Chấp nhận</button>
        </div>
      </article>)}
    </div>
  </section>
}

function CustomerCard({ user }) {
  return <article className="customer-card"><div className="customer-avatar">{initials(user.fullName)}</div>
    <div className="customer-info"><h3>{user.fullName}
      {user.type === 'GUEST' && <small className="guest-badge">Guest</small>}</h3>
      <p>{user.email || 'Chưa có email'}</p><span>{user.phone || 'Chưa có số điện thoại'}</span></div></article>
}

function AgendaItem({ item, onEdit, onDelete }) {
  if (item.type === 'note') {
    return (
      <article className={`agenda-card agenda-note note-${item.color}`}>
        <div className="agenda-icon"><FileText size={17} /></div>
        <div><span>Ghi chú</span><h4>{item.title}</h4><p>{item.content}</p></div>
        <ItemActions onEdit={onEdit} onDelete={onDelete} />
      </article>
    )
  }
  return (
    <article className="agenda-card agenda-appointment">
      <div className="agenda-time"><strong>{formatTime(item.startTime)}</strong><span>{formatTime(item.endTime)}</span></div>
      <div className="agenda-content">
        {item.invitationStatus && <span className={`status-badge ${INVITATION[item.invitationStatus]?.className}`}>
          {INVITATION[item.invitationStatus]?.label}
        </span>}
        <h4>{item.title}</h4><p>{item.contactName ? `Với ${item.contactName}` : 'Không gắn người liên hệ'}</p>
        {item.note && <small>{item.note}</small>}
      </div>
      <ItemActions onEdit={onEdit} onDelete={onDelete} />
    </article>
  )
}

function ItemActions({ onEdit, onDelete }) {
  return <div className="item-actions">
    <button onClick={onEdit} title="Chỉnh sửa"><Pencil size={15} /></button>
    <button onClick={onDelete} title="Xóa"><Trash2 size={15} /></button>
  </div>
}

function AppointmentEditor({ contacts, date, item, onClose, onSaved }) {
  const [form, setForm] = useState({
    title: item?.title || '',
    contactKey: item?.guestId ? `GUEST:${item.guestId}`
      : item?.contactId ? `USER:${item.contactId}` : '',
    date: item?.startTime?.slice(0, 10) || date,
    endDate: item?.endTime?.slice(0, 10) || date,
    startTime: item ? formatTime(item.startTime) : '09:00',
    endTime: item ? formatTime(item.endTime) : '10:00',
    note: item?.note || '',
  })
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const submit = async (event) => {
    event.preventDefault(); setSaving(true); setError('')
    const startDateTime = new Date(`${form.date}T${form.startTime}:00`)
    if (startDateTime < new Date()) {
      setError('Không thể tạo hoặc chuyển cuộc hẹn vào thời gian trong quá khứ')
      setSaving(false)
      return
    }
    const [contactType, contactValue] = form.contactKey.split(':')
    const data = {
      title: form.title.trim(),
      contactId: contactType === 'USER' ? Number(contactValue) : null,
      guestId: contactType === 'GUEST' ? Number(contactValue) : null,
      startTime: `${form.date}T${form.startTime}:00`,
      endTime: `${form.endDate}T${form.endTime}:00`,
      note: form.note.trim() || null,
    }
    try {
      item ? await api.updateAppointment(item.id, data) : await api.createAppointment(data)
      onSaved()
    } catch (err) { setError(err.message) } finally { setSaving(false) }
  }
  const changeDate = (value) => setForm({ ...form, date: value, endDate: value })
  const changeStartTime = (value) => {
    const end = shiftDateTime(form.date, value, 1)
    setForm({ ...form, startTime: value, endTime: end.time, endDate: end.date })
  }
  const changeEndTime = (value) => {
    const start = shiftDateTime(form.endDate, value, -1)
    setForm({ ...form, date: start.date, startTime: start.time, endTime: value })
  }
  return (
    <EditorShell title={item ? 'Chỉnh sửa cuộc hẹn' : 'Tạo cuộc hẹn'} kicker="Calendar event" onClose={onClose}>
      <form onSubmit={submit}>
        <label><span>Tiêu đề</span><input value={form.title} onChange={(e) => setForm({...form, title: e.target.value})}
          placeholder="Ví dụ: Họp nhóm, khám bệnh..." maxLength={160} required /></label>
        <label><span>Người liên hệ <small>(không bắt buộc)</small></span><div className="field-with-icon"><UserRound size={17} />
          <select value={form.contactKey} onChange={(e) => setForm({...form, contactKey: e.target.value})}>
            <option value="">Không gắn người liên hệ</option>
            {contacts.map((u) => <option key={`${u.type}-${u.id}`} value={`${u.type}:${u.id}`}>
              {u.fullName}{u.type === 'GUEST' ? ' (guest)' : ''}
            </option>)}
          </select></div></label>
        <label><span>Ngày</span><input type="date" min={toLocalDate()} value={form.date} onChange={(e) => changeDate(e.target.value)} required /></label>
        <div className="form-row">
          <label><span>Bắt đầu</span><input type="time" value={form.startTime} onChange={(e) => changeStartTime(e.target.value)} required /></label>
          <label><span>Kết thúc</span><input type="time" value={form.endTime} onChange={(e) => changeEndTime(e.target.value)} required /></label>
        </div>
        {form.endDate !== form.date && <div className="service-summary"><Clock3 size={17} /> Kết thúc vào ngày {form.endDate}</div>}
        <label><span>Ghi chú</span><textarea value={form.note} onChange={(e) => setForm({...form, note: e.target.value})} maxLength={500} /></label>
        {error && <div className="form-error">{error}</div>}
        <EditorActions onClose={onClose} saving={saving} label={item ? 'Lưu thay đổi' : 'Tạo cuộc hẹn'} />
      </form>
    </EditorShell>
  )
}

function NoteEditor({ date, item, onClose, onSaved }) {
  const [form, setForm] = useState({
    title: item?.title || '', content: item?.content || '',
    noteDate: item?.noteDate || date, color: item?.color || 'yellow',
  })
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const submit = async (event) => {
    event.preventDefault(); setSaving(true); setError('')
    try {
      item ? await api.updateNote(item.id, form) : await api.createNote(form)
      onSaved()
    } catch (err) { setError(err.message) } finally { setSaving(false) }
  }
  return (
    <EditorShell title={item ? 'Chỉnh sửa ghi chú' : 'Thêm ghi chú'} kicker="Personal note" onClose={onClose}>
      <form onSubmit={submit}>
        <label><span>Tiêu đề</span><input value={form.title} onChange={(e) => setForm({...form, title: e.target.value})} maxLength={120} required /></label>
        <label><span>Ngày</span><input type="date" value={form.noteDate} onChange={(e) => setForm({...form, noteDate: e.target.value})} required /></label>
        <label><span>Nội dung</span><textarea className="note-textarea" value={form.content} onChange={(e) => setForm({...form, content: e.target.value})} maxLength={1000} required /></label>
        <label><span>Màu ghi chú</span><div className="color-picker">
          {['yellow', 'blue', 'green', 'pink'].map((color) => <button type="button" key={color}
            className={`${color} ${form.color === color ? 'active' : ''}`} onClick={() => setForm({...form, color})} />)}
        </div></label>
        {error && <div className="form-error">{error}</div>}
        <EditorActions onClose={onClose} saving={saving} label={item ? 'Lưu ghi chú' : 'Thêm ghi chú'} />
      </form>
    </EditorShell>
  )
}

function EditorShell({ title, kicker, onClose, children }) {
  return <div className="modal-backdrop" onMouseDown={onClose}><div className="modal" onMouseDown={(e) => e.stopPropagation()}>
    <div className="modal-header"><div><p className="section-kicker">{kicker}</p><h2>{title}</h2></div>
      <button className="icon-button" onClick={onClose}><X size={20} /></button></div>{children}</div></div>
}
function EditorActions({ onClose, saving, label }) {
  return <div className="modal-actions"><button type="button" className="secondary-button" onClick={onClose}>Hủy</button>
    <button type="submit" className="solid-button" disabled={saving}>{saving ? 'Đang lưu...' : label}</button></div>
}

function Sidebar({ activeView, onNavigate, mobileOpen, onClose, onLogout }) {
  return <><button className={`sidebar-backdrop ${mobileOpen ? 'visible' : ''}`} onClick={onClose} />
    <aside className={`sidebar ${mobileOpen ? 'is-open' : ''}`}>
      <div className="brand"><div className="brand-mark"><CalendarDays size={22} /></div><div><strong>Hẹn Nhé</strong><span>Calendar</span></div></div>
      <nav>
        <button className={activeView === 'calendar' ? 'active' : ''} onClick={() => onNavigate('calendar')}><LayoutDashboard size={19} /> Lịch của tôi</button>
        <button className={activeView === 'appointments' ? 'active' : ''} onClick={() => onNavigate('appointments')}><CalendarDays size={19} /> Cuộc hẹn</button>
        <button className={activeView === 'notes' ? 'active' : ''} onClick={() => onNavigate('notes')}><FileText size={19} /> Ghi chú</button>
        <button className={activeView === 'customers' ? 'active' : ''} onClick={() => onNavigate('customers')}><UsersRound size={19} /> Danh bạ</button>
      </nav>
      <div className="sidebar-note"><div className="note-icon"><Sparkles size={18} /></div><strong>Mẹo nhỏ</strong><p>Nhấp đúp vào một ngày để tạo cuộc hẹn nhanh.</p></div>
      <button className="logout-button" onClick={onLogout}><LogOut size={17} /> Đăng xuất</button>
      <div className="sidebar-footer">Phiên bản 2.0</div>
    </aside></>
}

function LoginPage({ onLogin }) {
  const [mode, setMode] = useState('login')
  const [form, setForm] = useState({
    fullName: '', email: '', phone: '', username: '', password: '',
  })
  const [show, setShow] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const submit = async (event) => {
    event.preventDefault(); setLoading(true); setError('')
    try {
      const session = mode === 'login'
        ? await api.login({ username: form.username, password: form.password })
        : await api.register({
          fullName: form.fullName.trim(),
          email: form.email.trim(),
          phone: form.phone.trim() || null,
          username: form.username.trim(),
          password: form.password,
        })
      onLogin(session)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }
  const switchMode = (next) => {
    setMode(next)
    setError('')
  }
  return <main className="login-page"><section className="login-visual">
    <div className="login-brand"><div className="brand-mark"><CalendarDays size={22} /></div>
      <div><strong>Hẹn Nhé</strong><span>Calendar</span></div></div>
    <div className="login-message"><span className="hero-pill"><Sparkles size={14} /> Quản lý nhẹ nhàng</span>
      <h1>Mỗi ngày rõ ràng,<br />mọi việc đúng hẹn.</h1>
      <p>Lịch tháng trực quan cho cuộc hẹn và ghi chú cá nhân.</p></div><div className="login-orbit" />
  </section><section className="login-panel"><div className="login-card">
    <div className="auth-tabs">
      <button className={mode === 'login' ? 'active' : ''} onClick={() => switchMode('login')}>Đăng nhập</button>
      <button className={mode === 'register' ? 'active' : ''} onClick={() => switchMode('register')}>Đăng ký</button>
    </div>
    <div className="login-lock">{mode === 'login' ? <LockKeyhole size={22} /> : <UserPlus size={22} />}</div>
    <p className="section-kicker">{mode === 'login' ? 'Chào mừng trở lại' : 'Tài khoản mới'}</p>
    <h2>{mode === 'login' ? 'Đăng nhập hệ thống' : 'Đăng ký tài khoản'}</h2>
    <p className="login-subtitle">{mode === 'login'
      ? 'Dùng tài khoản của bạn để mở calendar.'
      : 'Đăng ký xong bạn sẽ được đăng nhập ngay.'}</p>
    <form onSubmit={submit}>
      {mode === 'register' && <>
        <label><span>Họ và tên</span><input autoFocus value={form.fullName}
          onChange={(e) => setForm({...form, fullName: e.target.value})} maxLength={120} required /></label>
        <div className="form-row auth-form-row">
          <label><span>Email</span><input type="email" value={form.email}
            onChange={(e) => setForm({...form, email: e.target.value})} required /></label>
          <label><span>Số điện thoại</span><input value={form.phone}
            onChange={(e) => setForm({...form, phone: e.target.value})} maxLength={30} /></label>
        </div>
      </>}
      <label><span>Username</span><input autoFocus={mode === 'login'} value={form.username}
        onChange={(e) => setForm({...form, username: e.target.value})}
        pattern="[A-Za-z0-9]+" minLength={4} maxLength={50} required /></label>
      <label><span>Mật khẩu</span><div className="password-field"><input
        type={show ? 'text' : 'password'} value={form.password}
        onChange={(e) => setForm({...form, password: e.target.value})} minLength={8} required />
        <button type="button" onClick={() => setShow(!show)}>
          {show ? <EyeOff size={18} /> : <Eye size={18} />}</button></div></label>
      {mode === 'register' && <small className="password-hint">
        Username chỉ gồm chữ và số. Mật khẩu cần ít nhất 8 ký tự, 1 chữ hoa và 1 ký tự đặc biệt.
      </small>}
      {error && <div className="form-error">{error}</div>}
      <button className="login-button" disabled={loading}>
        {loading ? 'Đang xử lý...' : mode === 'login' ? 'Đăng nhập' : 'Tạo tài khoản'}
      </button>
    </form>
    {mode === 'login' && <div className="demo-account"><strong>Tài khoản dùng thử</strong>
      <span><code>minhanh</code> / <code>MinhAnh@123</code></span></div>}
  </div></section></main>
}

function calendarGrid(cursor) {
  const first = new Date(cursor.getFullYear(), cursor.getMonth(), 1)
  const mondayOffset = (first.getDay() + 6) % 7
  const start = new Date(first)
  start.setDate(first.getDate() - mondayOffset)
  return Array.from({ length: 42 }, (_, index) => {
    const date = new Date(start)
    date.setDate(start.getDate() + index)
    return { date: toLocalDate(date), inMonth: date.getMonth() === cursor.getMonth() }
  })
}
function shiftDateTime(date, time, hours) {
  const value = new Date(`${date}T${time}:00`)
  value.setHours(value.getHours() + hours)
  return { date: toLocalDate(value), time: value.toTimeString().slice(0, 5) }
}
function viewFromHash() {
  const value = window.location.hash.replace('#', '')
  return ['calendar', 'appointments', 'notes', 'customers'].includes(value) ? value : 'calendar'
}
function viewMeta(view) {
  return {
    calendar: { eyebrow: 'Lịch cá nhân', title: 'Lịch của tôi' },
    appointments: { eyebrow: 'Quản lý lịch hẹn', title: 'Cuộc hẹn' },
    notes: { eyebrow: 'Ghi chú cá nhân', title: 'Ghi chú' },
    customers: { eyebrow: 'Người liên hệ', title: 'Danh bạ' },
  }[view]
}
function initials(name = '') {
  const parts = name.trim().split(/\s+/)
  return `${parts[0]?.[0] || ''}${parts.at(-1)?.[0] || ''}`.toUpperCase()
}
function invitationClass(item) {
  return item.invitationStatus ? INVITATION[item.invitationStatus]?.className : 'scheduled'
}

export default App
