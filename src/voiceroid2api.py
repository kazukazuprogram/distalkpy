#!/usr/bin/env python3
# coding: utf-8

import pywinauto
from time import sleep, time
from os.path import realpath

MAX_COUNT = 10


class VOICEROID2:
    def __init__(self):
        # デスクトップのエレメント
        self.parentUIAElement = pywinauto.uia_element_info.UIAElementInfo()
        # voiceroidを捜索する
        self.voiceroid2 = self.search_child_byname(
            "VOICEROID2", self.parentUIAElement)
        # *がついている場合
        if not self.voiceroid2:
            self.voiceroid2 = self.search_child_byname(
                "VOICEROID2*", self.parentUIAElement)

        # テキスト要素のElementInfoを取得
        self.TextEditViewEle = self.search_child_byclassname(
            "TextEditView", self.voiceroid2)
        self.textBoxEle = self.search_child_byclassname(
            "TextBox", self.TextEditViewEle)

        # コントロール取得
        self.textBoxEditControl = pywinauto.controls.uia_controls.EditWrapper(
            self.textBoxEle)

        # ボタン取得
        buttonsEle = self.search_child_byclassname(
            "Button", self.TextEditViewEle, target_all=True)

        # 再生ボタンを探す
        self.playButtonEle = None
        self.saveButtonEle = None
        for buttonEle in buttonsEle:
            # テキストブロックを捜索
            textBlockEle = self.search_child_byclassname(
                "TextBlock", buttonEle)
            if textBlockEle.name == "再生":
                self.playButtonEle = buttonEle
            elif textBlockEle.name == "音声保存":
                self.saveButtonEle = buttonEle
            if self.playButtonEle is not None and self.saveButtonEle is not None:
                break

        # ボタンコントロール取得
        self.playButtonControl = pywinauto.controls.uia_controls.ButtonWrapper(
            self.playButtonEle)
        self.saveButtonControl = pywinauto.controls.uia_controls.ButtonWrapper(
            self.saveButtonEle)

    def search_child_byclassname(self, class_name, uiaElementInfo, target_all=False, count=0):
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
            return self.search_child_byclassname(class_name, uiaElementInfo, target_all, count+1)
        else:
            return target

    def search_child_byname(self, name, uiaElementInfo, count=0):
        # 全ての子要素検索
        for childElement in uiaElementInfo.children():
            # Nameの一致確認
            if childElement.name == name:
                return childElement
        # 無かったらFalse
        if count >= MAX_COUNT:
            return False
        return self.search_child_byname(name, uiaElementInfo, count+1)

    def setText(self, text):
        self.textBoxEditControl.set_edit_text(text)

    def talk(self, text):
        self.setText(text)
        # 再生ボタン押下
        self.playButtonControl.click()

    def getElementsFromFileSelector(self, fileSelector):
        DUIViewWndClassName = self.search_child_byclassname("DUIViewWndClassName", fileSelector)
        AppControlHost = self.search_child_byclassname("AppControlHost", DUIViewWndClassName)
        filenameText = self.search_child_byclassname("Edit", AppControlHost)
        saveOKButton = self.search_child_byname('保存(S)', fileSelector)
        saveOKButtonControl = pywinauto.controls.uia_controls.ButtonWrapper(saveOKButton)
        filenameTextControl = pywinauto.controls.uia_controls.EditWrapper(filenameText)
        return filenameTextControl, saveOKButtonControl

    def render(self, text, path):
        t = time()
        print("RENDER!")
        self.setText(text)
        self.saveButtonControl.click()
        saveWindow = self.search_child_byclassname("Window", self.voiceroid2)
        okButton = self.search_child_byname("OK", saveWindow)
        okButtonControl = pywinauto.controls.uia_controls.ButtonWrapper(okButton)
        okButtonControl.click()
        fileWindow = self.search_child_byclassname("#32770", saveWindow)
        filenameTextControl, saveOKButtonControl = self.getElementsFromFileSelector(fileWindow)
        filenameTextControl.set_edit_text(realpath(path))
        saveOKButtonControl.click()
        print("Render prepare time :", time()-t)
        print("Rendering ... ")
        while True:
            sleep(0.1)
            print("Confirm...", end="")
            infoDialog = self.search_child_byname("情報", saveWindow)
            if infoDialog is not False:
                print("OK")
                break
            print("no")
        print("Rendered!")
        infoButton = self.search_child_byname("OK", infoDialog)
        infoButtonControl = pywinauto.controls.uia_controls.ButtonWrapper(infoButton)
        infoButtonControl.click()
        print("Render time :", time()-t)
