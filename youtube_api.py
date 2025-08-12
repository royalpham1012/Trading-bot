import googleapiclient.discovery
from datetime import datetime, timedelta
import time

# API Key của bạn
API_KEY = 'AIzaSyAIfRfMhFCFVCF-hC3qlVU5RFsnib0jNYw'

# Xây dựng service YouTube API
youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=API_KEY)

# Hàm lấy channel ID từ handle (@username)
def get_channel_id(handle):
    request = youtube.channels().list(
        part='id',
        forHandle=handle
    )
    response = request.execute()
    if 'items' in response and len(response['items']) > 0:
        return response['items'][0]['id']
    else:
        print(f"Không tìm thấy channel cho handle: {handle}")
        return None

# Hàm lấy danh sách video/stream từ channel
def get_videos(channel_id, start_date, handle, is_streams=False):
    videos = []
    page_token = None
    published_after = start_date.isoformat() + 'Z'  # Định dạng ISO cho API

    while True:
        params = {
            'part': 'snippet',
            'channelId': channel_id,
            'order': 'date',  # Sắp xếp theo ngày, mới nhất trước
            'type': 'video',
            'publishedAfter': published_after,
            'maxResults': 50,
            'pageToken': page_token
        }
        if is_streams:
            params['eventType'] = 'completed'  # Chỉ lấy completed live streams cho tab /streams

        request = youtube.search().list(**params)
        response = request.execute()

        for item in response.get('items', []):
            title = item['snippet']['title']
            publish_date_str = item['snippet']['publishedAt']  # ISO format
            video_id = item['id']['videoId']
            link = f"https://www.youtube.com/watch?v={video_id}"
            videos.append((publish_date_str, title, link, handle))  # Thêm handle làm nguồn

        page_token = response.get('nextPageToken')
        if not page_token:
            break

    return videos

# Danh sách nguồn
sources = [
    {'handle': 'SeanLe714', 'is_streams': True},  # Từ /streams
    {'handle': 'rfavietnamese', 'is_streams': False},  # Từ /videos
    # Thêm nguồn khác nếu cần, ví dụ: {'handle': 'anotherhandle', 'is_streams': False}
]

# Vòng lặp quét mỗi 4 tiếng
while True:
    # Tính ngày bắt đầu: 3 ngày trước
    date_threshold = datetime.now() - timedelta(days=3)

    # Thu thập tất cả video
    all_videos = []
    for source in sources:
        channel_id = get_channel_id(source['handle'])
        if channel_id:
            videos = get_videos(channel_id, date_threshold, source['handle'], source['is_streams'])
            all_videos.extend(videos)

    # Sắp xếp lại toàn bộ theo ngày descending (mới nhất trước)
    all_videos.sort(key=lambda x: datetime.fromisoformat(x[0].replace('Z', '+00:00')), reverse=True)

    # In ra màn hình
    print(f"Quét lúc: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if all_videos:
        for date_str, title, link, handle in all_videos:
            date = datetime.fromisoformat(date_str.replace('Z', '+00:00')).strftime('%Y-%m-%d')
            print(f"Title: {title}")
            print(f"Date: {date}")
            print(f"Link: {link}")
            print(f"Source: {handle}")
            print()
    else:
        print("Không có video mới trong 3 ngày qua.")
    print("--- Kết thúc quét ---")

    # Lưu vào file TXT (overwrite mỗi lần để chỉ giữ dữ liệu mới nhất)
    with open('youtube_videos.txt', 'w', encoding='utf-8') as f:
        f.write(f"Quét lúc: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        if all_videos:
            for date_str, title, link, handle in all_videos:
                # Chuyển ISO sang YYYY-MM-DD
                date = datetime.fromisoformat(date_str.replace('Z', '+00:00')).strftime('%Y-%m-%d')
                f.write(f"Title: {title}\nDate: {date}\nLink: {link}\nSource: {handle}\n\n")
        else:
            f.write("Không có video mới trong 3 ngày qua.\n")

    # Chờ 4 tiếng (14400 giây)
    time.sleep(14400)
