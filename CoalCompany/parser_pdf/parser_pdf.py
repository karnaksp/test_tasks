"""
Praser PDF data for testing on Data Analytics position
"""

import os
import re
import xlsxwriter
import PyPDF2
from colorama import Fore, Style


compiled = {}

#######################################################################################
#######################################################################################
ENDFLAG = "FO=Full"
TRANSMITTALPATTERN = r"КИЙЗАССКИЙ БЛОК №(\d+).*\.pdf"
TRANSMITTALPATTERN2 = r"Кийзасский №(\d+).*\.pdf"
TRANSMITTALPATTERN3 = r"Кийзасский блок №(\d+).*\.pdf"
BLOCK_NUMBER = None
DATA_BUM = None
FACE_EXCAVATOR = r"Забой экскаватора ([\w\s]+)1\.3"
DATE_PATTERN = r"([0-9]{1,2})/([0-9]{1,2})/([0-9]{2,4})"
STRENGTH = r"Максимальная крепость пород по Протодъяконову : f= (\d+)"
HORIZON = r"горизонт, м (\+\d+\+\d+)"
PROFLINES = r"профильные линии (\d+\-\d+)"
V_BLOCK = r"3. ОЖИДАЕМЫЙ ОБЪЕМ ВЗОРВАННОЙ ГОРНОЙ МАССЫ (\d+\s\d+)"
V_DRILLING = r"ОБЪЕМ БУРЕНИЯ (\d+\s\d+)"
NUM_WELL = r"КОЛИЧЕСТВО СКВАЖИН (\d+)"
CONS_EXP = r"РЗУ.*?=.*?(\d+\s\d+,\d+)"
CONS_EXP0 = r"21. Дополнительные средства используемые при заряжании и забойке скважин: (\d+\s\d+,\d+)"
CONS_EXP2 = r"Скважинная сеть(\d+\s\d+,\d+)"
CONS_EXP3 = r"(\d+\s\d+,\d+)\n\d+,\d+\n15. Предполагаемый расход средств инициирования по наименованиям:"
NITRONIT = r"\nНитронит (\d+,\d+)"
GRANULIT = r"\nГранулит.*?(\d+,\d+)"
DETONATORS = r"РЗУ.*?=.*?\d+\s\d+,\d+\n(\d+,\d+)"
DETONATORS0 = r"21. Дополнительные средства используемые при заряжании и забойке скважин: \d+\s\d+,\d+\n(\d+,\d+)"
DETONATORS2 = r"Скважинная сеть\d[\d\s.,]*\b\n(\d+,\d+)"
DETONATORS3 = (
    r"(\d+,\d+)\n15\. Предполагаемый расход средств инициирования по наименованиям:"
)
SPEC_CONS_EXP = r"УДЕЛЬНЫЙ РАСХОД ВЗРЫВЧАТЫХ МАТЕРИАЛОВ (\d+,\d+)"
SPEC_CONS_EXP_T = (
    r"УДЕЛЬНЫЙ РАСХОД ВЗРЫВЧАТЫХ МАТЕРИАЛОВ В ТРОТИЛОВОМ ЭКВИВАЛЕНТЕ (\d+,\d+)"
)
INTERVAL_DECLARATION = r"Интервал замедлений (\d+,.*?\d+)"
INTERVAL_DECLARATION0 = r"Интервал замедлений (\d+)"
NET_WELLS = r"Сетка расположения скважин (\d+ х \d+ м)"
HEIGHT_UP = r"высота уступа, м (\d+)"
SRC_PATH = os.getcwd()
DEST_PATH = SRC_PATH
#######################################################################################
#######################################################################################


def get_valid_directory(prompt, default_path=None):
    """
    Prompt the user to input a valid directory path.
    """
    if default_path and os.path.exists(default_path):
        while True:
            use_default = input(
                f"Use default directory '{default_path}'? (y/n): "
            ).lower()
            if use_default == "y":
                return default_path
            elif use_default == "n":
                break
            else:
                print("Please enter 'y' or 'n'.")

    directory = input(prompt)
    while not os.path.exists(directory):
        directory = input("Directory doesn't exist. Please enter a valid directory: ")
    return directory


def file_scrape(root_path):
    """
    Function to recursively scrape files in the given root path, identifying PDF files matching specific patterns and collecting data from them.
    :param root_path: The root path from which to start the file scraping process
    :return: None
    """
    for f in os.listdir(root_path):
        if (
            os.path.isfile(os.path.join(root_path, f))
            & f.endswith("pdf")
            & (
                (re.match(TRANSMITTALPATTERN, f) is not None)
                or (re.match(TRANSMITTALPATTERN2, f) is not None)
                or (re.match(TRANSMITTALPATTERN3, f) is not None)
            )
        ):
            print(Fore.GREEN + "file " + f + Style.RESET_ALL)
            global BLOCK_NUMBER, DATA_BUM
            BLOCK_NUMBER = str(re.search(r"№(\S+)", f).group())
            data_b = re.search(r"\b\d{2}\.\d{2}\.\d{4}\b", f)
            DATA_BUM = data_b.group() if data_b else ""
            pdf_data_collect(os.path.join(root_path, f), f)
        elif os.path.isdir(os.path.join(root_path, f)):
            print(Fore.YELLOW + "dir: " + f + "\n" + Style.RESET_ALL)
            file_scrape(os.path.join(root_path, f))


def calculate_avg(numbers_array):
    """
    Calculate the results based on the given numbers_array.

    Args:
        numbers_array (list): A list of strings representing the numbers to be calculated.

    Returns:
        tuple: A tuple containing the calculated results for deep well, D well, L fillers, and L stoppings.
    """
    deep_wells = []
    d_wells = []
    l_fillers = []
    l_stoppings = []
    m_wells = []
    ninth_numbers_sum = []
    for line in numbers_array:
        split_matches = line.split("\n")
        for line in split_matches:
            numbers = line.split()
            if len(numbers) == 10:
                deep_well = float(numbers[0].replace(",", ".")) * float(
                    numbers[8].replace(",", ".")
                )
                d_well = float(numbers[1].replace(",", ".")) * float(
                    numbers[8].replace(",", ".")
                )
                m_well = float(numbers[2].replace(",", ".")) * float(
                    numbers[8].replace(",", ".")
                )
                l_filler = float(numbers[5].replace(",", ".")) * float(
                    numbers[8].replace(",", ".")
                )
                l_stopping = float(numbers[6].replace(",", ".")) * float(
                    numbers[8].replace(",", ".")
                )

                deep_wells.append(deep_well)
                d_wells.append(d_well)
                m_wells.append(m_well)
                l_fillers.append(l_filler)
                l_stoppings.append(l_stopping)

                ninth_number_sum = float(numbers[8].replace(",", "."))
                ninth_numbers_sum.append(ninth_number_sum)

    sum_deep_well = sum(deep_wells)
    sum_d_well = sum(d_wells)
    sum_m_well = sum(m_wells)
    sum_l_fillers = sum(l_fillers)
    sum_l_stoppings = sum(l_stoppings)
    total_ninth_sum = sum(ninth_numbers_sum)

    result_deep_well = sum_deep_well / total_ninth_sum
    result_d_well = sum_d_well / total_ninth_sum
    resilt_m_well = sum_m_well / total_ninth_sum
    result_l_fillers = sum_l_fillers / total_ninth_sum
    result_l_stoppings = sum_l_stoppings / total_ninth_sum

    return (
        result_deep_well,
        result_d_well,
        resilt_m_well,
        result_l_fillers,
        result_l_stoppings,
    )


def pdf_data_collect(pdf_path, f):
    """
    Collect data from a PDF file and store it in a dictionary with various attributes.

    Parameters:
    - pdf_path: str, the path to the PDF file
    - f: str, the file name

    Returns:
    - None
    """
    word_arr = []
    newword_arr = []

    pdf_reader = PyPDF2.PdfReader(open(pdf_path, "rb"))

    for page_obj in pdf_reader.pages:
        word_arr += page_obj.extract_text().splitlines()

    newword_arr = "\n".join(word_arr)

    numbers_array = re.findall(
        r"\nзабойки\n(.*?)(?=\n[А-Яа-яЁё])", newword_arr, re.DOTALL
    )

    try:
        (
            result_deep_well,
            result_d_well,
            resilt_m_well,
            result_l_fillers,
            result_l_stoppings,
        ) = calculate_avg(numbers_array)
    except Exception as e:
        print("An error occurred:", e)
        print(Fore.RED + "Teble not found!!!" + "\n" + Style.RESET_ALL)
        result_deep_well = result_d_well = resilt_m_well = result_l_fillers = (
            result_l_stoppings
        ) = ""

    strength = re.search(STRENGTH, newword_arr)
    strength = strength.group(1) if strength else ""

    excavator = re.search(FACE_EXCAVATOR, newword_arr)
    excavator = excavator.group(1) if excavator else ""

    horizon = re.search(HORIZON, newword_arr)
    horizon = horizon.group(1) if horizon else ("")

    proflines = re.search(PROFLINES, newword_arr)
    proflines = proflines.group(1) if proflines else ("")

    v_block = re.search(V_BLOCK, newword_arr)
    v_block = v_block.group(1) if v_block else ""

    v_drilling = re.search(V_DRILLING, newword_arr)
    v_drilling = v_drilling.group(1) if v_drilling else ""

    num_well = re.search(NUM_WELL, newword_arr)
    num_well = num_well.group(1) if num_well else ""

    cons_exp = re.search(CONS_EXP0, newword_arr)
    if not cons_exp:
        cons_exp = re.search(CONS_EXP, newword_arr)
        if not cons_exp:
            cons_exp = re.search(CONS_EXP2, newword_arr)
            if not cons_exp:
                cons_exp = re.search(CONS_EXP3, newword_arr)
    cons_exp = cons_exp.group(1) if cons_exp else ""

    nitronit = re.search(NITRONIT, newword_arr)
    nitronit = nitronit.group(1) if nitronit else ""

    granulit = re.search(GRANULIT, newword_arr)
    granulit = granulit.group(1) if granulit else ""

    detonators = re.search(DETONATORS0, newword_arr)
    if not detonators:
        detonators = re.search(DETONATORS, newword_arr)
        if not detonators:
            detonators = re.search(DETONATORS2, newword_arr)
            if not detonators:
                detonators = re.search(DETONATORS3, newword_arr)
    detonators = detonators.group(1) if detonators else ""

    spec_cons_exp = re.search(SPEC_CONS_EXP, newword_arr)
    spec_cons_exp = spec_cons_exp.group(1) if spec_cons_exp else ""

    spec_cons_exp_t = re.search(SPEC_CONS_EXP_T, newword_arr)
    spec_cons_exp_t = spec_cons_exp_t.group(1) if spec_cons_exp_t else ""

    net_well = re.search(NET_WELLS, newword_arr)
    net_well = net_well.group(1) if net_well else ""

    h_up = re.search(HEIGHT_UP, newword_arr)
    h_up = h_up.group(1) if h_up else ""

    interval_declaration = re.search(INTERVAL_DECLARATION, newword_arr)
    if not interval_declaration:
        interval_declaration = re.search(INTERVAL_DECLARATION0, newword_arr)
    interval_declaration = interval_declaration.group(1) if interval_declaration else ""

    name_key = f[:-4]
    compiled[name_key] = {
        "block_number": BLOCK_NUMBER,
        "tname": pdf_path,
        "excavator": excavator,
        "strength": strength,
        "horizon": horizon,
        "proflines": proflines,
        "data_bum": DATA_BUM,
        "v_block": v_block,
        "v_drilling": v_drilling,
        "num_well": num_well,
        "cons_exp": cons_exp,
        "nitronit": nitronit,
        "granulit": granulit,
        "detonators": detonators,
        "spec_cons_exp": spec_cons_exp,
        "spec_cons_exp_t": spec_cons_exp_t,
        "interval_declaration": interval_declaration,
        # "text_body": newword_arr,
        "result_deep_well": result_deep_well,
        "result_d_well": result_d_well,
        "result_m_well": resilt_m_well,
        "result_l_fillers": result_l_fillers,
        "result_l_stoppings": result_l_stoppings,
        "net_well": net_well,
        "h_up": h_up,
    }


def main():
    """
    Main function to scrape PDF files from a source directory,
    collect data, and write it to an Excel file.
    """
    print("Choose your source directory directory")
    src_path = get_valid_directory("SET SCRAPING SOURCE DIRECTORY: ", SRC_PATH)
    print("Choose your output directory")
    dest_path = get_valid_directory("SET OUTPUT DIRECTORY: ", DEST_PATH)
    row = 1
    file_scrape(src_path)

    # excel
    book = xlsxwriter.Workbook(dest_path + "\\PDF_Dump.xlsx")
    link_format = book.add_format({"color": "blue"})
    sh = book.add_worksheet()

    # Setting the header
    headers = [
        "Блок №",
        "Имя файла",
        "Экскаватор",
        "Крепость",
        "Горизонт",
        "Профлинии",
        "Дата взрыва",
        "Объем блока",
        "Объем бурения",
        "Количество скважин",
        "Расход ВВ, всего",
        "В том числе Нитронит",
        "В том числе Гранулит",
        "В том числе Детонаторы",
        "Уд. расход ВВ",
        "Уд. расход ВВ в тротилле",
        "Интервал замедлений",
        # "Text Body",
        "Средняя глубина скважины",
        "Средний диаметр скважины",
        "Средняя масса скважины заряда",
        "Средняя длина заряда",
        "Средняя длина забойки",
        "Сетка бурения",
        "Высота уступа",
    ]

    for transmittal_key, data in compiled.items():
        # print("processing " + transmittal_key + "...")
        data_values = list(data.values())
        for col_idx, col_name in enumerate(headers):
            sh.write(0, col_idx, col_name)
            if col_idx == 1:
                sh.write_url(
                    row,
                    col_idx,
                    data["tname"],
                    link_format,
                    transmittal_key,
                )
            else:
                sh.write(row, col_idx, data_values[col_idx])
        row += 1

    book.close()
    print("Completed")
    input("press any key to exit")


if __name__ == "__main__":
    main()
