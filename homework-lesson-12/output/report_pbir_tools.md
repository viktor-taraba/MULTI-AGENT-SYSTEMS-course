# Автономні Python-інструменти для локального редагування Power BI PBIR/PBIX (тільки стандартна бібліотека)

Дата оновлення: 2026-04

---

## Виконавче резюме
Цей документ — детальний технічний посібник і набір чисто-Python (stdlib) функцій для локального редагування Power BI звітів у форматах PBIR (файлова/JSON-орієнтована структура) та PBIX (zip-пакет з бінарними компонентами). Головний підхід — працювати напряму з JSON-файлами PBIR (definition/report.json, pages/*/visuals/*/visual.json, themes/*) за допомогою атомарних операцій: резервні копії, атомарний запис JSON, базова валідація та дифування змін.

Редагування PBIX через розпаковування та перепакування можливе, але ризиковане: внутрішні бінарні компоненти (DataModel/VertiPaq) та підписи можуть бути пошкоджені. Модельні зміни (зміни структури таблиць, типів стовпців або низькорівневе редагування VertiPaq) не можуть бути надійно виконані чистими stdlib-інструментами і потребують локальних бінарних програм (Power BI Desktop, Tabular Editor, pbir-cli) — ці інструменти можна викликати опціонально через subprocess (приклади наведені нижче).

---

## Стратегія дослідження
1. Проаналізувати публічно відомі структури PBIX/PBIR та приклади інструментів (GitHub, блоги, спільноти).  
2. Визначити безпечний набір операцій, які можна виконати лише зі стандартною бібліотекою Python: читання/запис JSON, архівація/розархівація, атомарні операції та зміни visual.json або reportExtensions.json.  
3. Розробити конкретні, мінімальні функції зі зрозумілими сигнатурами та докстрінгами українською мовою.  
4. Документувати обмеження і сценарії, які потребують локальних бінарів, описати як їх можна викликати опціонально через subprocess.  
5. Підготувати тестовий набір (unittest) для базової перевірки безпечних операцій.

---

## Технічний фон — PBIX vs PBIR (коротко)
- PBIX: zip-подібний файл, який містить JSON і бінарні файли: Report/Layout (інколи JSON), DataModel (бінарний VertiPaq), DataMashup (M), [Content_Types].xml, Metadata тощо. Розпакування файлу дозволяє інспекцію, але перепакування може пошкодити підписи/метадані або змінити порядок файлів, що призведе до помилок при відкритті у Power BI Desktop.
- PBIR: новіша структура (папка з JSON-файлами): definition/report.json, pages/*/page.json, pages/*/visuals/*/visual.json, reportExtensions.json, registered resources, themes/*.json. PBIR створений для кодо-орієнтованої роботи з звітами і значно безпечніший для редагування вручну.

Ключова рекомендація: якщо звіт у PBIR — працюйте напряму з JSON; якщо PBIX — працюйте на копії, робіть резервні копії та тестуйте у Power BI Desktop після змін.

---

## Важливі зауваги щодо безпеки та атомарності
- Обов'язкове резервне копіювання перед будь-якими змінами.  
- Атомарний запис JSON: запис у тимчасовий файл у тій же директорії + os.replace (або os.rename на більш старих ОС) + fsync файлу за можливості.  
- Під час роботи з PBIX переконайтесь, що Power BI Desktop закритий (Windows file lock).  
- Для запису у бінарні частини (DataModel) — НЕ використовувати прямі текстові патчі, натомість користуйтеся локальними бінарними інструментами.

---

## Реалізації функцій (чистий Python 3.8+, тільки стандартна бібліотека)
Нижче — повні реалізації функцій: backup_report, is_pbir, unzip_pbix, rezip_folder_to_pbix, read_json_file, write_json_file (атомарно), validate_pbir_basic, get_visual_json, set_visual_property, add_report_extension_measure, try_patch_layout_in_binary.

Усі приклади і функції використовують тільки: zipfile, json, pathlib, tempfile, shutil, os, hashlib. subprocess використовується лише в секції "Subprocess (optional) usage" — закоментовано.

---

### Імпорти та утиліти (спільні)
```python
import os
import zipfile
import json
import tempfile
import shutil
import hashlib
from pathlib import Path

# Утиліта для обчислення sha256 файлу
def file_sha256(path):
    """Повертає hex sha256 суми файлу"""
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()
```


### 1) backup_report
```python
def backup_report(path, out_folder=None):
    """
    Зробити резервну копію PBIR-папки або PBIX-файлу.

    Аргументи:
    - path: шлях до PBIR директорії або до .pbix файлу (str або Path)
    - out_folder: (опціонально) директорія для збереження бекапу; якщо None, використовується parent(path)

    Повертає: шлях до створеного архіву або копії (str)

    >>> p = backup_report('example/Report.Report')
    >>> isinstance(p, str)
    True
    """
    path = Path(path)
    if out_folder:
        out_dir = Path(out_folder)
    else:
        out_dir = path.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    ts = tempfile.mktemp(prefix='backup_')  # тільки для унікальності імені
    if path.is_dir():
        base_name = out_dir / f"{path.name}_backup"
        archive_path = shutil.make_archive(str(base_name), 'zip', root_dir=str(path))
        return archive_path
    elif path.is_file():
        # копіюємо файл з міткою
        dst = out_dir / f"{path.stem}_backup{path.suffix}"
        # уникаємо перезапису
        i = 0
        candidate = dst
        while candidate.exists():
            i += 1
            candidate = out_dir / f"{path.stem}_backup_{i}{path.suffix}"
        shutil.copy2(str(path), str(candidate))
        return str(candidate)
    else:
        raise FileNotFoundError(f"Path not found: {path}")
```

Notes: використовує shutil.make_archive для директорій; копіює файли з copy2 щоб зберегти метадані.


### 2) is_pbir
```python
def is_pbir(path):
    """
    Перевіряє чи вказаний шлях є PBIR (папкою з definition/report.json та pages).

    Повертає: True або False

    >>> is_pbir('example/Report.Report')
    False
    """
    p = Path(path)
    if not p.exists() or not p.is_dir():
        return False
    # основні чек-файли
    if (p / 'definition' / 'report.json').exists():
        return True
    if (p / 'definition' / 'pages').exists():
        return True
    return False
```


### 3) unzip_pbix
```python
def unzip_pbix(pbix_path, out_folder):
    """
    Розпаковує .pbix файл у вказану директорію.

    - pbix_path: шлях до .pbix
    - out_folder: директорія для розпакування

    Примітка: PBIX може містити бінарні файли; повторна упаковка не гарантує цілісність.
    """
    pbix_path = Path(pbix_path)
    out_folder = Path(out_folder)
    out_folder.mkdir(parents=True, exist_ok=True)
    # Просте розпакування zip
    with zipfile.ZipFile(str(pbix_path), 'r') as z:
        z.extractall(str(out_folder))
```

Safety: переконайтесь, що Power BI Desktop закритий; працюйте на копії файлу.


### 4) rezip_folder_to_pbix
```python
def rezip_folder_to_pbix(src_folder, out_pbix, ensure_content_types_first=True):
    """
    Запаковує директорію у .pbix (zip). Пише [Content_Types].xml першим при бажанні.

    - src_folder: розпакована структура
    - out_pbix: шлях вихідного pbix
    - ensure_content_types_first: якщо True, намагається додати [Content_Types].xml першим

    Примітка: перезапакування може не відновити підписи/метадані. Перевіряйте результат у Power BI Desktop.
    """
    src = Path(src_folder)
    out_pbix = Path(out_pbix)
    # видалити існуючий файл якщо є
    if out_pbix.exists():
        out_pbix.unlink()
    with zipfile.ZipFile(str(out_pbix), 'w', compression=zipfile.ZIP_DEFLATED) as z:
        # Write [Content_Types].xml first якщо є
        ct = src / '[Content_Types].xml'
        if ensure_content_types_first and ct.exists():
            z.write(str(ct), '[Content_Types].xml')
        # Потім все решта
        for file in sorted(src.rglob('*')):
            if not file.is_file():
                continue
            rel = file.relative_to(src)
            # Уникаємо дубляжу [Content_Types].xml
            if ensure_content_types_first and rel.name == '[Content_Types].xml':
                continue
            z.write(str(file), str(rel))
```

Важливо: порядок файлів може бути критичним; тому ми намагаємось писати [Content_Types].xml першим. Проте інші метадані можуть також впливати.


### 5) read_json_file
```python
def read_json_file(path, encodings=('utf-8', 'utf-16-le', 'utf-16')):
    """
    Читає JSON-файл, пробуючи набір кодувань (UTF-8, UTF-16 LE, UTF-16).

    Повертає: Python dict

    >>> d = read_json_file('example/definition/report.json')
    >>> isinstance(d, dict)
    True
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(path)
    last_err = None
    for enc in encodings:
        try:
            with open(str(p), 'r', encoding=enc) as f:
                return json.load(f)
        except Exception as e:
            last_err = e
            continue
    # якщо всі варіанти не спрацювали — підняти останню помилку
    raise last_err
```


### 6) write_json_file (атомарно)
```python
def write_json_file(path, obj, pretty=True, encoding='utf-8'):
    """
    Атомарно записує JSON: запис у тимчасовий файл у тій же директорії та os.replace.

    - path: куди записати
    - obj: об'єкт Python
    - pretty: форматувати з відступами
    - encoding: кодування для запису
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(prefix=p.name, suffix='.tmp', dir=str(p.parent))
    try:
        with os.fdopen(fd, 'w', encoding=encoding) as tmp:
            if pretty:
                json.dump(obj, tmp, ensure_ascii=False, indent=2)
            else:
                json.dump(obj, tmp, ensure_ascii=False, separators=(',', ':'))
            tmp.flush()
            try:
                os.fsync(tmp.fileno())
            except Exception:
                # fsync може не підтримуватися у всіх середовищах
                pass
        os.replace(tmp_path, str(p))
    finally:
        # у разі винятку mkstemp може повернути вже закритий дескриптор
        if Path(tmp_path).exists():
            try:
                Path(tmp_path).unlink()
            except Exception:
                pass
```

Атомарність досягається через tempfile у тій же директорії + os.replace.


### 7) validate_pbir_basic
```python
def validate_pbir_basic(report_folder):
    """
    Базова перевірка PBIR: наявність definition/report.json та pages/pages.json і валідність JSON-файлів.

    Повертає: список рядків з помилками (порожній = пройшов)
    """
    errors = []
    root = Path(report_folder)
    if not root.exists():
        errors.append('report folder not found')
        return errors
    req = [root / 'definition' / 'report.json', root / 'definition' / 'pages' / 'pages.json']
    for r in req:
        if not r.exists():
            errors.append(f'missing required file: {r}')
    # Спроба парсингу декількох JSON
    for json_path in root.rglob('*.json'):
        try:
            with open(str(json_path), 'r', encoding='utf-8') as f:
                json.load(f)
        except Exception:
            # Друга спроба з іншими кодуваннями
            try:
                read_json_file(str(json_path))
            except Exception as e:
                errors.append(f'json parse error: {json_path} -> {e}')
    return errors
```


### 8) get_visual_json
```python
def get_visual_json(report_folder, page_name, visual_name):
    """
    Повертає dict з visual.json для вказаного візуалу.

    Параметри:
    - report_folder: Report.Report
    - page_name: ім'я каталогу сторінки (наприклад, 'Page.Page')
    - visual_name: ім'я каталогу візуалу
    """
    p = Path(report_folder) / 'definition' / 'pages' / page_name / 'visuals' / visual_name / 'visual.json'
    return read_json_file(str(p))
```


### 9) set_visual_property
```python
def set_visual_property(report_folder, page_name, visual_name, property_path, value, confirm=False):
    """
    Встановлює значення властивості у visual.json.

    - property_path: або стрічка 'a.b.c' або список ключів ['a','b','c']
    - confirm: якщо False -> dry-run (повертає план змін), якщо True -> застосовує зміни

    Повертає: словник {'changed': bool, 'path': path_to_file, 'old_value': ..., 'new_value': ...}
    """
    p = Path(report_folder) / 'definition' / 'pages' / page_name / 'visuals' / visual_name / 'visual.json'
    if not p.exists():
        raise FileNotFoundError(p)
    obj = read_json_file(str(p))
    if isinstance(property_path, str):
        keys = property_path.split('.')
    else:
        keys = list(property_path)
    cur = obj
    for k in keys[:-1]:
        if k not in cur or not isinstance(cur[k], dict):
            cur[k] = {}
        cur = cur[k]
    old = cur.get(keys[-1], None)
    changed = (old != value)
    result = {'changed': changed, 'path': str(p), 'old_value': old, 'new_value': value}
    if not changed:
        return result
    if not confirm:
        # dry-run
        return result
    # apply
    cur[keys[-1]] = value
    write_json_file(str(p), obj, pretty=True)
    return result
```

За замовчуванням функція не виконує запис (confirm=False), що забезпечує безпечний dry-run.


### 10) add_report_extension_measure
```python
def add_report_extension_measure(report_folder, measure_name, dax_expression, confirm=False):
    """
    Додає або оновлює extension measure у definition/reportExtensions.json.

    - measure_name: ім'я міри
    - dax_expression: рядок DAX
    - confirm: dry-run якщо False

    Повертає: {'changed': bool, 'path': path, 'old': ..., 'new': ...}
    """
    p = Path(report_folder) / 'definition' / 'reportExtensions.json'
    if p.exists():
        ext = read_json_file(str(p))
    else:
        ext = {}
    measures = ext.get('measures', {})
    old = measures.get(measure_name)
    new = {'definition': dax_expression}
    changed = (old != new)
    result = {'changed': changed, 'path': str(p), 'old': old, 'new': new}
    if not changed:
        return result
    if not confirm:
        return result
    measures[measure_name] = new
    ext['measures'] = measures
    write_json_file(str(p), ext, pretty=True)
    return result
```

Примітка: не всі версії Power BI Desktop можуть коректно інтерпретувати reportExtensions.json; перевіряйте у Desktop.


### 11) try_patch_layout_in_binary (небезпечна операція)
```python
def try_patch_layout_in_binary(file_path, replacements, confirm=False, encodings=('utf-8','utf-16-le','utf-16')):
    """
    Небезпечна операція: намагається знайти текстові фрагменти в бінарному файлі і замінити їх.

    - file_path: шлях до бінарного файлу
    - replacements: dict старий_рядок->новий_рядок
    - confirm: якщо False -> dry-run (повертає чи знайдено збіги), якщо True -> записує зміни

    Повертає: dict {'found': bool, 'changes': [{'encoding':enc,'old_count':n,'new_count':m}, ...]}
    """
    p = Path(file_path)
    if not p.exists():
        raise FileNotFoundError(file_path)
    results = {'found': False, 'changes': []}
    b = p.read_bytes()
    for enc in encodings:
        try:
            s = b.decode(enc)
        except Exception:
            continue
        orig = s
        changed = False
        details = {'encoding': enc, 'replacements': []}
        for old, new in replacements.items():
            count_old = s.count(old)
            if count_old:
                changed = True
                s = s.replace(old, new)
                details['replacements'].append({'old': old, 'count': count_old})
        if changed:
            results['found'] = True
            results['changes'].append(details)
            if confirm:
                # записуємо назад у тому ж кодуванні
                tmp = p.with_suffix('.tmp')
                tmp.write_text(s, encoding=enc)
                os.replace(str(tmp), str(p))
        # якщо хочемо перевіряти інші кодування — продовжуємо
    return results
```

Сильне попередження: ця функція може пошкодити бінарні файли. Використовувати лише на бекапі та з confirm=True свідомо.

---

## Безпечний приклад: перейменування .pbix -> .zip, розпакування, редагування JSON, зворотне пакування
Нижче — runnable приклад, що демонструє повний цикл. Використовуйте на копіях і обов'язково зробіть резервну копію.

```python
from pathlib import Path
import shutil

orig = Path('Sales.pbix')
if not orig.exists():
    raise FileNotFoundError('Sales.pbix not found')
# 1) backup оригіналу
bk = backup_report(str(orig))
print('Backup:', bk)
# 2) переіменувати у .zip (тимчасово)
zip_path = orig.with_suffix('.zip')
shutil.copy2(orig, zip_path)
# 3) розпакувати
tmpdir = Path(tempfile.mkdtemp(prefix='pbix_'))
unzip_pbix(str(zip_path), str(tmpdir))
# 4) Редагувати report.json або Layout (приклад: змінити report title якщо є)
report_json = tmpdir / 'Report' / 'definition' / 'report.json'
if report_json.exists():
    doc = read_json_file(str(report_json))
    # приклад: встановити властивість title
    doc['name'] = doc.get('name', 'Report') + ' (patched)'
    write_json_file(str(report_json), doc)
else:
    print('report.json не знайдено, пробуємо знайти layout…')
# 5) перепакувати у pbix
out_pbix = orig.parent / (orig.stem + '_patched.pbix')
rezip_folder_to_pbix(str(tmpdir), str(out_pbix), ensure_content_types_first=True)
print('Created', out_pbix)

# Cleanup: можете видалити тимчасові файли, але зберігайте backup за замовчуванням
# shutil.rmtree(tmpdir)
# zip_path.unlink()
```

Warning: треба переконатись, що [Content_Types].xml присутній і записується першим. Навіть з цим пакетування може бути некоректним через внутрішні підписи/метадані.

---

## Subprocess (optional) usage — приклад відкриття PBIX в Power BI Desktop на Windows
Тільки як опціональний локальний fallback; не є залежністю бібліотеки. Команди приведені як приклад виклику локального бінарного додатку через subprocess. Працює тільки на локальній машині, де встановлений Power BI Desktop.

```python
# OPTIONAL: відкриття pbix у Power BI Desktop (Windows)
# import subprocess
# pbidesktop = r"C:\Program Files\Microsoft Power BI Desktop\bin\PBIDesktop.exe"
# subprocess.run([pbidesktop, r"C:\path\to\Sales_patched.pbix"], check=False)
```

Платформні caveats:
- На Windows переконайтесь у точному шляху до PBIDesktop.exe; інсталятор може розміщувати файл в іншому каталозі.  
- Power BI Desktop може блокувати файл під час відкриття (file lock) — робіть операції з файлами тільки коли Desktop закритий.  
- Цей виклик не використовує мережеві або REST API; він виконує локальну програму.

Зауваження: інші локальні інструменти (Tabular Editor, pbir-cli) можна викликати схожим способом — вони також є опціональними.

---

## Testing and Validation (Actionable steps + unittest приклад)
Далі — кроки тестування та приклад тестів standard-library unittest.

Actionable steps:
1. Підготувати мінімальний PBIR-пакет у тимчасовій теці (definition/report.json, pages/... і один visual.json).  
2. Виконати backup_report і перевірити, що файл архіву або копія створена.  
3. Тестувати read_json_file / write_json_file: записати JSON та переконатись, що після запису файл валідний JSON і сума sha256 змінилась передбачувано.  
4. Тест set_visual_property: dry-run (confirm=False) не має змінювати файл; потім confirm=True має змінити і хеш файлу змінитись.  
5. Простий json-diff: читати стару та нову версії і порівнювати ключі/значення у змінених файлах.

Приклад unittest (запустити у середовищі де дозволені операції з файловою системою):

```python
import unittest
import tempfile
import os
from pathlib import Path

class TestPBIRTools(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix='pbir_test_'))
        # створимо мінімальну структуру
        rpt = self.tmp / 'Report.Report'
        (rpt / 'definition' / 'pages' / 'Page.Page' / 'visuals' / 'Card_1').mkdir(parents=True)
        # minimal report.json
        write_json_file(str(rpt / 'definition' / 'report.json'), {'name':'TestReport'})
        write_json_file(str(rpt / 'definition' / 'pages' / 'pages.json'), {'pages':['Page.Page']})
        write_json_file(str(rpt / 'definition' / 'pages' / 'Page.Page' / 'visuals' / 'Card_1' / 'visual.json'), {'format':{}})
        self.report_folder = str(rpt)
    def tearDown(self):
        shutil.rmtree(str(self.tmp))
    def test_backup(self):
        bk = backup_report(self.report_folder)
        self.assertTrue(Path(bk).exists())
    def test_json_atomic_write_and_read(self):
        p = Path(self.report_folder) / 'definition' / 'report.json'
        old_hash = file_sha256(str(p))
        doc = read_json_file(str(p))
        doc['x'] = 1
        write_json_file(str(p), doc)
        new_hash = file_sha256(str(p))
        self.assertNotEqual(old_hash, new_hash)
    def test_set_visual_property_dry_run_and_commit(self):
        p = Path(self.report_folder) / 'definition' / 'pages' / 'Page.Page' / 'visuals' / 'Card_1' / 'visual.json'
        old = read_json_file(str(p))
        old_hash = file_sha256(str(p))
        res = set_visual_property(self.report_folder, 'Page.Page', 'Card_1', 'format.card.title.fontSize', 12, confirm=False)
        self.assertTrue(res['changed'])
        # файл не мав змін у dry-run
        self.assertEqual(old_hash, file_sha256(str(p)))
        # тепер commit
        res2 = set_visual_property(self.report_folder, 'Page.Page', 'Card_1', 'format.card.title.fontSize', 12, confirm=True)
        self.assertTrue(res2['changed'])
        self.assertNotEqual(old_hash, file_sha256(str(p)))
    def test_json_diff_simple(self):
        # простий diff: зчитати старий та новий
        p = Path(self.report_folder) / 'definition' / 'report.json'
        old = read_json_file(str(p))
        old['y'] = 0
        write_json_file(str(p), old)
        new = read_json_file(str(p))
        self.assertIn('y', new)

if __name__ == '__main__':
    unittest.main()
```

Ці тести перевіряють основну атомарність запису, резервне копіювання та поведінку dry-run vs commit у set_visual_property.

---

## Limitations and Risks (детально)
1. Форматні несумісності:
   - PBIX містить бінарні DataModel/VertiPaq, які неможливо надійно редагувати лише стандартними текстовими операціями.  
   - DataMashup може бути у різних формах (текст або бінарний контейнер).  
   - Порядок файлів в архіві (особливо [Content_Types].xml першим) часто важливий для відкриття PBIX; інші приховані метадані/підписи можуть впливати.
2. OS / файл-системні нюанси:
   - Windows: Power BI Desktop може блокувати .pbix (file lock). Перед редагуванням переконайтесь, що Desktop закритий.  
   - Linux/Mac: можна редагувати zip-структуру, але відкривати/тестувати результат рекомендується в Windows/Power BI Desktop.
3. Кодування: деякі JSON або M-код можуть бути у UTF-16 LE — read_json_file намагається перевірити utf-8 та utf-16-le.
4. Legal / support boundaries:
   - Офіційна підтримка Microsoft не гарантує безпечність ручних змін у PBIX/PBIR; модифікація файлів може виходити за межі підтримки. Рекомендується перевіряти ліцензійні умови інструментів (Tabular Editor, pbir-cli) перед використанням.
5. PBIR adoption timeline (важливо):
   - За інформацією, опублікованою Microsoft, є релізи/повідомлення про PBIR та планування переходу: приклади публічних повідомлень містять дати (перевірити офіційні документи):
     - Power BI блог: 2024-06-11 (запис/реліз, згадка про розвиток формату або суміжні зміни) — перевірте офіційний блог Microsoft для точного URL і контексту.  
     - Microsoft notice: 2026-01-25 (оголошення про встановлення PBIR як дефолтного формату або зміни у поведінці) — перевірте офіційні документи Microsoft щодо актуальності та деталей.
   - Примітка: точні URL можуть змінюватись; настійно рекомендую перевірити офіційний Power BI Blog та документацію Microsoft для найновішої інформації.
6. Які операції неможливо виконати лише зі stdlib:
   - Редагування структури DataModel (створення/видалення таблиць, зміна типів, створення фізичних колонок у VertiPaq).  
   - Низькорівнева валідація моделі та виконання DAX для перевірки результатів — для цього потрібен Analysis Services / Power BI Desktop або інші локальні бінари.  

Рекомендації: завжди виконувати фінальну перевірку у Power BI Desktop після будь-яких змін; використовувати локальні інструменти (Tabular Editor, pbir-cli, Power BI Desktop) лише як опціональний fallback і тільки якщо вони доступні та легально дозволені.

---

## Чітке розмежування: що можливо тільки зі stdlib vs що вимагає локальних бінарів
- Можливо тільки зі стандартною бібліотекою Python (stdib): читання/запис JSON (PBIR), модифікація visual.json, theme.json, reportExtensions.json, архівація/розархівація PBIX (zip), атомарні операції та створення резервних копій.
- Потребує локальних бінарів (необхідні для надійних змін): модифікація DataModel/VertiPaq, повна конвертація PBIX↔PBIR гарантійно, компіляція/виконання DAX у контексті моделі для валідації. Ці інструменти можуть бути викликані локально через subprocess, але вони не є мережевими/REST залежностями.

---

## Джерела та подальше читання
- PBIR Format Reference / skill (GitHub): https://github.com/data-goblin/power-bi-agentic-development/blob/main/plugins/pbip/skills/pbir-format/SKILL.md (перевірено 2026).  
- pbir.tools (GitHub публічний репозиторій): https://github.com/maxanatsko/pbir.tools (перевірено 2026).  
- "What makes up a Power BI Desktop PBIX File" — FourMoo, 2017-05-02: https://www.fourmoo.com/2017/05/02/what-makes-up-a-power-bi-desktop-pbix-file/ (ілюстративно).  
- Power BI Blog та офіційні повідомлення Microsoft: перевіряйте офіційний Power BI Blog для реліз-нотів (включно з повідомленнями навколо 2024-06-11 та 2026-01-25). Якщо точні URL недоступні, зверніться до https://powerbi.microsoft.com/en-us/blog/ і знайдіть записи по датах (2024-06-11, 2026-01-25) для підтвердження деталей.
- Microsoft Fabric / Power BI Community обговорення про unzip-modify-rezip ризики: https://community.fabric.microsoft.com/ (пошук за темою "How to edit PBIX unzip modify rezip"), приклад обговорення знайдено в 2026.
- Tabular Editor: https://tabulareditor.com/ (перевірити ліцензію для локального використання).

---

## Заключні рекомендації
1. За можливості працюйте з PBIR — це найменш ризикований шлях для чисто локального, кодо-орієнтованого редагування.  
2. Завжди робіть резервну копію перед змінами.  
3. Викличте Power BI Desktop локально для фінальної ручної перевірки після змін — це найнадійніший спосіб впевнитися, що звіт не пошкоджено.  
4. Для змін моделей використовуйте локальні бінарні інструменти (Tabular Editor, pbir-cli, Power BI Desktop) як опціональні fallback та автоматизуйте їх лише якщо вони встановлені локально і ліцензійно дозволені.  

---

Звіт підготовлено як технічний довідник і набір працюючих прикладів для локального редагування Power BI звітів за допомогою Python стандартної бібліотеки. Усі операції, що модифікують файли, повинні виконуватись на копіях та з обережністю.