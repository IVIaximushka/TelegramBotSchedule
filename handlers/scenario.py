from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from services.keyboard import make_column_keyboard, make_keyboard_by_template
from services.parsing_tools import (filtered_data, format_disciplines,
                                    get_sections, parse_html_table)
from services.web_tools import (begin_connection, end_connection, get_courses,
                                get_faculties, get_html_table,
                                get_specialities, get_study_plans, push_button,
                                set_course, set_faculty, set_speciality,
                                set_study_plan)

router = Router()


FILTERS = [
    ["1 семестр", "2 семестр", "Все семестры"],
    ["С экзаменом", "Без экзамена", "Без фильтра по экзамену"],
    ["С зачётом", "Без зачёта", "Без фильтра по зачёту"],
    ["Показать количество часов", "Убрать количество часов"],
    ["⎌ Вернуться к выбору предметной секции"],
]


class StudyPlanStates(StatesGroup):
    choosing_first_faculty = State()
    choosing_second_faculty = State()
    choosing_third_faculty = State()
    choosing_speciality = State()
    choosing_study_plan = State()
    choosing_course = State()


class TableStates(StatesGroup):
    choose_discipline = State()
    choose_filter = State()


@router.message(Command(commands=["study_plan"]))
async def cmd_study_plan(message: Message, state: FSMContext):
    user_data = await state.get_data()
    if "driver" in user_data and user_data["driver"] is not None:
        end_connection(user_data["driver"])
    await state.clear()

    driver = begin_connection()
    await state.update_data(driver=driver)

    faculties = get_faculties(driver)
    await state.update_data(faculties=faculties)

    await message.answer(
        text="Выберите интересующее подразделение университета",
        reply_markup=make_column_keyboard(list(map(lambda x: x[0], faculties.keys()))),
    )
    await state.set_state(StudyPlanStates.choosing_first_faculty)


@router.message(StudyPlanStates.choosing_first_faculty)
async def choose_first_faculty(message: Message, state: FSMContext):
    user_data = await state.get_data()
    faculties = user_data["faculties"]

    if (message.text, 1) in faculties:
        first_faculty = (message.text, 1)
        await state.update_data(first_faculty=first_faculty)

        second_faculties = faculties[first_faculty]
        await message.answer(
            text="Выберите интересующий институт университета",
            reply_markup=make_column_keyboard(
                list(map(lambda x: x[0], second_faculties.keys()))
            ),
        )
        await state.set_state(StudyPlanStates.choosing_second_faculty)
    else:
        await message.answer(
            text="Извините, но такого подразделения нет. Выберите интересующее подразделение университета",
            reply_markup=make_column_keyboard(
                list(map(lambda x: x[0], faculties.keys()))
            ),
        )


@router.message(StudyPlanStates.choosing_second_faculty)
async def choose_second_faculty(message: Message, state: FSMContext):
    user_data = await state.get_data()
    faculties = user_data["faculties"]
    first_faculty = user_data["first_faculty"]

    if (message.text, 2) in faculties[first_faculty]:
        second_faculty = (message.text, 2)
        await state.update_data(second_faculty=second_faculty)

        third_faculties = faculties[first_faculty][second_faculty]
        if len(third_faculties) > 0:
            await message.answer(
                text="Выберите интересующее отделение института",
                reply_markup=make_column_keyboard(
                    list(map(lambda x: x[0], third_faculties))
                ),
            )
            await state.set_state(StudyPlanStates.choosing_third_faculty)
        else:
            driver = user_data["driver"]
            set_faculty(driver, second_faculty)
            specialities = get_specialities(driver)
            await message.answer(
                text="Отлично, мы определились с институтом! Теперь выберите направление подготовки",
                reply_markup=make_column_keyboard(specialities),
            )
            await state.set_state(StudyPlanStates.choosing_speciality)
    else:
        await message.answer(
            text="Извините, но такого института нет. Выберите интересующий институт университета",
            reply_markup=make_column_keyboard(
                list(map(lambda x: x[0], faculties[first_faculty].keys()))
            ),
        )


@router.message(StudyPlanStates.choosing_third_faculty)
async def choose_third_faculty(message: Message, state: FSMContext):
    user_data = await state.get_data()
    faculties = user_data["faculties"]
    first_faculty = user_data["first_faculty"]
    second_faculty = user_data["second_faculty"]

    if (message.text, 3) in faculties[first_faculty][second_faculty]:
        third_faculty = (message.text, 3)
        await state.update_data(third_faculty=third_faculty)

        driver = user_data["driver"]
        set_faculty(driver, third_faculty)
        specialities = get_specialities(driver)
        await message.answer(
            text="Отлично, мы определились с отделением института! Теперь выберите направление подготовки",
            reply_markup=make_column_keyboard(specialities),
        )
        await state.set_state(StudyPlanStates.choosing_speciality)
    else:
        await message.answer(
            text="Извините, но такого отделения нет. Выберите интересующее отделение института",
            reply_markup=make_column_keyboard(
                list(map(lambda x: x[0], faculties[first_faculty][second_faculty]))
            ),
        )


@router.message(StudyPlanStates.choosing_speciality)
async def choose_speciality(message: Message, state: FSMContext):
    user_data = await state.get_data()
    driver = user_data["driver"]
    specialities = get_specialities(driver)

    if message.text in specialities:
        speciality = message.text
        await state.update_data(speciality=speciality)

        set_speciality(driver, speciality)
        study_plans = get_study_plans(driver)
        await message.answer(
            text="Так держать! Теперь выберите интересующий учебный план",
            reply_markup=make_column_keyboard(study_plans),
        )
        await state.set_state(StudyPlanStates.choosing_study_plan)
    else:
        await message.answer(
            text="Извините, но такого направления нет. Выберите интересующее направление подготовки",
            reply_markup=make_column_keyboard(specialities),
        )


@router.message(StudyPlanStates.choosing_study_plan)
async def choose_study_plan(message: Message, state: FSMContext):
    user_data = await state.get_data()
    driver = user_data["driver"]
    study_plans = get_study_plans(driver)

    if message.text in study_plans:
        study_plan = message.text
        await state.update_data(study_plan=study_plan)

        set_study_plan(driver, study_plan)
        courses = get_courses(driver)
        await message.answer(
            text="Осталось только выбрать курс, и можно начать строить план)",
            reply_markup=make_column_keyboard(courses),
        )
        await state.set_state(StudyPlanStates.choosing_course)
    else:
        await message.answer(
            text="Извините, но такого учебного плана нет. Выберите интересующий учебный план",
            reply_markup=make_column_keyboard(study_plans),
        )


@router.message(StudyPlanStates.choosing_course)
async def choose_course(message: Message, state: FSMContext):
    user_data = await state.get_data()
    driver = user_data["driver"]
    courses = get_courses(driver)

    if message.text in courses:
        course = message.text
        await state.update_data(course=course)

        set_course(driver, course)
        push_button(driver)
        html_table = get_html_table(driver)
        end_connection(driver)
        await state.update_data(driver=None)

        data_frame = parse_html_table(html_table)
        await state.update_data(data_frame=data_frame)

        sections = get_sections(data_frame)
        await message.answer(
            text="Теперь определитесь с предметной секцией",
            reply_markup=make_column_keyboard(sections + ['⎌ Выбрать другое подразделение университета']),
        )
        await state.set_state(TableStates.choose_discipline)
    else:
        await message.answer(
            text="Извините, но такого курса нет. Выберите интересующий курс обучения",
            reply_markup=make_column_keyboard(courses),
        )


@router.message(TableStates.choose_discipline)
async def choose_section(message: Message, state: FSMContext):
    user_data = await state.get_data()
    sections = get_sections(user_data["data_frame"])

    if message.text in sections:
        section = message.text
        await state.update_data(section=section)
        await state.update_data(semester=0)
        await state.update_data(exam=None)
        await state.update_data(test=None)
        await state.update_data(hours=False)
        user_data = await state.get_data()
        await message.answer(
            text="Учебный план готов!",
        )
        study_plan = format_disciplines(
            filtered_data(
                user_data["data_frame"],
                user_data["section"],
                user_data["semester"],
                user_data["exam"],
                user_data["test"],
                user_data["hours"],
            )
        )
        await message.answer(**study_plan.as_kwargs())
        await message.answer(
            text="Можете выбрать фильтры на учебный план\n\n"
                 "Часы указаны в формате(лекции/практики/лабораторные)",
            reply_markup=make_keyboard_by_template(FILTERS),
        )
        await state.set_state(TableStates.choose_filter)
    elif message.text == '⎌ Выбрать другое подразделение университета':
        user_data = await state.get_data()
        if "driver" in user_data and user_data["driver"] is not None:
            end_connection(user_data["driver"])
        await state.clear()

        driver = begin_connection()
        await state.update_data(driver=driver)

        faculties = get_faculties(driver)
        await state.update_data(faculties=faculties)

        await message.answer(
            text="Выберите интересующее подразделение университета",
            reply_markup=make_column_keyboard(list(map(lambda x: x[0], faculties.keys()))),
        )
        await state.set_state(StudyPlanStates.choosing_first_faculty)
    else:
        await message.answer(
            text="Извините, но такой секции нет. Выберите интересующую предметную секцию",
            reply_markup=make_column_keyboard(sections + ['⎌ Выбрать другое подразделение университета']),
        )


@router.message(TableStates.choose_filter)
async def choose_filter(message: Message, state: FSMContext):
    if message.text in FILTERS[0]:
        semester = message.text
        await state.update_data(
            semester=int(semester[0]) if semester[0].isdigit() else 0
        )
    elif message.text in FILTERS[1]:
        exam = message.text
        if exam == FILTERS[1][0]:
            exam = True
        elif exam == FILTERS[1][1]:
            exam = False
        else:
            exam = None
        await state.update_data(exam=exam)
    elif message.text in FILTERS[2]:
        test = message.text
        if test == FILTERS[2][0]:
            test = True
        elif test == FILTERS[2][1]:
            test = False
        else:
            test = None
        await state.update_data(test=test)
    elif message.text in FILTERS[3]:
        hours = message.text
        if hours == FILTERS[3][0]:
            hours = True
        else:
            hours = False
        await state.update_data(hours=hours)

    if message.text in FILTERS[-1]:
        user_data = await state.get_data()
        sections = get_sections(user_data["data_frame"])
        await message.answer(
            text="Теперь определитесь с предметной секцией",
            reply_markup=make_column_keyboard(sections + ['⎌ Выбрать другое подразделение университета']),
        )
        await state.set_state(TableStates.choose_discipline)
    else:
        user_data = await state.get_data()
        study_plan = format_disciplines(
            filtered_data(
                user_data["data_frame"],
                user_data["section"],
                user_data["semester"],
                user_data["exam"],
                user_data["test"],
                user_data["hours"],
            )
        )
        await message.answer(**study_plan.as_kwargs())
        await message.answer(text="Можете выбрать ещё фильтры")
