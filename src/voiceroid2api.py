#!/usr/bin/env python3
# coding: utf-8

import pywinauto
from time import sleep, time
from os.path import realpath

MAX_COUNT = 10


class InternalError(Exception):
    pass


class VOICEROID2:
    def __init__(self):
        print("Initallizing ... ")
        # デスクトップのエレメント
        print("[{}/{}] Finding Desktop Element".format(1, 10))
        self.parentUIAElement = pywinauto.uia_element_info.UIAElementInfo()
        # voiceroidを捜索する
        print("[{}/{}] Finding VOICEROID2".format(2, 10))
        self.voiceroid2 = self.__search_child_byname(
            "VOICEROID2", self.parentUIAElement)
        # *がついている場合
        if not self.voiceroid2:
            print("[{}/{}] Finding VOICEROID2 (2)".format(3, 10))
            self.voiceroid2 = self.__search_child_byname(
                "VOICEROID2*", self.parentUIAElement)
            if not self.voiceroid2:
                raise InternalError("VOICEROID2 not found.")
        else:
            print("[{}/{}] Finding VOICEROID2 (2) (skipped)".format(3, 10))
        # テキスト要素のElementInfoを取得
        print("[{}/{}] Finding TextEditViewEle".format(4, 10))
        self.TextEditViewEle = self.__search_child_byclassname(
            "TextEditView", self.voiceroid2)
        print("[{}/{}] Finding textBoxEle".format(5, 10))
        self.textBoxEle = self.__search_child_byclassname(
            "TextBox", self.TextEditViewEle)

        # コントロール取得
        print("[{}/{}] Finding textBoxEditControl".format(6, 10))
        self.textBoxEditControl = pywinauto.controls.uia_controls.EditWrapper(
            self.textBoxEle)

        # ボタン取得
        print("[{}/{}] Finding buttonsEle".format(7, 10))
        buttonsEle = self.__search_child_byclassname(
            "Button", self.TextEditViewEle, target_all=True)

        # 再生ボタンを探す
        print("[{}/{}] Finding play button".format(8, 10))
        self.playButtonEle = None
        self.saveButtonEle = None
        for buttonEle in buttonsEle:
            # テキストブロックを捜索
            textBlockEle = self.__search_child_byclassname(
                "TextBlock", buttonEle)
            if textBlockEle.name == "再生":
                self.playButtonEle = buttonEle
            elif textBlockEle.name == "音声保存":
                self.saveButtonEle = buttonEle
            if self.playButtonEle is not None and self.saveButtonEle is not None:
                break

        # ボタンコントロール取得
        print("[{}/{}] Finding playButtonControl".format(9, 10))
        self.playButtonControl = pywinauto.controls.uia_controls.ButtonWrapper(
            self.playButtonEle)
        print("[{}/{}] Finding saveButtonControl".format(10, 10))
        self.saveButtonControl = pywinauto.controls.uia_controls.ButtonWrapper(
            self.saveButtonEle)
        print("Initallized VOICEROID2")

    def __search_child_byclassname(self, class_name, uiaElementInfo, target_all=False, count=0):
        target = list()
        # 全ての子要素検索
        for childElement in uiaElementInfo.children():
            # ClassNameの一致確認
            if childElement.class_name == class_name:
                if not target_all:
                    return childElement
                else:
                    target.append(childElement)
        if not target_all:
            if count >= MAX_COUNT:
                # 無かったらFalse
                return False
            return self.__search_child_byclassname(class_name, uiaElementInfo, target_all, count+1)
        else:
            return target

    def __search_child_byname(self, name, uiaElementInfo, count=0):
        # 全ての子要素検索
        children = uiaElementInfo.children()
        for childElement in children:
            # Nameの一致確認
            if childElement.name == name:
                return childElement
        # 無かったらFalse
        if count >= MAX_COUNT:
            return False
        return self.__search_child_byname(name, uiaElementInfo, count+1)

    def setText(self, text):
        self.textBoxEditControl.set_edit_text(text)

    def talk(self, text):
        self.setText(text)
        # 再生ボタン押下
        self.playButtonControl.click()

    def __getElementsFromFileSelector(self, fileSelector):
        DUIViewWndClassName = self.__search_child_byclassname("DUIViewWndClassName", fileSelector)
        AppControlHost = self.__search_child_byclassname("AppControlHost", DUIViewWndClassName)
        filenameText = self.__search_child_byclassname("Edit", AppControlHost)
        saveOKButton = self.__search_child_byname('保存(S)', fileSelector)
        saveOKButtonControl = pywinauto.controls.uia_controls.ButtonWrapper(saveOKButton)
        filenameTextControl = pywinauto.controls.uia_controls.EditWrapper(filenameText)
        return filenameTextControl, saveOKButtonControl

    def render(self, text, path):
        t = time()
        print("RENDER!")
        self.setText(text)
        self.saveButtonControl.click()
        saveWindow = self.__search_child_byclassname("Window", self.voiceroid2)
        okButton = self.__search_child_byname("OK", saveWindow)
        okButtonControl = pywinauto.controls.uia_controls.ButtonWrapper(okButton)
        okButtonControl.click()
        fileWindow = self.__search_child_byclassname("#32770", saveWindow)
        filenameTextControl, saveOKButtonControl = self.__getElementsFromFileSelector(fileWindow)
        filenameTextControl.set_edit_text(realpath(path))
        saveOKButtonControl.click()
        print("Render prepare time :", time()-t)
        print("Rendering ... ")
        while True:
            sleep(0.1)
            print("Confirm...", end="")
            infoDialog = self.__search_child_byname("情報", saveWindow)
            if infoDialog is not False:
                print("OK")
                break
            print("no")
        print("Rendered!")
        infoButton = self.__search_child_byname("OK", infoDialog)
        infoButtonControl = pywinauto.controls.uia_controls.ButtonWrapper(infoButton)
        infoButtonControl.click()
        print("Render time :", time()-t)


if __name__ == '__main__':
    v2 = VOICEROID2()
    v2.render("こんにちは")
