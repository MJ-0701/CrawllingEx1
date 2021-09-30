import pandas as pd
from models import FileDiffInfo


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

            # 이전 버전 조회
            before_df = pd.read_excel(f'{before_dir_path}/{file_name}')

        except FileNotFoundError:
            continue

    # 시트 데이터가 같은지 비교 후 같지 않다면 상세 비교
    if not before_df.equals(after_df):  # 데이터가 다를경우
        # 두 데이터의 다른 부분 추출
        df = pd.concat([before_df, after_df])   # concat() 함수로 두 데이터 프레임을 합쳐주고
        duplicates_df = df.drop_duplicates(keep=False)  # 중복된 데이터를 제거해 준다. keep=False 옵션을 주어야 모든 중복 데이터가 제거된 결과를 반환한다. 설정하지 않을 경우 기본값 first가 셋팅되어 첫 번째 중복 데이터만 제거된다.

        # ROW 데이터 스트링 리스트로 변환
        before_list = [str(r) for r in before_df.values.tolist()]
        after_list = [str(r) for r in after_df.values.tolist()]

        # 변경 전 데이터, 변경 후 데이터 분류
        changed_list = []
        duplicates_list = [str(r) for r in duplicates_df.values.tolist()]
        for row in duplicates_list:
            try:
                before_list.index(row)
                changed_list.append(f'~{row}~')     # 데이터를 추가할때 before에 있던 데이터는 앞뒤로 ~ 처리를 해준다 추후 내용을 전달할때 마크다운 역할을 하기 때문이다(슬랙 마크다운 문법).

            except ValueError:
                pass

            try:
                after_list.index(row)
                changed_list.append(row)
            except ValueError:  # index() 로 찾는데 데이터가 없을 경우 해당 에러가 발생한다. 데이터가 없는건 에러가 아니기때문에 pass 처리 해준다.
                pass
        # 변경된 정보를 핸들링할 객체 생성
        info = FileDiffInfo(file_name, changed_list)
        diff_info_list.append(info)

    return diff_info_list
