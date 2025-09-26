# upgraded 폴더 구조 설명

`upgraded` 폴더는 레거시(`legacy`) 폴더의 모든 파일과 디렉터리 구조를 그대로 복사하여 최신화 작업을 위한 공간입니다.

## 주요 구조
- MANIFEST.in, README.rst, distribute_setup.py, distribute-0.6.10.tar.gz, setup.py: 프로젝트 메타 및 설치 관련 파일
- docs/: 문서 및 빌드 산출물
  - Makefile, build/, source/
  - build/ 하위에 doctrees, html, html/_sources, html/_static 등
  - source/ 하위에 rst 문서와 conf.py, _static
- guachi/: 주요 파이썬 모듈 및 테스트 코드
  - __init__.py, config.py, database.py, tests/
  - tests/ 하위에 여러 테스트 파일
- guachi.egg-info/: 패키징 정보 파일
  - PKG-INFO, SOURCES.txt, dependency_links.txt, top_level.txt

## 목적
이 폴더는 레거시 코드를 최신 Python 환경에 맞게 업그레이드하고, 테스트 및 문서화, 패키징 등 모든 작업을 독립적으로 수행할 수 있도록 구성되어 있습니다.

각 파일은 레거시 폴더의 동일한 파일을 기반으로 하며, 업그레이드 작업 시 이 폴더 내에서 수정 및 개선이 이루어집니다.
