import pandas as pd


def _compare_file_list(compare_list: list, compare_target_list) -> list:
    '''
    두 파일 리스트를 비교하여 다른 파일 정보가 있다면
    해당 파일 이름을 리스트에 담아 리턴.

    :param compare_list: 비교할 리스트
    :param compare_target_list: 비교 대상 리스트
    :return: 다른 항목 리스트
    '''

    result_list = []
    for name in compare_list:
        if name not in compare_target_list:
            result_list.append(name)

    return result_list


def get_dir_update_info(before_xlsx_path_list: list, after_xlsx_path_list: list) -> (list, list):
    '''
    이전 파일 리스트와 현재 파일리스트를 비교하여
    삭제된 파일과 추가된 파일을 파악하여 반환

    :param before_xlsx_path_list: 이전 파일경로 리스트
    :param after_xlsx_path_list : 어베이트 후 파일경로 리스트
    :return: 삭제 파일 리스트와 생성된 파일 리스트
    '''

    deleted_file_list = []
    new_file_list = []

    after_file_name_list = [after.split('/')[-1] for after in
                            after_xlsx_path_list]  # 파일경로 / 를 기준으로 스플릿 하여 마지막 인덱스(파일이름) 을 가져온다.
    before_file_name_list = [before.split('/')[-1] for before in before_xlsx_path_list]

    deleted_file_list = _compare_file_list(before_file_name_list, after_file_name_list)
    new_file_list = _compare_file_list(after_file_name_list, before_file_name_list)

    return deleted_file_list, new_file_list


# read_excel()로 xlsx 파일을 읽으면 기본적으로 첫 번쨰 시트의 데이터를 가져온다. 이떄 주의할 점은 파일을 읽을 떄 추가/삭제 여부에 따라 before 디렉토리에 존재하지 않을 수 있다. 존재하지 않으면 FileNotFoundError 가 발생할 수 있다.
# 여기서 존재하지 않는 건 에러가 아닌 디렉토리 업데이트 상태이다 프로그램이 종료되는 걸 방지하기 위해 try/catch로 묶어주고 FileNotFoundError 발생시 continue 처리 해준다.
# 비교 할 엑셀 파일의 이름은 같아야 한다.
def get_file_diff_info_list(after_xlsx_path_list: list, before_dir_path: str) -> list:
    diff_info_list = []
    for xlsx_path in after_xlsx_path_list:
        # 엑셀파일 읽기
        try:
            after_df = pd.read_excel(xlsx_path)
            file_name = xlsx_path.split('/')[-1]
            print('after -', file_name, ':')
            print(after_df)

            # 이전 버전 조회
            before_df = pd.read_excel(f'{before_dir_path}/{file_name}')
            print('before -', file_name, ':')
            print(before_df)
        except FileNotFoundError:
            continue

    return diff_info_list
