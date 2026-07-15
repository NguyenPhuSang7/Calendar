# Báo Cáo Tóm Tắt Selenium PyTest Automation Suite

Tài liệu này tóm tắt thông tin chi tiết về bộ kiểm thử tự động (Test Automation Suite) được phát triển bằng **Selenium WebDriver** và **PyTest** cho dự án **"Hẹn Nhé - Calendar & Appointment Manager"**.

---

## 🛠️ Công Cụ Kiểm Thử (Testing Tools)

| Công cụ / Thư viện | Phiên bản | Vai trò trong dự án |
| :--- | :--- | :--- |
| **Python** | 3.14.6 | Ngôn ngữ lập trình chính để phát triển bộ kịch bản kiểm thử. |
| **PyTest** | 9.1.1 | Testing Framework chính giúp tổ chức, quản lý và thực thi các ca kiểm thử. |
| **Selenium WebDriver** | 4.x | Thư viện tự động hóa tương tác trực tiếp với các phần tử DOM trên trình duyệt. |
| **Chrome / ChromeDriver** | 126+ | Trình duyệt thực tế dùng để chạy kiểm thử trong chế độ đồ họa/không đầu (headless). |
| **WebDriver Manager** | 4.x | Tự động tải xuống, cấu hình và quản lý các phiên bản driver phù hợp cho Chrome và Firefox. |
| **Docker** | 24+ | Khởi chạy môi trường ứng dụng (Frontend, Backend, Postgres Database). |

---

## 📋 Tóm Tắt Các File Kiểm Thử (Test Files Summary)

Bộ kịch bản kiểm thử được tổ chức theo mô hình **Page Object Model (POM)** chia thành 5 file test chính ứng với các module nghiệp vụ của ứng dụng:

### 1. `test_auth.py` (Authentication & Security)
Chứa các ca kiểm thử liên quan đến cơ chế đăng ký tài khoản, đăng nhập hệ thống và các ràng buộc dữ liệu bảo mật ở phía client và server.
* **TC-AUTH-01 (Valid Registration)**: Đăng ký tài khoản hợp lệ, tự động sinh JWT token và chuyển hướng tới Dashboard thành công.
* **TC-AUTH-02 (Invalid Username Space)**: Kiểm tra ràng buộc HTML5 ở phía client, ngăn chặn các tài khoản chứa khoảng trắng.
* **TC-AUTH-03 (Weak Password)**: Gửi mật khẩu yếu (lacking uppercase/special chars) và kiểm tra lỗi kiểm định dữ liệu từ Backend.
* **TC-AUTH-04 (Duplicate Account)**: Đăng ký hai tài khoản trùng tên/email, hệ thống trả về thông báo lỗi dạng 409 Conflict.
* **TC-AUTH-05 (Login Flow)**: Xác nhận đăng nhập thành công với thông tin đúng và báo lỗi hiển thị chính xác khi thông tin sai.

### 2. `test_calendar.py` (Calendar Grid & Responsive UI)
Kiểm tra khả năng hiển thị lưới lịch tháng, bảng thông tin chi tiết ngày và kiểm định tính đáp ứng giao diện trên nhiều độ phân giải khác nhau.
* **TC-UI-01 (View Monthly Calendar)**: Lưới lịch 35/42 ngày hiển thị đầy đủ, tiêu đề tháng năm chính xác, đồng bộ hóa khi chuyển tháng.
* **TC-UI-02 (Responsive Desktop - 1440px)**: Xác thực bố cục lớn hiển thị sidebar menu cố định bên trái mà không bị đè lên tiêu đề.
* **TC-UI-03 (Responsive Tablet - 768px)**: Sidebar tự động ẩn sang chế độ rút gọn (collapsible), kích hoạt nút hamburger menu độc lập.
* **TC-UI-04 (Responsive Mobile - 390px)**: Tiêu đề sidebar ẩn hẳn, nội dung giao diện co giãn hợp lý và các icon hành động không bị đè lệch.

### 3. `test_contacts.py` (Contacts & Friendship)
Đảm bảo các tương tác xã hội giữa người dùng hệ thống và việc quản lý danh sách liên hệ khách (guest) hoạt động chính xác.
* **TC-FRD-01 (Search & Request Friend)**: Tìm kiếm người dùng bằng email/username, gửi lời mời kết bạn và hiển thị trạng thái `"Đã gửi lời mời"`.
* **TC-FRD-04 (Accept Request)**: Người nhận chấp nhận lời mời, chuyển đổi trạng thái thành `"Bạn bè"` hai chiều tức thời.
* **TC-FRD-05 (Decline Request)**: Từ chối lời mời kết bạn, trả quan hệ về trạng thái `"Kết bạn"` ban đầu.
* **TC-GST-01 (Guest & Privacy)**: Tạo liên hệ khách (guest) và xác thực tính riêng tư (chỉ người tạo mới nhìn thấy thông tin khách trong danh bạ).

### 4. `test_notes.py` (Personal Notes)
Kiểm tra khả năng tạo, sửa, xóa các ghi chú nhanh cá nhân được đính kèm vào các ô ngày trên lịch.
* **TC-NOTE-01 (Past Notes)**: Tạo thành công ghi chú tại một mốc thời gian trong quá khứ.
* **TC-NOTE-02 (Edit & Delete Notes)**: Chỉnh sửa tiêu đề/nội dung ghi chú và kiểm tra việc xóa ghi chú đồng bộ hóa lập tức trên giao diện.
* **TC-NOTE-03 (Note Isolation)**: Kiểm tra bảo mật giữa các tài khoản, ghi chú của User A tuyệt đối không hiển thị ở tài khoản User B.

### 5. `test_appointment.py` (Appointments & Invitations)
Kiểm tra quy trình tạo lịch hẹn cá nhân, lịch hẹn nhóm (gửi lời mời) và các quy tắc kiểm định thời gian.
* **TC-APT-01 (Personal Appointment)**: Tạo cuộc hẹn cá nhân không có khách mời, hiển thị chính xác trên Agenda.
* **TC-APT-02 (Past Date Block)**: Hệ thống ngăn chặn việc tạo lịch hẹn ở mốc thời gian đã qua trong quá khứ.
* **TC-APT-03 (Invalid Time Range)**: Xác nhận backend từ chối cuộc hẹn có thời gian kết thúc trước thời gian bắt đầu.
* **TC-APT-04 (Auto time offset)**: UI tự động điều chỉnh thời gian kết thúc lệch 1 tiếng so với giờ bắt đầu được thiết lập.
* **TC-APT-11 (CRUD & Authorization)**: Chủ sở hữu có toàn quyền sửa/xóa cuộc hẹn, người được mời chỉ được phép phản hồi trạng thái.
* **TC-APT-07 (Invitation Workflow)**: Luồng gửi lời mời hẹn tới bạn bè, bạn bè chấp nhận/từ chối và đồng bộ hóa trạng thái trên lịch của cả hai bên.

---

## 📈 Kết Quả Thực Thi Thành Công (Test Results)

Tất cả **23 ca kiểm thử** được tích hợp đầy đủ các hàm đợi đồng bộ hóa DOM (`wait_for_dashboard_load`, `wait_for_friend_request_status`, `wait_for_note_to_disappear`), đã vượt qua kiểm thử thành công trên môi trường localhost.

```bash
======================= 23 passed in 292.73s (0:04:52) ========================
```

---

## 📸 Cơ Chế Ghi Nhận Lỗi (Screenshot on Failure)
Để phục vụ quá trình gỡ lỗi dễ dàng, bộ kiểm thử được cấu hình thêm một hook PyTest đặc biệt trong `conftest.py`:
* Khi bất kỳ ca kiểm thử nào gặp lỗi (`AssertionError` hoặc `TimeoutException`), hệ thống sẽ tự động chụp màn hình trạng thái trình duyệt tại thời điểm đó và lưu vào thư mục `testing/selenium_pytest/screenshots/` với tên file là tên hàm test tương ứng (ví dụ: `test_accept_friend_request.png`).
