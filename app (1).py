from flask import Flask, render_template, request, redirect, url_for
# Импортируем нужные функции и классы из библиотеки Flask: Flask (основной класс приложения),
# render_template (для рендеринга HTML-шаблонов), request (для обработки входящих данных), 
# redirect (для перенаправления пользователей) и url_for (для построения URL-адресов).

from flask_sqlalchemy import SQLAlchemy
# Импортируем класс SQLAlchemy для работы с базами данных.

app = Flask(__name__)
# Создаем экземпляр приложения Flask.

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# Настраиваем URI для подключения к базе данных SQLite. База данных будет находиться в файле database.db.

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Отключаем отслеживание изменений объектов SQLAlchemy, чтобы не было лишних затрат по памяти.

db = SQLAlchemy(app)
# Создаем экземпляр SQLAlchemy, передавая ему приложение Flask для настройки.

class DynamicTable(db.Model):
    # Определяем модель DynamicTable, которая будет представлять таблицу в базе данных
    id = db.Column(db.Integer, primary_key=True)
    # Создаем колонку 'id' типа Integer, которая будет являться первичным ключом
    data = db.Column(db.String(200), nullable=False)
    # Создаем колонку 'data' типа String с максимальной длиной 200 символов, которая не может быть пустой (nullable=False)
    data_type = db.Column(db.String(100), nullable=False)
    # Создаем колонку 'data_type' типа String с максимальной длиной 100 символов, которая также не может быть пустой (nullable=False)


@app.cli.command("db_init")
# Определяем новую команду CLI (Command Line Interface) для инициализации базы данных с именем "db_init"
def db_init():
    """Инициализация базы данных."""
    db.create_all()  # Создание обновленной структуры базы данных. Создаем все таблицы в базе данных, которые описаны в моделях (если они еще не существуют)

@app.route('/') 
def index():
    # Определяем маршрут для корневого URL ('/') и связанную с ним функцию index.
    tables = DynamicTable.query.all()
    # Получаем все записи из таблицы DynamicTable.
    
    return render_template('index.html', tables=tables)
    # Рендерим шаблон index.html, передавая ему данные 'tables'.

@app.route('/create_table', methods=['POST'])
# Определяем маршрут '/create_table', который обрабатывает только POST-запросы.
def create_table():
    table_name = request.form.get('table_name')
    # Извлекаем имя таблицы из данных формы, отправленных в POST-запросе.

    return redirect(url_for('index'))


@app.route('/add_data', methods=['POST'])
# Определяем маршрут '/add_data', который также обрабатывает только POST-запросы.
def add_data():
    data = request.form.get('data')
    # Извлекаем основное значение из данных формы (поле с именем 'data').
    data_type = request.form.get('data_type')
     # Извлекаем дополнительный тип данных из данных формы (поле с именем 'data_type').
    new_entry = DynamicTable(data=data, data_type=data_type)
    # Создаем новый объект записи в модели DynamicTable с извлеченными значениями (data и data_type).
    db.session.add(new_entry)
    # Добавляем новую запись в текущую сессию базы данных.
    # Сохраняем изменения сессии в базе данных.

    return redirect(url_for('index'))
    # Перенаправляем пользователя обратно на главную страницу после добавления данных.

@app.route('/delete_data/<int:id>', methods=['POST'])
def delete_data(id):
    # Определяем маршрут для удаления данных, принимающий ID записи и ожидающий POST-запросы.
    entry = DynamicTable.query.get(id)
    # Находим запись в таблице по переданному ID.
    
    db.session.delete(entry)
    # Удаляем найденную запись из сессии SQLAlchemy.
    
    db.session.commit()
    # Сохраняем изменения в базе данных.
    
    return redirect(url_for('index'))
    # Перенаправляем пользователя на главную страницу после удаления данных.

@app.route('/update_data/<int:id>', methods=['POST'])
def update_data(id):
    # Определяем маршрут для обновления данных, принимающий ID записи и ожидающий POST-запросы.
    entry = DynamicTable.query.get(id)
    # Находим запись в таблице по переданному ID.
    
    entry.data = request.form.get('data')
    # Обновляем поле 'data' новой информацией из формы.
    
    db.session.commit()
    # Сохраняем изменения в базе данных.
    
    return redirect(url_for('index'))
    # Перенаправляем пользователя на главную страницу после обновления данных.

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создание базы данных и таблиц, если они не существуют.
    
    app.run(debug=True)
    # Запускаем приложение в режиме отладки, чтобы видеть ошибки и изменения в реальном времени.