# -*- coding: utf-8 -*-
__version__ = "1.0.0"

import os
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

from kivy.app import App
from kivy.clock import mainthread
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.utils import platform


class SmartFinderApp(App):
    title = "Smart Finder Pro"

    def build(self):
        root = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(10))

        title = Label(
            text="Smart Finder Pro - بحث داخل ملفات Word",
            font_size="22sp", bold=True,
            size_hint_y=None, height=dp(55),
            halign="center",
        )
        root.add_widget(title)

        self.file_label = Label(
            text="لم يتم اختيار ملف Word",
            size_hint_y=None, height=dp(45),
            halign="center", valign="middle",
        )
        self.file_label.bind(size=self._update_text_size)
        root.add_widget(self.file_label)

        choose_btn = Button(
            text="اختيار ملف Word (.docx)",
            size_hint_y=None, height=dp(52),
        )
        choose_btn.bind(on_release=self.choose_docx)
        root.add_widget(choose_btn)

        self.text_input = TextInput(
            hint_text="اكتب الكلمة أو العبارة التي تريد البحث عنها...",
            multiline=False, size_hint_y=None, height=dp(52),
            halign="right",
        )
        root.add_widget(self.text_input)

        search_btn = Button(
            text="بدء البحث",
            size_hint_y=None, height=dp(58),
        )
        search_btn.bind(on_release=self.search_in_word)
        root.add_widget(search_btn)

        scroll = ScrollView(size_hint=(1, 1))
        self.result_label = Label(
            text="جاهز. اختر ملف Word ثم اكتب كلمة البحث.",
            font_size="16sp", halign="right", valign="top",
            size_hint_y=None,
        )
        self.result_label.bind(
            texture_size=lambda instance, value:
            setattr(instance, "height", max(value[1] + dp(20), dp(100)))
        )
        self.result_label.bind(size=self._update_text_size)
        scroll.add_widget(self.result_label)
        root.add_widget(scroll)

        self.selected_file = None
        self._chooser = None
        return root

    def _update_text_size(self, instance, _value):
        instance.text_size = (instance.width - dp(10), None)

    @mainthread
    def set_status(self, text):
        self.result_label.text = text

    def choose_docx(self, *_args):
        if platform == "android":
            try:
                from androidstorage4kivy import Chooser
                self._chooser = Chooser(self._android_file_selected)
                self._chooser.choose_content(
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
                self.result_label.text = "اختر ملف Word من مدير الملفات..."
                return
            except Exception as exc:
                self.result_label.text = f"تعذر فتح اختيار الملفات: {exc}"
                return

        try:
            from plyer import filechooser
            filechooser.open_file(
                on_selection=self._desktop_file_selected,
                filters=["*.docx"], multiple=False,
            )
        except Exception as exc:
            self.result_label.text = f"تعذر فتح اختيار الملفات: {exc}"

    def _android_file_selected(self, shared_files):
        if not shared_files:
            self.result_label.text = "لم يتم اختيار ملف."
            return
        try:
            from androidstorage4kivy import SharedStorage
            copied = SharedStorage().copy_from_shared(shared_files[0])
            if not copied:
                raise RuntimeError("تعذر نسخ الملف إلى مساحة التطبيق.")
            self._set_selected_file(copied)
        except Exception as exc:
            self.result_label.text = f"خطأ في فتح الملف: {exc}"

    def _desktop_file_selected(self, selection):
        if not selection:
            self.result_label.text = "لم يتم اختيار ملف."
            return
        self._set_selected_file(selection[0])

    def _set_selected_file(self, path):
        path = os.path.abspath(path)
        if not path.lower().endswith(".docx"):
            self.result_label.text = "الرجاء اختيار ملف Word بصيغة DOCX."
            return
        self.selected_file = path
        self.file_label.text = f"الملف: {Path(path).name}"
        self.result_label.text = "تم اختيار الملف. اكتب كلمة البحث ثم اضغط «بدء البحث»."

    @staticmethod
    def extract_paragraphs_from_docx(file_path):
        paragraphs = []
        with zipfile.ZipFile(file_path, "r") as docx:
            xml_content = docx.read("word/document.xml")
        root = ET.fromstring(xml_content)

        for paragraph in root.iter():
            if not (paragraph.tag.endswith("}p") or paragraph.tag == "p"):
                continue
            parts = []
            for elem in paragraph.iter():
                if (elem.tag.endswith("}t") or elem.tag == "t") and elem.text:
                    parts.append(elem.text)
            text = "".join(parts).strip()
            if text:
                paragraphs.append(text)
        return paragraphs

    def search_in_word(self, *_args):
        keyword = self.text_input.text.strip()

        if not self.selected_file:
            self.result_label.text = "اختر ملف Word أولاً."
            return
        if not keyword:
            self.result_label.text = "اكتب كلمة أو عبارة للبحث عنها أولاً."
            return

        try:
            paragraphs = self.extract_paragraphs_from_docx(self.selected_file)
        except FileNotFoundError:
            self.result_label.text = "لم يعد الملف متاحاً. اختره من جديد."
            return
        except zipfile.BadZipFile:
            self.result_label.text = "الملف ليس DOCX صالحاً أو أنه تالف."
            return
        except KeyError:
            self.result_label.text = "ملف Word غير صالح: لم يتم العثور على document.xml."
            return
        except Exception as exc:
            self.result_label.text = f"خطأ أثناء قراءة الملف: {exc}"
            return

        keyword_lower = keyword.casefold()
        matches = [
            (index, paragraph)
            for index, paragraph in enumerate(paragraphs, start=1)
            if keyword_lower in paragraph.casefold()
        ]

        if not matches:
            self.result_label.text = (
                f"❌ لم يتم العثور على «{keyword}».\n\n"
                f"تم فحص {len(paragraphs)} فقرة."
            )
            return

        lines = [
            f"✅ تم العثور على «{keyword}»",
            f"عدد الفقرات المطابقة: {len(matches)}",
            "",
        ]
        for number, paragraph in matches[:100]:
            lines.extend([f"الفقرة {number}:", paragraph, ""])

        if len(matches) > 100:
            lines.append(f"... تم عرض أول 100 نتيجة من أصل {len(matches)}.")

        self.result_label.text = "\n".join(lines)


if __name__ == "__main__":
    SmartFinderApp().run()
