import requests
import time
import json
import os

#config.py에서 설정값 불러오기
from config import MOBSF_URL, MOBSF_API_KEY, HEADERS, APK_PATH

def upload_apk(file_path):
    """APK 파일을 MobSF 서버에 업로드"""
    if not os.path.isfile(file_path):
        print("[!] APK 파일이 존재하지 않습니다.")
        return {}

    with open(file_path, 'rb') as f:
        files = {
            'file': (os.path.basename(file_path), f, 'application/octet-stream')
        }
        print(f"[+] Uploading APK: {file_path}")
        response = requests.post(f'{MOBSF_URL}/api/v1/upload', headers=HEADERS, files=files)

    print(f"[*] Status Code: {response.status_code}")
    print(f"[*] Response Text: {response.text}")

    try:
        return response.json()
    except Exception as e:
        print(f"[!] JSON 파싱 오류: {e}")
        return {}


def scan_apk(upload_response):
    """정적 분석 요청"""
    scan_data = {
        'hash': upload_response['hash'],
        'scan_type': upload_response['scan_type'],
        'file_name': upload_response['file_name']
    }
    print("[+] Requesting static analysis scan...")
    response = requests.post(f'{MOBSF_URL}/api/v1/scan', data=scan_data, headers=HEADERS)
    return response.json()


def get_report(scan_hash):
    """분석 보고서 가져오기 (JSON)"""
    print("[+] Fetching report...")
    params = {
        'hash': scan_hash,
        'type': 'static'
    }
    response = requests.post(f'{MOBSF_URL}/api/v1/report_json', data=params, headers=HEADERS)
    return response.json()


def parse_report(report):
    """보고서에서 주요 정보 요약 출력"""
    print("\n===== 분석 요약 =====")
    print(f"앱 이름: {report.get('app_name')}")
    print(f"패키지명: {report.get('package_name')}")
    print(f"위험 권한: {report.get('permissions', {}).get('dangerous', [])}")
    print(f"외부 URL 탐지: {report.get('urls')}")
    print(f"하드코딩 이메일: {report.get('emails')}")
    print(f"하드코딩 키워드: {report.get('code_analysis', {}).get('high_risk', [])}")
    print("=====================\n")


def main():
    #1. APK 업로드
    upload_response = upload_apk(APK_PATH)
    if 'hash' not in upload_response:
        print("[!] 업로드 실패: 'hash' 값이 응답에 없습니다.")
        return

    #2. 정적 분석 요청
    scan_response = scan_apk(upload_response)

    #3. 분석 대기
    time.sleep(3)

    #4. 보고서 가져오기
    report = get_report(upload_response['hash'])

    #5. 요약 출력
    parse_report(report)

    #6. 저장
    with open('static_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=4, ensure_ascii=False)
        print("[+] 분석 결과가 'static_report.json'에 저장되었습니다.")


if __name__ == '__main__':
    main()
