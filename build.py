#! /usr/bin/env python
import argparse
import os
import subprocess


MODES = ['base','local']

def get_mode():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-m', '--mode',
        help = 'Docker build mode [base, local]',
    )
    args =parser.parse_args()

    # 모듈 호출에 옵션으로 mode를 전달한 경우
    if args.mode:
        mode = args.mode.strip().lower()

    # 사용자 입력으로 mode를 선택한 경우
    else:
        while True:
            print('Select mode')
            print('1. base')
            print('2. local')
            selected_mode = input('Choice: ')
            try:
                mode_index = int(selected_mode) - 1
                mode = MODES[mode_index]
                break
            except IndexError:
                print('1 ~ 2번을 입력하세요')
    return mode

def mode_function(mode):
    if mode == 'base':
        build_base()
    elif mode == 'local':
        build_local()
    else:
        raise ValueError(f'{MODES}에 속하는 모드만 가능합니다')

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


# 모듈 호출에 옵션으로 mode를 전달한 경우


if __name__=='__main__':
    mode = get_mode()
    mode_function(mode)

