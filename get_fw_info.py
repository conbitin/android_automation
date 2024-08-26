import subprocess

def extract_info_after_colon(lines):
  """
  Hàm trích xuất thông tin sau dấu ':' từ các dòng cho trước.

  Args:
    lines: Một danh sách các dòng chứa thông tin.

  Returns:
    Một danh sách chứa các phần thông tin đã trích xuất.
  """

  results = []
  for line in lines:
    # Tìm vị trí của dấu ':'
    index = line.find(':')
    if index != -1:
      # Lấy phần sau dấu ':'
      result = line[index+1:].strip()
      results.append(result)
    else:
      print("Dòng không chứa dấu ':'")

  return results

def get_app_info():
    """
    Lấy thông tin chi tiết về các ứng dụng đã cài đặt trên thiết bị Android, bao gồm package name, versionCode và versionName.

    Returns:
        list: Danh sách các tuple, mỗi tuple chứa (package_name, version_code, version_name).
    """

    # Lấy danh sách các gói ứng dụng
    result = subprocess.run(['adb', 'shell', 'pm', 'list', 'packages', '-3'], capture_output=True, text=True)
    package_names = extract_info_after_colon(result.stdout.splitlines())

    app_infos = []
    for package_name in package_names:
        # Lấy versionCode và versionName
        dumpsys_result = subprocess.run(['adb', 'shell', 'dumpsys', 'package', package_name], capture_output=True, text=True)
        dumpsys_lines = dumpsys_result.stdout.splitlines()

        version_code = None
        version_name = None
        for line in dumpsys_lines:
            if 'versionCode=' in line:
                version_code = line.split('=')[1].split(' ')[0].strip()
            elif 'versionName=' in line:
                version_name = line.split('=')[1].strip()

        app_infos.append((package_name, version_code, version_name))

    return app_infos

def get_build_fingerprint():
  """Lấy thông tin build fingerprint của thiết bị Android.

  Returns:
    Chuỗi chứa build fingerprint hoặc None nếu có lỗi xảy ra.
  """

  cmd = 'adb shell getprop ro.build.fingerprint'
  try:
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()
  except subprocess.CalledProcessError as e:
    print(f"Lỗi khi thực hiện lệnh: {e}")
    return None

if __name__ == "__main__":
   fingerprint = get_build_fingerprint()
   if fingerprint:
     print(f"Build fingerprint: {fingerprint}")
   else:
     print("Không thể lấy được build fingerprint.")
   app_info = get_app_info()
   for package, version_code, version_name in app_info:
     print(f"Package: {package}, Version Code: {version_code}, Version Name: {version_name}")
