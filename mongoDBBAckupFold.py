import os
import subprocess
import datetime
from pathlib import Path

# 설정
DB_NAME = "kangwon_mall_db"
# BASE_DIR = Path(__file__).resolve().parent / "backups"
# C:\BackUp 경로로 수정 (Raw string 'r' 사용)
BASE_DIR = Path(r"C:\BackUp")


def backup_mongodb_to_folder(db_name=DB_NAME, base_dir=BASE_DIR):
    """
    MongoDB 데이터를 날짜/시간별 폴더 형태로 백업합니다.
    (각 컬렉션이 products.bson, orders.bson 등 개별 BSON 파일로 분리되어 저장됨)
    """
    # 1. 실행 시간 기준 백업 폴더 생성 (예: backups/backup_20260906_063351)
    now_str = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    target_backup_dir = base_dir / f"backup_{now_str}"
    target_backup_dir.mkdir(parents=True, exist_ok=True)

    # 2. mongodump 실행 (--out 옵션으로 폴더 형태 분리 저장)
    cmd = f'mongodump --db "{db_name}" --out "{target_backup_dir}"'

    print("=" * 60)
    print(f" [강원약초] MongoDB 폴더별 BSON 백업 시작 (DB: {db_name})")
    print(f" 저장 대상 경로: {target_backup_dir}")
    print("=" * 60)

    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )

        if result.returncode == 0:
            db_folder = target_backup_dir / db_name
            print("\n[백업 성공!] 모든 컬렉션이 BSON 파일로 분리 저장되었습니다.")
            print(f"최종 저장 위치: {db_folder}\n")

            # 생성된 BSON 파일 목록 출력
            if db_folder.exists():
                print("생성된 BSON 파일 목록:")
                for item in sorted(db_folder.glob("*.bson")):
                    size_kb = item.stat().st_size / 1024
                    print(f"  - {item.name:<25} ({size_kb:.1f} KB)")
            return str(db_folder)
        else:
            print("\n[백업 실패!]")
            print(result.stderr)
            return None

    except Exception as e:
        print(f"\n[오류 발생]: {e}")
        return None


if __name__ == '__main__':
    backup_mongodb_to_folder()
