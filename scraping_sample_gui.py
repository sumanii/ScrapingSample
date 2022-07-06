# -*- coding: utf-8 -*-

from tkinter import Grid
import scraping_sample
import PySimpleGUI as sg
import os

fileRadioDict = {
    "0": "excel",
    "1": "csv",
}


def main():
    """
    main 関数
    """
    sg.theme("LightBlue")   # デザインテーマの設定

    # ウィンドウに配置するコンポーネント
    layout = [[sg.Text("保存先フォルダ"), sg.InputText("", enable_events=True, key="save_folder"), sg.FolderBrowse("フォルダを選択", key="save_folder_dialog")],
              [sg.Text("ファイル形式"), sg.Radio("excel", key="excel_radio", default=True, group_id="file_radio"),
               sg.Radio("csv", key="csv_radio", group_id="file_radio")],
              [sg.Checkbox("ブラウザ表示", default=True, key="browser_view")],
              [sg.Button("実行", key="exec_btn"), sg.Button("終了", key="exit_btn")]]

    # ウィンドウの生成
    window = sg.Window("スクレイピング サンプル", layout)

    # イベントループ
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "exit_btn":
            break
        elif event == "exec_btn":
            saveFolder = values["save_folder"]
            if saveFolder == "":
                sg.popup_error("保存先フォルダを指定してください")
                continue
            if os.path.isdir(saveFolder) == False:
                sg.popup_error("指定された保存先フォルダが存在しません")
                continue

            fileRadio: int
            if values["excel_radio"] == True:
                fileRadio = 0
            else:  # if values["csv_radio"] == True:
                fileRadio = 1

            # print("フォルダ: ", saveFolder)
            # print("ファイル形式: ", fileRadio)
            # print("ブラウザ非表示: ", values["browser_view"])

            scraping_sample.Search2ndBase(
                saveFolder, fileRadio, values["browser_view"])

            sg.popup("完了しました")

    window.close()


if __name__ == "__main__":
    main()
