# Hẹn Nhé - Calendar & Appointment Manager

Ứng dụng quản lý lịch hẹn quy mô nhỏ, tập trung vào nghiệp vụ calendar, ghi chú cá nhân, danh bạ, kết bạn và xác nhận cuộc hẹn.

## Tính năng

- Đăng ký và đăng nhập bằng JWT.
- Username chỉ gồm chữ và số, không có khoảng trắng hoặc ký tự đặc biệt.
- Mật khẩu tối thiểu 8 ký tự, có ít nhất 1 chữ hoa và 1 ký tự đặc biệt.
- Calendar tháng responsive cho desktop, tablet và mobile.
- Tạo, chỉnh sửa, xóa cuộc hẹn; không cho phép tạo lịch trong quá khứ.
- Khi đổi giờ bắt đầu, giờ kết thúc tự tăng 1 giờ và ngược lại.
- Tạo ghi chú cho cả ngày trong quá khứ hoặc tương lai.
- Tìm user theo tên, email hoặc số điện thoại và gửi lời mời kết bạn.
- User chỉ xuất hiện trong Danh bạ sau khi lời mời kết bạn được chấp nhận.
- Guest là liên hệ riêng, chỉ người tạo nhìn thấy và không có tài khoản đăng nhập.
- Lịch với guest tự động `ACCEPTED`.
- Lịch với user thật tạo lời mời `PENDING`; người được mời có thể chấp nhận hoặc từ chối.
- Lịch và ghi chú được giới hạn theo tài khoản liên quan.
- Swagger/OpenAPI cho backend.
- Mật khẩu được mã hóa bằng BCrypt.

## Tech stack

- Backend: Java 17, Spring Boot 3.3.5, Spring Security, Spring Data JPA.
- Database: PostgreSQL 16.
- API docs: Springdoc OpenAPI / Swagger UI.
- Frontend: React 18, Vite 5, Lucide React.
- Deployment local: Docker Compose, Nginx.
- Tests: JUnit 5, Spring Boot Test, H2.

## Yêu cầu

### Cách 1: Chạy bằng Docker (khuyến nghị)

- Git 2.x.
- Docker Desktop mới, có Docker Compose V2.
- Windows 10/11, macOS hoặc Linux.
- Tối thiểu khoảng 2 GB RAM trống cho Docker.

Không cần cài Java, Maven, Node.js hay PostgreSQL nếu chạy hoàn toàn bằng Docker.

### Cách 2: Chạy thủ công để phát triển

- Java JDK 17.
- Maven 3.9+.
- Node.js 20+ và npm 10+.
- PostgreSQL 16.

## Cài đặt bằng Docker

### 1. Clone repository

```bash
git clone https://github.com/NguyenPhuSang7/Calendar.git
cd Calendar
```

### 2. Cấu hình môi trường

Project có giá trị mặc định để chạy local ngay. Để đổi mật khẩu database hoặc JWT secret:

```powershell
# Windows PowerShell
Copy-Item .env.example .env
```

```bash
# macOS / Linux
cp .env.example .env
```

Mở `.env` và thay ít nhất:

```dotenv
POSTGRES_PASSWORD=your-local-database-password
APP_JWT_SECRET=your-random-secret-at-least-32-characters
```

Không commit file `.env`.

### 3. Khởi động

Đảm bảo Docker Desktop đang chạy, sau đó:

```bash
docker compose up -d --build
```

Lần chạy đầu cần tải image và build source nên có thể mất vài phút.

### 4. Truy cập

| Thành phần | URL |
| --- | --- |
| Web application | http://localhost:3000 |
| Swagger UI | http://localhost:8080/swagger-ui.html |
| OpenAPI JSON | http://localhost:8080/v3/api-docs |
| PostgreSQL | `localhost:5432` |

Kiểm tra container:

```bash
docker compose ps
```

Xem log:

```bash
docker compose logs -f
```

Tắt hệ thống nhưng giữ dữ liệu:

```bash
docker compose down
```

Tắt và xóa toàn bộ database local:

```bash
docker compose down -v
```

## Tài khoản demo

Các tài khoản sau được tạo tự động khi database chưa có user:

| Username | Password | Họ tên |
| --- | --- | --- |
| `minhanh` | `MinhAnh@123` | Nguyễn Minh Anh |
| `hoangnam` | `HoangNam@123` | Trần Hoàng Nam |
| `thaovy` | `ThaoVy@123` | Lê Thảo Vy |
| `giahan` | `GiaHan@123` | Phạm Gia Hân |

Người dùng cũng có thể đăng ký tài khoản mới ở trang đăng nhập.

## Chạy thủ công

### 1. Tạo PostgreSQL database

Ví dụ:

```sql
CREATE DATABASE appointment_db;
CREATE USER appointment WITH PASSWORD 'appointment';
GRANT ALL PRIVILEGES ON DATABASE appointment_db TO appointment;
```

Đặt biến môi trường phù hợp với hệ điều hành:

```powershell
# Windows PowerShell
$env:SPRING_DATASOURCE_URL="jdbc:postgresql://localhost:5432/appointment_db"
$env:SPRING_DATASOURCE_USERNAME="appointment"
$env:SPRING_DATASOURCE_PASSWORD="appointment"
$env:APP_JWT_SECRET="replace-with-a-random-secret-at-least-32-characters"
```

```bash
# macOS / Linux
export SPRING_DATASOURCE_URL="jdbc:postgresql://localhost:5432/appointment_db"
export SPRING_DATASOURCE_USERNAME="appointment"
export SPRING_DATASOURCE_PASSWORD="appointment"
export APP_JWT_SECRET="replace-with-a-random-secret-at-least-32-characters"
```

### 2. Chạy backend

```bash
cd backend
mvn spring-boot:run
```

Backend chạy tại http://localhost:8080.

### 3. Chạy frontend

Mở terminal khác:

```bash
cd frontend
npm install
npm run dev
```

Frontend development chạy tại http://localhost:5173 và proxy `/api` sang backend tại cổng `8080`.

## Chạy test và build

### 1. Backend
Chạy unit test và tạo gói jar:
```bash
cd backend
mvn clean test
mvn clean package
```

### 2. Frontend
Cài đặt thư viện và build gói production:
```bash
cd frontend
npm install
npm run build
```

### 3. E2E Test Suite (Selenium + PyTest)
Mã kiểm thử tự động toàn diện tích hợp lưu ảnh chụp màn hình tự động khi gặp lỗi.
Yêu cầu: Python 3.10+, Google Chrome cài đặt trên máy.

Cấu hình môi trường ảo và chạy:
```bash
cd testing/selenium_pytest
python -m venv venv
# Kích hoạt môi trường ảo:
# Windows PowerShell: .\venv\Scripts\Activate.ps1 (hoặc CMD: .\venv\Scripts\activate)
# macOS / Linux: source venv/bin/activate

pip install -r requirements.txt
pytest -v
```

Kiểm tra toàn bộ project bằng Docker:
```bash
docker compose build backend frontend
```

## Biến môi trường

| Biến | Mặc định local | Ý nghĩa |
| --- | --- | --- |
| `POSTGRES_DB` | `appointment_db` | Tên database |
| `POSTGRES_USER` | `appointment` | User PostgreSQL |
| `POSTGRES_PASSWORD` | `appointment` | Password PostgreSQL local |
| `SPRING_DATASOURCE_URL` | `jdbc:postgresql://localhost:5432/appointment_db` | JDBC URL khi chạy backend thủ công |
| `SPRING_DATASOURCE_USERNAME` | `appointment` | JDBC username |
| `SPRING_DATASOURCE_PASSWORD` | `appointment` | JDBC password |
| `APP_JWT_SECRET` | Development secret | Khóa ký JWT, cần đổi khi deploy |
| `APP_JWT_EXPIRATION_HOURS` | `8` | Thời hạn JWT |
| `APP_CORS_ALLOWED_ORIGINS` | `http://localhost:5173,http://localhost:3000` | Danh sách origin được phép |

## Nghiệp vụ danh bạ

### User thật

1. User A tìm User B theo tên, email hoặc số điện thoại.
2. User A gửi lời mời kết bạn.
3. User B chấp nhận hoặc từ chối.
4. Chỉ sau khi chấp nhận, hai bên mới xuất hiện trong Danh bạ của nhau.
5. Tạo lịch với user thật sẽ cần người đó xác nhận.

### Guest

1. Một user tạo guest trong Danh bạ của mình.
2. Guest không có username/password và không thể đăng nhập.
3. Guest chỉ hiển thị với user đã tạo.
4. Lịch với guest được xem là đã chấp nhận ngay vì guest không thể phản hồi trong hệ thống.

## API chính

| Method | Endpoint | Mô tả |
| --- | --- | --- |
| `POST` | `/api/auth/register` | Đăng ký tài khoản |
| `POST` | `/api/auth/login` | Đăng nhập và nhận JWT |
| `GET` | `/api/contacts` | Danh bạ của user hiện tại |
| `POST` | `/api/guests` | Tạo guest riêng |
| `GET` | `/api/users/search?q=...` | Tìm user |
| `GET` | `/api/friend-requests` | Lời mời kết bạn đang chờ |
| `POST` | `/api/friend-requests/{userId}` | Gửi lời mời kết bạn |
| `PATCH` | `/api/friend-requests/{requestId}` | Phản hồi lời mời kết bạn |
| `GET` | `/api/appointments` | Lấy lịch theo ngày hoặc khoảng ngày |
| `POST` | `/api/appointments` | Tạo cuộc hẹn |
| `PUT` | `/api/appointments/{id}` | Chỉnh sửa cuộc hẹn |
| `DELETE` | `/api/appointments/{id}` | Xóa cuộc hẹn |
| `GET` | `/api/appointments/invitations` | Lời mời lịch đang chờ |
| `PATCH` | `/api/appointments/{id}/invitation` | Phản hồi lời mời lịch |
| `GET` | `/api/notes` | Lấy ghi chú theo khoảng ngày |
| `POST` | `/api/notes` | Tạo ghi chú |
| `PUT` | `/api/notes/{id}` | Chỉnh sửa ghi chú |
| `DELETE` | `/api/notes/{id}` | Xóa ghi chú |

Với Swagger, gọi `/api/auth/login`, lấy trường `token`, sau đó bấm **Authorize** và nhập token.

## Cấu trúc repository

```text
Calendar/
|-- backend/              Spring Boot API và automated tests
|-- frontend/             React/Vite application
|-- .env.example          Mẫu biến môi trường
|-- docker-compose.yml    PostgreSQL, backend và frontend
`-- README.md
```

## Lưu ý production

- Thay toàn bộ password mặc định và `APP_JWT_SECRET`.
- Chỉ cho phép CORS từ domain frontend thật.
- Không public trực tiếp cổng PostgreSQL.
- Dùng HTTPS và reverse proxy.
- Thay `ddl-auto: update` bằng Flyway hoặc Liquibase migration.
- Cân nhắc phân trang/rate limit cho tìm kiếm user.
- Thiết lập backup PostgreSQL định kỳ.

## License

Project được phát hành theo [MIT License](LICENSE).
