#!/usr/bin/env python3
"""
Client04.py - 2507302045 - Quản lý cấu hình trading bot từ xa
Chạy trên Android (Termux) để thay đổi cấu hình database
"""

import requests
import json
import os
import sys
import time
import threading
from datetime import datetime

# Cấu hình
SERVER_URL = "https://2e06c59cde61.ngrok-free.app"  # Ngrok URL
TIMEOUT = 10

class ConfigManager:
    def __init__(self, server_url):
        self.server_url = server_url
        self.session = requests.Session()
        self.session.timeout = TIMEOUT
    
    def test_connection(self):
        """Test kết nối đến server"""
        try:
            response = self.session.get(f"{self.server_url}/api/health")
            if response.status_code == 200:
                data = response.json()
                return data.get('status') == 'healthy'
            return False
        except Exception as e:
            print(f"❌ Lỗi kết nối: {e}")
            return False
    
    def get_all_config(self):
        """Lấy toàn bộ cấu hình"""
        try:
            response = self.session.get(f"{self.server_url}/api/config")
            if response.status_code == 200:
                return response.json()['config']
            else:
                print(f"❌ Lỗi HTTP: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            return None
    
    def update_setting(self, key, value):
        """Cập nhật setting"""
        try:
            data = {'key': key, 'value': value}
            response = self.session.put(f"{self.server_url}/api/config/settings", json=data)
            if response.status_code == 200:
                result = response.json()
                return result.get('success', False)
            return False
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            return False
    
    def update_strategy(self, strategy_name, strategy_type):
        """Cập nhật strategy"""
        try:
            data = {'strategy_name': strategy_name, 'strategy_type': strategy_type}
            response = self.session.put(f"{self.server_url}/api/config/strategies", json=data)
            if response.status_code == 200:
                result = response.json()
                return result.get('success', False)
            return False
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            return False
    
    def update_strategy_config(self, strategy_name, symbol, volume, stop_loss, take_profit, timeframe):
        """Cập nhật strategy config"""
        try:
            data = {
                'strategy_name': strategy_name,
                'symbol': symbol,
                'volume': volume,
                'stop_loss': stop_loss,
                'take_profit': take_profit,
                'timeframe': timeframe
            }
            response = self.session.put(f"{self.server_url}/api/config/strategy-config", json=data)
            if response.status_code == 200:
                result = response.json()
                return result.get('success', False)
            return False
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            return False
    
    def update_test_setting(self, key, value):
        """Cập nhật test setting"""
        try:
            data = {'key': key, 'value': value}
            response = self.session.put(f"{self.server_url}/api/config/test-settings", json=data)
            if response.status_code == 200:
                result = response.json()
                return result.get('success', False)
            return False
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            return False
    
    def refresh_bot(self):
        """Gửi lệnh refresh bot"""
        try:
            response = self.session.post(f"{self.server_url}/api/refresh-bot")
            if response.status_code == 200:
                result = response.json()
                return True, result.get('message', 'Refresh bot thành công')
            else:
                error_data = response.json()
                return False, error_data.get('message', 'Lỗi không xác định')
        except Exception as e:
            return False, f"Lỗi kết nối: {e}"
    
    def get_mt5_account_info(self):
        """Lấy thông tin tài khoản MT5"""
        try:
            response = self.session.get(f"{self.server_url}/api/mt5-account-info")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Lỗi HTTP: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            return None
    
    def get_config_info(self):
        """Lấy thông tin cấu hình từ server"""
        try:
            response = self.session.get(f"{self.server_url}/api/config")
            if response.status_code == 200:
                data = response.json()
                return data.get('config', {}).get('settings', {})
            else:
                print(f"❌ Lỗi HTTP: {response.status_code}")
                return {}
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            return {}

def clear_screen():
    """Xóa màn hình"""
    os.system('clear' if os.name == 'posix' else 'cls')

def show_header():
    """Hiển thị header"""
    print("=" * 60)
    print("🤖 QUẢN LÝ CẤU HÌNH TRADING BOT")
    print("=" * 60)
    print(f"📡 Server: {SERVER_URL}")
    print(f"⏰ Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)

def show_mt5_account_info(config_manager):
    """Hiển thị thông tin tài khoản MT5 với cập nhật realtime"""
    # Biến để kiểm soát vòng lặp
    stop_updating = False
    update_count = 0
    
    def check_for_enter():
        """Thread để kiểm tra phím Enter"""
        nonlocal stop_updating
        input("Nhấn Enter để dừng cập nhật...")
        stop_updating = True
    
    # Bắt đầu thread kiểm tra phím Enter
    enter_thread = threading.Thread(target=check_for_enter, daemon=True)
    enter_thread.start()
    
    print("🔄 Bắt đầu cập nhật realtime mỗi 30 giây...")
    time.sleep(0.5)
    
    while not stop_updating:
        try:
            update_count += 1
            
            # Xóa màn hình và hiển thị header
            clear_screen()
            print("=" * 60)
            print("🤖 QUẢN LÝ CẤU HÌNH TRADING BOT")
            print("=" * 60)
            print(f"📡 Server: {SERVER_URL}")
            print(f"⏰ Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("-" * 60)
            print("💰 THÔNG TIN TÀI KHOẢN MT5 (REALTIME)")
            print("=" * 60)
            
            # Hiển thị trạng thái cập nhật
            loading_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
            loading_char = loading_chars[update_count % len(loading_chars)]
            print(f"{loading_char} Đang cập nhật... (Lần thứ {update_count})")
            
            # Lấy thông tin tài khoản MT5
            account_info = config_manager.get_mt5_account_info()
            if not account_info:
                print("❌ Không thể lấy thông tin tài khoản MT5")
                print("Có thể do:")
                print("  - Bot chưa khởi động")
                print("  - MT5 chưa kết nối")
                print("  - Server không hỗ trợ API này")
                print("\n🔄 Đang thử lại...")
                time.sleep(3)
                continue
            
            # Hiển thị thông tin tài khoản
            if 'account' in account_info:
                account = account_info['account']
                print("\n📊 THÔNG TIN TÀI KHOẢN:")
                print(f"  🆔 Login: {account.get('login', 'N/A')}")
                print(f"  🏦 Server: {account.get('server', 'N/A')}")
                print(f"  💰 Balance: ${account.get('balance', 0):,.2f}")
                print(f"  💵 Equity: ${account.get('equity', 0):,.2f}")
                print(f"  📈 Profit: ${account.get('profit', 0):,.2f}")
                print(f"  💳 Margin: ${account.get('margin', 0):,.2f}")
                print(f"  🔒 Free Margin: ${account.get('free_margin', 0):,.2f}")
                print(f"  📊 Margin Level: {account.get('margin_level', 0):,.2f}%")
                print(f"  🎯 Currency: {account.get('currency', 'N/A')}")
            
            # Hiển thị các lệnh đang mở
            if 'positions' in account_info:
                positions = account_info['positions']
                print(f"\n📋 LỆNH ĐANG MỞ ({len(positions)} lệnh):")
                if positions:
                    print(f"{'Ticket':<10} {'Symbol':<10} {'Type':<6} {'Volume':<8} {'Price':<10} {'Profit':<12} {'Comment':<15}")
                    print("-" * 80)
                    for pos in positions:
                        ticket = pos.get('ticket', 'N/A')
                        symbol = pos.get('symbol', 'N/A')
                        pos_type = 'BUY' if pos.get('type', 0) == 0 else 'SELL'
                        volume = pos.get('volume', 0)
                        price = pos.get('price_open', 0)
                        profit = pos.get('profit', 0)
                        comment = pos.get('comment', 'N/A')
                        
                        # Thêm màu sắc cho profit
                        profit_str = f"${profit:<11.2f}"
                        if profit > 0:
                            profit_str = f"📈 {profit_str}"
                        elif profit < 0:
                            profit_str = f"📉 {profit_str}"
                        
                        print(f"{ticket:<10} {symbol:<10} {pos_type:<6} {volume:<8.2f} {price:<10.5f} {profit_str} {comment:<15}")
                else:
                    print("  Không có lệnh nào đang mở")
            
            # Lấy thông tin cấu hình
            config_info = config_manager.get_config_info()
            
            # Hiển thị thống kê
            if 'summary' in account_info:
                summary = account_info['summary']
                print(f"\n📈 THỐNG KÊ:")
                print(f"  📊 Tổng lệnh mở: {summary.get('total_positions', 0)}")
                print(f"  💰 Tổng profit: ${summary.get('total_profit', 0):,.2f}")
                print(f"  📈 Lệnh có lãi: {summary.get('profitable_positions', 0)}")
                print(f"  📉 Lệnh thua lỗ: {summary.get('losing_positions', 0)}")
                
                # Thêm thông tin cấu hình
                if config_info:
                    print(f"\n⚙️ CẤU HÌNH:")
                    balance_at_5am = float(config_info.get('balanceat5am', 0))
                    min_balance = float(config_info.get('minbalance', 0))
                    drawdown_limit = float(config_info.get('drawdown', 0))
                    daily_profit_target = float(config_info.get('dailyprofittarget', 0))
                    current_profit = account.get('profit', 0)
                    
                    print(f"  💰 Balance at 5AM: ${balance_at_5am:,.2f}")
                    print(f"  🔒 Min Balance: ${min_balance:,.2f}")
                    print(f"  📉 Drawdown Limit: ${drawdown_limit:,.2f}")
                    print(f"  🎯 Daily Profit Target: ${daily_profit_target:,.2f}")
                    print(f"  📊 Profit hiện tại: ${current_profit:,.2f}")
                    
                    # Tính toán thêm
                    current_balance = account.get('balance', 0)
                    daily_profit = current_balance - balance_at_5am
                    drawdown_used = balance_at_5am - current_balance
                    
                    print(f"\n📊 PHÂN TÍCH:")
                    print(f"  📈 Daily Profit: ${daily_profit:,.2f}")
                    print(f"  📉 Drawdown Used: ${drawdown_used:,.2f}")
                    
                    # Hiển thị trạng thái
                    if daily_profit >= daily_profit_target:
                        print(f"  🎯 Daily Target: ✅ ĐẠT MỤC TIÊU")
                    else:
                        remaining = daily_profit_target - daily_profit
                        print(f"  🎯 Daily Target: ⏳ Còn ${remaining:,.2f}")
                    
                    if drawdown_used >= drawdown_limit:
                        print(f"  📉 Drawdown: ⚠️ VƯỢT GIỚI HẠN")
                    else:
                        remaining_dd = drawdown_limit - drawdown_used
                        print(f"  📉 Drawdown: ✅ Còn ${remaining_dd:,.2f}")
                    
                    if current_balance < min_balance:
                        print(f"  🔒 Min Balance: ⚠️ DƯỚI GIỚI HẠN")
                    else:
                        print(f"  🔒 Min Balance: ✅ AN TOÀN")
            
            # Hiển thị thời gian cập nhật
            if 'timestamp' in account_info:
                timestamp = account_info['timestamp']
                print(f"\n⏰ Cập nhật lúc: {timestamp}")
            
            print("\n" + "=" * 60)
            print(f"🔄 Cập nhật lần thứ {update_count} - Mỗi 30 giây - Nhấn Enter để dừng")
            
            # Chờ 30 giây trước khi cập nhật lại
            time.sleep(30)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Lỗi khi cập nhật: {e}")
            print("🔄 Đang thử lại...")
            time.sleep(3)
    
    print("\n✅ Đã dừng cập nhật realtime")
    input("Nhấn Enter để quay lại menu chính...")

def show_refresh_bot(config_manager):
    """Hiển thị chức năng refresh bot"""
    clear_screen()
    show_header()
    
    print("🔄 REFRESH BOT")
    print("=" * 60)
    print("Chức năng này sẽ gửi lệnh refresh đến bot để:")
    print("  - Tải lại cấu hình từ database")
    print("  - Khởi động lại các strategy")
    print("  - Xóa cache và file tạm thời")
    print("  - Đảm bảo bot hoạt động với cấu hình mới nhất")
    print("-" * 60)
    
    confirm = input("Bạn có chắc chắn muốn refresh bot? (y/n): ").strip().lower()
    
    if confirm == 'y':
        print("\n🔄 Đang gửi lệnh refresh bot...")
        
        try:
            success, message = config_manager.refresh_bot()
            
            if success:
                print("✅ Refresh bot thành công!")
                print(f"📝 Thông báo: {message}")
                
                print("\n📋 CÁC THAY ĐỔI ĐÃ THỰC HIỆN:")
                print("  ✅ Đã tải lại cấu hình từ database")
                print("  ✅ Đã khởi động lại các strategy")
                print("  ✅ Đã xóa cache và file tạm thời")
                print("  ✅ Bot đang hoạt động với cấu hình mới nhất")
                
            else:
                print("❌ Refresh bot thất bại!")
                print(f"📝 Lỗi: {message}")
                
        except Exception as e:
            print("❌ Lỗi khi refresh bot:")
            print(f"   {e}")
    
    else:
        print("❌ Đã hủy refresh bot")
    
    print("\n" + "=" * 60)
    input("Nhấn Enter để quay lại menu chính...")

def show_main_menu(config_manager):
    """Hiển thị menu chính"""
    while True:
        clear_screen()
        show_header()
        
        # Test kết nối
        if not config_manager.test_connection():
            print("❌ Không thể kết nối đến server!")
            print("Hãy kiểm tra:")
            print("  - Server có đang chạy không?")
            print("  - IP address có đúng không?")
            print("  - Port 5000 có mở không?")
            print(f"  - URL hiện tại: {SERVER_URL}")
            print("\nNhấn Enter để thử lại...")
            input()
            continue
        
        print("✅ Kết nối server thành công!")
        
        # Lấy thông tin cấu hình
        config = config_manager.get_all_config()
        if config:
            print(f"📊 Thống kê:")
            print(f"  - Settings: {len(config['settings'])} items")
            print(f"  - Strategies: {len(config['strategies'])} items")
            print(f"  - Strategy Configs: {len(config['strategy_config'])} items")
            print(f"  - Test Settings: {len(config['test_settings'])} items")
            
            # Hiển thị trạng thái refresh bot
            test_settings = config['test_settings']
            refresh_status = test_settings.get('refresh_bot', 'N/A')
            print(f"  - Refresh Bot: {refresh_status}")
        
        print("\n🔧 MENU CHÍNH:")
        print("  1. ⚙️  Quản lý Settings")
        print("  2. 🎯 Quản lý Strategies")
        print("  3. ⚙️  Quản lý Strategy Config")
        print("  4. 🧪 Quản lý Test Settings")
        print("  5. 🔄 Refresh Bot")
        print("  6. 📊 Xem toàn bộ cấu hình")
        print("  7. 💰 Thông tin tài khoản MT5")
        print("  0. 🚪 Thoát")
        print("-" * 60)
        
        choice = input("Chọn chức năng (0-7): ").strip()
        
        if choice == '0':
            print("👋 Tạm biệt!")
            break
        elif choice == '1':
            print("⚠️ Chức năng này chưa được implement")
            input("Nhấn Enter để tiếp tục...")
        elif choice == '2':
            print("⚠️ Chức năng này chưa được implement")
            input("Nhấn Enter để tiếp tục...")
        elif choice == '3':
            print("⚠️ Chức năng này chưa được implement")
            input("Nhấn Enter để tiếp tục...")
        elif choice == '4':
            print("⚠️ Chức năng này chưa được implement")
            input("Nhấn Enter để tiếp tục...")
        elif choice == '5':
            show_refresh_bot(config_manager)
        elif choice == '6':
            print("⚠️ Chức năng này chưa được implement")
            input("Nhấn Enter để tiếp tục...")
        elif choice == '7':
            show_mt5_account_info(config_manager)
        else:
            print("❌ Lựa chọn không hợp lệ!")
            input("Nhấn Enter để tiếp tục...")

def main():
    """Hàm chính"""
    global SERVER_URL
    
    print("🚀 KHỞI ĐỘNG CLIENT04.PY")
    print("=" * 60)
    
    # Kiểm tra kết nối mạng
    print("📡 Kiểm tra kết nối...")
    
    config_manager = ConfigManager(SERVER_URL)
    
    if not config_manager.test_connection():
        print(f"❌ Không thể kết nối đến {SERVER_URL}")
        print("\n🔧 HƯỚNG DẪN KHẮC PHỤC:")
        print("1. Đảm bảo server04.py đang chạy trên máy chủ")
        print("2. Kiểm tra IP address trong file client04.py")
        print("3. Đảm bảo port 5000 được mở")
        print("4. Kiểm tra firewall")
        print(f"\nIP hiện tại: {SERVER_URL}")
        change_ip = input("Bạn có muốn thay đổi IP không? (y/n): ").lower()
        if change_ip == 'y':
            new_ip = input("Nhập IP mới: ").strip()
            if new_ip:
                SERVER_URL = f"http://{new_ip}:5000"
                config_manager = ConfigManager(SERVER_URL)
                print(f"✅ Đã thay đổi IP thành: {SERVER_URL}")
                input("Nhấn Enter để tiếp tục...")
    
    # Hiển thị menu chính
    show_main_menu(config_manager)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Chương trình bị gián đoạn")
        print("👋 Tạm biệt!")
    except Exception as e:
        print(f"\n❌ Lỗi không mong muốn: {e}")
        print("Hãy kiểm tra lại và thử lại") 