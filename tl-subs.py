import argparse
import os

from playwright.sync_api import sync_playwright

SUPPORTED_LANGUAGES = [
    'nl', 'af', 'sq', 'am', 'ar', 'hy', 'as', 'ay', 'az', 'bm', 'eu', 'be', 'bn', 'bho', 'my', 'bs', 'bg', 'ca', 'ceb',
    'ny', 'zh-TW', 'zh-CN', 'co', 'da', 'dv', 'doi', 'de', 'en', 'eo', 'et', 'ee', 'fi', 'fr', 'fy', 'gl', 'ka', 'el',
    'gn', 'gu', 'ht', 'ha', 'haw', 'iw', 'hi', 'hmn', 'hu', 'ga', 'ig', 'is', 'ilo', 'id', 'it', 'ja', 'jw', 'yi', 'kn',
    'kk', 'km', 'rw', 'ky', 'ku', 'ckb', 'gom', 'ko', 'kri', 'hr', 'lo', 'la', 'lv', 'ln', 'lt', 'lg', 'lb', 'mk', 'sv',
    'mai', 'mg', 'ml', 'ms', 'mt', 'mi', 'mr', 'lus', 'mn', 'ne', 'no', 'or', 'ug', 'uk', 'uz', 'om', 'ps', 'fa', 'pl',
    'pt', 'pa', 'qu', 'ro', 'ru', 'sm', 'sa', 'gd', 'nso', 'sr', 'st', 'sn', 'sd', 'si', 'sk', 'sl', 'su', 'so', 'es',
    'sw', 'tg', 'tl', 'ta', 'tt', 'te', 'th', 'ti', 'cs', 'ts', 'tk', 'tr', 'ak', 'ur', 'vi', 'cy', 'xh', 'yo', 'zu'
]
SUPPORTED_EXTENSIONS = ['.srt', '.sub', '.sbv', '.ass', '.vtt', '.stl']

description = 'Translate subtitles using https://translatesubtitles.co into any language.'
file_path_help = 'Path to the subtitle file to translate'
output_dir_help = 'Path to the directory to save the translated file to'
target_lang_help = 'Language to translate the subtitles into'


def format_list(input: list, max_width=115) -> str:
    lines, line = [], ''
    for item in input:
        line += item + ', '
        if len(line) >= max_width:
            lines.append(line[:-2])
            line = ''
    lines.append(line[:-2])

    if len(lines) > 1:
        output = '\n   '.join(lines)
    else:
        output = lines[0]
    return f'  [{output}]'


def validate_args(file_path: str, output_dir: str, target_lang: str):
    _, file_extension = os.path.splitext(file_path)
    if not os.path.exists(file_path):
        print(f"Error: Given subtitle file '{file_path}' does not exist")
        exit(1)
    if file_extension not in SUPPORTED_EXTENSIONS:
        print(f"Error: Invalid file extension. Supported file extensions are: \n{format_list(SUPPORTED_EXTENSIONS)}")
        exit(1)
    if not target_lang.lower() in SUPPORTED_LANGUAGES:
        print(f"Error: Invalid target language. Supported target languages are: \n{format_list(SUPPORTED_LANGUAGES)}")
        exit(1)
    if not os.path.exists(output_dir):
        print(f"Error: Given output directory '{output_dir}' does not exist")
        exit(1)


def main(file_path: str, output_dir: str, target_lang: str):
    validate_args(file_path, output_dir, target_lang)
    file_name, file_ext = os.path.splitext(os.path.basename(file_path))
    output_file = f'{file_name}.tl.{target_lang}{file_ext}'

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        page.goto('https://translatesubtitles.co/')

        # Upload file
        page.set_input_files('input[type=file]', file_path)
        popup_div = page.wait_for_selector('.popup-vip.notranslate')
        close_link = popup_div.wait_for_selector('a.close')
        close_link.click()

        # Translate
        language_select = page.locator('.goog-te-combo')
        language_select.select_option(target_lang)
        page.get_by_text("1. Translate ").click()
        page.wait_for_function('() => document.querySelector("#loader").style.display === "none"')

        # Download
        with page.expect_download() as download_info:
            page.get_by_text("2. Download ").click()
        download = download_info.value
        download.save_as(os.path.join(output_dir, output_file))

        browser.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('file_path', help=file_path_help)
    parser.add_argument('-o', '--output-dir', help=output_dir_help, default=os.getcwd())
    parser.add_argument('-l', '--target-lang', help=target_lang_help, default='nl')
    args = parser.parse_args()

    main(args.file_path, args.output_dir, args.target_lang)
