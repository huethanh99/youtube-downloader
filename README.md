# Youtube Downloader GUI

Một ứng dụng tải video YouTube đơn giản, trực quan (GUI) được xây dựng bằng Python.

## Lời Tri Ân (Special Thanks) ❤️

Ứng dụng này sẽ không thể tồn tại nếu không có bộ lõi xử lý tuyệt vời từ dự án [yt-dlp](https://github.com/yt-dlp/yt-dlp). 

Tôi xin gửi lời cảm ơn sâu sắc đến đội ngũ phát triển `yt-dlp` cùng cộng đồng mã nguồn mở đã ngày đêm duy trì và tạo ra công cụ dòng lệnh tải video mạnh mẽ nhất thế giới. Dự án này tôn trọng, kế thừa trọn vẹn sức mạnh xử lý của `yt-dlp` gốc, và chỉ đóng góp thêm một lớp giao diện đồ họa (GUI) nhằm giúp những người dùng không chuyên về kỹ thuật cũng có thể dễ dàng tiếp cận và sử dụng công cụ tuyệt vời này.

---

## Các Tính năng Chính
- **Tải Playlist thông minh:** Hỗ trợ tải toàn bộ danh sách phát. Tự động lướt qua các video bị lỗi (như lỗi 500) hoặc các video đã tải rồi để tiếp tục quá trình tải mà không bị gián đoạn.
- **Tải Video & Âm thanh:** Lựa chọn linh hoạt tải Video (có thể chọn độ phân giải tối đa lên tới 1080p, 4K) hoặc chỉ tải Âm thanh (Audio mp3 chất lượng cao).
- **Tự động nhúng Phụ đề:** Có tùy chọn tự động tải và nhúng thẳng phụ đề (Việt/Anh) vào video.
- **Dễ sử dụng:** Đã được đóng gói sẵn thành file cài đặt `.exe` dành cho Windows, không cần cài đặt Python, FFmpeg hay gõ lệnh phức tạp.

## Hướng dẫn cài đặt
1. **[Tải bộ cài đặt youtube-downloader-setup.exe tại đây](dist/youtube-downloader-setup.exe)** (hoặc tự truy cập vào thư mục `dist` của mã nguồn để tải).
2. Chạy file cài đặt, ứng dụng sẽ tự động sao chép các tệp cần thiết (bao gồm cả FFmpeg) vào máy bạn.
3. Mở ứng dụng từ Desktop, dán đường dẫn (link) video hoặc playlist và bấm tải.

## Giấy phép (License)
Dự án này kế thừa tinh thần mã nguồn mở tự do tuyệt đối và được phát hành dưới giấy phép **[The Unlicense](http://unlicense.org/)** (Tài sản công cộng), hoàn toàn giống với dự án yt-dlp gốc. Bạn có toàn quyền sử dụng, chỉnh sửa và phân phối lại.
