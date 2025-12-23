import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime
import threading
from main import FileOperations # импорт из файла

class FileCopyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Утилита для копирования файлов")
        self.root.geometry("1000x800")
        self.root.configure(bg="#f5f5f5")

        # переменные
        self.source_path = tk.StringVar()
        self.destination_path = tk.StringVar()
        self.copy_mode = tk.StringVar(value="single")  # single или multiple
        self.operation_in_progress = False

        self.create_widgets()
        self.center_window()

    def center_window(self): # центрирование окна на экране
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self): # cоздание элементов интерфейса (их тут много)

        # заголовок
        header_frame = tk.Frame(self.root, bg="#2196F3", height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="Утилита для копирования файлов",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#2196F3"
        ).pack(expand=True)

        # основной контейнер
        main_frame = tk.Frame(self.root, bg="#f5f5f5")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # выбор режима копирования
        mode_frame = tk.LabelFrame(
            main_frame,
            text="Режим копирования",
            font=("Arial", 10, "bold"),
            bg="#f5f5f5",
            relief="groove"
        )
        mode_frame.pack(fill="x", pady=(0, 15))

        tk.Radiobutton(
            mode_frame,
            text="Копировать один файл",
            variable=self.copy_mode,
            value="single",
            font=("Arial", 10),
            bg="#f5f5f5",
            command=self.on_mode_change
        ).pack(side="left", padx=20, pady=10)

        tk.Radiobutton(
            mode_frame,
            text="Копировать несколько файлов",
            variable=self.copy_mode,
            value="multiple",
            font=("Arial", 10),
            bg="#f5f5f5",
            command=self.on_mode_change
        ).pack(side="left", padx=20, pady=10)

        # источник файлов
        source_frame = tk.LabelFrame(
            main_frame,
            text="Источник",
            font=("Arial", 10, "bold"),
            bg="#f5f5f5",
            relief="groove"
        )
        source_frame.pack(fill="x", pady=(0, 15))

        # поле для пути источника
        source_entry_frame = tk.Frame(source_frame, bg="#f5f5f5")
        source_entry_frame.pack(fill="x", padx=10, pady=10)

        tk.Entry(
            source_entry_frame,
            textvariable=self.source_path,
            font=("Arial", 10),
            state="readonly",
            readonlybackground="white"
        ).pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.source_button = tk.Button(
            source_entry_frame,
            text="Выбрать...",
            command=self.select_source,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10),
            width=12,
            cursor="hand2"
        )
        self.source_button.pack(side="right")

        # информация об источнике
        self.source_info_label = tk.Label(
            source_frame,
            text="",
            font=("Arial", 9),
            fg="#666666",
            bg="#f5f5f5",
            anchor="w"
        )
        self.source_info_label.pack(fill="x", padx=10, pady=(0, 5))

        # назначение копирования
        dest_frame = tk.LabelFrame(
            main_frame,
            text="Назначение",
            font=("Arial", 10, "bold"),
            bg="#f5f5f5",
            relief="groove"
        )
        dest_frame.pack(fill="x", pady=(0, 15))

        # поле для пути назначения
        dest_entry_frame = tk.Frame(dest_frame, bg="#f5f5f5")
        dest_entry_frame.pack(fill="x", padx=10, pady=10)

        tk.Entry(
            dest_entry_frame,
            textvariable=self.destination_path,
            font=("Arial", 10),
            state="readonly",
            readonlybackground="white"
        ).pack(side="left", fill="x", expand=True, padx=(0, 10))

        tk.Button(
            dest_entry_frame,
            text="Выбрать...",
            command=self.select_destination,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10),
            width=12,
            cursor="hand2"
        ).pack(side="right")

        # опции для копирования
        options_frame = tk.LabelFrame(
            main_frame,
            text="Опции",
            font=("Arial", 10, "bold"),
            bg="#f5f5f5",
            relief="groove"
        )
        options_frame.pack(fill="x", pady=(0, 20))

        self.overwrite_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            options_frame,
            text="Перезаписывать существующие файлы",
            variable=self.overwrite_var,
            font=("Arial", 10),
            bg="#f5f5f5"
        ).pack(anchor="w", padx=10, pady=8)

        self.preserve_metadata_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            options_frame,
            text="Сохранять метаданные файлов",
            variable=self.preserve_metadata_var,
            font=("Arial", 10),
            bg="#f5f5f5"
        ).pack(anchor="w", padx=10, pady=(0, 8))

        # кнопка для копирования
        self.copy_button = tk.Button(
            main_frame,
            text="Начать копирование",
            command=self.start_copy,
            bg="#FF9800",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=30,
            pady=10,
            cursor="hand2",
            state="normal"
        )
        self.copy_button.pack(pady=(0, 15))

        self.progress = ttk.Progressbar(
            main_frame,
            mode='indeterminate',
            length=400
        )

        self.status_label = tk.Label(
            main_frame,
            text="Готово к работе",
            font=("Arial", 10),
            fg="#666666",
            bg="#f5f5f5"
        )
        self.status_label.pack()

        # журнал операций
        log_frame = tk.LabelFrame(
            main_frame,
            text="Журнал операций",
            font=("Arial", 10, "bold"),
            bg="#f5f5f5",
            relief="groove"
        )
        log_frame.pack(fill="both", expand=True, pady=(10, 0))

        # текстовое поле для логов
        text_frame = tk.Frame(log_frame, bg="#f5f5f5")
        text_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.log_text = tk.Text(
            text_frame,
            height=8,
            font=("Consolas", 9),
            bg="white",
            fg="#333333",
            wrap="word"
        )
        self.log_text.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(text_frame, command=self.log_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=scrollbar.set)

        # кнопка очистки журнала
        tk.Button(
            log_frame,
            text="Очистить журнал",
            command=self.clear_log,
            bg="#9E9E9E",
            fg="white",
            font=("Arial", 9),
            cursor="hand2"
        ).pack(pady=(0, 5))

    def on_mode_change(self): # обработчик изменения режима копирования
        if self.copy_mode.get() == "single":
            self.source_button.config(text="Выбрать файл...")
        else:
            self.source_button.config(text="Выбрать папку...")
        
        # очистка информации об источнике
        self.source_path.set("")
        self.source_info_label.config(text="")

    def select_source(self): # выбор источника для копирования
        try:
            if self.copy_mode.get() == "single":
                # Выбор одного файла
                file_path = filedialog.askopenfilename(
                    title="Выберите файл для копирования",
                    filetypes=[("Все файлы", "*.*")]
                )
                if file_path:
                    self.source_path.set(file_path)
                    self.update_source_info(file_path)
                    self.log_message(f"Выбран файл: {os.path.basename(file_path)}")
            else:
                # Выбор папки
                dir_path = filedialog.askdirectory(title="Выберите папку для копирования")
                if dir_path:
                    self.source_path.set(dir_path)
                    self.update_source_info(dir_path)
                    self.log_message(f"Выбрана папка: {os.path.basename(dir_path)}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось выбрать источник: {str(e)}")

    def select_destination(self): # выбор назначения папки для копирования
        try:
            dir_path = filedialog.askdirectory(title="Выберите папку назначения")
            if dir_path:
                self.destination_path.set(dir_path)
                self.log_message(f"Папка назначения: {dir_path}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось выбрать папку назначения: {str(e)}")

    def update_source_info(self, path): # jбновление информации об источнике (если вылезла ошибка)
        try:
            info = FileOperations.get_file_info(path)
            if info.get("error"):
                self.source_info_label.config(text=f"Ошибка: {info['error']}", fg="red")
            elif info["is_dir"]:
                size_formatted = FileOperations.format_size(info.get("size", 0))
                file_count = info.get("file_count", 0)
                text = f"Папка | Файлов: {file_count} | Размер: {size_formatted}"
                self.source_info_label.config(text=text, fg="#666666")
            else:
                size_formatted = FileOperations.format_size(info.get("size", 0))
                text = f"Файл: {info['filename']} | Размер: {size_formatted}"
                self.source_info_label.config(text=text, fg="#666666")
        except Exception as e:
            self.source_info_label.config(text=f"Ошибка получения информации: {str(e)}", fg="red")

    def log_message(self, message): # добавление сообщения в журнал и так-же показывает время
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_line = f"[{timestamp}] {message}\n"

        self.log_text.insert("end", log_line)
        self.log_text.see("end")
        self.root.update()

    def clear_log(self): # очистка журнала
        self.log_text.delete("1.0", "end")
        self.log_message("Журнал очищен")

    def update_status(self, message):
        self.status_label.config(text=message)
        self.log_message(message)

    def start_copy(self):
        if self.operation_in_progress:
            return

        source = self.source_path.get()
        destination = self.destination_path.get()

        # проверка входных данных
        if not source:
            messagebox.showwarning("Внимание", "Пожалуйста, выберите источник для копирования")
            return

        if not destination:
            messagebox.showwarning("Внимание", "Пожалуйста, выберите папку назначения")
            return

        if not os.path.exists(source):
            messagebox.showerror("Ошибка", "Источник не существует или путь указан неверно")
            return

        if not os.path.exists(destination):
            try:
                os.makedirs(destination)
                self.log_message(f"Создана папка назначения: {destination}")
            except:
                messagebox.showerror("Ошибка", "Не удалось создать папку назначения")
                return

        # запуск копирования в отдельном потоке
        self.operation_in_progress = True
        self.copy_button.config(state="disabled", text="Копирование...")
        self.progress.pack(pady=(0, 10))
        self.progress.start(10)

        thread = threading.Thread(target=self.perform_copy, args=(source, destination))
        thread.daemon = True
        thread.start()

    def perform_copy(self, source, destination): # выполнение копирования файлов с использованием модуля
        try:
            options = {
                'overwrite': self.overwrite_var.get(),
                'preserve_metadata': self.preserve_metadata_var.get()
            }

            if self.copy_mode.get() == "single":
                # Копирование одного файла
                dest_file, filename = FileOperations.copy_file(source, destination, **options)
                self.update_status(f"Файл скопирован: {filename}")
                self.log_message(f"Файл сохранен как: {os.path.basename(dest_file)}")

            else:
                # Копирование нескольких файлов (всей папки)
                dest_folder, folder_name, file_count = FileOperations.copy_directory(source, destination, **options)
                self.update_status(f"Папка скопирована: {folder_name}")
                self.log_message(f"Скопировано файлов: {file_count}")

            self.log_message("Копирование успешно завершено!")

	# проверка на ошибки и прочее
        except FileNotFoundError as e:
            self.update_status(f"Ошибка: {str(e)}")
            self.root.after(0, lambda: messagebox.showerror("Ошибка", str(e)))
        except PermissionError:
            error_msg = "Нет прав доступа к файлу или папке"
            self.update_status(f"Ошибка: {error_msg}")
            self.root.after(0, lambda: messagebox.showerror("Ошибка", error_msg))
        except Exception as e:
            self.update_status(f"Ошибка при копировании: {str(e)}")
            self.root.after(0, lambda: messagebox.showerror("Ошибка", f"Ошибка при копировании: {str(e)}"))
        finally:
            self.operation_in_progress = False
            self.root.after(0, self.finish_operation)

    def finish_operation(self): # конец копирования
        self.progress.stop()
        self.progress.pack_forget()
        self.copy_button.config(state="normal", text="Начать копирование")

        self.update_status("Готово к работе")
