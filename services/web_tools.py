from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


def begin_connection() -> webdriver.Chrome:
    driver = webdriver.Chrome()
    driver.get("https://shelly.kpfu.ru/e-ksu/study_plan_for_web")
    return driver


def end_connection(driver: webdriver.Chrome) -> None:
    driver.quit()


def get_faculties(driver: webdriver.Chrome) -> dict:
    faculty_element = Select(driver.find_element(By.NAME, "p_faculty"))
    faculty_list = list(map(lambda x: x.text, faculty_element.options))
    faculties = {}
    first, second, third = "", "", ""
    for faculty in faculty_list:
        if " " * 12 in faculty:
            third = faculty.strip()
            faculties[(first, 1)][(second, 2)].append((third, 3))
        elif " " * 8 in faculty:
            second = faculty.strip()
            faculties[(first, 1)][(second, 2)] = []
        else:
            first = faculty.strip()
            faculties[(first, 1)] = {}
    return faculties


def set_faculty(driver: webdriver.Chrome, faculty: tuple[str, int]) -> None:
    faculty_element = Select(driver.find_element(By.NAME, "p_faculty"))
    faculty_element.select_by_visible_text(" " * faculty[1] + faculty[0])


def get_specialities(driver: webdriver.Chrome) -> list:
    speciality_element = Select(driver.find_element(By.NAME, "p_speciality"))
    speciality_list = list(map(lambda x: x.text, speciality_element.options))
    return speciality_list


def set_speciality(driver: webdriver.Chrome, speciality: str) -> None:
    speciality_element = Select(driver.find_element(By.NAME, "p_speciality"))
    speciality_element.select_by_visible_text(speciality)


def get_study_plans(driver: webdriver.Chrome) -> list:
    study_plan_element = Select(driver.find_element(By.NAME, "p_sp"))
    study_plan_list = list(map(lambda x: x.text, study_plan_element.options))
    return study_plan_list


def set_study_plan(driver: webdriver.Chrome, study_plan: str) -> None:
    study_plan_element = Select(driver.find_element(By.NAME, "p_sp"))
    study_plan_element.select_by_visible_text(study_plan)


def get_courses(driver: webdriver.Chrome) -> list:
    course_element = Select(driver.find_element(By.NAME, "p_course"))
    course_list = list(map(lambda x: x.text, course_element.options))
    return course_list


def set_course(driver: webdriver.Chrome, course: str) -> None:
    course_element = Select(driver.find_element(By.NAME, "p_course"))
    course_element.select_by_visible_text(course)


def push_button(driver: webdriver.Chrome) -> None:
    button = driver.find_element(By.XPATH, "//input[@value='Выбрать']")
    button.click()


def get_html_table(driver: webdriver.Chrome) -> None:
    html_table = driver.find_element(By.CLASS_NAME, "T_TABLE")
    return html_table.get_attribute("innerHTML")
