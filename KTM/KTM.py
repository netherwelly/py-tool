#! /usr/bin/python

# Nguyen Tan Phat
# MSSV: 23-0-00111
# Du an ket thuc mon

import csv
import os
import socket
from ping3 import ping
import speedtest
from tabulate import tabulate

class NetworkManager:
    def __init__(self):
        self.devices = []

    def add_device(self, name, device_type, location, ip, description):
        if any(device['name'] == name for device in self.devices):
            print(f"Thiết bị có tên {name} đã tồn tại.")
            return
        self.devices.append({
            'name': name,
            'type': device_type,
            'location': location,
            'ip': ip,
            'description': description
        })
        print(f"Thiết bị {name} đã được thêm vào.")

    def delete_device(self, name):
        self.devices = [device for device in self.devices if device['name'] != name]
        print(f"Thiết bị {name} đã bị xóa.")

    def edit_device(self, name, device_type=None, location=None, ip=None, description=None):
        for device in self.devices:
            if device['name'] == name:
                if device_type:
                    device['type'] = device_type
                if location:
                    device['location'] = location
                if ip:
                    device['ip'] = ip
                if description:
                    device['description'] = description
                print(f"Thiết bị {name} đã được cập nhật.")
                return
        print(f"Không tìm thấy thiết bị với tên {name}.")

    def search_device(self, name=None, device_type=None, location=None, ip=None):
        results = [device for device in self.devices if
                   (name and device['name'] == name) or
                   (device_type and device['type'] == device_type) or
                   (location and device['location'] == location) or
                   (ip and device['ip'] == ip)]
        print(tabulate(results, headers="keys"))

    def list_devices(self):
        if not self.devices:
            print("Không có thiết bị nào trong hệ thống.")
        else:
            print(tabulate(self.devices, headers="keys"))

    def save_to_file(self, filename):
        with open(filename, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['name', 'type', 'location', 'ip', 'description'])
            writer.writeheader()
            writer.writerows(self.devices)
        print(f"Dữ liệu đã được lưu vào tệp {filename}.")

    def load_from_file(self, filename):
        if not os.path.exists(filename):
            print(f"Tệp {filename} không tồn tại.")
            return
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            self.devices = [row for row in reader]
        print(f"Dữ liệu đã được tải từ tệp {filename}.")

    def import_from_csv(self, filename):
        if not os.path.exists(filename):
            print(f"Tệp {filename} không tồn tại.")
            return
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.add_device(row['name'], row['type'], row['location'], row['ip'], row['description'])

    def export_to_csv(self, filename, devices_to_export):
        with open(filename, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['name', 'type', 'location', 'ip', 'description'])
            writer.writeheader()
            writer.writerows(devices_to_export)
        print(f"Thiết bị đã được xuất ra tệp {filename}.")

class NetworkTools:
    def ping_device(self, ip_address):
        response_time = ping(ip_address)
        if response_time is None:
            print(f"Không thể kết nối tới {ip_address}.")
        else:
            print(f"Thời gian phản hồi từ {ip_address}: {response_time} giây.")

    def nslookup(self, domain):
        try:
            ip_address = socket.gethostbyname(domain)
            print(f"Địa chỉ IP của {domain} là {ip_address}.")
        except socket.gaierror:
            print(f"Không thể tra cứu tên miền {domain}.")

    def check_bandwidth(self):
        st = speedtest.Speedtest()
        download_speed = st.download() / 1_000_000  # Mbps
        upload_speed = st.upload() / 1_000_000  # Mbps
        print(f"Tốc độ tải xuống: {download_speed:.2f} Mbps")
        print(f"Tốc độ tải lên: {upload_speed:.2f} Mbps")

    def network_discovery(self, ip_range):
        print(f"Đang quét mạng {ip_range}...")
        # Để đơn giản, chúng ta có thể sử dụng ping trong một khoảng IP
        active_hosts = []
        for i in range(1, 255):
            ip = f"{ip_range}.{i}"
            response = ping(ip)
            if response:
                active_hosts.append(ip)
        if active_hosts:
            print("Các thiết bị hoạt động trong mạng:")
            for host in active_hosts:
                print(host)
        else:
            print("Không tìm thấy thiết bị nào hoạt động.")

def main():
    manager = NetworkManager()
    tools = NetworkTools()

    while True:
        print("\n1. Quản lý thiết bị\n2. Lưu/ Tải dữ liệu\n3. Kiểm tra mạng\n4. Thoát")
        choice = input("Chọn một chức năng: ")

        if choice == "1":
            print("\n1. Thêm thiết bị\n2. Xóa thiết bị\n3. Sửa thiết bị\n4. Tìm thiết bị\n5. Liệt kê thiết bị")
            sub_choice = input("Chọn một chức năng quản lý thiết bị: ")

            if sub_choice == "1":
                name = input("Tên thiết bị: ")
                device_type = input("Loại thiết bị: ")
                location = input("Vị trí: ")
                ip = input("Địa chỉ IP: ")
                description = input("Mô tả: ")
                manager.add_device(name, device_type, location, ip, description)
            elif sub_choice == "2":
                name = input("Tên thiết bị cần xóa: ")
                manager.delete_device(name)
            elif sub_choice == "3":
                name = input("Tên thiết bị cần sửa: ")
                new_ip = input("Địa chỉ IP mới (nhấn Enter nếu không thay đổi): ")
                manager.edit_device(name, ip=new_ip)
            elif sub_choice == "4":
                ip = input("Nhập địa chỉ IP để tìm: ")
                manager.search_device(ip=ip)
            elif sub_choice == "5":
                manager.list_devices()

        elif choice == "2":
            print("\n1. Lưu dữ liệu\n2. Tải dữ liệu\n3. Nhập từ CSV\n4. Xuất ra CSV")
            sub_choice = input("Chọn một chức năng: ")

            if sub_choice == "1":
                filename = input("Tên tệp để lưu: ")
                manager.save_to_file(filename)
            elif sub_choice == "2":
                filename = input("Tên tệp để tải: ")
                manager.load_from_file(filename)
            elif sub_choice == "3":
                filename = input("Tên tệp CSV để nhập: ")
                manager.import_from_csv(filename)
            elif sub_choice == "4":
                filename = input("Tên tệp CSV để xuất: ")
                manager.export_to_csv(filename, manager.devices)

        elif choice == "3":
            print("\n1. Ping\n2. NSLookup\n3. Kiểm tra băng thông\n4. Khám phá mạng")
            sub_choice = input("Chọn một chức năng kiểm tra mạng: ")

            if sub_choice == "1":
                ip = input("Nhập địa chỉ IP: ")
                tools.ping_device(ip)
            elif sub_choice == "2":
                domain = input("Nhập tên miền: ")
                tools.nslookup(domain)
            elif sub_choice == "3":
                tools.check_bandwidth()
            elif sub_choice == "4":
                ip_range = input("Nhập dải IP (vd: 192.168.1): ")
                tools.network_discovery(ip_range)

        elif choice == "4":
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng thử lại.")

if __name__ == "__main__":
    main()

