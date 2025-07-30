#!/usr/bin/env python3
"""
Client04.py - Quản lý cấu hình trading bot từ xa
Chạy trên Android (Termux) để thay đổi cấu hình database
"""

import requests
import json
import os
import sys
from datetime import datetime

# Cấu hình
SERVER_URL = "https://f5d21b259c01.ngrok-free.app"  # Ngrok URL
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

def show_settings_menu(config_manager):
    """Hiển thị menu quản lý settings"""
    while True:
        clear_screen()
        show_header()
        print("⚙️  QUẢN LÝ SETTINGS")
        print("-" * 60)
        
        # Lấy settings hiện tại
        config = config_manager.get_all_config()
        if not config:
            print("❌ Không thể lấy cấu hình")
            input("Nhấn Enter để quay lại...")
            return
        
        settings = config['settings']
        print("📋 Settings hiện tại:")
        for i, (key, value) in enumerate(settings.items(), 1):
            print(f"  {i:2d}. {key:<20} = {value}")
        
        print("\n🔧 Tùy chọn:")
        print("  0. Quay lại menu chính")
        print("  [số] Chọn setting để sửa")
        print("  'add' Thêm setting mới")
        
        choice = input("\nChọn tùy chọn: ").strip().lower()
        
        if choice == '0':
            return
        elif choice == 'add':
            key = input("Nhập key mới: ").strip()
            value = input("Nhập value: ").strip()
            if key and value:
                if config_manager.update_setting(key, value):
                    print("✅ Đã thêm setting thành công")
                else:
                    print("❌ Không thể thêm setting")
                input("Nhấn Enter để tiếp tục...")
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(settings):
                keys = list(settings.keys())
                key = keys[idx]
                current_value = settings[key]
                print(f"\n📝 Sửa setting: {key}")
                print(f"Giá trị hiện tại: {current_value}")
                new_value = input("Giá trị mới: ").strip()
                if new_value:
                    if config_manager.update_setting(key, new_value):
                        print("✅ Đã cập nhật setting thành công")
                    else:
                        print("❌ Không thể cập nhật setting")
                    input("Nhấn Enter để tiếp tục...")
            else:
                print("❌ Lựa chọn không hợp lệ")
                input("Nhấn Enter để tiếp tục...")

def show_strategies_menu(config_manager):
    """Hiển thị menu quản lý strategies"""
    while True:
        clear_screen()
        show_header()
        print("🎯 QUẢN LÝ STRATEGIES")
        print("-" * 60)
        
        config = config_manager.get_all_config()
        if not config:
            print("❌ Không thể lấy cấu hình")
            input("Nhấn Enter để quay lại...")
            return
        
        strategies = config['strategies']
        print("📋 Strategies hiện tại:")
        for i, strategy in enumerate(strategies, 1):
            print(f"  {i:2d}. {strategy['strategy_name']:<12} = {strategy['strategy_type']}")
        
        print("\n🔧 Tùy chọn:")
        print("  0. Quay lại menu chính")
        print("  [số] Chọn strategy để sửa")
        
        choice = input("\nChọn tùy chọn: ").strip()
        
        if choice == '0':
            return
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(strategies):
                strategy = strategies[idx]
                strategy_name = strategy['strategy_name']
                current_type = strategy['strategy_type']
                print(f"\n📝 Sửa strategy: {strategy_name}")
                print(f"Loại hiện tại: {current_type}")
                new_type = input("Loại mới: ").strip()
                if new_type:
                    if config_manager.update_strategy(strategy_name, new_type):
                        print("✅ Đã cập nhật strategy thành công")
                    else:
                        print("❌ Không thể cập nhật strategy")
                    input("Nhấn Enter để tiếp tục...")
            else:
                print("❌ Lựa chọn không hợp lệ")
                input("Nhấn Enter để tiếp tục...")

def show_strategy_config_menu(config_manager):
    """Hiển thị menu quản lý strategy config"""
    while True:
        clear_screen()
        show_header()
        print("⚙️  QUẢN LÝ STRATEGY CONFIG")
        print("-" * 60)
        
        config = config_manager.get_all_config()
        if not config:
            print("❌ Không thể lấy cấu hình")
            input("Nhấn Enter để quay lại...")
            return
        
        strategy_configs = config['strategy_config']
        
        # Nhóm theo strategy
        strategies = {}
        for cfg in strategy_configs:
            strategy_name = cfg['strategy_name']
            if strategy_name not in strategies:
                strategies[strategy_name] = []
            strategies[strategy_name].append(cfg)
        
        print("📋 Strategy Configs:")
        for i, (strategy_name, configs) in enumerate(strategies.items(), 1):
            print(f"\n  {i}. {strategy_name}:")
            for cfg in configs:
                print(f"     {cfg['symbol']}: {cfg['volume']}-{cfg['stop_loss']}-{cfg['take_profit']}-{cfg['timeframe']}")
        
        print("\n🔧 Tùy chọn:")
        print("  0. Quay lại menu chính")
        print("  [số] Chọn strategy để sửa config")
        
        choice = input("\nChọn tùy chọn: ").strip()
        
        if choice == '0':
            return
        elif choice.isdigit():
            idx = int(choice) - 1
            strategy_names = list(strategies.keys())
            if 0 <= idx < len(strategy_names):
                strategy_name = strategy_names[idx]
                edit_strategy_config(config_manager, strategy_name, strategies[strategy_name])
            else:
                print("❌ Lựa chọn không hợp lệ")
                input("Nhấn Enter để tiếp tục...")

def edit_strategy_config(config_manager, strategy_name, configs):
    """Sửa config cho một strategy cụ thể"""
    while True:
        clear_screen()
        show_header()
        print(f"⚙️  SỬA CONFIG: {strategy_name}")
        print("-" * 60)
        
        print("📋 Configs hiện tại:")
        for i, cfg in enumerate(configs, 1):
            print(f"  {i:2d}. {cfg['symbol']}: {cfg['volume']}-{cfg['stop_loss']}-{cfg['take_profit']}-{cfg['timeframe']}")
        
        print("\n🔧 Tùy chọn:")
        print("  0. Quay lại")
        print("  [số] Chọn config để sửa")
        print("  'add' Thêm config mới")
        
        choice = input("\nChọn tùy chọn: ").strip().lower()
        
        if choice == '0':
            return
        elif choice == 'add':
            print(f"\n📝 Thêm config cho {strategy_name}:")
            symbol = input("Symbol (ví dụ: xauusd): ").strip().lower()
            volume = input("Volume (ví dụ: 0.02): ").strip()
            stop_loss = input("Stop Loss (ví dụ: 1300): ").strip()
            take_profit = input("Take Profit (ví dụ: 2200): ").strip()
            timeframe = input("Timeframe (ví dụ: TIMEFRAME_M1): ").strip()
            
            if all([symbol, volume, stop_loss, take_profit, timeframe]):
                try:
                    if config_manager.update_strategy_config(
                        strategy_name, symbol, float(volume), 
                        float(stop_loss), float(take_profit), timeframe
                    ):
                        print("✅ Đã thêm config thành công")
                    else:
                        print("❌ Không thể thêm config")
                except ValueError:
                    print("❌ Giá trị không hợp lệ")
                input("Nhấn Enter để tiếp tục...")
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(configs):
                cfg = configs[idx]
                print(f"\n📝 Sửa config: {cfg['symbol']}")
                print(f"Hiện tại: {cfg['volume']}-{cfg['stop_loss']}-{cfg['take_profit']}-{cfg['timeframe']}")
                
                volume = input(f"Volume mới (hiện tại: {cfg['volume']}): ").strip()
                stop_loss = input(f"Stop Loss mới (hiện tại: {cfg['stop_loss']}): ").strip()
                take_profit = input(f"Take Profit mới (hiện tại: {cfg['take_profit']}): ").strip()
                timeframe = input(f"Timeframe mới (hiện tại: {cfg['timeframe']}): ").strip()
                
                # Sử dụng giá trị cũ nếu không nhập mới
                volume = volume if volume else str(cfg['volume'])
                stop_loss = stop_loss if stop_loss else str(cfg['stop_loss'])
                take_profit = take_profit if take_profit else str(cfg['take_profit'])
                timeframe = timeframe if timeframe else cfg['timeframe']
                
                try:
                    if config_manager.update_strategy_config(
                        strategy_name, cfg['symbol'], float(volume), 
                        float(stop_loss), float(take_profit), timeframe
                    ):
                        print("✅ Đã cập nhật config thành công")
                    else:
                        print("❌ Không thể cập nhật config")
                except ValueError:
                    print("❌ Giá trị không hợp lệ")
                input("Nhấn Enter để tiếp tục...")
            else:
                print("❌ Lựa chọn không hợp lệ")
                input("Nhấn Enter để tiếp tục...")

def show_test_settings_menu(config_manager):
    """Hiển thị menu quản lý test settings"""
    while True:
        clear_screen()
        show_header()
        print("🧪 QUẢN LÝ TEST SETTINGS")
        print("-" * 60)
        
        config = config_manager.get_all_config()
        if not config:
            print("❌ Không thể lấy cấu hình")
            input("Nhấn Enter để quay lại...")
            return
        
        test_settings = config['test_settings']
        print("📋 Test Settings hiện tại:")
        for i, (key, value) in enumerate(test_settings.items(), 1):
            print(f"  {i:2d}. {key:<15} = {value}")
        
        print("\n🔧 Tùy chọn:")
        print("  0. Quay lại menu chính")
        print("  [số] Chọn setting để sửa")
        
        choice = input("\nChọn tùy chọn: ").strip()
        
        if choice == '0':
            return
        elif choice.isdigit():
            idx = int(choice) - 1
            keys = list(test_settings.keys())
            if 0 <= idx < len(keys):
                key = keys[idx]
                current_value = test_settings[key]
                print(f"\n📝 Sửa test setting: {key}")
                print(f"Giá trị hiện tại: {current_value}")
                new_value = input("Giá trị mới (ON/OFF): ").strip().upper()
                if new_value in ['ON', 'OFF']:
                    if config_manager.update_test_setting(key, new_value):
                        print("✅ Đã cập nhật test setting thành công")
                    else:
                        print("❌ Không thể cập nhật test setting")
                    input("Nhấn Enter để tiếp tục...")
                else:
                    print("❌ Giá trị phải là ON hoặc OFF")
                    input("Nhấn Enter để tiếp tục...")
            else:
                print("❌ Lựa chọn không hợp lệ")
                input("Nhấn Enter để tiếp tục...")

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
        
        print("\n🔧 MENU CHÍNH:")
        print("  1. ⚙️  Quản lý Settings")
        print("  2. 🎯 Quản lý Strategies")
        print("  3. ⚙️  Quản lý Strategy Config")
        print("  4. 🧪 Quản lý Test Settings")
        print("  5. 📊 Xem toàn bộ cấu hình")
        print("  0. 🚪 Thoát")
        print("-" * 60)
        
        choice = input("Chọn chức năng (0-5): ").strip()
        
        if choice == '0':
            print("👋 Tạm biệt!")
            break
        elif choice == '1':
            show_settings_menu(config_manager)
        elif choice == '2':
            show_strategies_menu(config_manager)
        elif choice == '3':
            show_strategy_config_menu(config_manager)
        elif choice == '4':
            show_test_settings_menu(config_manager)
        elif choice == '5':
            show_full_config(config_manager)
        else:
            print("❌ Lựa chọn không hợp lệ!")
            input("Nhấn Enter để tiếp tục...")

def show_full_config(config_manager):
    """Hiển thị toàn bộ cấu hình"""
    clear_screen()
    show_header()
    print("📊 TOÀN BỘ CẤU HÌNH")
    print("=" * 60)
    
    config = config_manager.get_all_config()
    if not config:
        print("❌ Không thể lấy cấu hình")
        input("Nhấn Enter để quay lại...")
        return
    
    print("\n⚙️ SETTINGS:")
    for key, value in config['settings'].items():
        print(f"  {key} = {value}")
    
    print("\n🎯 STRATEGIES:")
    for strategy in config['strategies']:
        print(f"  {strategy['strategy_name']} = {strategy['strategy_type']}")
    
    print("\n⚙️ STRATEGY CONFIGS:")
    for cfg in config['strategy_config']:
        print(f"  {cfg['strategy_name']} - {cfg['symbol']}: {cfg['volume']}-{cfg['stop_loss']}-{cfg['take_profit']}-{cfg['timeframe']}")
    
    print("\n🧪 TEST SETTINGS:")
    for key, value in config['test_settings'].items():
        print(f"  {key} = {value}")
    
    print("\n" + "=" * 60)
    input("Nhấn Enter để quay lại...")

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
