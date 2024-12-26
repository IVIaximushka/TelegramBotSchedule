import aiogram.utils.formatting as fmt
import pandas as pd


def parse_html_table(html_table: str) -> pd.DataFrame:
    data = pd.read_html("<table>" + html_table + "</table>")[0]
    data = data.drop(19, axis=1).drop([0, 1, 2], axis=0)
    data.columns = [
        "id",
        "name",
        "all",
        "all_aud",
        "all_lec",
        "all_prac",
        "all_lab",
        "indep",
        "control",
        "first_lec",
        "first_prac",
        "first_lab",
        "first_ex",
        "first_test",
        "second_lec",
        "second_prac",
        "second_lab",
        "second_ex",
        "second_test",
    ]
    return data


def get_sections(data: pd.DataFrame) -> list[str]:
    sections = data[data["id"].isnull()]["name"].to_list()
    return sections


def format_disciplines(data: pd.DataFrame) -> fmt.Text:
    formatted_disciplines_by_choice = []
    disciplines = data.copy()
    by_choice = data[data["name"].str.contains("Дисциплины по выбору ", case=False)]
    for index, discipline in by_choice.iterrows():
        disciplines_by_choice = data[
            data["id"].notna()
            & data["id"].str.contains(discipline["id"])
            & (data["id"] != discipline["id"])
        ]["name"].to_list()

        formatted_disciplines_by_choice.append(
            fmt.as_marked_section(
                discipline["hours"] + ":", *disciplines_by_choice, marker="   ◦ "
            )
        )

        disciplines = disciplines[
            data["id"].notna()
            & ~(data["id"].notna() & data["id"].str.contains(discipline["id"]))
        ]

    disciplines = disciplines["hours"].to_list()
    if len(disciplines) > 0 or len(formatted_disciplines_by_choice) > 0:
        formatted_disciplines = fmt.as_marked_list(
            *disciplines, *formatted_disciplines_by_choice, marker="● "
        )
        return formatted_disciplines
    return fmt.Text("По таким фильтрам дисциплин нет!")


def filtered_data(
    data: pd.DataFrame,
    section: str = "Дисциплины (модули)",
    semester: int = 0,
    exam: bool = None,
    test: bool = None,
    hours: bool = False,
) -> pd.DataFrame:

    disciplines = _get_disciplines(data, section)
    disciplines = _filter_semester(disciplines, semester)
    disciplines = _filter_exams(disciplines, semester, exam)
    disciplines = _filter_tests(disciplines, semester, test)
    disciplines = _add_hours(disciplines, semester, hours)

    return disciplines


def _get_disciplines(data: pd.DataFrame, section: str) -> pd.DataFrame:
    section_index = data[data["name"] == section].index.to_list()[0]
    disciplines = []
    ind = section_index + 1
    while ind <= max(data.index.to_list()) and not pd.isna(data["id"][ind]):
        disciplines.append(data.loc[ind])
        ind += 1
    disciplines = pd.DataFrame(disciplines)
    return disciplines


def _filter_semester(data: pd.DataFrame, semester: int) -> pd.DataFrame:
    if semester == 1:
        return data[data["first_lec"].notna()]
    elif semester == 2:
        return data[data["second_lec"].notna()]
    return data


def _filter_exams(data: pd.DataFrame, semester: int, exam: bool = True) -> pd.DataFrame:
    if exam is None:
        return data
    have_exam = (lambda x: x.notna()) if exam else (lambda x: x.isna())
    if semester == 1:
        return data[have_exam(data["first_ex"])]
    elif semester == 2:
        return data[have_exam(data["second_ex"])]
    return data[(have_exam(data["first_ex"])) | (have_exam(data["second_ex"]))]


def _filter_tests(data: pd.DataFrame, semester: int, test: bool) -> pd.DataFrame:
    if test is None:
        return data
    have_test = (lambda x: x.notna()) if test else (lambda x: x.isna())
    if semester == 1:
        return data[have_test(data["first_test"])]
    elif semester == 2:
        return data[have_test(data["second_test"])]
    return data[(have_test(data["first_test"])) | (have_test(data["second_test"]))]


def _add_hours(data: pd.DataFrame, semester: int, add: bool) -> pd.DataFrame:
    if not add:
        data["hours"] = data["name"]
        return data
    if semester == 1:
        semester_string = "first"
    elif semester == 2:
        semester_string = "second"
    else:
        semester_string = "all"
    data["hours"] = (
        data["name"]
        + ": "
        + data[semester_string + "_lec"]
        + "/"
        + data[semester_string + "_prac"]
        + "/"
        + data[semester_string + "_lab"]
    )
    return data
