import subprocess
import datetime


def backup_mongodb():
    now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"backup_kangwon_{now}.gz"
    cmd = f"mongodump --db kangwon_mall_db --archive={filename} --gzip"

    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"백업 완료: {filename}")
    else:
        print(f"백업 실패: {result.stderr}")


if __name__ == '__main__':
    backup_mongodb()
