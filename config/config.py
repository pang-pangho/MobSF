# config / config.py

# MobSF 서버 정보
MOBSF_URL = 'http://127.0.0.1:8000'
MOBSF_API_KEY = '' # 기본값

# 분석할 APK 파일 경로
APK_PATH = './apk_smples/sample.apk'

# API 요청에 필요한 헤더
HEADERS = {
    'Authorization' : MOBSF_API_KEY
}

# 분석 옵션
DEFAULT_ANALYSIS_OPTIONS = {
    'scan_type' : 'apk',
    'enable_static' : True,
    'enable_dynamic' : True
}

# 에뮬레이터 정보
EMULATOR_CONFIG = {
    'name' : 'Pixel_4_API_30',
    'adb_path' : 'C:/Users/cosco/AppData/Local/Android/Sdk/platform-tools/adb.exe', #값 변경 필요
    'frida_server_port' : 27042
}