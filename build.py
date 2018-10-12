#!/usr/bin/env python
import os
import subprocess
import argparse
import sys


# ./build.py -m     <mode>
# ./build.py --mode <mode>

MODES = ['base','local','dev','production']


def get_mode():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode',
                        help='Docker build mode [{}]'.format(','.join(MODES)),
                        )
    args = parser.parse_args()

    if args.mode:
        mode = args.mode.strip().lower()

    # 사용자 입력으로 mode를 선택한 경우
    else:
        while True:
            for index, mode_name in enumerate(MODES, start=1):
                print(f'{index}: {mode_name}')
            selected_mode = input('Choice: ')
            try:
                mode_index = int(selected_mode) - 1
                mode = MODES[mode_index]
                break
            except IndexError:
                print('1 ~ 4번을 입력하세요')
    return mode

# 사용자가 입력한 mode
def mode_function(mode):
    if mode in MODES:
        cur_module=sys.modules[__name__]
        getattr(cur_module, f'build_{mode}')()

def build_base():
    try:
        # pipenv lock으로 requirements.txt생성
        subprocess.call('pipenv lock --requirements > requirements.txt', shell=True)

        # docker build
        subprocess.call('docker build -t mb-project:base -f Dockerfile.base .', shell=True)
    finally:
        # 끝난 후 requirements.txt파일 삭제
        os.remove('requirements.txt')

def build_local():
    try:
        # pipenv lock으로 requirements.txt생성
        subprocess.call('pipenv lock --requirements > requirements.txt', shell=True)

        # docker build
        subprocess.call('docker build -t mb-project:local -f Dockerfile.local .', shell=True)
    finally:
        # 끝난 후 requirements.txt파일 삭제
        os.remove('requirements.txt')


def build_dev():
    try:
        # pipenv lock으로 requirements.txt생성
        subprocess.call('pipenv lock --requirements > requirements.txt', shell=True)

        # docker build
        subprocess.call('docker build -t mb-project:dev -f Dockerfile.dev .', shell=True)
    finally:
        # 끝난 후 requirements.txt파일 삭제
        os.remove('requirements.txt')


def build_production():
    try:
        # pipenv lock으로 requirements.txt생성
        subprocess.call('pipenv lock --requirements > requirements.txt', shell=True)

        # docker build
        subprocess.call('docker build -t mb-project:production -f Dockerfile.production .', shell=True)
    finally:
        # 끝난 후 requirements.txt파일 삭제
        os.remove('requirements.txt')


# 모듈 호출에 옵션으로 mode를 전달할 경우

if __name__ == "__main__":
    mode = get_mode()
    mode_function(mode)




